from pandas import DataFrame
import pandas

# PARAM
MAP_KEYS = ['D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1', 'PER', 'PBR', 'DIV']
COLOR_SCALE = ['#F63538', '#BF4045', '#8B444E', '#414554', '#35764E', '#2F9E4F', '#30CC5A']  # Low <---> High
COLOR_BOUND = {
    'Y-1': ([-30, -20, -10, 0, 10, 20, 30], [-25, -15, -5, 5, 15, 25]),
    'M-6': ([-24, -16, -8, 0, 8, 16, 24], [-20, -12, -4, 4, 12, 20]),
    'M-3': ([-18, -12, -6, 0, 6, 12, 18], [-15, -9, 3, 3, 9, 15]),
    'M-1': ([-10, -6.7, -3.3, 0, 3.3, 6.7, 10], [-8.35, -5, -1.65, 1.65, 5, 8.35]),
    'W-1': ([-6, -4, -2, 0, 2, 4, 6], [-5, -3, -1, 1, 3, 5]),
    'D-1': ([-3, -2, -1, 0, 1, 2, 3], [-2.5, -1.5, -0.1, 0.1, 1.5, 2.5])
}

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
    for col, (na, bins) in COLOR_BOUND.items():
        color = data[col].apply(
            lambda rt:
            COLOR_SCALE[3] if str(rt) == 'nan' else \
            COLOR_SCALE[0] if rt <= bins[0] else \
            COLOR_SCALE[1] if bins[0] < rt <= bins[1] else \
            COLOR_SCALE[2] if bins[1] < rt <= bins[2] else \
            COLOR_SCALE[3] if bins[2] < rt <= bins[3] else \
            COLOR_SCALE[4] if bins[3] < rt <= bins[4] else \
            COLOR_SCALE[5] if bins[4] < rt <= bins[5] else \
            COLOR_SCALE[6]
        )
        color.name = f'{col}-C'
        colored = colored.join(color.astype(str), how='left')

    for f in ['PBR', 'PER', 'DIV']:
        re_scale = COLOR_SCALE if f == 'DIV' else COLOR_SCALE[::-1].copy()
        value = data[data[f] != 0][f].dropna().sort_values(ascending=False)

        v = value.tolist()
        limit = [v[int(len(value) / 7) * i] for i in range(len(re_scale))] + [v[-1]]
        _color = pandas.cut(value, bins=limit[::-1], labels=re_scale, right=True)
        _color.name = f"{f}-C"
        colored = colored.join(_color.astype(str), how='left').fillna(re_scale[0 if f == 'DIV' else -1])
        colored = colored.replace('nan', re_scale[0 if f == 'DIV' else -1])
    colored = colored.fillna(COLOR_SCALE[3])
    for col in colored:
        colored.at[colored.index[-1], col] = "#C8C8C8"
    return data.join(colored, how='left')


class baseDataFrame(DataFrame):

    
    def __init__(self, stocks:DataFrame):
        _map_name = stocks.iloc[0]['indexName']
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
        stocks['marketCap'] = stocks['size'].apply(num2cap)
        stocks['meta'] = stocks['name'] + "(" + stocks['ticker'] + ")" \
                        + "<br>시총: " + stocks['marketCap'] + '원'\
                        + "<br>종가: " + stocks['close']
        stocks['kind'] = 'stock'
        objs = [stocks]

        industry = grouping(*stocks.groupby(by=['industryName']))
        industry['kind'] = 'industry'
        if _map_name == 'WI26':
            industry['cover'] = _cap_type
        objs.append(industry)

        if _map_name == 'WICS':
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

