from datetime import date, datetime, timedelta
from pandas import DateOffset
from pykrx import stock
from pytz import timezone
from typing import Union, Iterable
from yfinance import Ticker


class _tradingDate(object):
    
    __slots__ = (
        "span",
        "near"
    )
    
    def __init__(self):
        
        # Set Current Time-zone
        _now_ = datetime.now(timezone('Asia/Seoul'))
        
        # Fetching Time-span of the Market
        # looking for 5year market data. reference point is executive datetime(@_now_).
        # resourced from pykrx(; NAVER, KRX) or yfinance(; Yahoo Finance). 
        # pykrx is prior to yfinance (incase of server block).
        # datetime interval (or frequency) is 1 day, weekend and holiday not included(automatic)
        _anc_ = _now_ - timedelta(5 * 365)        
        _src_ = stock.get_market_ohlcv_by_date(
            fromdate=_anc_.strftime("%Y%m%d"),
            todate=_now_.strftime("%Y%m%d"),
            ticker="005930",
            freq='d',
            adjusted=True,
            name_display=False
        )
        if _src_.empty:
            _src_ = Ticker("005930.KS") \
                .history(
                    start=_anc_.date(),
                    end=_now_.date(),
                    interval='1d'
                )
        self.span = span = _src_.index.date
        
        # Find Recent Market Date
        # default date is the last index of the dates, however in case of market running,
        # current real-time market date is excluded.        
        self.near = span[-1]
        if not _now_.strftime('%A') in ['Saturday', 'Sunday']:
            if 930 <= int(datetime.now(timezone('Asia/Seoul')).strftime("%H%M")) < 1531:
                if len(_src_.columns) == 6:
                    self.near = span[-2]
        return

    def __call__(self) -> Iterable:
        return self.span
    
    def __contains__(self, date:Union[str, datetime, date]) -> bool:
        if isinstance(date, str):
            if "-" in date:
                date = datetime.strptime(date, "%Y-%m-%d")
            else:
                date = datetime.strptime(date, "%Y%m%d")
        if isinstance(date, datetime):
            date = date.date()
        return date in self.span

    def __getitem__(self, interval:str) -> str:
        if not '-' in interval:
            raise KeyError(f'Wrong interval format: {interval}')
        
        interval = interval.lower()
        if interval.startswith('d'):
            key = 'days'
        elif interval.startswith('w'):
            key = 'weeks'
        elif interval.startswith('m'):
            key = 'months'
        elif interval.startswith('y'):
            key = 'years'
        else:
            raise KeyError(f'Wrong interval format: {interval}')
        
        _offset = (self.near - DateOffset(**{key: int(interval[2:])})).date()
        while not _offset in self:
            _offset = (_offset - DateOffset(days=1)).date()
        return _offset
    
    def __iter__(self):
        for interval in ('D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1'):
            return interval, self[interval]

    def __len__(self) -> int:
        return len(self.span)
    
    def __str__(self) -> str:
        return self.near.strftime("%Y%m%d")
 
    


# Alias
TradingDate = _tradingDate()


if __name__ == "__main__":

    print(TradingDate)
    print(TradingDate.near)
    print(TradingDate.span)
    print(datetime(2001, 1, 1) in TradingDate)
    print("2024-07-26" in TradingDate)
    print(TradingDate["-1d"])
    print(TradingDate["-1w"])
    print(TradingDate["-1m"])
    print(TradingDate["-3m"])
    print(TradingDate["-6m"])
    print(TradingDate["-1y"])