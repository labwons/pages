try:
    from ...fetch.macro.ecos import Ecos
    from ...fetch.macro.fred import Fred
    from ...fetch.macro.naver import krwusd
except ImportError:
    from src.fetch.macro.ecos import Ecos
    from src.fetch.macro.fred import Fred
    from src.fetch.macro.naver import krwusd
from datetime import datetime, timezone, timedelta
from pandas import concat, DataFrame, read_json
from pykrx.stock import get_index_ohlcv_by_date
from time import time
from typing import Dict, List
if "PATH" not in globals():
    try:
        from ...common.path import PATH
    except ImportError:
        from src.common.path import PATH

class Macro(DataFrame):
    meta: Dict = {'KOSPI': {'name': 'KOSPI', 'unit': '', 'group': '지수', 'hoverTemplate': ': %{y:.2f}<extra></extra>'},
                  'KOSDAQ': {'name': 'KOSDAQ', 'unit': '', 'group': '지수', 'hoverTemplate': ': %{y:.2f}<extra></extra>'}}
    _log: List[str] = []
    def __init__(self, update:bool=False):
        stime = time()
        self.log = f'RUN [Build Macro Cache]'

        self.meta.update(Ecos.metaData())
        for symbol, item in Fred.predef.items():
            self.meta[symbol] = {
                "name": item["name"],
                "unit": item["unit"],
                "group": item["category"],
                "hoverTemplate": item["hoverTemplate"]
            }

        basis = read_json(PATH.MACRO, orient='index')
        try:
            tz = timezone(timedelta(hours=9))
            ck = datetime.now(tz)
            ks = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '1001')['종가']
            kq = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '2001')['종가']
            ks.name = 'KOSPI'
            kq.name = 'KOSDAQ'
            index = concat([ks, kq], axis=1)
            basis = concat([index, basis.drop(columns=index.columns)], axis=1)
        except (KeyError, Exception):
            self.log = "  - KRX Not accessible: update failed"
            pass

        if not update:
            super().__init__(basis)
            self.log = f'END [Build Macro Cache]'
            return

        Ecos.api = "CEW3KQU603E6GA8VX0O9"
        ecos = Ecos()
        fred = Fred()

        super().__init__(concat(objs=[basis[['KOSPI', 'KOSDAQ']], ecos, fred], axis=1))
        self.log = f'END [Build Macro Cache] / Elapsed: {time() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @property
    def status(self) -> list:
        selector = {
            'KOSPI': {
                'icon': 'bi-graph-up',
                'digit': 2,
            },
            'KOSDAQ': {
                'icon': 'bi-graph-up',
                'digit': 2,
            },
            '731Y0030000003': {
                'icon': 'bi-currency-exchange',  # 원/달러 환율
                'digit': 1,
            },
            '817Y002010195000': {
                'icon': 'bi-percent',  # 국고채2년
                'digit': 3,
            },
            '817Y002010210000': {
                'icon': 'bi-percent',  # 국고채10년
                'digit': 3,
            },
            '901Y056S23A': {
                'icon': 'bi-piggy-bank-fill',  # 증시예탁금
                'digit': 0,
            },
            '901Y056S23E': {
                'icon': 'bi-cash-stack',  # 신용융자잔고
                'digit': 0,
            },
            '901Y056S23F': {
                'icon': 'bi-credit-card',  # 신용대주잔고
                'digit': 0,
            },
            '403Y001*AA': {
                'icon': 'bi-truck',  # 수출지수
                'digit': 2,
            },
            '901Y062P63AC': {
                'icon': 'bi-house-up-fill',  # KB부동산매매지수(아파트, 전국)
                'digit': 2,
            },
            '901Y063P64AC': {
                'icon': 'bi-house-up-fill',  # KB부동산전세지수(아파트, 전국)
                'digit': 2,
            },
            '901Y067I16E': {
                'icon': 'bi-graph-up-arrow',  # 경기선행지수순환변동
                'digit': 1,
            },
        }

        data = []
        for col, spec in selector.items():
            name, unit = self.meta[col]['name'], self.meta[col]['unit']
            unit = unit.replace("-", "")
            if col == '731Y0030000003':
                obj = krwusd()
                obj.update({
                    'code': col,
                    'unit': unit,
                    'name': name
                })
            else:
                serial = self[col].dropna()
                obj = {
                    'code': col,
                    'date': serial.index[-1].strftime("%Y-%m-%d"),
                    'value': serial.values[-1],
                    'change': float(round(100 * serial.pct_change().values[-1], 2)),
                    'unit': unit.replace("백만원", "억원"),
                    'name': name.replace("(아파트, 전국)", ""),
                }
            obj['digit'] = spec['digit']
            obj['icon'] = spec['icon']
            obj['color'] = '#1861A8' if obj['change'] < 0 else '#C92A2A'
            if obj['change'] > 0:
                obj['change'] = f"+{obj['change']}"
            else:
                if col in ['KOSPI', 'KOSDAQ', '901Y062P63AC', '901Y063P64AC', '901Y067I16E']:
                    obj['icon'] = obj['icon'].replace('up', 'down')
            if col in ['901Y056S23A', '901Y056S23E', '901Y056S23F']:
                obj['value'] = obj['value'] / 100
            data.append(obj)
        return data

    def serialize(self) -> dict:
        objs = {}
        for col in self:
            serial = self[col].dropna()
            objs[col] = {
                'date': serial.index.strftime('%Y-%m-%d').tolist(),
                'data': serial.tolist()
            }
        return objs


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    macro = Macro(update=False)
    # print(macro)
    # print(macro.log)
    # print(macro.serialize())
    # print(macro.meta)
    # print(macro.status)
    # for n, meta in enumerate(macro.meta.values()):
    #     print(n + 1, meta)
    for n, stat in enumerate(macro.status):
        print(n + 1, stat)

