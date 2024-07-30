try:
    from ..market.date import TradingDate
except ImportError:
    from app.market.date import TradingDate
from datetime import date, datetime, timedelta
from pandas import DataFrame
from pykrx import stock
from requests.exceptions import JSONDecodeError, SSLError
from typing import Dict, List, Union, Iterable
import pandas as pd


def marketCap(td:Union[date, datetime, str]=None) -> DataFrame:
    _cols_ = {'종가':'close', '시가총액':'marketCap', 
              '거래량':'volume', '거래대금':'amount', '상장주식수':'shares'}
    date = TradingDate(td) if td else f'{TradingDate}'
    try:
        _get_ = stock \
                .get_market_cap_by_ticker(
                    date=date, 
                    market="ALL", 
                    alternative=True
                )
        _get_.rename(columns=_cols_, inplace=True)
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_)
    _get_.index.name = "ticker"
    return _get_

def multiple(td:Union[date, datetime, str]=None) -> DataFrame:
    _cols_ = ['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']
    date = TradingDate(td) if td else f'{TradingDate}'
    try:
        _get_ = stock \
                .get_market_fundamental(
                    date=date, 
                    market="ALL", 
                    alternative=True
                )
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_)
    _get_.index.name = "ticker"
    return _get_

def ipo(td:Union[date, datetime, str]=None) -> DataFrame:
    _url_ = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    _cols_ = {'회사명':'name', '종목코드':'ticker', 
              '상장일':'ipo', '주요제품':'products', '결산월':'settlementMonth'}
    _date_ = TradingDate(td)
    try:
        _get_ = pd.read_html(io=_url_, header=0)[0][_cols_.keys()]
        _get_.rename(columns=_cols_, inplace=True)
    except (KeyError, RecursionError, JSONDecodeError, SSLError):
        _get_ = DataFrame(columns=_cols_.values())
    _get_.set_index(keys='ticker', inplace=True)
    _get_.index = _get_.index.astype(str).str.zfill(6)
    _get_['ipo'] = pd.to_datetime(_get_['ipo'])
    return _get_[_get_['ipo'].dt.date <= td]

def earningRate(periods:Dict[str, date]) -> DataFrame:
    def _base_return() -> DataFrame:
        _objs = {}
        _base = stock.get_market_ohlcv_by_ticker(date=periods['D+0'].strftime("%Y%m%d"), market="ALL")['종가']
        for key, dt in periods.items():
            _fetch = stock.get_market_ohlcv_by_ticker(date=dt.strftime("%Y%m%d"), market="ALL")['종가']
            _objs[key] = round(100 * (_base / _fetch - 1), 2)
        return pd.concat(objs=_objs, axis=1)
    
    def _update_return(tickers:Iterable) -> DataFrame:
        fromdate, todate = (periods['Y-1'] - timedelta(30)).strftime("%Y%m%d"), periods['D+0'].strftime("%Y%m%d")
        data = []
        for ticker in tickers:
            src = stock.get_market_ohlcv_by_date(ticker=ticker, fromdate=fromdate, todate=todate)['종가']
            data.append({
                label: round(100 * src.pct_change(periods=dt)[-1], 2)
                for label, dt in [('D-1', 1), ('W-1', 5), ('M-1', 21), ('M-3', 63), ('M-6', 126), ('Y-1', 252)]
            })
        return DataFrame(data, index=tickers)

    _shares = pd.concat({dt: marketCap(periods[dt])['shares'] for dt in ['D+0', 'Y-1']}, axis=1)
    _shares = _shares[~_shares['D+0'].isna()]
    _normal = _shares[_shares['D+0'] == _shares['Y-1']].index
    _change = _shares[_shares['D+0'] != _shares['Y-1']].index
    
    _return = _base_return()
    return pd.concat([_return[_return.index.isin(_normal)], _update_return(_change)])

def largeCaps(self) -> List[str]:
    return stock.get_index_portfolio_deposit_file('1028') + \
           stock.get_index_portfolio_deposit_file('2203')


if __name__ == "__main__":
    print(marketCap())
    print(multiple())
    print(ipo())
    print(earningRate())
