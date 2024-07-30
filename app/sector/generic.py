try:
    import fetch
except ImportError:
    from app.sector import fetch
from pandas import DataFrame
from typing import Any, Dict
import pandas, os


class Wise(DataFrame):
    
    def __init__(self, index:str, auto_update:bool=False):
        _date = fetch.index_date()
        _name = fetch.index_name(index)
        _code = fetch.KEYS[_name]
        _path = os.path.join(os.path.dirname(__file__), rf'archive/{_name.lower()}.json')
        _root = f"https://raw.githubusercontent.com/labwons/pages/main/app/sector/archive/{_name.lower()}.json"
        
        if auto_update:
            super().__init__(
                pandas.concat(
                    objs=[fetch.index_component(_date, cd) for cd in _code],
                    axis=0,
                    ignore_index=False
                )
            )
            self.to_json(_path, orient='index')
            return
        try:
            super().__init__(pandas.read_json(_path, orient='index'))
        except (FileExistsError, FileNotFoundError):
            super().__init__(pandas.read_json(_root, orient='index'))
        return        
    
    
if __name__ == "__main__":
    
    print(Wise('WICS'))