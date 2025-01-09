from numpy import nan
from pandas import DataFrame, Series
from ta.trend import MACD


def typicalPrice(ohlcv:DataFrame):
    return (ohlcv.high + ohlcv.low + ohlcv.close) / 3

def simpleMA(ohlct:DataFrame, use:str='typical', *args:int) -> DataFrame:
    copyOhlct = ohlct.copy()
    basePrice = ohlct.typical if use == 'typical' else ohlct.close
    if not args:
        args = [5, 20, 60, 120, 200]
    for arg in args:
        copyOhlct[f'{arg}MA'] = basePrice.rolling(arg).mean()
    return copyOhlct

def bollingerBand(ohlct:DataFrame, use:str='typical', window:int=20, stddevFactor:int=2) -> DataFrame:
    copyOhlct = ohlct.copy()
    basePrice = ohlct.typical if use == 'typical' else ohlct.close
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

# def macd(ohlct:DataFrame) -> DataFrame: