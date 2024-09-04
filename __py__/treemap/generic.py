try:
    from ..market.fetch.date import TradingDate
    from ..sector.generic import Sector
    from ..market.generic import Market
    from core import baseTreeMap
except ImportError:
    from __py__.market.fetch.date import TradingDate
    from __py__.sector.generic import Sector
    from __py__.market.generic import Market
    from __py__.treemap.core import baseTreeMap
from typing import Dict


class MarketMap(object):

    def __init__(self, auto_update=False):
        sector = Sector(auto_update=False)
        number = Market(auto_update=auto_update)
        self._merge = sector.join(number.drop(columns=[col for col in number if col in sector]))
        return

    def __str__(self) -> str:
        lc = self.largeCap.copy()
        lcs = self.largeCapSamsungExcluded.copy()
        md = self.midCap.copy()
        return f"""\t"Date": "{TradingDate.near.strftime('%Y.%m.%d')[2:]} 기준 ",
    "LargeCap": {lc.drop(columns=["kind"]).to_dict(orient='list')},
    "LargeCapWithoutSamsung" : {lcs.drop(columns=["kind"]).to_dict(orient='list')},
    "MidCap": {md.drop(columns=["kind"]).to_dict(orient='list')},
    "LargeSectors": {lc[lc["kind"] == "sector"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')},
    "MidSectors": {md[md["kind"] == "sector"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')},
    "LargeIndustries": {lc[(lc["kind"] == "industry") | (lc["name"].isin(['에너지', '유틸리티']))].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')},
    "MidIndustries": {md[(md["kind"] == "industry") | (md["name"].isin(['에너지', '유틸리티']))].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')}
""".replace("'", '"').replace("nan", '""')

    @property
    def largeCap(self) -> baseTreeMap:
        attr = f"_large"
        if not hasattr(self, attr):
            base = self._merge[self._merge['stockSize'] == 'large']
            self.__setattr__(attr, baseTreeMap(base))
        return self.__getattribute__(attr)
    
    @property
    def largeCapSamsungExcluded(self) -> baseTreeMap:
        attr = f"_large_samsung_excluded"
        if not hasattr(self, attr):
            base = self._merge[self._merge['stockSize'] == 'large']
            base = base.drop(index=['005930'])
            self.__setattr__(attr, baseTreeMap(base))
        return self.__getattribute__(attr)
    
    @property
    def midCap(self) -> baseTreeMap:
        attr = f"_mid"
        if not hasattr(self, attr):
            base = self._merge[self._merge['stockSize'] != 'large'].copy()
            base = base.sort_values(by="marketCap", ascending=False).head(400)
            self.__setattr__(attr, baseTreeMap(base))
        return self.__getattribute__(attr)