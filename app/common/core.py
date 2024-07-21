try:
    from .tradingdate import TradingDate
except ImportError:
    from app.common.tradingdate import TradingDate
from datetime import date
from pandas import DataFrame
from pykrx import stock
from typing import Union


def marketCaps(td:Union[date, str]=None) -> DataFrame:
    if not td:
        td = TradingDate.end.strftime("%Y%m%d")
    return stock.get_market_cap_by_ticker(date=td, market="ALL", alternative=True)



if __name__ == "__main__":
    print(marketCaps())