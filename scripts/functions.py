from typing import Callable, Union, List, Any
from pandas import DataFrame, Series
import requests
import numpy as np
import pandas as pd
from scripts.disease_map import DISEASE_MAPS, DISEASE_NAMES


def custom_value_counts(func: Callable[..., pd.Series]) -> Callable[..., pd.Series]:
    def wrapper(self: Series, total: bool = False, *args: any, **kwargs: any) -> Union[Series, DataFrame]:
        if total:
            unsupported_args = {'bins', 'normalize'}

            # Raise error for unsupported arguments
            if unsupported_args.intersection(kwargs.keys()):
                raise ValueError(f"The 'total' argument does not support the following arguments: {unsupported_args}.")

            count = func(self, *args, **kwargs)
            # Drop na if kwargs['dropna'] is True
            if kwargs.get('dropna', True):
                self = self.dropna()

            # Wrapper transformation
            percentage = count / len(self) * 100
            result = pd.concat([count, percentage], axis=1, keys=['n', '%'])

            # Sort values
            sort_kwargs = {
                'by': 'n',
                'ascending': True if kwargs.get('ascending', True) else False,
                'inplace': True
            }
            if kwargs.get('sort', True):
                result.sort_values(**sort_kwargs)

            return result
        else:
            return func(self, *args, **kwargs)

    return wrapper


# TODO: add docs
def create_descriptive_table(df: DataFrame, columns: List[str], dropna: bool = True) -> DataFrame:
    keys_list = [' '.join(col.split('_')).capitalize() for col in columns]

    value_counts_list = [df[col].value_counts(total=True, ascending=False, dropna=dropna) for col in columns]

    grouped_df = pd.concat(value_counts_list, axis=0, keys=keys_list, names=['feature', 'value'])

    return grouped_df


def create_disease_count(df: pd.DataFrame, disease_names=None, disease_maps=None) -> Series:

    # Default args
    if disease_maps is None:
        disease_maps = DISEASE_MAPS
    if disease_names is None:
        disease_names = DISEASE_NAMES

    # Check for valid columns
    if not df.columns.isin(['disease_orpha', 'disease_omim', 'disease_cid10']).all():
        raise ValueError('df must contain the following columns: '
                         '["disease_orpha", "disease_omim", "disease_cid10"]')

    series = []
    for name, data in zip(disease_names, disease_maps):
        s = pd.Series(dtype=int)
        for key in ['orpha', 'cid10', 'omim']:
            for value in data[key]:
                x = df[f'disease_{key}'].dropna().apply(lambda x: x.split(',')[0])
                if value in x.values:
                    count = x[x == value].count()
                    s[f'{key} {value}'] = count
        s.name = name + ' (n=' + str(s.sum()) + ')'
        s.sort_values(ascending=False, inplace=True)
        series.append(s)

    final_series = pd.concat(series, axis=0, keys=[s.name for s in series])
    final_series.name = 'n'

    return final_series


def get_disease_name(x: str) -> float | Any:
    url = 'https://api.orphadata.com/rd-cross-referencing'
    params = {'lang': 'en'}
    endpoint_map = {
        'ORPHA': 'orphacodes',
        'CID10': 'icd-10s',
        'OMIM': 'omims'
    }

    # Get code
    code = x.split(':')[1]

    # Define the endpoint
    prefix = x.split(':')[0]
    endpoint = endpoint_map.get(prefix)

    if endpoint is None:
        print(f"Invalid code prefix: {prefix}")
        return np.nan

    r = requests.get(f'{url}/{endpoint}/{code}', params=params)

    if r.status_code != 200:
        print(f"Request failed with status code {r.status_code} for row {x}")
        return np.nan

    data = r.json()['data']['results']
    # Check if data is a list and return the first 'Preferred term', else return the 'Preferred term' directly
    return data[0]['Preferred term'] if isinstance(data, list) else data['Preferred term']
