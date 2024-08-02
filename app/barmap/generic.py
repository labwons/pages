try:
    from ..sector.generic import Wise
    from ..market.generic import Market
    from core import baseDataFrame
except ImportError:
    from app.sector.generic import Wise
    from app.market.generic import Market
    from app.barmap.core import baseDataFrame
from pandas import DataFrame
from typing import Dict


class MarketMap(object):

    _market_:Market = Market(auto_update=False)
    def __init__(self, index:str, update_index:bool=False, update_market:bool=False):
        wise = Wise(index, auto_update=update_index)
        if update_market:
            self._market_ = Market(auto_update=update_market)
        self._market_ = self._market_.drop(columns=[col for col in self._market_ if col in wise])

        self._merge = wise.join(self._market_, how='left')
        return

    @property
    def largeCap(self) -> baseDataFrame:
        attr = f"_{self._merge['indexName'].iloc[0]}_large"
        if not hasattr(self, attr):
            base = self._merge[self._merge['stockSize'] == 'large']
            self.__setattr__(attr, baseDataFrame(base))
        return self.__getattribute__(attr)
    
    @property
    def midCap(self) -> baseDataFrame:
        attr = f"_{self._merge['indexName'].iloc[0]}_mid"
        if not hasattr(self, attr):
            base = self._merge[self._merge['stockSize'] != 'large'].copy()
            base = base.sort_values(by="marketCap", ascending=False).head(400)
            self.__setattr__(attr, baseDataFrame(base))
        return self.__getattribute__(attr)