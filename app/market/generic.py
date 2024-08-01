try:
    from .fetch import krx
except ImportError:
    from app.market.fetch import krx
from pandas import DataFrame
from typing import List
import pandas, os


class Market(DataFrame):
    
    def __init__(self, auto_update:bool=False):
        try:
            _path = os.path.join(os.path.dirname(__file__), r"archive/market.json")                
        except NameError:
            _path = "https://raw.githubusercontent.com/labwons/pages/main/app/market/archive/market.json"
            
        if auto_update:
            print("Fetching Market Cap... ", end="")
            _market_cap = krx.marketCap()
            print("Success")
            
            print("Fetching Multiple... ", end="")
            _multiple = krx.multiple()
            print("Success")
            
            print("Fetching IPO... ", end="")
            _ipo = krx.ipo()
            print("Success")
            
            print("Fetching Earning Ratio... ", end="")
            _earning_ratio = krx.earningRatio()
            print("Success")
            
            super().__init__(
                pandas.concat(
                    objs=[_market_cap, _multiple, _ipo, _earning_ratio],
                    axis=1,
                    ignore_index=False
                )
            )
            self['ipo'] = self['ipo'].astype(str)
            self.to_json(_path, orient='index')
            return
            
        super().__init__(pandas.read_json(_path, orient='index'))
        self.index = self.index.astype(str).str.zfill(6)
        self.index.name = 'ticker'
        return
    
