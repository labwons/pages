import sys
sys.path.append(r'D:\J.H.LEE\05. CODING\LABWONS\pages')
try:
    from ..common import PATH
    from fetch import KEY, fetch
except ImportError:
    from app.common import PATH
    from app.sector.fetch import KEY, fetch
from pandas import concat, DataFrame
from typing import Dict, Iterable, Union
import pandas as pd


class Wise(DataFrame):
    def __init__(self, _type:str):
        if _type.upper() == 'WICS':
            file = PATH.JSONWICS
            keys = KEY.WICS
        elif _type.upper() == 'WI26':
            file = PATH.JSONWI26
            keys = KEY.WI26
        else:
            raise KeyError(f'Unknown MAP Type: {_type}')
        
        try:
            data = pd.read_json(file, orient='index')
        except (FileNotFoundError, FileExistsError):
            data = pd.concat(
                objs=[fetch(code) for code in keys],
                axis=0,
                ignore_index=True
            )
            data.set_index(keys='ticker', inplace=True)
        super().__init__(data)
        return
    
    
if __name__ == "__main__":

    
    print(Wise('WICS'))
