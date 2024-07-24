try:
    from .core import sector
except ImportError:
    from app.sector.fetch import sector
from pandas import concat, DataFrame
from typing import Dict, Iterable, Union


class wise(DataFrame):
    def __init__(self, index:Union[Dict, Iterable]):
        super().__init__(
            concat(
                objs=[sector(cd) for cd in index], 
                axis=0, 
                ignore_index=True
            ))
        self.set_index(keys='ticker', inplace=True)
        return
