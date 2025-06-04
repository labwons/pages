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


FAQ = [
    {'q': '사용법을 모르겠어요.', 'a': '영상을 통해 사용법을 확인하세요. (영상 준비 중)'},
    {'q': '자료 출처가 어디인가요?', 'a': '한국은행 경제통계시스템과 미국 연방준비경제데이터 시스템 입니다. 일부 데이터(YoY, MoM)은 가공되었습니다.'},
    {'q': '언제 업데이트 되나요?', 'a': '주가 지수는 정규장 시간 마감(15:30) 이후 15분~30분 내, 기타 데이터는 한국 시간 저녁 9시 이후에 업데이트 됩니다.'},
    {'q': '사용하다 불편한 점이 있어요. 고쳐주세요.',
     'a': '고장 신고, 정보 정정 및 기타 문의는 snob.labwons@gmail.com 으로 연락주세요!<i class="bi bi-emoji-smile-fill"></i>'},
    {'q': '정보 수정이 필요해요.',
     'a': '고장 신고, 정보 정정 및 기타 문의는 snob.labwons@gmail.com 으로 연락주세요!<i class="bi bi-emoji-smile-fill"></i>'},
]

class Macro(DataFrame):
    faqs: List[Dict] = FAQ
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
                "format": item["format"]
            }

        try:
            tz = timezone(timedelta(hours=9))
            ck = datetime.now(tz)
            ks = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '1001')['종가']
            kq = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '2001')['종가']
            ks.name = 'KOSPI'
            kq.name = 'KOSDAQ'
            objs = [ks, kq]
        except (KeyError, Exception):
            objs = []
            self.log = "  - KRX Not accessible: update failed"
            pass

        if not update:
            basis = read_json(PATH.MACRO, orient='index')
            if objs:
                index = concat(objs, axis=1)
                basis = basis.drop(columns=index.columns)
                super().__init__(concat([index, basis], axis=1))
            else:
                super().__init__(basis)
            self.log = f'END [Build Macro Cache]'
            return

        Ecos.api = "CEW3KQU603E6GA8VX0O9"
        ecos = Ecos()
        fred = Fred()
        objs += [ecos, fred]

        super().__init__(concat(objs=objs, axis=1))
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
                    'value': float(serial.values[-1]) if unit in ['%', '', '원'] else int(serial.values[-1] / 100),
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
    print(macro)
    # print(macro.log)
    # print(macro.serialize())
    # print(macro.meta)
    # print(macro.status)
    # for n, meta in enumerate(macro.meta.values()):
    #     print(n + 1, meta)
    for n, stat in enumerate(macro.status):
        print(n + 1, stat)

