try:
    from ..common.calendar import Calendar
except ImportError:
    from dev.common.calendar import Calendar
from datetime import timedelta
from pandas import DataFrame
from pykrx import stock


def ohlcv(ticker:str) -> DataFrame:
    fetch = stock.get_market_ohlcv_by_date(
        ticker=ticker, 
        fromdate=(Calendar[-1] - timedelta(3650)).strftime("%Y%m%d"), 
        todate=str(Calendar)
    )
    fetch.index.name = "date"
    fetch.drop(columns=["등락률"], inplace=True)
    fetch.columns = ["open", "high", "low", "close", "volume"]
    return fetch