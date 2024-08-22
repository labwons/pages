try:
    from ..sector.generic import Sector
    from ..market.generic import Market
    from core import baseDataFrame
except ImportError:
    from __py__.sector.generic import Sector
    from __py__.market.generic import Market
    from __py__.treemap.core import baseDataFrame
from typing import Dict


class MarketMap(object):

    def __init__(self, auto_update=False):
        sector = Sector(auto_update=False)
        number = Market(auto_update=auto_update)
        self._merge = sector.join(number.drop(columns=[col for col in number if col in sector]))
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