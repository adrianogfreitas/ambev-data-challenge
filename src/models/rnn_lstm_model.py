# -*- coding: utf-8 -*-
"""03-agf-model.ipynb
TODO:
- cruzar regras de atendimento parcial com metas do mes (ating/pont/acum)
- acum pode significar ating+pontos
- transformar em regex

# Ambev data challenge
## Adriano Freitas

## Modelo de previsão de cumprimento da meta

Este notebook tem o objetivo de criar um modelo para prever o cumprimento da meta.
"""

from ml_belt.prep import Prep
import pandas as pd
import numpy as np
import os
import re

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

def log(df, text):
    print(text)
    print(df.shape)
    print(df.columns)
    return df

data_path = 'data/processed/'
file_name = 'ambev-final-dataset-processed.csv'

df = pd.read_csv(os.path.join(data_path, file_name), low_memory=False)
df.shape
df.head()

"""### Preparando dataframe

#### Scaling e Encoding
"""

pattern = re.compile('nom_\w+')
col_search = np.vectorize(lambda x, pattern=pattern: bool(pattern.search(x)))
idx_filter = col_search(df.columns)
nom_cols = df.columns[idx_filter]

drop_cols = [
    'ord_mes_referencia', 
    'dis_nome_kpi', 
    'per_peso_kpi', 
    'nom_prazo',
    'nom_regra_alcance_parcial', 
    'bin_meta_projeto', 
    'per_pontos_mes',
    'per_acum_mes', 
    'per_ating_acumulado',
    'per_pontos_acumulado', 
    'per_acum_acumulado', 
    'per_ating_fim_exer',
    'per_pontos_fim_exer', 
    'per_acum_fim_exer'
]

prep_df = Prep(df) \
    .apply_custom(log, {'text': 'init'}) \
    .drop_cols(drop_cols) \
    .apply_custom(log, {'text': 'cols dropped'}) \
    .encode(nom_cols) \
    .apply_custom(log, {'text': 'encoded'}) \
    .scale() \
    .apply_custom(log, {'text': 'scaled'})

print(prep_df.df.head())

"""#### Spliting X e y mantendo sequência de 3 meses"""

train_df = prep_df.df.values
print(train_df.shape)

i_len = 10621 * 3

if os.path.isfile('data/processed/X.npy') and os.path.isfile('data/processed/y.npy'):
    X = np.load('data/processed/X.npy')
    y = np.load('data/processed/y.npy')
else:
    for i in range (i_len, len(train_df)):
        if i == i_len:
            X = np.array([train_df[i - i_len : i, :17]])
            y = np.array([train_df[i, 17]])
            print(X.shape, y.shape)
        else:
            X = np.append(X, np.array([train_df[i - i_len : i, :17]]), axis=0)
            y = np.append(y, np.array([train_df[i, 17]]), axis=0)
            if i == i_len + 1:
                print(X.shape, y.shape)
            if i % 1000 == 0:
                print(i, X.shape, y.shape)
    np.save('data/processed/X', X)
    np.save('data/processed/y', y)

print(X.shape, y.shape)
quit()

"""## Criando o modelo"""

input_shape = (X.shape[1], 17)

model = Sequential()
model.add(LSTM(units = 100, 
               return_sequences = True, 
               input_shape = input_shape))
model.add(Dropout(0.3))

model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.3))

model.add(LSTM(units = 50))
model.add(Dropout(0.3))

model.add(Dense(units = 1, activation = 'sigmoid'))  # linear

model.compile(optimizer='rmsprop', 
              loss='mean_squared_error', 
              metrics=['mean_absolute_error'])

es = EarlyStopping(monitor='loss', min_delta=1e-10, patience=10, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, verbose=1)
mcp = ModelCheckpoint(filepath='weights.{epoch:02d}-{val_loss:.2f}.hdf5', 
                      monitor='loss', save_best_only=True, verbose=1)

model.fit(X, y, epochs=100, batch_size=32, callbacks=[es, reduce_lr, mcp])
