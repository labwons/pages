from labwons.logs import logger
from labwons.fetch.macro.schema import FIELD_FRED

from datetime import datetime, timedelta
from pandas import concat, DataFrame, Series
from pandas_datareader import get_data_fred
from requests.exceptions import SSLError
from time import perf_counter, sleep
from typing import List



class MacroFred:

    @classmethod
    def saveAs(cls, path:str):
        logger.info('RUN [CACHE MACRO FRED]')
        stime = perf_counter()

        objs = {}
        for label, meta in FIELD_FRED.items():
            objs[meta.symbol] = series = cls.fetch(meta.symbol)
            if series.empty:
                logger.error(f'- FAILED TO FETCH: {label}')
                del objs[meta.symbol]

        data = concat(objs=objs, axis=0)
        data = data.reset_index()
        data.columns = ['symbol', 'date', 'value']
        data.to_parquet(path, engine='pyarrow', compression='zstd')
        logger.info(f'END [CACHE MACRO FRED]: {perf_counter() - stime:.2f}s')
        return

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


if __name__ == "__main__":
    print(len(FIELD_FRED))