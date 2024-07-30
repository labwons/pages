try:
    from date import TradingDate
except ImportError:
    from app.market.fetch.date import TradingDate
from datetime import date, datetime, timedelta
from pandas import DataFrame
from pykrx import stock
from requests.exceptions import JSONDecodeError, SSLError
from typing import Dict, List, Union, Iterable
import pandas as pd


def marketCap(td:str='') -> DataFrame:
    if not td:
        td = str(TradingDate)
        
    _cols_ = {'종가':'close', '시가총액':'marketCap', 
              '거래량':'volume', '거래대금':'amount', '상장주식수':'shares'}
    try:
        _get_ = stock.get_market_cap_by_ticker(
            date=td, 
            market="ALL", 
            alternative=True
        ).rename(columns=_cols_)
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_.values())
    _get_.index.name = "ticker"
    return _get_


def multiple(td:str='') -> DataFrame:
    if not td:
        td = str(TradingDate)
        
    _cols_ = ['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']
    try:
        _get_ = stock.get_market_fundamental(
            date=td, 
            market="ALL", 
            alternative=True
        )
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_)
    _get_.index.name = "ticker"
    return _get_


def ipo() -> DataFrame:
    _url_ = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    _cols_ = {'회사명':'name', '종목코드':'ticker', 
              '상장일':'ipo', '주요제품':'products', '결산월':'settlementMonth'}
    try:
        _get_ = pd.read_html(io=_url_, header=0, encoding='euc-kr')[0][_cols_.keys()]
        _get_.rename(columns=_cols_, inplace=True)
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_.values())
    _get_.set_index(keys='ticker', inplace=True)
    _get_.index = _get_.index.astype(str).str.zfill(6)
    _get_['ipo'] = pd.to_datetime(_get_['ipo'])
    return _get_


def earningRatio() -> DataFrame:
    def _base_return() -> DataFrame:
        _objs = {}
        _base = stock.get_market_ohlcv_by_ticker(date=str(TradingDate), market="ALL")['종가']
        for interval, date in TradingDate:
            _fetch = stock.get_market_ohlcv_by_ticker(date=date.strftime("%Y%m%d"), market="ALL")['종가']
            _objs[interval] = round(100 * (_base / _fetch - 1), 2)
        return pd.concat(objs=_objs, axis=1)
    
    def _update_return(tickers:Iterable) -> DataFrame:
        fromdate, todate = TradingDate['Y-2'].strftime("%Y%m%d"), str(TradingDate)
        objs = []
        for ticker in tickers:
            src = stock.get_market_ohlcv_by_date(ticker=ticker, fromdate=fromdate, todate=todate)['종가']
            obj = {"ticker": ticker}
            for interval, date in TradingDate:
                src_copy = src[src.index.date >= date]
                obj[interval] = round(100 * (src_copy.iloc[-1] / src_copy.iloc[0] - 1), 2)
            objs.append(obj)
        return DataFrame(objs).set_index(keys='ticker')

    _shares = pd.concat({dt: marketCap(TradingDate[dt].strftime("%Y%m%d"))['shares'] for dt in ['D-0', 'Y-1']}, axis=1)
    _shares = _shares[~_shares['D-0'].isna()]
    _normal = _shares[_shares['D-0'] == _shares['Y-1']].index
    _change = _shares[_shares['D-0'] != _shares['Y-1']].index
    
    _return = _base_return()
    return pd.concat([_return[_return.index.isin(_normal)], _update_return(_change)])




if __name__ == "__main__":
    print(marketCap())
    print(multiple())
    print(ipo())
    print(earningRatio())
