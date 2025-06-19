try:
    from .metadata import ECOSMETA, FREDMETA
    from ...common.env import FILE
    from ...fetch.macro.krx import krxIndex
except ImportError:
    from src.build.baseline.metadata import ECOSMETA, FREDMETA
    from src.common.env import FILE
    from src.fetch.macro.krx import krxIndex
from pandas import concat, read_parquet, DataFrame
from time import perf_counter
from typing import List


class MacroBaseline:

    _log: List[str] = []
    def __init__(self):
        stime = perf_counter()
        self.log = f'  >> RUN [CACHING MACRO]'

        try:
            krx = krxIndex()
        except Exception as reason:
            krx = DataFrame()
            self.log = f'     ... FAILED to fetch KOSPI/KOSDAQ index: {reason}'

        ecos = read_parquet(FILE.ECOS, engine='pyarrow')
        fred = read_parquet(FILE.FRED, engine='pyarrow')
        self.data = concat([krx, ecos, fred], axis=1)

        # METADATA
        self.meta = {}
        for label, meta in ECOSMETA:
            self.meta[f'{meta.symbol}{meta.code}'] = {
                "name": label,
                "unit": meta.unit,
                "group": meta.category,
                "hover": meta.hover
            }

        for label, meta in FREDMETA:
            self.meta[meta.symbol] = {
                "name": label,
                "unit": meta.unit,
                "group": meta.category,
                "hover": meta.hover
            }

        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    macro = MacroBaseline()
    print(macro.log)
    print(macro.meta)