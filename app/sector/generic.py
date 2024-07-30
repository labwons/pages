try:
    import fetch
except ImportError:
    from app.sector import fetch
from pandas import DataFrame
from pykrx.stock import get_index_portfolio_deposit_file
from typing import List
import pandas, os


class Wise(DataFrame):
    
    __kq__:List[str] = []
    
    def __init__(self, index:str, auto_update:bool=False):
        if not self.__kq__:
            self.__kq__ = get_index_portfolio_deposit_file('2001')
            
        _name = fetch.index_name(index)        
        try:
            _path = os.path.join(os.path.dirname(__file__), rf'archive/{_name.lower()}.json')
        except NameError:
            _path = f"https://raw.githubusercontent.com/labwons/pages/main/app/sector/archive/{_name.lower()}.json"
        
        if auto_update:
            _date = fetch.index_date()
            _code = fetch.KEYS[_name]
            super().__init__(
                pandas.concat(
                    objs=[fetch.index_component(_date, cd) for cd in _code],
                    axis=0,
                    ignore_index=False
                )
            )
            self['name'] = self.apply(lambda x: f'{x}*' if x.index in self.__kq__ else x, axis=1)
            self.to_json(_path, orient='index')
            return
    
        super().__init__(pandas.read_json(_path, orient='index'))    
        self.index = self.index.astype(str).str.zfill(6)
        self.index.name = 'ticker'
        return        
    
    
if __name__ == "__main__":
    
    print(Wise('WICS'))