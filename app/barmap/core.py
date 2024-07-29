try:
    from ..common.deco import memorize
except ImportError:
    from app.common.deco import memorize
from pandas import DataFrame
import pandas as pd


class bmFrame(DataFrame):
    
    KEYS = ['PER', 'PBR', 'D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1']
    def __init__(self, stocks:DataFrame):
        super().__init__(stocks)
        self['size'] = (self['marketCap'] / 100000000).astype(int)
        self['close'] = self['close'].apply(lambda x: f"{x:,}원")
        
        objs = [self, self.industry]
        if self._get_map_name() == "WICS":
            objs.append(self.sector)
        objs.append(self.header)
        super().__init__(pd.concat(objs=objs, axis=0, ignore_index=True))
        return
    
    def _get_map_name(self) -> str:
        _get = self.iloc[0]['industryName']
        return 'WICS' if _get.startswith('WICS') else 'WI26'
    
    @memorize
    def industry(self) -> DataFrame:
        cover = self._get_map_name()
        objs = []
        for (code, name), group in self.groupby(by=['industryCode', 'industryName']):
            obj = {
                'ticker': code.zfill(6),
                'name': name,
                'cover': group.iloc[0]['sectorName'] if cover == 'WICS' else cover,
                'size': group['size'].sum(),
                'DIV': 0 if group['DIV'].empty else group['DIV'].mean()
            }
            obj.update({
                key: (group[key] * group['size'] / group['size'].sum()).sum() \
                for key in self.KEYS
            })
            objs.append(obj)
        return DataFrame(objs)
    
    @memorize
    def sector(self) -> DataFrame:
        cover = self._get_map_name()
        if cover == 'WI26':
            return DataFrame()
        objs = []
        for (code, name), group in self.groupby(by=['sectorCode', 'sectorName']):
            obj = {
                'ticker': code.zfill(6),
                'name': name,
                'cover': cover,
                'size': group['size'].sum(),
                'DIV': 0 if group['DIV'].empty else group['DIV'].mean()
            }
            obj.update({
                key: (group[key] * group['size'] / group['size'].sum()).sum() \
                for key in self.KEYS
            })
            objs.append(obj)
        return DataFrame(objs)
    
    @memorize
    def header(self) -> DataFrame:
        return DataFrame(
            index=[0],
            data={
                'ticker': '000000',
                'name': self._get_map_name(),
                'cover': '',
                'size': self['size'].sum(),
            }
        )
        
    