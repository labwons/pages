try:
    from ..resource.baseleine import Tools
    from ..resource.metadata import METADATA, MARKETMAP
except ImportError:
    from src.build.resource.baseline import Tools
    from src.build.resource.metadata import METADATA, MARKETMAP
from datetime import datetime
from pandas import concat, DataFrame
from pandas.errors import IntCastingNaNError
from pykrx.stock import get_index_portfolio_deposit_file
from time import time
from typing import Any, Dict, List



HEX2RGB = lambda x: (int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16))
CONNECT = lambda x, x1, y1, x2, y2: ( (y2 - y1) / (x2 - x1) ) * (x - x1) + y1


# KEYS = {
#     'D-1': {
#         'na': '(미제공)',
#         'valueScale': [-3, -2, -1, 0, 1, 2, 3],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'W-1': {
#         'na': '(미제공)',
#         'valueScale': [-6, -4, -2, 0, 2, 4, 6],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'M-1': {
#         'na': '(미제공)',
#         'valueScale': [-10, -6.7, -3.3, 0, 3.3, 6.7, 10],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'M-3': {
#         'na': '(미제공)',
#         'valueScale': [-18, -12, -6, 0, 6, 12, 18],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'M-6': {
#         'na': '(미제공)',
#         'valueScale': [-24, -16, -8, 0, 8, 16, 24],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'Y-1': {
#         'na': '(미제공)',
#         'valueScale': [-30, -20, -10, 0, 10, 20, 30],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'pct52wHigh': {
#         'na': '(미제공)',
#         'valueScale': [-30, -20, -10, 0, None, None, None],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 0,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'pct52wLow': {
#         'na': '(미제공)',
#         'valueScale': [None, None, None, 0, 10, 20, 30],
#         'colorScale': BLUE2RED,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'dividendYield': {
#         'na': '(미제공)',
#         'valueScale': [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 0,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'fiscalDividendYield': {
#         'na': '(미제공)',
#         'valueScale': [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 0,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'foreignRate': {
#         'na': '(미제공)',
#         'valueScale': [None, None, None, 0, 20, 40, 60],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'trailingProfitRate': {
#         'na': '(미제공)',
#         'valueScale': [-15, -10, -5, 0, 5, 10, 15],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'trailingPE': {
#         'na': '(적자 | 미제공)',
#         'valueScale': None,
#         'colorScale': RED2GREEN[::-1],
#         'defaultColorIndex': 6,
#         'iconMax': 'bi-emoji-frown-fill',
#         'iconMin': 'bi-emoji-smile-fill',
#     },
#     'trailingPS': {
#         'na': '(미제공)',
#         'valueScale': None,
#         'colorScale': RED2GREEN[::-1],
#         'defaultColorIndex': 6,
#         'iconMax': 'bi-emoji-frown-fill',
#         'iconMin': 'bi-emoji-smile-fill',
#     },
#     'estimatedPE': {
#         'na': '(적자 | 미제공)',
#         'valueScale': None,
#         'colorScale': RED2GREEN[::-1],
#         'defaultColorIndex': 6,
#         'iconMax': 'bi-hand-thumbs-down-fill',
#         'iconMin': 'bi-hand-thumbs-up-fill',
#     },
#     'PBR': {
#         'na': '(미제공)',
#         'valueScale': None,
#         'colorScale': RED2GREEN[::-1],
#         'defaultColorIndex': 6,
#         'iconMax': 'bi-emoji-frown-fill',
#         'iconMin': 'bi-emoji-smile-fill',
#     },
#     'fiscalDebtRatio' : {
#         'na': '(미제공)',
#         'valueScale':  [30, 60, 90, 120, 150, 180, 210],
#         'colorScale': RED2GREEN[::-1],
#         'defaultColorIndex': 6,
#         'iconMax': 'bi-emoji-frown-fill',
#         'iconMin': 'bi-emoji-smile-fill',
#     },
#     'beta': {
#         'na': '(미제공)',
#         'valueScale': [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-graph-up-arrow',
#         'iconMin': 'bi-graph-down-arrow',
#     },
#     'turnoverRatio': {
#         'na': '(미제공)',
#         'valueScale': [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-arrow-left-right',
#         'iconMin': 'bi-three-dots',
#     },
#     'averageRevenueGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 5, 10, 15, 20, 25, 30],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'averageProfitGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 5, 10, 15, 20, 25, 30],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'averageEpsGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 10, 20, 30, 40, 50, 60],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'RevenueGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 5, 10, 15, 20, 25, 30],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'ProfitGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 5, 10, 15, 20, 25, 30],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     },
#     'EpsGrowth_A': {
#         'na': '(미제공)',
#         'valueScale': [0, 10, 20, 30, 40, 50, 60],
#         'colorScale': RED2GREEN,
#         'defaultColorIndex': 3,
#         'iconMax': 'bi-emoji-smile-fill',
#         'iconMin': 'bi-emoji-frown-fill',
#     }
# }


