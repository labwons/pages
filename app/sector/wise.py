try:
    from .core.fetch import sector
except ImportError:
    from app.sector.core.fetch import sector
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
        return
