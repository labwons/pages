try:
    from ..common import PATH
    from fetch import fetch
except ImportError:
    from app.common import PATH
    from app.sector.fetch import fetch
from pandas import DataFrame
from typing import Dict, Union
import pandas as pd


class Wise(DataFrame):
    
    def __init__(self, _type:Union[str, Dict]):
        if isinstance(_type, str):
            if _type.upper() == 'WICS':
                file = PATH.JSONWICS
            elif _type.upper() == 'WI26':
                file = PATH.JSONWI26
            else:
                raise KeyError(f'Unknown MAP Type: {_type}')
            
            try:
                data = pd.read_json(file, orient='index')
            except (FileNotFoundError, FileExistsError):
                pass
        super().__init__(fetch(_type))
        return   
    
    
if __name__ == "__main__":

    
    print(Wise('WICS'))
