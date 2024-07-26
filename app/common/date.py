try:
    from deco import memorize
except ImportError:
    from app.common.deco import memorize    
from datetime import date, datetime, timedelta
from pandas import DataFrame, DateOffset
from pykrx import stock
from pytz import timezone
from requests.exceptions import JSONDecodeError, SSLError
from typing import Union
from yfinance import Ticker
import requests


class _tradingDate(object):

    def __init__(self):
        return

    def __call__(self, td:Union[date, datetime, str]=None) -> date:
        return self.dateCheck(td=td)

    def __str__(self) -> str:
        return self.near.strftime("%Y%m%d")
 
    def __getitem__(self, n:int) -> date:
        return self.base.index[n].date()

    def __len__(self) -> int:
        return len(self.base)
    
    @memorize
    def anchorDate(self) -> date:
        return self.currentDate - timedelta(5 * 365)
    
    @memorize
    def currentDate(self) -> date:
        return datetime.now(timezone('Asia/Seoul')).date()
    
    @memorize
    def base(self) -> DataFrame:
        _base = stock \
            .get_market_ohlcv_by_date(
                fromdate=self.anchorDate.strftime("%Y%m%d"),
                todate=self.currentDate.strftime("%Y%m%d"),
                ticker="005930",
                freq='d',
                adjusted=True,
                name_display=False
            )
        if _base.empty:
            _base = Ticker("005930.KS") \
                .history(
                    start=self.anchorDate,
                    end=self.currentDate,
                    interval='1d'
                )
        return _base
    
    @memorize
    def near(self) -> date:
        return self[-1].date()    

    @memorize
    def periods(self) -> dict:
        objs = {'D+0': datetime.strptime(self.wiseDate, "%Y%m%d")}
        find = {'D-1': {'days':1}, 'W-1': {'weeks':1}, 'M-1': {'months':1}, 'M-3': {'months':3}, 'M-6': {'months':6}, 'Y-1': {'years':1}}
        for arg, kwarg in find.items():
            _find = objs['D+0'] - DateOffset(**kwarg)
            while not _find in self._base:
                _find = _find - DateOffset(days=1)
            objs[arg] = _find.date()
        return objs
    
    @property
    def clock(self) -> int:
        return int(datetime.now(timezone('Asia/Seoul')).strftime("%H%M"))

    @memorize
    def wiseDate(self) -> str:
        try:
            html = requests.get('https://www.wiseindex.com/Index/Index#/G1010.0.Components').text
            pin1 = html.find("기준일")
            pin2 = pin1 + html[pin1:].find("</p>")
            return html[pin1 + 6 : pin2].replace(".", "")
        except (JSONDecodeError, SSLError):
            return self[-2].strftime("%Y%m%d")

    def dateCheck(self, td:Union[date, datetime, str]=None) -> date:
        if not td:
            return TradingDate.end
        if isinstance(td, date):
            return td
        if isinstance(td, datetime):
            return td.date()
        if isinstance(td, str):
            return datetime.strptime(td, "%Y%m%d")
        raise KeyError(f'Wrong format {td}')


# Alias
TradingDate = _tradingDate()


if __name__ == "__main__":

    print(TradingDate)
    print(TradingDate.start)
    print(TradingDate.end)
    print(TradingDate[-2])
    print(TradingDate.wiseDate)
    print(TradingDate.periods)
    print(TradingDate.strf(-2))
        