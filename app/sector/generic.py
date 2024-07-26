try:
    from fetch import fetch
except ImportError:
    from app.sector.fetch import fetch
from pandas import concat, DataFrame
from typing import Dict, Iterable, Union


class Wise(DataFrame):
    def __init__(self, index:Dict[str, str]):
        super().__init__(
            concat(
                objs=[fetch(cd) for cd in index], 
                axis=0, 
                ignore_index=True
            ))
        self.set_index(keys='ticker', inplace=True)
        return
