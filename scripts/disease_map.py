from pandas import Series
import pandas as pd

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
