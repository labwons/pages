from labwons.fetch.macro.schema import FIELD_FRED

from datetime import datetime, timedelta
from pandas import concat, DataFrame, Series
from pandas_datareader import get_data_fred
from requests.exceptions import SSLError
from time import perf_counter, sleep
from typing import List



class MacroFred:

    @classmethod
    def merge(cls) -> DataFrame:
        objs = {}
        for label, meta in FIELD_FRED.items():
            objs[meta.symbol] = series = cls.fetch(meta.symbol)
            if series.empty:
                print(f'- FAILED TO FETCH: {label}')
                del objs[meta.symbol]
        return concat(objs=objs, axis=1)

    @classmethod
    def fetch(cls, symbol: str, period:int=50, fs:int=5) -> Series:
        while fs > 0:
            try:
                fetched = get_data_fred(
                    symbols=symbol,
                    start=datetime.today() - timedelta(365 * period),
                    end=datetime.today()
                )
                return Series(name=symbol, index=fetched.index, data=fetched[symbol], dtype=float)
            except SSLError:
                fs -= 1
                sleep(5)
        return Series()


if __name__ == "__main__":
    print(MacroFred.merge())