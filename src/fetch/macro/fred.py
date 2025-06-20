from datetime import datetime, timedelta
from pandas import concat, DataFrame, Series
from pandas_datareader import get_data_fred
from requests.exceptions import SSLError
from time import perf_counter, sleep
from typing import List



class Fred:

    _log: List[str] = []
    def __init__(self):
        return

    def __call__(self, symbol:str, period:int=10):
        return self.fetch(symbol, period)

    @classmethod
    def fetch(cls, symbol: str, period:int=10, fs:int=5) -> Series:
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

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    def data(self, metadata:dict) -> DataFrame:
        stime = perf_counter()
        self.log = f'  >> RUN [CACHING FRED]'

        objs = {}
        for label, meta in metadata:
            try:
                objs[meta.symbol] = series = Fred.fetch(meta.symbol)
                if series.empty:
                    self.log = f'     ... FAILED to fetch: {label}: Try count exceeded'
                    del objs[meta.symbol]
            except Exception as reason:
                self.log = f'     ... FAILED to fetch: {label}: {reason}'

        data = concat(objs=objs, axis=1)
        data = data[data.index >= datetime(1990, 1, 1)]
        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return data


if __name__ == "__main__":
    fred = Fred()
    print(fred)
    for col in fred:
        data = fred[col]
        if data.empty:
            print(col, "empty")
        else:
            data = data.dropna()
            print(col, data.values[-1], f'@{data.index[-1]}')