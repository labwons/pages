try:
    from ..treemap.core import MAP_KEYS, coloring, num2cap
    from ..market.generic import Market
    from ..sector.generic import Sector
except ImportError:
    from __py__.treemap.core import MAP_KEYS, coloring, num2cap
    from __py__.market.generic import Market
    from __py__.sector.generic import Sector

from pandas import DataFrame
from typing import Dict
import pandas as pd
    
    
class Rank(object):

    __mem__ = {}
    def __init__(self):
        sector = Sector(auto_update=False)
        number = Market(auto_update=False)
        _merge = sector.join(number.drop(columns=[col for col in number if col in sector]))
        _merge[MAP_KEYS] = round(_merge[MAP_KEYS], 2)
        self._merge = coloring(_merge)
        return

    def __str__(self) -> str:
        self.analyze('sectorName')
        self.analyze('industryName')
        _str = ""
        for n, (var, data) in enumerate(self.__mem__.items()):
            _str += f'\t"{var}": {data}'
            if n < len(self.__mem__) - 1:
                _str += ",\n"
        return _str.replace("'", '"')

    def _sort(self, df:DataFrame) -> Dict[str, DataFrame]:
        final = {}
        for key in MAP_KEYS:
            if key in ['PER', 'PBR']:
                df = df[df[key] > 0]
            _sort = df.sort_values(by=key, ascending=False)
            point = int(len(_sort) / 2) if len(_sort) < 20 else 10
            if key == "DIV":
                _join = _sort.head(2 * point).copy()
            else:            
                _join = pd.concat(objs=[_sort.head(point), _sort.tail(point)], axis=0).copy()
            _join['count'] = f'{len(_join)} / {len(_sort)} 종목'
            _join['meta'] = "시가총액: " + (_join['marketCap']/100000000).apply(num2cap) + '원<br>' \
                            '종가: ' + _join['close'].astype(int).apply(lambda x: f"{x:,d}원")
            if key == "PER":
                _join['meta'] = _join['meta'] + '<br>EPS: ' + _join['EPS'].astype(int).apply(lambda x: f"{x:,d}원")
            elif key == 'PBR':
                _join['meta'] = _join['meta'] + '<br>BPS: ' + _join['BPS'].astype(int).apply(lambda x: f"{x:,d}원")
            else:
                pass
            _join = _join[['name', 'meta', key, f'{key}-C', 'count']]
            final[key] = _join
        return final

    def analyze(self, column:str):
        for (name, ), group in self._merge.groupby(by=[column]):
            _sorted = self._sort(group)
            for key, data in _sorted.items():
                count = data['count'].values[0]
                data = data.drop(columns=['count'])
                json = data.to_dict(orient='list')
                json['count'] = count
                self.__mem__[f"{name.replace('WI26 ', '')}_{key}"] = json
        return