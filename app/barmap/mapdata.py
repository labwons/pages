from pandas import DataFrame
import pandas as pd
import os


def fetch(index:DataFrame, properties:DataFrame) -> DataFrame:
    if not str(index.index.name) == 'ticker':
        index = index.set_index(keys='ticker')
    basis = index.join(properties, how='left')
    basis = basis.sort_values(by='marketCap', ascending=False)
    basis = basis.head(1000)
    return basis