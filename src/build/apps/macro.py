try:
    from ..baseline.metadata import ECOSMETA, FREDMETA, KRXMETA, MACRO
    from ...fetch.macro.naver import krwusd
except ImportError:
    from src.build.baseline.metadata import ECOSMETA, FREDMETA, KRXMETA, MACRO
    from src.fetch.macro.naver import krwusd
from pandas import concat, DataFrame
from time import perf_counter
from typing import Dict, List


class Macro:

    _log: List[str] = []
    def __init__(self, baseline:DataFrame):
        stime = perf_counter()
        self.log = f'  >> BUILD [MACRO]'

        self.data = baseline.copy()

        # METADATA
        self.meta = {}
        for kind in [KRXMETA, ECOSMETA, FREDMETA]:
            for label, meta in kind:
                key = f'{meta.symbol}{meta.code}' if 'code' in meta else meta.symbol
                self.meta[key] = {
                    "name": label,
                    "unit": meta.unit,
                    "group": meta.category,
                    "hover": meta.hover
                }

        self.log = f'  >> BUILD END: {perf_counter() - stime:.2f}s'
        self._log[0] += f': {len(baseline.columns)} items'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @property
    def status(self) -> list:
        data = []
        for symbol, meta in MACRO.STATUS:

            # conv = {'십억원': 1e+9, '억원': 1e+8, '천만원': 1e+7, '백만원': 1e+6}
            name = self.meta[symbol]['name']
            unit = self.meta[symbol]['unit'].replace("-", "")
            if symbol == '731Y0030000003':
                obj = krwusd()
                obj.update({'code': symbol, 'unit': unit, 'name': name})
            else:
                serial = self.data[symbol].dropna()
                obj = {
                    'code': symbol,
                    'date': serial.index[-1].strftime("%Y-%m-%d"),
                    'value': serial.values[-1],
                    'change': float(round(100 * serial.pct_change().values[-1], 2)),
                    'unit': unit.replace("백만원", "억원"),
                    'name': name.replace("(아파트, 전국)", ""),
                }
            obj['digit'] = meta.digit
            obj['icon'] = meta.icon
            obj['color'] = '#1861A8' if obj['change'] < 0 else '#C92A2A'
            if obj['change'] > 0:
                obj['change'] = f"+{obj['change']}"
            else:
                if symbol in ['1001', '2001', '901Y062P63AC', '901Y063P64AC', '901Y067I16E']:
                    obj['icon'] = obj['icon'].replace('up', 'down')
            if symbol in ['901Y056S23A', '901Y056S23E', '901Y056S23F']:
                obj['value'] = obj['value'] / 100
            data.append(obj)
        return data

    def serialize(self) -> dict:
        objs = {}
        for col in self.data:
            serial = self.data[col].dropna()
            objs[col] = {
                'date': serial.index.strftime('%Y-%m-%d').tolist(),
                'data': serial.tolist()
            }
        return objs


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from src.common.env import FILE
    from pandas import read_parquet



    macro = Macro(read_parquet(FILE.MACRO_BASELINE, engine='pyarrow'))
    print(macro.log)
    # print(macro.serialize())
    # print(macro.meta)
    print(macro.status)

    for n, stat in enumerate(macro.status):
        print(n + 1, stat)

