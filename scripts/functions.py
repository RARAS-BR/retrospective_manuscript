from typing import Callable, Union, List, Dict
from pandas import DataFrame, Series
import pandas as pd


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
def create_descriptive_table(df: DataFrame, columns: List[str]) -> DataFrame:
    keys_list = [' '.join(col.split('_')).capitalize() for col in columns]

    value_counts_list = [df[col].value_counts(total=True, ascending=False) for col in columns]

    grouped_df = pd.concat(value_counts_list, axis=0, keys=keys_list, names=['feature', 'value'])

    return grouped_df

