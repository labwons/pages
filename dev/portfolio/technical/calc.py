try:
    from ..fetch.krx import krx
except ImportError:
    from dev.portfolio.fetch.krx import krx

from datetime import timedelta
from numpy import nan
from pandas import DataFrame, Series
from scipy.stats import linregress
from ta.trend import MACD, PSARIndicator
from ta import add_momentum_ta
from typing import Union
from warnings import filterwarnings
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")


class TechnicalFrame(DataFrame):

    BASE_PRICE = 'typical'

    @classmethod
    def typicalPrice(cls, ohlcv: DataFrame):
        return round((ohlcv.High + ohlcv.Low + ohlcv.Close) / 3, 0)

    @classmethod
    def simpleMA(cls, ohlct: DataFrame, *args: int) -> DataFrame:
        copyOhlct = ohlct.copy()
        basePrice = ohlct[cls.BASE_PRICE]
        if not args:
            args = [5, 20, 60, 120, 200]
        for arg in args:
            copyOhlct[f'MA{arg}'] = basePrice.rolling(arg).mean()
        return copyOhlct

    @classmethod
    def bollingerBand(cls, ohlct:DataFrame, window:int=20, stddevFactor:int=2) -> DataFrame:
        copyOhlct = ohlct.copy()
        basePrice = ohlct[cls.BASE_PRICE]
        copyOhlct['middle'] = middle = basePrice.rolling(window).mean()
        copyOhlct['stddev'] = stddev = basePrice.rolling(window).std()
        copyOhlct['upperband'] = upperband = middle + stddevFactor * stddev
        copyOhlct['lowerband'] = lowerband = middle - stddevFactor * stddev
        copyOhlct['uppertrend'] = uppertrend = middle + (stddevFactor / 2) * stddev
        copyOhlct['lowertrend'] = lowertrend = middle - (stddevFactor / 2) * stddev
        copyOhlct['width'] = 100 * (2 * stddevFactor * stddev) / middle
        copyOhlct['pctb'] = ((basePrice - lowerband) / (upperband - lowerband)).where(upperband != lowerband, nan)
        copyOhlct['pctt'] = ((basePrice - lowertrend) / (uppertrend - lowertrend)).where(uppertrend != lowertrend, nan)
        return copyOhlct

    @classmethod
    def macd(cls, ohlct:DataFrame) -> DataFrame:
        copyOhlct = ohlct.copy()
        basePrice = ohlct[cls.BASE_PRICE]
        macd = MACD(close=basePrice)
        copyOhlct['macd'] = macd.macd()
        copyOhlct['signal'] = macd.macd_signal()
        copyOhlct['diff'] = macd.macd_diff()
        return copyOhlct

    @classmethod
    def rsi(cls, ohlct:DataFrame) -> DataFrame:
        copy = add_momentum_ta(ohlct.copy(), "High", "Low", "Close", "Volume")
        return copy.rename(columns={c:c.replace("momentum_", "") for c in copy})

    @classmethod
    def regression(cls, ohlct:DataFrame, *args:Union[int, float]) -> DataFrame:
        def _fit(price:Series) -> Series:
            data = price.reset_index(level=0)
            xrange = (data['Date'].diff()).dt.days.fillna(1).astype(int).cumsum()

            slope, intercept, _, _, _ = linregress(x=xrange, y=data[data.columns[-1]])
            fitted = slope * xrange + intercept
            fitted.name = f'{price.name}Fit'
            return pd.concat(objs=[data, fitted], axis=1).set_index(keys='Date')[fitted.name]

        basePrice = ohlct[cls.BASE_PRICE]
        objs = {'전구간 추세': _fit(basePrice)}
        for yy in [5, 2, 1, 0.5, 0.25] if not args else args:
            key = f"{yy}Y 추세" if isinstance(yy, int) else f"{int(yy * 12)}M 추세"
            date = basePrice.index[-1] - timedelta(int(yy * 365))
            if basePrice.index[0] > date:
                fit = Series(name=key, index=basePrice.index)
            else:
                fit = _fit(basePrice[basePrice.index >= date])
            objs[key] = fit
        return ohlct.join(round(pd.concat(objs=objs, axis=1), 0))

    @classmethod
    def deviation(cls, base:DataFrame) -> DataFrame:
        cols = [col for col in base if col.endswith('추세')]
        objs = {}
        for col in cols:
            name = col.replace("추세", "편차")
            unit = base[[cls.BASE_PRICE, col]].dropna()
            if unit.empty:
                objs[name] = Series(name=col, dtype=float)
            else:
                objs[name] = 100 * (unit[cls.BASE_PRICE]/unit[col] - 1)
                # objs[name] = (unit[use]/unit[col] - 1) / (abs(unit[use]/unit[col] - 1).sum() / len(unit))
        return pd.concat(objs=objs, axis=1)

    @classmethod
    def psar(cls, ohlct:DataFrame) -> DataFrame:
        copyOhlct = ohlct.copy()
        fromTa = PSARIndicator(copyOhlct.High, copyOhlct.Low, copyOhlct.Close)
        copyOhlct['up'] = fromTa.psar_up()
        copyOhlct['down'] = fromTa.psar_down()
        copyOhlct['psar'] = copyOhlct.apply(lambda x: x['up'] if pd.isna(x['down']) else x['down'], axis=1)
        copyOhlct['pct'] = 100 * (copyOhlct.typical / copyOhlct.psar - 1)
        return copyOhlct

    @classmethod
    def push(cls, a: DataFrame, *b: DataFrame):
        for _b in b:
            b_ = _b.drop(columns=a.columns.intersection(_b.columns))
            a = pd.merge(a, b_, left_index=True, right_index=True, how='outer')
        return a

    def __init__(self, ticker_or_ohlcv:Union[str, DataFrame], **kwargs):
        if isinstance(ticker_or_ohlcv, str):
            data = krx(ticker=ticker_or_ohlcv, period=kwargs["period"] if "period" in kwargs else 10).ohlcv
        elif isinstance(ticker_or_ohlcv, DataFrame):
            data = ticker_or_ohlcv.copy()
        else:
            raise TypeError()

        data['typical'] = self.typicalPrice(data)
        data = self.push(
            data,
            self.simpleMA(data, 5, 20, 60, 120, 200),
            self.bollingerBand(data),
            self.regression(data, 5, 2, 1, 0.5, 0.25),
            self.macd(data),
            self.rsi(data),
            self.psar(data)
        )
        data = self.push(data, self.deviation(data))
        super().__init__(data)
        return



if __name__ == "__main__":
    import pandas as pd
    df = pd \
        .read_csv("https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
        .set_index(keys="Date") \
        .drop(columns=["Adj Close"])
    df.index = pd.to_datetime(df.index)
    tf = TechnicalFrame(df)
    print(tf)

