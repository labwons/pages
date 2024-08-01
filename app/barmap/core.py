from pandas import DataFrame
from typing import Dict
import pandas


COLOR_SCALE = ['#F63538', '#BF4045', '#8B444E', '#414554', '#35764E', '#2F9E4F', '#30CC5A']  # Low <---> High
COLOR_PINS = {
    'Y-1': ([-30, -20, -10, 0, 10, 20, 30], [-25, -15, -5, 5, 15, 25]),
    'M-6': ([-24, -16, -8, 0, 8, 16, 24], [-20, -12, -4, 4, 12, 20]),
    'M-3': ([-18, -12, -6, 0, 6, 12, 18], [-15, -9, 3, 3, 9, 15]),
    'M-1': ([-10, -6.7, -3.3, 0, 3.3, 6.7, 10], [-8.35, -5, -1.65, 1.65, 5, 8.35]),
    'W-1': ([-6, -4, -2, 0, 2, 4, 6], [-5, -3, -1, 1, 3, 5]),
    'D-1': ([-3, -2, -1, 0, 1, 2, 3], [-2.5, -1.5, -0.1, 0.1, 1.5, 2.5])
}



class baseDataFrame(DataFrame):


    MAINKEY = ['D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1', 'PER', 'PBR', 'DIV']
    def __init__(self, map_type:str, stocks:DataFrame):
        _cap_type = "Large Cap"
        if not "005930" in stocks.index:
            _cap_type = "Mid Cap"
        
        stocks = stocks.copy()
        stocks.index.name = 'ticker'
        stocks.reset_index(inplace=True)
        stocks['cover'] = stocks['industryName'] \
                          .str.replace("WICS ", "") \
                          .str.replace("WI26 ", "")
        stocks['size'] = (stocks['marketCap'] / 100000000).astype(int)
        stocks['close'] = stocks['close'].astype(int).apply(lambda x: f"{x:,d}")
        stocks['marketCap'] = stocks['size'].apply(self._cap_reform)
        stocks['meta'] = stocks['name'] + "(" + stocks['ticker'] + ")" \
                        + "<br>시총: " + stocks['marketCap'] + '원'\
                        + "<br>종가: " + stocks['close']
        stocks['kind'] = 'stock'
        objs = [stocks]

        industry = self._grouping(*stocks.groupby(by=['industryName']))
        industry['kind'] = 'industry'
        if map_type == 'WI26':
            industry['cover'] = _cap_type
        objs.append(industry)

        if map_type == 'WICS':
            sector = self._grouping(*stocks.groupby(by=['sectorName']))
            sector['cover'] = _cap_type
            sector['kind'] = 'sector'
            objs.append(sector)

        data = {
            'name': _cap_type,
            'cover': '',
            'size': stocks['size'].sum(),
        }
        for key in self.MAINKEY:
            data[key] = round(stocks[key].mean(), 2)
        header = DataFrame(data=data, index=[0])
        objs.append(header)

        data = pandas.concat(objs=objs, axis=0, ignore_index=True)
        data = data.drop_duplicates(subset='name', keep='last')
        data = self._coloring(data)
        data = data[[
            'name', 'cover', 'size', 'meta', 'kind',
            'PER', 'PBR', 'DIV', 'PER-C', 'PBR-C', 'DIV-C',
            'D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1',
            'Y-1-C', 'M-6-C', 'M-3-C', 'M-1-C', 'W-1-C', 'D-1-C'
        ]]
        data[self.MAINKEY] = round(data[self.MAINKEY], 2)
        super().__init__(data)
        return

    def _grouping(self, *args):
        objs = []
        for (name, ), group in args:
            name = name.replace("WICS ", "").replace("WI26 ", "")
            size = group['size'].sum()
            obj = {
                'name': name,
                'size': size,
                'cover': group.iloc[0]['sectorName'],
                'meta': f"{name}<br>시총: {self._cap_reform(size)}원",
                'DIV': 0 if group['DIV'].empty else group['DIV'].mean()
            }
            for key in self.MAINKEY:
                obj[key] = round(
                    (group[key] * group['size'] / group['size'].sum()).sum(), 2
                )
            objs.append(obj)
        return DataFrame(objs)

    @staticmethod
    def _coloring(data:DataFrame):
        scale = ['#F63538', '#BF4045', '#8B444E', '#414554', '#35764E', '#2F9E4F', '#30CC5A']  # Low <---> High
        bound = {
            'Y-1': ([-30, -20, -10, 0, 10, 20, 30], [-25, -15, -5, 5, 15, 25]),
            'M-6': ([-24, -16, -8, 0, 8, 16, 24], [-20, -12, -4, 4, 12, 20]),
            'M-3': ([-18, -12, -6, 0, 6, 12, 18], [-15, -9, 3, 3, 9, 15]),
            'M-1': ([-10, -6.7, -3.3, 0, 3.3, 6.7, 10], [-8.35, -5, -1.65, 1.65, 5, 8.35]),
            'W-1': ([-6, -4, -2, 0, 2, 4, 6], [-5, -3, -1, 1, 3, 5]),
            'D-1': ([-3, -2, -1, 0, 1, 2, 3], [-2.5, -1.5, -0.1, 0.1, 1.5, 2.5])
        }

        colored = DataFrame(index=data.index)
        for col, (na, bins) in bound.items():
            color = data[col].apply(
                lambda rt:
                scale[3] if str(rt) == 'nan' else \
                scale[0] if rt <= bins[0] else \
                scale[1] if bins[0] < rt <= bins[1] else \
                scale[2] if bins[1] < rt <= bins[2] else \
                scale[3] if bins[2] < rt <= bins[3] else \
                scale[4] if bins[3] < rt <= bins[4] else \
                scale[5] if bins[4] < rt <= bins[5] else \
                scale[6]
            )
            color.name = f'{col}-C'
            colored = colored.join(color.astype(str), how='left')

        for f in ['PBR', 'PER', 'DIV']:
            re_scale = scale if f == 'DIV' else scale[::-1].copy()
            value = data[data[f] != 0][f].dropna().sort_values(ascending=False)

            v = value.tolist()
            limit = [v[int(len(value) / 7) * i] for i in range(len(re_scale))] + [v[-1]]
            _color = pandas.cut(value, bins=limit[::-1], labels=re_scale, right=True)
            _color.name = f"{f}-C"
            colored = colored.join(_color.astype(str), how='left').fillna(re_scale[0 if f == 'DIV' else -1])
            colored = colored.replace('nan', re_scale[0 if f == 'DIV' else -1])
        colored = colored.fillna(scale[3])
        for col in colored:
            colored.at[colored.index[-1], col] = "#C8C8C8"
        return data.join(colored, how='left')

    @staticmethod
    def _cap_reform(x:int):
        mod, res = int(x // 10000), int(x % 10000)
        if mod:
            return f"{mod}조 {res}억"
        return f"{res}억"