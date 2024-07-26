import sys
sys.path.append(r'D:\J.H.LEE\05. CODING\LABWONS\pages')
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
                data = fetch(_type)        
        elif isinstance(_type, Dict):
            data = fetch(_type)
        super().__init__(data)
        return   
    
    
if __name__ == "__main__":

    
    print(Wise('WICS'))
