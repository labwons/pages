try:
    import fetch
except ImportError:
    from app.sector import fetch
from pandas import DataFrame
from typing import Any, Dict
import pandas as pd
import os


class Wise(DataFrame):
    
    def __init__(self, index:str):
        _date = fetch.index_date()
        _name = fetch.index_name(index)
        _path = os.path.join(os.path.dirname(__file__), rf'archive/{_name.lower()}.json')
        _code = fetch.KEYS[_name]
        
        try:
            super() \
                .__init__(pd.read_json(_path, orient='index'))
        except (FileExistsError, FileNotFoundError, ValueError):
            super() \
                .__init__(pd.concat(
                    objs=[fetch.index_component(_date, cd) for cd in _code],
                    axis=0,
                    ignore_index=False
            ))
            self.to_json(_path, orient='index')        
        return   
    
    
if __name__ == "__main__":

    
    print(Wise('WICS'))
