try:
    from ..market.fetch.date import TradingDate
    from color import SCALE, paint
except ImportError:
    from __py__.market.fetch.date import TradingDate
    from __py__.treemap.color import SCALE, paint
from pandas import DataFrame
import pandas


# PARAM
MAP_KEYS = ['D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1', 'PER', 'PBR', 'DIV']


# FUNCTIONS
def num2cap(x:int) -> str:
    mod, res = int(x // 10000), int(x % 10000)
    if mod:
        return f"{mod}조 {res}억"
    return f"{res}억"

def grouping(*args):
    objs = []
    for (name, ), group in args:
        name = name.replace("WICS ", "").replace("WI26 ", "")
        size = group['size'].sum()
        obj = {
            'name': name,
            'size': size,
            'cover': group.iloc[0]['sectorName'],
            'meta': f"{name}<br>시총: {num2cap(size)}원",
            'DIV': 0 if group['DIV'].empty else group['DIV'].mean()
        }
        for key in MAP_KEYS:
            obj[key] = round(
                (group[key] * group['size'] / group['size'].sum()).sum(), 2
            )
        objs.append(obj)
    return DataFrame(objs)

def coloring(data:DataFrame):
    colored = DataFrame(index=data.index)
    for col in MAP_KEYS:
        if col in ['PER', 'PBR']:
            continue
        color = data[col].apply(paint, args=(col,))
        color.name = f'{col}-C'
        colored = colored.join(color.astype(str), how='left')

    for f in ['PBR', 'PER']:
        scale = SCALE[::-1].copy()
        value = data[data[f] != 0][f].dropna().sort_values(ascending=False)

        v = value.tolist()
        limit = [v[int(len(value) / 7) * i] for i in range(len(scale))] + [v[-1]]
        _color = pandas.cut(value, bins=limit[::-1], labels=scale, right=True)
        _color.name = f"{f}-C"
        colored = colored.join(_color.astype(str), how='left').fillna(scale[-1])
        colored = colored.replace('nan', scale[-1])
    colored = colored.fillna(SCALE[3])
    for col in colored:
        colored.at[colored.index[-1], col] = "#C8C8C8"
    return data.join(colored, how='left')


# CLASS: BASE DATAFRAME
class baseDataFrame(DataFrame):

    def __init__(self, stocks:DataFrame):
        _date = f"{TradingDate.near.strftime('%Y-%m-%d')} 기준"
        # _map_name = stocks.iloc[0]['indexName']
        _cap_type = f"대형주({_date})"
        if not "005930" in stocks.index:
            _cap_type = f"중형주({_date})"

        stocks = stocks.copy()
        stocks.index.name = 'ticker'
        stocks.reset_index(inplace=True)
        stocks['cover'] = stocks['industryName'] \
                          .str.replace("WICS ", "") \
                          .str.replace("WI26 ", "")
        stocks['size'] = (stocks['marketCap'] / 100000000).astype(int)
        stocks['close'] = stocks['close'].astype(int).apply(lambda x: f"{x:,d}")
        stocks['marketCap'] = stocks['size'].apply(num2cap)
        stocks['meta'] = stocks['name'] + "(" + stocks['ticker'] + ")" \
                        + "<br>시총: " + stocks['marketCap'] + '원'\
                        + "<br>종가: " + stocks['close']
        stocks['kind'] = 'stock'
        objs = [stocks]

        industry = grouping(*stocks.groupby(by=['industryName']))
        industry['kind'] = 'industry'
        # if _map_name == 'WI26':
        #     industry['cover'] = _cap_type
        objs.append(industry)

        # if _map_name == 'WICS':
        sector = grouping(*stocks.groupby(by=['sectorName']))
        sector['cover'] = _cap_type
        sector['kind'] = 'sector'
        objs.append(sector)

        data = {
            'name': _cap_type,
            'cover': '',
            'size': stocks['size'].sum(),
        }
        for key in MAP_KEYS:
            data[key] = round(stocks[key].mean(), 2)
        header = DataFrame(data=data, index=[0])
        objs.append(header)

        data = pandas.concat(objs=objs, axis=0, ignore_index=True)
        data = data.drop_duplicates(subset='name', keep='last')
        data = coloring(data)
        data = data[[
            'name', 'cover', 'size', 'meta', 'kind',
            'PER', 'PBR', 'DIV', 'PER-C', 'PBR-C', 'DIV-C',
            'D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1',
            'Y-1-C', 'M-6-C', 'M-3-C', 'M-1-C', 'W-1-C', 'D-1-C'
        ]]
        data[MAP_KEYS] = round(data[MAP_KEYS], 2)
        super().__init__(data)
        return

