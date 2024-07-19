from datetime import date, datetime, timedelta
from pandas import DataFrame, DateOffset
from pykrx.stock import get_market_ohlcv_by_date
from pytz import timezone
from requests.exceptions import JSONDecodeError, SSLError
from yfinance import Ticker
import requests


class _tradingDate(object):
    
    def __init__(self, extension:int=10):
        end = datetime.now(timezone('Asia/Seoul')).date()
        start = end - timedelta(extension * 365)
        try:
            base = get_market_ohlcv_by_date(
                fromdate=start.strftime("%Y%m%d"), 
                todate=end.strftime("%Y%m%d"), 
                ticker="005930",
                freq='d',
                adjusted=True,
                name_display=False
            )
        except JSONDecodeError:
            base = DataFrame()
        
        if base.empty:
            base = Ticker("005930.KS").history(interval="1d", start=start, end=end)
        self._base = base.index
        return
    
    def __str__(self) -> str:
        return f'''Market Status: {self.isMarketOpen}
   Start Date: {self.start}
     End Date: {self.end}
        Years: {self.years}Y
 Trading Days: {len(self):,}Days'''
 
    def __getitem__(self, n:int) -> date:
        return self._base[n].date()
    
    def __len__(self) -> int:
        return len(self._base)
    
    @property
    def clock(self) -> int:
        return int(datetime.now(timezone('Asia/Seoul')).strftime("%H%M"))
    
    @property
    def end(self) -> date:
        return self._base[-1].date()
    
    @property
    def isMarketOpen(self) -> bool:
        return (datetime.today().date() == self[-1]) and (900 <= self.clock < 1531)
    
    @property
    def periods(self) -> dict:
        objs = {'0D': self.end}
        find = {'1D': {'days':1}, '1W': {'weeks':1}, '1M': {'months':1}, '3M': {'months':3}, '6M': {'months':6}, '1Y': {'years':1}}
        for arg, kwarg in find.items():
            _find = self._base[-1] - DateOffset(**kwarg)
            while not _find in self._base:
                _find = _find - DateOffset(days=1)
            objs[arg] = _find.date()
        return objs        
        
    @property
    def start(self) -> date:
        return self._base[0].date()    
    
    @property
    def wiseDate(self) -> str:
        try:
            html = requests.get('https://www.wiseindex.com/Index/Index#/G1010.0.Components').text
            pin1 = html.find("기준일")
            pin2 = pin1 + html[pin1:].find("</p>")
            return html[pin1 + 6 : pin2].replace(".", "")
        except (JSONDecodeError, SSLError):
            return self.strf(-2)
    
    @property
    def years(self) -> int:
        return int(round((self.end - self.start).days/365, 2))
    
    def strf(self, n:int) -> str:
        return self[n].strftime("%Y%m%d")
    
    
        
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
        