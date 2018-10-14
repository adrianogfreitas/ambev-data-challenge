# -*- coding: utf-8 -*-
from ml_belt.prep import Prep
import pandas as pd

def rename_cols(df):
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
        'Peso KPI': 'dis_peso_kpi',
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
        'Status Meta': 'nom_status_meta'
    }

    df.rename(index=str, columns=new_names, inplace=True)
    return df

def replace_by_index(df, indexes, cols, val):
    """Put `val` into all `cols` of `indexes`."""
    for index in indexes:
        for col in cols:
            df.iat[index, df.columns.get_loc(col)] = val
            
    return df

def check_float(df, cols):
    """Transform to `np.nan` al values in `col` columns which cannot be converted to float."""
    for index, row in df.iterrows():
        for col in cols:
            try:
                df.at[index, col] = float(df.at[index, col])
            except:
                df.at[index, col] = np.nan
    return df

def replace_nan(df, cols_dict):
    """Wrap method `replace` from pandas,DataFrame to fit into Prep pipeline."""
    return df.replace(cols_dict, np.nan)

def bin_to_num(df, cols):
    """Change `sim` and `não` into 1 and 0."""
    for index, row in df.iterrows():
        for col in cols:
            val = df.at[index, col]
            if isinstance(val, str) and val.lower() == 'sim':
                df.at[index, col] = 1
            elif isinstance(val, str) and (val.lower() == 'não' or val.lower() == 'nao'):
                df.at[index, col] = 0
            else:
                df.at[index, col] = np.nan
    return df

if __name__ == '__main__':           
    df = pd.read_csv('data/interin/ambev-final-dataset_AmBev_final_dataset.csv')
    prep_df = Prep(df)

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

    prep_df \
        .apply_custom(rename_cols) \
        .apply_custom(replace_by_index, {
            'indexes': [9610, 31343],
            'cols': unnamed_cols,
            'val': np.nan
        }) \
        .drop_not_nulls(unnamed_cols) \
        .drop_cols(unnamed_cols) \
        .fill_null_with(-1.0, per_cols) \
        .apply_custom(check_float, {'cols': per_cols}) \
        .drop_nulls(per_cols) \
        .apply_custom(replace_nan, {'cols_dict': per_cols_replace})
        