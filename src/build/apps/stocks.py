try:
    from ...common.env import FILE, dDict
    from ...fetch.stock.krx import PyKrx
except ImportError:
    from src.common.env import FILE, dDict
    from src.fetch.stock.krx import PyKrx
from json import dumps
from pandas import DataFrame, Series
from pandas import concat, read_parquet
from time import perf_counter
from typing import List


# from ta import

class Stocks:

    _log: List[str] = []
    def __init__(self):
        self.basis = basis = read_parquet(FILE.BASELINE, engine='pyarrow')
        self.price = price = read_parquet(FILE.PRICE, engine='pyarrow')
        tickers = price.columns.get_level_values(0).unique()

        __mem__ = dDict()
        for ticker in tickers:
            if not ticker in basis.index:
                continue
            general = basis.loc[ticker]
            ohlcv = price[ticker].dropna().astype(int)
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3

            __mem__[ticker] = dDict(
                name=general['name'],
                date=ohlcv.index.astype(str).tolist(),
                ohlcv=self.convertOhlcv(ohlcv),
                sma=self.convertSma(typical),
                bollinger=self.convertBollinger(typical)
            )
        self.__mem__ = __mem__
        return

    def __iter__(self):
        for ticker, attr in self.__mem__:
            yield ticker, attr

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    def update(self, *tickers):
        self._log = [f'  >> RUN [CACHING STOCK PRICE]: ']
        stime = perf_counter()
        objs = {}
        for ticker in tickers:
            if not ticker:
                continue
            try:
                objs[ticker] = PyKrx(ticker).ohlcv
            except Exception as reason:
                self.log = f'     ...Failed TO FETCH PRICE: {ticker} / {reason}'

        if objs:
            self.price = concat(objs, axis=1)
        self._log[0] += f'{len(tickers):,d} items @{self.price.index.astype(str).values[-1]}'.replace("-", "/")
        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return



    @classmethod
    def convertOhlcv(cls, ohlcv:DataFrame) -> str:
        obj = {
            'open': ohlcv['open'],
            'high': ohlcv['high'],
            'low': ohlcv['low'],
            'close': ohlcv['close'],
            'volume': ohlcv['volume'],
        }
        for key in obj:
            obj[key] = obj[key].tolist()
        return dumps(obj).replace(" ", "")

    @classmethod
    def convertSma(cls, typical:Series) -> str:
        obj = {
            'sma5': typical.rolling(5).mean(),
            'sma20': typical.rolling(20).mean(),
            'sma60': typical.rolling(60).mean(),
            'sma120': typical.rolling(120).mean(),
            'sma200': typical.rolling(200).mean(),
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return dumps(obj).replace(" ", "")

    @classmethod
    def convertBollinger(cls, typical:Series) -> str:
        obj = {
            'upper': typical.rolling(20).mean() + 2 * typical.rolling(20).std(),
            'upperTrend': typical.rolling(20).mean() + 1 * typical.rolling(20).std(),
            'middle': typical.rolling(20).mean(),
            'lower': typical.rolling(20).mean() - 2 * typical.rolling(20).std(),
            'lowerTrend': typical.rolling(20).mean() - 1 * typical.rolling(20).std(),
            'width': 100 * 4 * typical.rolling(20).std() / typical.rolling(20).mean()
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return dumps(obj).replace(" ", "")


if __name__ == "__main__":
    stocks = Stocks()
    for t, stock in stocks:
        print(t)
