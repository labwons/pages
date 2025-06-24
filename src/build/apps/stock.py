try:
    from ...fetch.stock.krx import PyKrx
except ImportError:
    from src.fetch.stock.krx import PyKrx
from pandas import DataFrame, Series
from json import dumps


# from ta import

class Stock:

    def __init__(self, ticker: str, ref: DataFrame):
        self.krx = krx = PyKrx(ticker=ticker)
        self.N = ref.loc[ticker]
        self.ohlcv = ohlcv = krx.ohlcv
        self.date = ohlcv.index.astype(str).tolist()
        self.typ = (ohlcv.high + ohlcv.low + ohlcv.close) / 3
        return

    @property
    def jsonOhlcv(self) -> str:
        return dumps({
            'date': self.date,
            'open': self.ohlcv['open'].tolist(),
            'high': self.ohlcv['high'].tolist(),
            'low': self.ohlcv['low'].tolist(),
            'close': self.ohlcv['close'].tolist(),
            'volume': self.ohlcv['volume'].tolist(),
        }).replace(" ", "")

    @property
    def jsonMa(self) -> str:
        return dumps({
            'sma5': self.typ.rolling(5).mean().tolist(),
            'sma20': self.typ.rolling(20).mean().tolist(),
            'sma60': self.typ.rolling(60).mean().tolist(),
            'sma120': self.typ.rolling(120).mean().tolist(),
            'sma200': self.typ.rolling(200).mean().tolist(),
        })

    @property
    def jsonBollinger(self) -> str:
        return dumps({
            'upper': self.typ.rolling(20).mean() + 2 * self.typ.rolling(20).std(),
            'upperTrend': self.typ.rolling(20).mean() + 1 * self.typ.rolling(20).std(),
            'middle': self.typ.rolling(20).mean(),
            'lower': self.typ.rolling(20).mean() - 2 * self.typ.rolling(20).std(),
            'lowerTrend': self.typ.rolling(20).mean() - 1 * self.typ.rolling(20).std(),
            'width': 100 * 4 * self.typ.rolling(20).std() / self.typ.rolling(20).mean()
        })
