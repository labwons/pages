try:
    from .krx import PyKrx
    from .fnguide import fnguide
except ImportError:
    from src.fetch.stock.krx import PyKrx
    from src.fetch.stock.fnguide import fnguide
from pandas import concat, isna
from time import perf_counter
from typing import List


class CacheStock:

    _log: List[str] = []
    def __init__(self, *tickers:str, user:List=None):
        self.log = f'  >> RUN [CACHING STOCK DATA]: '
        stime = perf_counter()

        tickers = list(tickers)
        for _ticker in user:
            if not _ticker in tickers:
                tickers.append(_ticker)

        ohlcv = {}
        marketCap = {}
        perBand = {}
        foreignRate = {}
        for ticker in tickers:
            krx = PyKrx(ticker)
            fng = fnguide(ticker)

            try:
                ohlcv[ticker] = krx.ohlcv
            except Exception as reason:
                self.log = f'     ...FAILED TO FETCH OHLCV: {ticker} / {reason}'

            try:
                marketCap[ticker] = krx.getMarketCap()["시가총액"]
            except Exception as reason:
                self.log = f'     ...FAILED TO FETCH MARKET CAP: {ticker} / {reason}'

            try:
                perBand[ticker] = fng.multipleBand["PER"]
            except Exception as reason:
                self.log = f'     ...FAILED TO FETCH PER BAND: {ticker} / {reason}'

            try:
                foreignRate[ticker] = fng.foreignExhaustRate
            except Exception as reason:
                self.log = f'     ...FAILED TO FETCH FOREIGN EXHAUST RATE: {ticker} / {reason}'

        self.ohlcv = concat(ohlcv, axis=1)
        self.marketCap = concat(marketCap, axis=1)
        self.perBand = concat(perBand, axis=1)
        self.foreignRate = concat(foreignRate, axis=1)

        self._log[0] += f'{len(tickers):,d} items @{self.ohlcv.index.astype(str).values[-1]}'.replace("-", "/")
        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

if __name__ == "__main__":
    cache = CacheStock("005930", "000660")
    print(cache.log)
    print(cache.ohlcv)
    # print(cache.marketCap)
    # print(cache.perBand)
    # print(cache.foreignRate)