from typing import Dict
from pandas import DataFrame
import pandas as pd
import numpy as np
from scripts.variable_map import *


def process_tipo_tratamento(trat: pd.DataFrame, id_cols: list, column_map: dict, treatment_type: str):
    return (
        trat[id_cols + list(column_map.keys())]
        .dropna(subset=column_map.keys(), how='all')
        .assign(tipo_tratamento=treatment_type)
        .rename(column_map, axis=1)
    )


# Load files
FILE_PATH = 'scripts/original_data/'
SAVE_PATH = 'data/'
forms: Dict[str, DataFrame] = {}
for form in ['inclusao', 'identificacao', 'diagnostico', 'tratamento', 'internacao', 'obito', 'seguimento']:
    df: pd.DataFrame = pd.read_csv(f'{FILE_PATH}{form}.csv', low_memory=False)
    df = df[df['project_id'] == 17].reset_index(drop=True)
    df.drop(columns='project_id', inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    df.drop(columns=['data_preenchimento', 'responsavel_preenchimento'], inplace=True)
    forms[form] = df

inc = forms['inclusao']
idn = forms['identificacao']
diag = forms['diagnostico']
trat = forms['tratamento']
inter = forms['internacao']
obito = forms['obito']
seg = forms['seguimento']
centros = pd.read_csv(f'{FILE_PATH}centros.csv', low_memory=False)

# TODO: add to pipeline
# Fix outliers: 'Sem diagnóstico' with 'momento_diagnostico'
index_mask = diag[diag['status_diagnostico'] == 'Sem diagnóstico']['momento_diagnostico'].dropna().index
diag.loc[index_mask, 'momento_diagnostico'] = np.nan


# Preprocess: Identificação form
id_df = pd.merge(
    inc[['record_id', 'id_centro', 'data_consulta_revisada',
         'data_1a_consulta_centro', 'data_1a_consulta_especialidade']],
    idn[['record_id', 'id_centro', 'data_nascimento', 'idade', 'raca_cor',
         'genero', 'cidade_nascimento', 'regiao_nascimento', 'pais_nasc',
         'regiao_residencia', 'cidade_residencia']],
    on=['record_id', 'id_centro'],
    how='inner'
)

# Cast: columns starting with 'data_' to datetime
for col in id_df.filter(regex='^data_').columns:
    id_df[col] = pd.to_datetime(id_df[col])

# Feature: calculate ages
for new_col, col in zip(
        ['idade', 'idade_1a_consulta_centro', 'idade_1a_consulta_especialidade'],
        ['data_consulta_revisada', 'data_1a_consulta_centro', 'data_1a_consulta_especialidade']):
    id_df[new_col] = (
            id_df[col]
            - id_df['data_nascimento']
    ).dt.days.div(365.25)
    # Fix outliers: set negative age to NaN
    id_df.loc[id_df[new_col] < 0, new_col] = np.nan


for new_col, col in zip(
        ['tempo_acompanhamento_centro', 'tempo_acompanhamento_especialidade'],
        ['data_1a_consulta_centro', 'data_1a_consulta_especialidade']):
    id_df[new_col] = (
            id_df['data_consulta_revisada']
            - id_df[col]
    ).dt.days.div(365.25)
    id_df.loc[id_df[new_col] < 0, new_col] = np.nan


# Preprocess: Diagnóstico form
diag = pd.merge(
    diag[['record_id', 'id_centro', 'instance_id',
          'status_diagnostico', 'doenca_cid10',
          'doenca_orpha', 'doenca_omim', 'fonte_pagadora',
          'momento_diagnostico', 'data_diagnostico', 'sintomas',
          'recorrencia_familiar', 'consanguinidade_relatada',
          'idade_inicio_sintomas_dias', 'tipo_diagnostico',
          'idade_materna', 'idade_paterna'
          ]],
    id_df[['record_id', 'id_centro', 'data_nascimento']],
    on=['record_id', 'id_centro'],
    how='left'
)
diag['idade_inicio_sintomas'] = diag['idade_inicio_sintomas_dias'].div(365.25)

# Cast: datetime feature
diag['data_diagnostico'] = pd.to_datetime(diag['data_diagnostico'])

# Feature: odisseia diagnóstica
diag['idade_diagnostico'] = (
        diag['data_diagnostico']
        - diag['data_nascimento']
).dt.days.div(365.25)
diag.loc[diag['idade_diagnostico'] < 0, 'idade_diagnostico'] = np.nan

diag['odisseia_diagnostica'] = (
    diag['idade_diagnostico']
    - diag['idade_inicio_sintomas'].div(365.25)
)
_mask1 = diag['odisseia_diagnostica'] < 0
_mask2 = diag['status_diagnostico'] != 'Diagnóstico confirmado'
_mask3 = diag['momento_diagnostico'] != 'Pós-natal'
diag.loc[_mask1 | (_mask2 & _mask3), 'odisseia_diagnostica'] = np.nan

# Drop 'data_nascimento'
diag.drop(columns='data_nascimento', inplace=True)


# Preprocess: Tratamento form
id_cols = ['record_id', 'id_centro', 'instance_id']
diet_map = {
    'data_inicio_trat_diet': 'data_inicio',
    'ft_pag_trat_diet': 'fonte_pagadora'
}
reab_map = {
    'data_inicio_trat_reab': 'data_inicio',
    'ft_pag_trat_reab': 'fonte_pagadora'
}
med_map = {
    'data_inicio_trat_med': 'data_inicio',
    'ft_pag_trat_med': 'fonte_pagadora',
    'desc_trat_med': 'descricao'
}
outro_map = {
    'data_inicio_trat_outro': 'data_inicio',
    'ft_pag_trat_outro': 'fonte_pagadora',
    'desc_trat_outro': 'descricao'
}

tipo_tratamento_df = pd.concat([
    process_tipo_tratamento(trat, id_cols, diet_map, 'Dietético'),
    process_tipo_tratamento(trat, id_cols, reab_map, 'Reabilitação'),
    process_tipo_tratamento(trat, id_cols, med_map, 'Medicamentoso'),
    process_tipo_tratamento(trat, id_cols, outro_map, 'Outro')
])

# Cast datetime
tipo_tratamento_df['data_inicio'] = pd.to_datetime(tipo_tratamento_df['data_inicio'])

# Feature: idade inicio tratamento
tipo_tratamento_df = pd.merge(
    tipo_tratamento_df,
    id_df[['record_id', 'data_nascimento']],
    on='record_id',
    how='left'
)
tipo_tratamento_df['idade_inicio_tratamento'] = (
        tipo_tratamento_df['data_inicio']
        - tipo_tratamento_df['data_nascimento']
).dt.days.div(365.25)
tipo_tratamento_df.loc[tipo_tratamento_df['idade_inicio_tratamento'] < 0, 'idade_inicio_tratamento'] = np.nan

trat.drop(columns=[
    'data_inicio_trat_med', 'desc_trat_med', 'ft_pag_trat_med',
    'data_inicio_trat_diet', 'ft_pag_trat_diet', 'data_inicio_trat_reab',
    'ft_pag_trat_reab', 'desc_trat_outro', 'data_inicio_trat_outro',
    'ft_pag_trat_outro'], inplace=True)

# Preprocess: Seguimento form

inter['ocorrencia_internacao'] = 1
obito['ocorrencia_obito'] = 1

# Feature: idade óbito
obito = pd.merge(
    obito,
    id_df[['record_id', 'data_nascimento']],
    on='record_id',
    how='left'
)
obito['data_obito'] = pd.to_datetime(obito['data_obito'])
obito['idade_obito'] = (
        obito['data_obito']
        - obito['data_nascimento']
).dt.days.div(365.25)
obito.loc[obito['idade_obito'] < 0, 'idade_obito'] = np.nan
obito.drop(columns='data_nascimento', inplace=True)

seg = pd.merge(
    seg[['record_id', 'id_centro', 'quantidade_internacoes']],
    inter[['record_id', 'id_centro', 'data_internacao', 'cid_internacao', 'ocorrencia_internacao']],
    on=['record_id', 'id_centro'],
    how='outer'
)
seg = pd.merge(
    seg,
    obito[['record_id', 'id_centro', 'data_obito', 'idade_obito', 'necropsia_realizada', 'cid10', 'ocorrencia_obito']],
    on=['record_id', 'id_centro'],
    how='outer'
)
seg['ocorrencia_internacao'] = seg['ocorrencia_internacao'].fillna(0)
seg['ocorrencia_obito'] = seg['ocorrencia_obito'].fillna(0)
seg.rename(columns={'cid10': 'cid_obito'}, inplace=True)


# Anonimize sensitive data
id_df['record_id_anon'] = pd.factorize(id_df['record_id'])[0] + 1
# id_df['id_centro_anon'] = pd.factorize(id_df['id_centro'])[0] + 1
# Create a mapping between the original and anonymized ids
record_id_map = (
    id_df[['record_id', 'record_id_anon']]
    .drop_duplicates().set_index('record_id')
    ['record_id_anon'].to_dict()
)

# center_id_map = (
#     id_df[['id_centro', 'id_centro_anon']]
#     .drop_duplicates().set_index('id_centro')
#     ['id_centro_anon'].to_dict()
# )

# Map record_id and id_centro for all dataframes
for df in [id_df, diag, trat, tipo_tratamento_df, seg]:
    df['record_id'] = df['record_id'].map(record_id_map)
#     df['id_centro'] = df['id_centro'].map(center_id_map).astype('category')

# Drop 'record_id_anon' and 'id_centro_anon' from id_df
id_df.drop(columns=[
    'record_id_anon',
    # 'id_centro_anon'
], inplace=True)

# Map variables and columns values
id_df['raca_cor'] = id_df['raca_cor'].map(raca_cor)
id_df['genero'] = id_df['genero'].map(genero)
id_df['regiao_nascimento'] = id_df['regiao_nascimento'].map(regiao_nascimento)
id_df['regiao_residencia'] = id_df['regiao_residencia'].map(regiao_residencia)
diag['status_diagnostico'] = diag['status_diagnostico'].map(status_diagnostico)
diag['momento_diagnostico'] = diag['momento_diagnostico'].map(momento_diagnostico)
diag['tipo_diagnostico'] = diag['tipo_diagnostico'].map(tipo_diagnostico)
diag['recorrencia_familiar'] = diag['recorrencia_familiar'].map(recorrencia_familiar)
diag['consanguinidade_relatada'] = diag['consanguinidade_relatada'].map(consanguinidade_relatada)
trat['alvo_tratamento'] = trat['alvo_tratamento'].map(alvo_tratamento)
trat['acompanha_outra_especialidade'] = trat['acompanha_outra_especialidade'].map(acompanha_outra_especialidade)
tipo_tratamento_df['tipo_tratamento'] = tipo_tratamento_df['tipo_tratamento'].map(tipo_tratamento)
seg['ocorrencia_internacao'] = seg['ocorrencia_internacao'].map(ocorrencia_internacao)
seg['ocorrencia_obito'] = seg['ocorrencia_obito'].map(ocorrencia_obito)
seg['necropsia_realizada'] = seg['necropsia_realizada'].map(necropsia_realizada)


id_df.rename(columns=identificacao_columns, inplace=True)
diag.rename(columns=diagnostico_columns, inplace=True)
trat.rename(columns=tratamento_columns, inplace=True)
tipo_tratamento_df.rename(columns=tipo_tratamento_columns, inplace=True)
seg.rename(columns=seguimento_columns, inplace=True)


# Save to csv
id_df.to_csv(f'{SAVE_PATH}identification.csv', index=False)
diag.to_csv(f'{SAVE_PATH}diagnostic.csv', index=False)
trat.to_csv(f'{SAVE_PATH}treatment.csv', index=False)
tipo_tratamento_df.to_csv(f'{SAVE_PATH}treatment_type.csv', index=False)
seg.to_csv(f'{SAVE_PATH}follow_up.csv', index=False)
centros.to_csv(f'{SAVE_PATH}centers.csv', index=False)