class MarketMap:

    _log: List[str] = []
    # meta: Dict[str, Dict[str, Any]] = KEYS.copy()
    def __init__(self, baseline:DataFrame):
        stime = time()
        self.log = f'BUILD [MARKET MAP]'

        resource = baseline.copy()

        # DEFINE TARGET TICKERS:
        # IF NETWORK IS NORMAL, TARGET TICKERS WILL BE KOSPI200, KOSDAQ150 TICKERS.
        # IF NETWORK FAILS, TOP 350 TICKERS WILL BE SELECTED.
        tickers = self.largeCaps()

        # TYPE CASTING BEFORE FACTORIZE MAP DATA.
        baseline = baseline.copy()
        baseline = baseline[baseline.index.isin(tickers)] if tickers else baseline.head(350)
        for col, meta in METADATA:
            if col == "RENAME":
                continue
            if meta.dtype != str and meta.dtype != datetime:
                try:
                    baseline[col] = baseline[col].astype(meta.dtype)
                except (IntCastingNaNError, ValueError):
                    baseline[col] = baseline[col].astype(float)

        # SIZING, NAMING, HOVER INFORMATION FACTORIZE
        baseline['size'] = (baseline['marketCap'] / 1e+8).astype(int)
        baseline['name'] = baseline[['name', 'market']].apply(lambda r: f'{r["name"]}*' if r.market == 'KOSDAQ' else r['name'], axis=1)
        baseline['ceiling'] = baseline['industryName']
        baseline['meta'] = baseline.name + '(' + baseline.index + ')<br>' \
                     + '시가총액: ' + baseline['size'].apply(Tools.krw2currency) + '원<br>' \
                     + '종가: ' + baseline.close.apply(lambda x: f"{x:,d}원")

        # IF INDUSTRY == SECTOR, INDUSTRY INFORMATION WILL BE DROPPED.
        _duplicated = baseline[baseline.industryName == baseline.sectorName]["sectorName"] \
                       .drop_duplicates() \
                       .tolist()

        # INCLUDE SAMSUNG(005930) CASE
        ws_industry = self.grouping(baseline, "industryName")
        ws_industry.index = ws_industry.index.str.pad(width=6, side="left", fillchar='W')
        ws_industry = ws_industry[~ws_industry["name"].isin(_duplicated)]

        ws_sector = self.grouping(baseline, "sectorName")
        ws_sector["ceiling"] = "대형주"
        ws_sector.index = ws_sector.index.str.pad(width=6, side="left", fillchar='W')

        ws_top = DataFrame(baseline.select_dtypes(include=['int']).sum()).T
        ws_top[['name', 'meta']] = ['대형주', Tools.krw2currency(ws_top.iloc[0]['size'])]
        ws_top.index = ['WS0000']

        # EXCLUDE SAMSUNG(005930) CASE
        ns_industry = self.grouping(baseline, "industryName", "005930")
        ns_industry.index = ns_industry.index.str.pad(width=6, side="left", fillchar='N')
        ns_industry = ns_industry[~ns_industry["name"].isin(_duplicated)]

        ns_sector = self.grouping(baseline, "sectorName", "005930")
        ns_sector["ceiling"] = "대형주(삼성전자 제외)"
        ns_sector.index = ns_sector.index.str.pad(width=6, side="left", fillchar='N')

        ns_top = DataFrame(baseline[~baseline.index.isin(['005930'])].select_dtypes(include=['int']).sum()).T
        ns_top[['name', 'meta']] = ["대형주(삼성전자 제외)", Tools.krw2currency(ns_top.iloc[0]['size'])]
        ns_top.index = ['NS0000']

        base = concat([baseline, ws_industry, ns_industry, ws_sector, ns_sector, ws_top, ns_top])
        base = base[
            [key for key, meta in MARKETMAP if key != "COLORS"] + ['meta', 'ceiling', 'size', 'name']
        ]

        # FACTORIZE FOR DATA DISPLAY(HOVER, STATIC TEXT)
        # FINAL VALUE WILL BE CONCATENATED WITH NUMBER AND UNIT, IF THE NUMBER IS NOT PROVIDED,
        # PROPER REASON WILL BE GIVEN.
        refactor = base.copy()
        for key, meta in MARKETMAP:
            if key == "COLORS":
                continue
            meta.update(METADATA[key])
            if meta.dtype == int:
                refactor[key] = refactor[key].astype(int).astype(str) + meta.unit
            if meta.dtype == float:
                refactor[key] = round(refactor[key], meta.digit).astype(str) + meta.unit

        refactor.loc[refactor['pctFiftyTwoWeekHigh'] == '0.0%', 'pctFiftyTwoWeekHigh'] = '52주 최고가'
        refactor.loc[refactor['pctFiftyTwoWeekLow'] == '0.0%', 'pctFiftyTwoWeekLow'] = '52주 최저가'

        for key in refactor:
            if key in ["name", "size", "ceiling", "meta"]:
                continue
            refactor.loc[(refactor[key] == 'nan%') | (refactor[key] == 'nan'), key] = '미제공'
            refactor.loc[["WS0000", "NS0000"], key] = ""

        advance = ['estimatedProfitGrowthState', 'estimatedEpsGrowthState', 'trailingEps',
                   'yoyProfitState', 'yoyEpsState']
        refactor = refactor.join(resource[advance])
        refactor['estimatedProfitGrowth'] = refactor['estimatedProfitGrowthState'].combine_first(refactor['estimatedProfitGrowth'])
        refactor['estimatedEpsGrowth'] = refactor['estimatedEpsGrowthState'].combine_first(refactor['estimatedEpsGrowth'])
        refactor['trailingPE'] = refactor[['trailingPE', 'trailingEps']].apply(lambda r: '적자' if r.trailingEps <= 0 else r.trailingPE , axis=1)
        refactor['yoyProfit'] = refactor['yoyProfitState'].combine_first(refactor['yoyProfit'])
        refactor['yoyEps'] = refactor['yoyEpsState'].combine_first(refactor['yoyEps'])
        refactor = refactor.drop(columns=advance)
        self.data = refactor.join(self.paint(base))
        # self.data.to_clipboard()

        meta = {}
        for key, _meta in MARKETMAP:
            if key == "COLORS":
                continue
            meta[key] = {
                'label': METADATA[key].label,
                'unit': METADATA[key].unit,
                'scale': _meta.scale,
                'color': _meta.color,
            }
        self.meta = meta

        self.stat = self.minmax(base)

        self.log = f'BUILD [MARKET MAP] FINISHED'
        self.log = f'- {len(self.data)} Items / Elapsed: {time() - stime:.2f}s'
        return

    @classmethod
    def largeCaps(cls) -> list:
        try:
            return get_index_portfolio_deposit_file('2203') + get_index_portfolio_deposit_file('1028')
        except Exception as reason:
            cls._log.append(f"- skipped fetching krx350: {reason}")
            return []

    @classmethod
    def grouping(cls, frm:DataFrame, key:str, *exclude:str) -> DataFrame:
        objs = []
        for name, group in frm.groupby(by=key):
            if exclude:
                group = group[~group.index.isin(exclude)]
            '''
            Default Grouping Factors: 
            Weighted Mean
            '''
            size = group['size'].sum()
            w = group['size'] / size
            obj = {col: (w * group[col]).sum() for col in group if group[col].dtype in [float, int]}
            obj.update({
                "ticker": group.iloc[0][key.replace("Name", "Code")],
                "name": name,
                "size": size,
                "ceiling": 'TBD' if key.startswith('sector') else group.iloc[0]['sectorName'],
                'meta': f'{name}<br>시가총액: {Tools.krw2currency(size)}원'
            })
            '''
            Exception Grouping Factors:
            Arithmetic Mean
            '''
            # Not Defined Yet

            objs.append(obj)
        return DataFrame(data=objs).set_index(keys='ticker')

    @classmethod
    def paint(cls, frm:DataFrame):
        rgb2hex = lambda r, g, b: f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'
        connect = lambda x, x1, y1, x2, y2: ((y2 - y1) / (x2 - x1)) * (x - x1) + y1
        def _paint_(_value, _scale, _color, _index):
            if _value <= _scale[0]:
                return rgb2hex(*_color[0])
            if _value >= _scale[-1]:
                return rgb2hex(*_color[-1])

            n = 0
            while n < len(_scale) - 1:
                if _scale[n] < _value <= _scale[n + 1]:
                    break
                n += 1

            if n == len(_scale) - 1:
                return _color[_index]

            r1, g1, b1 = _color[n]
            r2, g2, b2 = _color[n + 1]
            return rgb2hex(
                connect(_value, _scale[n], r1, _scale[n + 1], r2),
                connect(_value, _scale[n], g1, _scale[n + 1], g2),
                connect(_value, _scale[n], b1, _scale[n + 1], b2)
            )

        objs = {}
        for key, meta in MARKETMAP:
            if key == "COLORS":
                continue
            scale = meta.scale
            color = MARKETMAP.COLORS[meta.color]
            index = meta.index
            objs[f'{key}Color'] = frm[key].apply(_paint_, _scale=scale, _color=color, _index=index)
        colors = concat(objs, axis=1)
        colors.iloc[-2:] = "#C8C8C8"
        return colors

    @classmethod
    def minmax(cls, frm:DataFrame):
        objs = {}
        cols = ["min", "max", "minT", "maxT", "minC", "maxC", "minI", "maxI", "label"]
        rgb2hex = lambda r, g, b: f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'
        for key, meta in MARKETMAP:
            if key == 'COLORS':
                continue
            data = frm[key]
            _min = frm[frm[key] == data.min()]
            _max = frm[frm[key] == data.max()]
            minv = METADATA[key].dtype(data.min())
            maxv = METADATA[key].dtype(data.max())
            if METADATA[key].dtype == float:
                minv = round(minv, METADATA[key].digit)
                maxv = round(maxv, METADATA[key].digit)
            objs[key] = [
                f'{"-" if len(_min) > 1 else minv}{METADATA[key].unit}',
                f'{"-" if len(_min) > 1 else maxv}{METADATA[key].unit}',
                "(복수 종목)" if len(_min) > 1 else _min.iloc[0]['name'],
                "(복수 종목)" if len(_max) > 1 else _max.iloc[0]['name'],
                rgb2hex(*MARKETMAP.COLORS[meta.color][0]),
                rgb2hex(*MARKETMAP.COLORS[meta.color][-1]),
                meta.iconMax,
                meta.iconMin,
                METADATA[key].label
            ]
        return DataFrame(data=objs, index=cols)

    # @property
    # def desc(self) -> DataFrame:
    #     tg = self[self.index.str.isdigit()]
    #     desc = tg.describe()
    #     mn = {col: ",".join(tg[tg[col] == tg[col].min()].index) for col in desc}
    #     mx = {col: ",".join(tg[tg[col] == tg[col].max()].index) for col in desc}
    #     desc = concat([desc, DataFrame([mn, mx], index=["minT", "maxT"])])
    #     return desc
    #
    # @property
    # def peakPoint(self) -> DataFrame:
    #     desc = self.desc.copy()
    #     peak = desc.loc[["min", "max", "minT", "maxT"]]
    #     drop = ['size']
    #     for col in peak:
    #         if ','in peak.loc['minT', col] or ',' in peak.loc['maxT', col]:
    #             drop.append(col)
    #         if col in drop:
    #             continue
    #         else:
    #             peak.loc['min', col] = f"{peak.loc['min', col]:,.1f} {self.meta[col]['unit']}"
    #             peak.loc['max', col] = f"{peak.loc['max', col]:,.1f} {self.meta[col]['unit']}"
    #         peak.loc['minT', col] = self.loc[peak.loc['minT', col], 'name']
    #         peak.loc['maxT', col] = self.loc[peak.loc['maxT', col], 'name']
    #         peak.loc['minC', col] = self.meta[col]['colorScale'][0]
    #         peak.loc['maxC', col] = self.meta[col]['colorScale'][-1]
    #         peak.loc['minI', col] = self.meta[col]['iconMin']
    #         peak.loc['maxI', col] = self.meta[col]['iconMax']
    #         peak.loc['label', col] = self.meta[col]['label']
    #
    #     peak = peak.drop(columns=drop)
    #     for key in self.meta:
    #         for _destroy in ['iconMax', 'iconMin']:
    #             del self.meta[key][_destroy]
    #     return peak

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)




if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    from src.common.env import FILE
    from pandas import read_parquet

    baseline = read_parquet(FILE.BASELINE, engine='pyarrow')

    marketMap = MarketMap(baseline)
    print(marketMap.log)
    print(marketMap.data.columns)
    print(marketMap.stat)
    # print(marketMap)
    # print(marketMap.desc)
    # print(marketMap.peakPoint)
    # print(marketMap.log)
    # print(marketMap.meta)
    # print(marketMap.gaussian)
    # print(marketMap.colors)
    # print(marketMap.to_dict(orient='index'))
