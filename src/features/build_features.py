# -*- coding: utf-8 -*-
"""Make transformations on dataset."""
from ml_belt.prep import Prep
import numpy as np
import pandas as pd

class PrepAmbev(Prep):
    """Make preprocessing for Ambev dataset. Inherit from Prep class of ml_belt lib."""

    def rename_cols(self):
        """Give a more meaningful name for columns."""
        new_names = {
            'Mês Referência': 'ord_mes_referencia',
            'País': 'nom_pais',
            'Mundo': 'nom_mundo',
            'Regional/Área': 'dis_regional_area',
            'Unidade': 'dis_unidade',
            'Grupo Cargo': 'nom_grupo_cargo',
            'Cargo': 'nom_cargo',
            'Grade': 'dis_grade',
            'Banda': 'nom_banda',
            'Área': 'nom_area',
            'Nome FuncionÁ¡rio': 'dis_nome_funcionario',
            'Nome Gestor': 'dis_nome_gestor',
            'Código KPI': 'nom_codigo_kpi',
            'Diretoria': 'nom_diretoria',
            'Áreas da Diretoria': 'nom_areas_diretoria',
            'Função': 'nom_funcao',
            'Tipo da Meta': 'nom_tipo_meta',
            'Categoria KPI': 'nom_categoria_kpi',
            'Nome KPI': 'dis_nome_kpi',
            'Peso KPI': 'per_peso_kpi',
            'Prazo': 'nom_prazo',
            'Regra Alcance Parcial': 'nom_regra_alcance_parcial',
            'Meta Projeto': 'bin_meta_projeto',
            '% Ating Mês': 'per_ating_mes',
            '% Pontos Mês': 'per_pontos_mes',
            '% Acum Mês': 'per_acum_mes',
            '% Ating Acumulado': 'per_ating_acumulado',
            '% Pontos Acumulado': 'per_pontos_acumulado',
            '% Acum Acumulado': 'per_acum_acumulado',
            '% Ating Fim Exer': 'per_ating_fim_exer',
            '% Pontos Fim Exer': 'per_pontos_fim_exer',
            '% Acum Fim Exer': 'per_acum_fim_exer',
            'Status Meta': 'bin_status_meta'
        }

        self._data.rename(index=str, columns=new_names, inplace=True)
        return self

    def replace_by_index(self, indexes, cols, val):
        """Put `val` into all `cols` of `indexes`."""
        for index in indexes:
            for col in cols:
                self._data.iat[index, self._data.columns.get_loc(col)] = val
        return self

    def check_float(self, cols):
        """Transform to `np.nan` al values in `col` columns which cannot be converted to float."""
        for index, row in self._data.iterrows():
            for col in cols:
                try:
                    self._data.at[index, col] = float(self._data.at[index, col])
                except:
                    self._data.at[index, col] = np.nan
        return self

    def replace_nan(self, cols_dict):
        """Wrap method `replace` from pandas.DataFrame to fit into Prep pipeline."""
        self._data = self._data.replace(cols_dict, np.nan)
        return self

    def bin_to_num(self, cols, one=['sim'], zero=None):
        """Change `one` to 1 and `zero` to 0.

        If `zero` is None, all values not in `one` will be changed to 0.
        If `zero` is passed, all values not in `one` and `zero` will be changed to np.nan.
        """
        i = 0
        for index, row in self._data.iterrows():
            for col in cols:
                val = self._data.at[index, col]
                if isinstance(val, str) and val in one:
                    self._data.at[index, col] = 1
                elif zero is None:
                    self._data.at[index, col] = 0
                elif isinstance(val, str) and val in zero:
                    self._data.at[index, col] = 0
                else:
                    self._data.at[index, col] = np.nan
        return self

    def transform_month(self, col):
        """Remove 2017 from month column."""
        self._data[col] = self._data.apply(lambda x, col=col: (x[col]-2017)/10000, axis=1)
        return self

    def filter_valid(self, col, valid_value):
        """Filter the dataset based on one column, keeping just rows with `valid_value` on `col`."""
        self._data = self._data[self._data[col] == valid_value]
        return self

    def calc_per_acum(self):
        """Calculate column `per_acum_acumulado` based on `per_peso_kpi` and `per_pontos_acumulado`."""
        for idx, row in self._data[self._data['per_acum_acumulado'].isna()].iterrows():
            self._data.at[idx, 'per_acum_acumulado'] = self._data.at[idx, 'per_peso_kpi'] * self._data.at[idx, 'per_pontos_acumulado']   
        return self

    def astype(self, cols, new_type):
        """Wrap method `astype` from pandas to fit into Prep pipeline."""
        for col in cols:
            self._data[col] = self._data[col].astype(new_type)
        return self

    def sort_values(self, cols):
        """Wrap method `sort_values` from pandas to fit into Prep pipeline."""
        self._data.sort_values(by=cols, inplace=True)
        return self


if __name__ == '__main__':           
    unnamed_cols = ['Unnamed: 33', 'Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36', 'Unnamed: 37']
    
    per_cols = [
        'per_ating_mes',
        'per_pontos_mes',
        'per_acum_mes',
        'per_ating_acumulado',
        'per_pontos_acumulado'
    ]

    per_cols_replace = {
        'per_ating_mes': -1,
        'per_pontos_mes': -1,
        'per_acum_mes': -1,
        'per_ating_acumulado': -1,
        'per_pontos_acumulado': -1
    }

    prep_df = PrepAmbev(pd.read_csv('data/interim/ambev-final-dataset_AmBev_final_dataset.csv', low_memory=False))
    
    prep_df \
        .rename_cols() \
        .replace_by_index(
            indexes = [9610, 31343],
            cols = unnamed_cols,
            val = np.nan
        ) \
        .drop_not_nulls(unnamed_cols) \
        .drop_cols(unnamed_cols) \
        .fill_null_with(-1.0, per_cols) \
        .check_float(cols = per_cols) \
        .drop_nulls(per_cols) \
        .replace_nan(cols_dict = per_cols_replace) \
        .bin_to_num(cols = ['bin_meta_projeto'], one = ['Sim'], zero = ['Não']) \
        .bin_to_num(cols = ['bin_status_meta'], one = 'Monitoramento Aprovado') \
        .transform_month(col = 'ord_mes_referencia') \
        .filter_valid(col ='bin_status_meta', valid_value = 1) \
        .drop_cols(['bin_status_meta']) \
        .drop_nulls(['nom_grupo_cargo', 'per_pontos_mes']) \
        .fill_null_with('N/A', ['nom_regra_alcance_parcial', 'nom_mundo', 'nom_area']) \
        .calc_per_acum() \
        .astype(cols = ['bin_meta_projeto'], new_type = 'float64') \
        .sort_values(['ord_mes_referencia', 'nom_codigo_kpi', 'dis_nome_funcionario'])
        
    df = prep_df.df
    df.to_csv('data/processed/ambev-final-dataset-processed.csv', index=False)
    