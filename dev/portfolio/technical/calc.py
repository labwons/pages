from datetime import timedelta
from numpy import nan
from pandas import DataFrame, Series
from scipy.stats import linregress
from ta.trend import MACD, PSARIndicator
from ta import add_momentum_ta
from typing import Union
from warnings import filterwarnings
import pandas as pd
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")


def typicalPrice(ohlcv:DataFrame):
    return round((ohlcv.High + ohlcv.Low + ohlcv.Close) / 3, 0)

def simpleMA(ohlct:DataFrame, use:str='typical', *args:int) -> DataFrame:
    copyOhlct = ohlct.copy()
    basePrice = ohlct.typical if use == 'typical' else ohlct.Close
    if not args:
        args = [5, 20, 60, 120, 200]
    for arg in args:
        copyOhlct[f'MA{arg}'] = basePrice.rolling(arg).mean()
    return copyOhlct

def bollingerBand(ohlct:DataFrame, use:str='typical', window:int=20, stddevFactor:int=2) -> DataFrame:
    copyOhlct = ohlct.copy()
    basePrice = ohlct.typical if use == 'typical' else ohlct.Close
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

def macd(ohlct:DataFrame, use:str='typical') -> DataFrame:
    copyOhlct = ohlct.copy()
    basePrice = ohlct.typical if use == 'typical' else ohlct.Close
    macd = MACD(close=basePrice)
    copyOhlct['macd'] = macd.macd()
    copyOhlct['signal'] = macd.macd_signal()
    copyOhlct['diff'] = macd.macd_diff()
    return copyOhlct

def rsi(ohlct:DataFrame) -> DataFrame:
    copy = add_momentum_ta(ohlct.copy(), "High", "Low", "Close", "Volume")
    return copy.rename(columns={c:c.replace("momentum_", "") for c in copy})

def regression(ohlct:DataFrame, use:str='typical', *args:Union[int, float]) -> DataFrame:
    def _fit(price:Series) -> Series:
        data = price.reset_index(level=0)
        xrange = (data['Date'].diff()).dt.days.fillna(1).astype(int).cumsum()

        slope, intercept, _, _, _ = linregress(x=xrange, y=data[data.columns[-1]])
        fitted = slope * xrange + intercept
        fitted.name = f'{price.name}Fit'
        return pd.concat(objs=[data, fitted], axis=1).set_index(keys='Date')[fitted.name]

    basePrice = ohlct.typical if use == 'typical' else ohlct.Close
    objs = {'전체': _fit(basePrice)}
    for yy in [5, 2, 1, 0.5, 0.25] if not args else args:
        key = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
        date = basePrice.index[-1] - timedelta(int(yy * 365))
        if basePrice.index[0] > date:
            fit = Series(name=key, index=basePrice.index)
        else:
            fit = _fit(basePrice[basePrice.index >= date])
        objs[key] = fit
    return ohlct.join(round(pd.concat(objs=objs, axis=1), 0))

def deviation(base:DataFrame, use:str='typical') -> DataFrame:
    cols = [col for col in base if not col in ['Open', 'High', 'Low', 'Close', 'Volume', 'typical']]
    objs = {}
    for col in cols:
        unit = base[[use, col]].dropna()
        if unit.empty:
            objs[col] = Series(name=col, dtype=float)
        else:
            objs[col] = 100 * (unit[use]/unit[col] - 1)
            # objs[col] = (unit[use]/unit[col] - 1) / (abs(unit[use]/unit[col] - 1).sum() / len(unit))
    return pd.concat(objs=objs, axis=1)

def psar(ohlct:DataFrame) -> DataFrame:
    copyOhlct = ohlct.copy()
    fromTa = PSARIndicator(copyOhlct.High, copyOhlct.Low, copyOhlct.Close)
    copyOhlct['up'] = fromTa.psar_up()
    copyOhlct['down'] = fromTa.psar_down()
    copyOhlct['psar'] = copyOhlct.apply(lambda x: x['up'] if pd.isna(x['down']) else x['down'], axis=1)
    copyOhlct['pct'] = 100 * (copyOhlct.typical / copyOhlct.psar - 1)
    return copyOhlct



if __name__ == "__main__":
    import pandas as pd


    df = pd \
        .read_csv("https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
        .set_index(keys="Date") \
        .drop(columns=["Adj Close"])
    df.index = pd.to_datetime(df.index)
    df['typical'] = typicalPrice(df)
    # print(df)

    # print(simpleMA(df))
    # print(bollingerBand(df))
    # print(macd(df))
    # print(rsi(df))
    # print(regression(df))
    print(deviation(regression(df)))
    # print(psar(df))


    # import plotly.graph_objects as go
    # reg = regression(df)
    # fig = go.Figure()
    # for n, col in enumerate(reg):
    #     fig.add_trace(go.Scatter(
    #         name=col,
    #         x=reg.index,
    #         y=reg[col],
    #         mode='lines',
    #         visible='legendonly',
    #         showlegend=True,
    #         line={
    #             'color':'black',
    #             'dash':'dash',
    #             'width':0.8
    #         },
    #         connectgaps=True,
    #         xhoverformat='%Y/%m/%d',
    #         yhoverformat=',d',
    #         hovertemplate=col + ': %{y}KRW<extra></extra>'
    #     ))
    # fig.show()

        

