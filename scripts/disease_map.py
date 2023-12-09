import pandas as pd
from IPython.display import display
Y, C, R = '\033[93m', '\033[96m', '\033[0m'

PKU = {
    'orpha': ['716'],
    'omim': ['261600'],
    'cid10': ['E70.0', 'E70.1']
}

CF = {
    'orpha': ['586'],
    'omim': ['219700'],
    'cid10': ['E84.0', 'E84.1', 'E84.8', 'E84.9']
}

ACRO = {
    'orpha': ['963'],
    'omim': ['102200', '300943'],
    'cid10': ['E22.0']
}

OI = {
    'orpha': ['666', '216796', '216820', '216812', '216804', '2771', '216828'],
    'omim': ['610682 - 610915 - 610967 - 610968 - 613848 - 613849 - 613982 - '
             '614856 - 615066 - 615220 - 616229 - 616507 - 166200 - 166210 - '
             '166220 - 166230 - 259420 - 259440', '610967'],
    'cid10': ['Q78.0']
}

DISEASE_MAPS = [PKU, CF, ACRO, OI]

DISEASE_NAMES = ['Phenylketonuria', 'Cystic Fibrosis', 'Acromegaly', 'Osteogenesis Imperfecta']


def display_disease_count(df: pd.DataFrame, disease_names=None, disease_maps=None) -> None:

    # Default args
    if disease_maps is None:
        disease_maps = DISEASE_MAPS
    if disease_names is None:
        disease_names = DISEASE_NAMES

    # Check for valid columns
    if not df.columns.isin(['disease_orpha', 'disease_omim', 'disease_cid10']).all():
        raise ValueError('df must contain the following columns: '
                         '["disease_orpha", "disease_omim", "disease_cid10"]')

    for name, data in zip(disease_names, disease_maps):
        s = pd.Series(dtype=int)
        for key in ['orpha', 'cid10', 'omim']:
            for value in data[key]:
                x = df[f'disease_{key}'].dropna().apply(lambda x: x.split(',')[0])
                if value in x.values:
                    count = x[x == value].count()
                    s[f'{key} {value}'] = count
        print(f'{Y}{name} {C}(n={s.sum()}){R}')
        s.sort_values(ascending=False, inplace=True)
        display(s)

