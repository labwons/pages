try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH
from pandas import (
    concat,
    DataFrame,
)
from scipy.stats import norm
from time import time
from typing import Any, Dict, List
import os


HEX2RGB = lambda x: (int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16))
CONNECT = lambda x, x1, y1, x2, y2: ( (y2 - y1) / (x2 - x1) ) * (x - x1) + y1

BLUE2RED = [
    '#1861A8', # R24 G97 B168
    '#228BE6', # R34 G139 B230
    '#74C0FC', # R116 G192 B252
    '#A6A6A6', # R168 G168 B168
    '#FF8787', # R255 G135 B135
    '#F03E3E', # R240 G62 B62
    '#C92A2A'  # R201 G42 B42
]
RED2GREEN = [
    '#F63538', # R246 G53 B56
    '#BF4045', # R191 G64 B69
    '#8B444E', # R139 G68 B78
    '#414554', # R65 G69 B84
    '#35764E', # R53 G118 B78
    '#2F9E4F', # R47 G158 B79
    '#30CC5A'  # R48 G204 B90
]
KEYS = {
    'D-1': {
        'na': '(미제공)',
        'valueScale': [-3, -2, -1, 0, 1, 2, 3],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'W-1': {
        'na': '(미제공)',
        'valueScale': [-6, -4, -2, 0, 2, 4, 6],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'M-1': {
        'na': '(미제공)',
        'valueScale': [-10, -6.7, -3.3, 0, 3.3, 6.7, 10],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'M-3': {
        'na': '(미제공)',
        'valueScale': [-18, -12, -6, 0, 6, 12, 18],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'M-6': {
        'na': '(미제공)',
        'valueScale': [-24, -16, -8, 0, 8, 16, 24],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'Y-1': {
        'na': '(미제공)',
        'valueScale': [-30, -20, -10, 0, 10, 20, 30],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'pct52wHigh': {
        'na': '(미제공)',
        'valueScale': [-30, -20, -10, 0, None, None, None],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 0,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'pct52wLow': {
        'na': '(미제공)',
        'valueScale': [None, None, None, 0, 10, 20, 30],
        'colorScale': BLUE2RED,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'dividendYield': {
        'na': '(미제공)',
        'valueScale': [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 0,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'fiscalDividendYield': {
        'na': '(미제공)',
        'valueScale': [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 0,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'foreignRate': {
        'na': '(미제공)',
        'valueScale': [None, None, None, 0, 20, 40, 60],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'trailingProfitRate': {
        'na': '(미제공)',
        'valueScale': [-15, -10, -5, 0, 5, 10, 15],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'trailingPE': {
        'na': '(적자 | 미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN[::-1],
        'defaultColorIndex': 6,
        'iconMax': 'bi-emoji-frown-fill',
        'iconMin': 'bi-emoji-smile-fill',
    },
    'trailingPS': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN[::-1],
        'defaultColorIndex': 6,
        'iconMax': 'bi-emoji-frown-fill',
        'iconMin': 'bi-emoji-smile-fill',
    },
    'estimatedPE': {
        'na': '(적자 | 미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN[::-1],
        'defaultColorIndex': 6,
        'iconMax': 'bi-hand-thumbs-down-fill',
        'iconMin': 'bi-hand-thumbs-up-fill',
    },
    'PBR': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN[::-1],
        'defaultColorIndex': 6,
        'iconMax': 'bi-emoji-frown-fill',
        'iconMin': 'bi-emoji-smile-fill',
    },
    'fiscalDebtRatio' : {
        'na': '(미제공)',
        'valueScale':  [30, 60, 90, 120, 150, 180, 210],
        'colorScale': RED2GREEN[::-1],
        'defaultColorIndex': 6,
        'iconMax': 'bi-emoji-frown-fill',
        'iconMin': 'bi-emoji-smile-fill',
    },
    'beta': {
        'na': '(미제공)',
        'valueScale': [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-graph-up-arrow',
        'iconMin': 'bi-graph-down-arrow',
    },
    'turnoverRatio': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-arrow-left-right',
        'iconMin': 'bi-three-dots',
    },
    'averageRevenueGrowth_A': {
        'na': '(미제공)',
        'valueScale': [0, 3, 6, 9, 12, 15, 18],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'averageProfitGrowth_A': {
        'na': '(미제공)',
        'valueScale': [-10, -5, 0, 5, 10, 15, 20],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'averageEpsGrowth_A': {
        'na': '(미제공)',
        'valueScale': [-10, -5, 0, 5, 10, 15, 20],
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'RevenueGrowth_A': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'ProfitGrowth_A': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    },
    'EpsGrowth_A': {
        'na': '(미제공)',
        'valueScale': None,
        'colorScale': RED2GREEN,
        'defaultColorIndex': 3,
        'iconMax': 'bi-emoji-smile-fill',
        'iconMin': 'bi-emoji-frown-fill',
    }
}

FAQ = [
    {'q': '실시간 업데이트는 안 되나요?', 'a': '실시간 업데이트는 제공되지 않습니다.<i class="bi bi-emoji-frown-fill"></i> 마지막 거래일 기준 데이터로 구성하였습니다.'},
    {'q': '제가 찾는 종목이 없어요.', 'a': '가독성을 위해 코스피200 지수와 코스닥150 지수 종목으로 구성하였으며 이외 종목은 제외됩니다.'},
    {'q': '언제 업데이트 되나요?', 'a': '정규장 시간 마감(15:30) 이후 15분~30분 내로 업데이트 됩니다. 휴장일에는 마지막 개장일 데이터가 유지됩니다.'},
    {'q': '자료 출처가 어디인가요?',
     'a': '섹터/업종 분류는 GICS 산업 분류 및 WISE INDEX를 참고하여 재구성하였습니다. 수익률은 한국거래소(KRX) 데이터를 참고하였으며 기타 지표는 네이버 및 에프앤가이드를 참고하였습니다.'},
    {'q': 'NXT 거래소 정보는 반영 안 되나요?',
     'a': 'NXT 거래소의 가격 정보는 반영되지 않으며 한국거래소(KRX) 기준 가격만 반영됩니다.'},
    {'q': '정보 수정이 필요해요.',
     'a': '고장 신고, 정보 정정 및 기타 문의는 snob.labwons@gmail.com 으로 연락주세요!<i class="bi bi-emoji-smile-fill"></i>'},
]


class MarketMap(DataFrame):

    _log: List[str] = []
    meta: Dict[str, Dict[str, Any]] = KEYS.copy()
    faqs: List[Dict] = FAQ
    def __init__(self, baseline:DataFrame):
        stime = time()
        self.log = f'RUN [Build Market Map]'

        super().__init__(baseline[baseline["stockSize"] == "large"])
        self.drop(columns=["date"], inplace=True)
        self['size'] = (self['marketCap'] / 1e+8).astype(int)
        self['ceiling'] = self['industryName']
        self['meta'] = self['name'] + '(' + self.index + ')<br>' \
                     + '시가총액: ' + self['size'].apply(self._format_cap) + '원<br>' \
                     + '종가: ' + self['close'].apply(lambda x: f"{x:,d}원")
        prior_sector = self[self["industryName"] == self["sectorName"]]["sectorName"] \
                       .drop_duplicates() \
                       .tolist()


        ws_industry = self._grouping("industryName")
        ws_industry.index = ws_industry.index.str.pad(width=6, side="left", fillchar='W')
        ws_industry = ws_industry[~ws_industry["name"].isin(prior_sector)]
        ws_sector = self._grouping("sectorName")
        ws_sector["ceiling"] = "대형주"
        ws_sector.index = ws_sector.index.str.pad(width=6, side="left", fillchar='W')
        ws_top = DataFrame(self.select_dtypes(include=['int']).sum()).T
        ws_top[['name', 'meta']] = ['대형주', self._format_cap(ws_top.iloc[0]['size'])]
        ws_top.index = ['WS0000']

        ns_industry = self._grouping("industryName", "005930")
        ns_industry.index = ns_industry.index.str.pad(width=6, side="left", fillchar='N')
        ns_industry = ns_industry[~ns_industry["name"].isin(prior_sector)]
        ns_sector = self._grouping("sectorName", "005930")
        ns_sector["ceiling"] = "대형주(삼성전자 제외)"
        ns_sector.index = ns_sector.index.str.pad(width=6, side="left", fillchar='N')
        ns_top = DataFrame(self[~self.index.isin(['005930'])].select_dtypes(include=['int']).sum()).T
        ns_top[['name', 'meta']] = ["대형주(삼성전자 제외)", self._format_cap(ns_top.iloc[0]['size'])]
        ns_top.index = ['NS0000']

        super().__init__(concat([self, ws_industry, ns_industry, ws_sector, ns_sector, ws_top, ns_top]))
        self.drop(inplace=True, columns=[
            "close", 'floatShares',
            'trailingRevenue', 'trailingEps', 'pctEstimated',
            'RevenueGrowth_Q', 'ProfitGrowth_Q', 'EpsGrowth_Q',
            "industryCode", "industryName", "sectorCode", "sectorName", "stockSize", 'volume'
        ])

        self._check_metadata(baseline.meta)
        self._chunk()
        self._round_up()

        self.log = f'END [Build Market Map] {len(self)} Items / Elapsed: {time() - stime:.2f}s'
        return

    def _check_metadata(self, baseline_meta:Dict[str, Dict[str, Any]]):
        for key in self.meta:
            if not key in self:
                raise KeyError(f'MAP metadata: {key} is not in MAP data')
        for col in self.select_dtypes(include=['number']).columns:
            if col in ['size', 'amount', 'marketCap', 'volume', 'shares']: continue
            if not col in baseline_meta:
                raise ValueError(f'MAP data key : "{col}" is not found in Baseline metadata')
            if not col in self.meta:
                raise KeyError(f'column: {col} is not predefined in MAP metadata')
            self.meta[col].update(baseline_meta[col])
        return

    def _chunk(self):
        for key, meta in self.meta.items():
            if meta['valueScale']:
                continue

            mean, std, mn, mx = self[key].mean(), self[key].std(), self[key].min(), self[key].max()
            if key in ['volume', 'PBR']:
                self.meta[key]['valueScale'] = [None, None, None, 0, mean / 2, mean, mean + std]
            elif key in ['estimatedPE', 'trailingPE', 'trailingPS']:
                dv = (min(mx, mean + 2 * std) - mean) / 4
                self.meta[key]['valueScale'] = [0.25 * mean, 0.5 * mean, 0.75 * mean, mean, dv, 2 * dv, 3 * dv]
            elif key == 'turnoverRatio':
                ks, kq = self[self['market'] == 'kospi'], self[self['market'] == 'kosdaq']
                ks = 100 * ks['amount'].sum() / ks['marketCap'].sum()
                kq = 100 * kq['amount'].sum() / kq['marketCap'].sum()
                dvn = mean - ks
                dvp = kq - mean
                self.meta[key]['valueScale'] = [ks, ks + 0.33 * dvn, ks + 0.66 * dvn, mean, mean + 0.33 * dvp, mean + 0.66 * dvp, kq]
                self.drop(inplace=True, columns=['amount', 'market', 'marketCap'])
            else:
                en, ep = max(mn, mean - 2 * std), min(mx, mean + 2 * std)
                dvn, dvp = mean - en, ep - mean
                self.meta[key]['valueScale'] = [
                    en + 0.25*dvn, en + 0.5*dvn, en + 0.75*dvn, mean,
                    mean + 0.25*dvp, mean + 0.5*dvp, mean + 0.75*dvp
                ]
            self.meta[key]['valueScale'] = [round(v, 2) for v in self.meta[key]['valueScale'] if v]
        return

    def _grouping(self, key:str, *exclude:str) -> DataFrame:
        objs = []
        for value, group in self.groupby(by=key):
            if exclude:
                group = group[~group.index.isin(exclude)]
            '''
            Default Grouping Factors: 
            Weighted Mean
            '''
            size = group['size'].sum()
            w = group['size'] / size
            obj = {col: (w * group[col]).sum() for col in group if group[col].dtype == float}
            obj.update({
                "ticker": group.iloc[0][key.replace("Name", "Code")],
                "name": value,
                "size": size,
                "volume": group['volume'].sum(),
                "amount": group['amount'].sum(),
                "ceiling": 'TBD' if key.startswith('sector') else group.iloc[0]['sectorName'],
                'meta': f'{value}<br>시가총액: ' + self._format_cap(size) + '원'
            })
            '''
            Exception Grouping Factors:
            Arithmetic Mean
            '''
            # Not Defined Yet

            '''
            Exception Grouping Factors:
            Customize
            '''
            obj['turnoverRatio'] = 100 * obj['amount'] / (obj['size'] * 1e+8)
            objs.append(obj)
        return DataFrame(data=objs).set_index(keys='ticker')

    def _round_up(self):
        for col in self:
            if col in self.meta and (not self.meta[col]['round'] == -1):
                self[col] = round(self[col], self.meta[col]['round'])
            # if col in self.meta:
            #     self[col] = self[col].astype(str).fillna(self.meta[col]['na'])
        return

    @property
    def colors(self) -> DataFrame:
        objs = {}
        for key, meta in self.meta.items():
            scale = [v if v else 0 for v in meta['valueScale']]
            rgb = [HEX2RGB(s) for s in meta['colorScale']]
            default = meta['colorScale'][meta['defaultColorIndex']]
            def _paint(value) -> str:
                if value == '':
                    return default
                value = float(value)
                if value <= scale[0]:
                    return meta['colorScale'][0]
                if value > scale[-1]:
                    return meta['colorScale'][-1]
                n = 0
                while n < len(meta['colorScale']) - 1:
                    if scale[n] < value <= scale[n + 1]:
                        break
                    n += 1
                r1, g1, b1 = rgb[n]
                r2, g2, b2 = rgb[n + 1]
                r = CONNECT(value, scale[n], r1, scale[n + 1], r2)
                g = CONNECT(value, scale[n], g1, scale[n + 1], g2)
                b = CONNECT(value, scale[n], b1, scale[n + 1], b2)
                return f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'.upper()
            objs[key] = self[key].fillna('').apply(_paint)
        colors = concat(objs, axis=1)
        colors.iloc[-2:] = "#C8C8C8"
        for key in self.meta:
            for _destroy in ['defaultColorIndex']:
                del self.meta[key][_destroy]
        return colors

    @property
    def desc(self) -> DataFrame:
        tg = self[self.index.str.isdigit()]
        desc = tg.describe()
        mn = {col: ",".join(tg[tg[col] == tg[col].min()].index) for col in desc}
        mx = {col: ",".join(tg[tg[col] == tg[col].max()].index) for col in desc}
        desc = concat([desc, DataFrame([mn, mx], index=["minT", "maxT"])])
        return desc

    @property
    def peakPoint(self) -> DataFrame:
        desc = self.desc.copy()
        peak = desc.loc[["min", "max", "minT", "maxT"]]
        drop = ['size']
        for col in peak:
            if ','in peak.loc['minT', col] or ',' in peak.loc['maxT', col]:
                drop.append(col)
            if col in drop:
                continue
            if col == "volume":
                if peak.loc['min', col] >= 10000:
                    peak.loc['min', col] = f"{peak.loc['min', col] // 10000:.0f}만 주"
                else:
                    peak.loc['min', col] = f"{peak.loc['min', col]:.0f} 주"
                if peak.loc['max', col] >= 10000:
                    peak.loc['max', col] = f"{peak.loc['max', col] // 10000:.0f}만 주"
                else:
                    peak.loc['max', col] = f"{peak.loc['max', col]:.0f} 주"
            else:
                peak.loc['min', col] = f"{peak.loc['min', col]:.1f} {self.meta[col]['unit']}"
                peak.loc['max', col] = f"{peak.loc['max', col]:.1f} {self.meta[col]['unit']}"
            peak.loc['minT', col] = self.loc[peak.loc['minT', col], 'name']
            peak.loc['maxT', col] = self.loc[peak.loc['maxT', col], 'name']
            peak.loc['minC', col] = self.meta[col]['colorScale'][0]
            peak.loc['maxC', col] = self.meta[col]['colorScale'][-1]
            peak.loc['minI', col] = self.meta[col]['iconMin']
            peak.loc['maxI', col] = self.meta[col]['iconMax']
            peak.loc['label', col] = self.meta[col]['label']

        peak = peak.drop(columns=drop)
        for key in self.meta:
            for _destroy in ['iconMax', 'iconMin']:
                del self.meta[key][_destroy]
        return peak

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @classmethod
    def _format_cap(cls, market_cap:int) -> str:
        zo, euk = int(market_cap // 10000), int(market_cap % 10000)
        return f'{zo}조 {euk}억' if zo else f'{euk}억'



if __name__ == "__main__":
    from src.build.service.baseline import MarketBaseline
    from pandas import set_option

    set_option('display.expand_frame_repr', False)
    baseline = MarketBaseline(update=False)
    # print(baseline)
    marketMap = MarketMap(baseline)
    # print(marketMap)
    # print(marketMap.desc)
    # print(marketMap.peakPoint)
    # print(marketMap.log)
    # print(marketMap.meta)
    # print(marketMap.gaussian)
    marketMap.show_gaussian()
    # print(marketMap.colors)
    # print(marketMap.to_dict(orient='index'))
