try:
    from ...fetch.macro.ecos import Ecos
    from ...fetch.macro.fred import Fred
except ImportError:
    from src.fetch.macro.ecos import Ecos
    from src.fetch.macro.fred import Fred
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
    meta: Dict = {}
    _log: List[str] = []
    def __init__(self, update:bool=False):
        stime = time()
        self.log = f'RUN [Build Macro Cache]'
        self.meta = Ecos.metaData()
        for symbol, item in Fred.predef.items():
            self.meta[symbol] = {
                "name": item["name"],
                "unit": item["unit"],
                "group": item["category"]
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
            super().__init__(read_json(PATH.MACRO, orient='index'))
            # if objs:
            #     index = concat(objs, axis=1)
            #     self.drop(columns)
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
        selector = [
            '731Y0030000003',  # 원/달러 환율
            '817Y002010151000',  # KORIBOR(6개월)
            '817Y002010195000',  # 국고채2년
            '817Y002010210000',  # 국고채10년
            '101Y004BBHA00',  # M2(평잔, 원계열)
            '901Y056S23A',  # 증시예탁금
            '901Y056S23E',  # 신용융자잔고
            '901Y056S23F',  # 신용대주잔고
            '403Y001*AA',  # 수출지수
            '901Y062P63AC',  # KB부동산매매지수(아파트, 전국)
            '901Y063P64AC',  # KB부동산전세지수(아파트, 전국)
            '901Y067I16E',  # 경기선행지수순환변동
        ]
        data = []
        for col in selector:
            serial = self[col].dropna()
            data.append({
                'code': col,
                'date': serial.index[-1].strftime("%Y-%m-%d"),
                'last': float(serial.iloc[-1]) if self.meta[col]['unit'] in ['%', '-', '원'] else int(serial.iloc[-1]),
                'pct': float(round(100 * serial.pct_change().values[-1], 2)),
                'unit': self.meta[col]['unit'],
                'name': self.meta[col]['name'],
            })
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
    print(str(macro.status))
    # for s, n in macro.meta.items():
    #     print(f'{s}: {n["name"]}')

