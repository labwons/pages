try:
    from ..common.date import TradingDate
    from ..common.deco import memorize
    from ..sector.generic import Wise
    from core import bmFrame
    import fetch
except ImportError:
    from app.common.date import TradingDate
    from app.common.deco import memorize
    from app.sector.generic import Wise
    from app.barmap.core import bmFrame
    from app.barmap import fetch
from datetime import date, datetime, timedelta
from pandas import DataFrame
from pykrx import stock
from requests.exceptions import JSONDecodeError, SSLError
from typing import Dict, List, Union, Iterable
import pandas as pd


class BarMap(Wise):
    
    def __init__(self, key:str):
        Wise.__init__(self, key)
        self['cover'] = self['industryName'].str.replace("WICS ", "").replace("WI26 ", "")
        self = self[['name', 'cover', 'industryCode', 'industryName', 'sectorCode', 'sectorName']]
        
        super().__init__(
            self \
            .join(self.marketCap, how='left') \
            .join(self.earningRate, how='left') \
            .join(self.multiple, how='left')
        )
        self.sort_values(by='marketCap', ascending=False, inplace=True)
        return
            
    @memorize
    def marketCap(self) -> DataFrame:
        return fetch.marketCap(TradingDate.near)
    
    @memorize
    def ipo(self) -> DataFrame:
        return fetch.ipo(TradingDate.near)
    
    @memorize
    def multiple(self) -> DataFrame:
        return fetch.multiple(TradingDate.near)
    
    @memorize
    def earningRate(self) -> DataFrame:
        return fetch.earningRate(TradingDate.periods)
    
    @memorize
    def largeIndex(self) -> List[str]:
        return fetch.largeCaps()
    
    @memorize
    def largeCaps(self) -> bmFrame:
        return bmFrame(self[self['ticker'].isin(self.largeIndex)])
    
    @memorize
    def midCaps(self) -> bmFrame:
        return bmFrame(self[~self['ticker'].isin(self.largeIndex)].head(500))
    
    
    
    
