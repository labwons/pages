from labwons.logs import logger
from labwons.fetch.stock.fnguide import FnGuide
from labwons.fetch.stock.krx import PyKrx

from time import perf_counter
import pandas as pd


class CacheStock:

    def __init__(self, *tickers):
        stime = perf_counter()
        logger.info(f'RUN [CACHING STOCK DATA]: {len(tickers):, d}ITEMS')

        failures = []

        _ohlcv = {}
        _marketCap = {}
        _perBand = {}
        _foreignRate = {}
        for ticker in tickers:
            if ticker is None or pd.isna(ticker):
                continue

            krx = PyKrx(ticker)
            fng = FnGuide(ticker)

            try:
                _ohlcv[ticker] = krx.ohlcv
            except Exception as reason:
                logger.error(f'- FAILED TO FETCH OHLCV: {ticker} / {reason}')
                failures.append(ticker)
                continue

            try:
                _marketCap[ticker] = krx.getMarketCap()
            except Exception as reason:
                logger.error(f'- FAILED TO FETCH MARKET CAP: {ticker} / {reason}')
                failures.append(ticker)
                continue

            try:
                _perBand[ticker] = fng.multipleBand["PER"]
            except Exception as reason:
                logger.error(f'- FAILED TO FETCH PER BAND: {ticker} / {reason}')
                failures.append(ticker)
                continue

            try:
                _foreignRate[ticker] = fng.foreignExhaustRate
            except Exception as reason:
                logger.error(f'- FAILED TO FETCH FOREIGN EXHAUST RATE: {ticker} / {reason}')
                failures.append(ticker)
                continue

        self.ohlcv = pd.concat(_ohlcv, axis=1)
        self.marketCap = pd.concat(_marketCap, axis=1)
        self.perBand = pd.concat(_perBand, axis=1)
        self.foreignRate = pd.concat(_foreignRate, axis=1)
        logger.info(f'END [CACHING STOCK DATA]: {perf_counter() - stime:.2f}s')
        logger.info(f'- Pricing Date: {self.ohlcv.index.astype(str).values[-1]}')
        logger.info(f'- Failed Items: {len(failures)} / {len(tickers)}')
        return