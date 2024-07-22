try:
    from tradingdate import TradingDate
except ImportError:
    from app.common.tradingdate import TradingDate
from datetime import date, datetime, timedelta
from pandas import DataFrame
from pykrx import stock
from requests.exceptions import JSONDecodeError, SSLError
from typing import Union, Iterable
import pandas as pd


def _dateCheck(td:Union[date, datetime, str]=None) -> date:
    if not td:
        return TradingDate.end
    if isinstance(td, date):
        return td
    if isinstance(td, datetime):
        return td.date()
    if isinstance(td, str):
        return datetime.strptime(td, "%Y%m%d")
    raise KeyError(f'Wrong format {td}')    


class marketCap(DataFrame):
    _cols = {'종가':'close', '시가총액':'marketCap', '거래량':'volume', '거래대금':'amount', '상장주식수':'shares'}
    def __init__(self, td:Union[date, datetime, str]=None):
        td = _dateCheck(td).strftime("%Y%m%d")
        try:
            super().__init__(stock.get_market_cap_by_ticker(date=td, market="ALL", alternative=True))
            self.rename(columns=self._cols, inplace=True)
            self.index.name = "ticker"
            return 
        except (JSONDecodeError, SSLError, KeyError):
            super().__init__(columns=self._cols.keys())
            return


class multiple(DataFrame):
    def __init__(self, td:Union[date, datetime, str]=None):
        td = _dateCheck(td).strftime("%Y%m%d")
        try:
            super().__init__(stock.get_market_fundamental(date=td, market="ALL", alternative=True))
            self.index.name = "ticker"
            return 
        except (JSONDecodeError, SSLError, KeyError, RecursionError):
            super().__init__(columns=['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS'])
            return


class ipo(DataFrame):
    _url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    _cols = {'회사명':'name', '종목코드':'ticker', '상장일':'ipo', '주요제품':'products', '결산월':'settlementMonth'}
    def __init__(self, td:Union[date, datetime, str]=None):
        td = _dateCheck(td)
        try:
            super().__init__(pd.read_html(io=self._url, header=0)[0][self._cols.keys()])
            self.rename(columns=self._cols, inplace=True)
        except (KeyError, JSONDecodeError, SSLError):
            super().__init__(columns=self._cols.values())
        self.set_index(keys='ticker', inplace=True)
        self.index = self.index.astype(str).str.zfill(6)
        self.ipo = pd.to_datetime(self.ipo)
        self = self[self.ipo.dt.date <= td]
        return
    

class priceReturn(DataFrame):

    def __init__(self):
        _periods = TradingDate.periods
        try:
            shares = pd.concat(objs=self._shares(_periods), axis=1)
            prices = pd.concat(objs=self._prices(_periods), axis=1)
            shares = shares[~shares['D+0'].isna()]

            static_index = shares[shares['D+0'] == shares['Y-1']].index
            dynamic_index = shares[shares['D+0'] != shares['Y-1']].index
            static_return = pd.concat(objs=self._static_return(prices), axis=1)
            static_return = static_return[static_return.index.isin(static_index)]
            dynamic_return = self._dynamic_return(dynamic_index, _periods)
            super().__init__(pd.concat(objs=[static_return, dynamic_return]))
        except (KeyError, JSONDecodeError, SSLError):
            super().__init__(columns=_periods.keys())
        self.drop(columns=['D+0'], inplace=True)
        self.index.name = 'ticker'
        return

    @staticmethod
    def _shares(periods:dict) -> dict:
        return {
            'D+0': marketCap(periods['D+0'])['shares'],
            'Y-1': marketCap(periods['Y-1'])['shares']
        }

    @staticmethod
    def _prices(periods:dict) -> dict:
        return {
            key: stock.get_market_ohlcv_by_ticker(
                date=date.strftime("%Y%m%d"), 
                market="ALL", 
                alternative=True
            )['종가']
            for key, date in periods.items()
        }

    @staticmethod
    def _static_return(prices:DataFrame) -> dict:
        return {
            key: round(100 * (prices['D+0'] / prices[key] - 1), 2)
            for key in prices
        }
    
    @staticmethod
    def _dynamic_return(tickers:Iterable, periods:dict) -> DataFrame:
        data = []
        for ticker in tickers:
            src = stock.get_market_ohlcv_by_date(
                ticker=ticker, 
                fromdate=(periods['Y-1'] - timedelta(30)).strftime("%Y%m%d"), 
                todate=periods['D+0'].strftime("%Y%m%d"), 
                freq='d', 
                adjusted=True, 
                name_display=False
            )['종가']
            data.append({
                label: round(100 * src.pct_change(periods=dt)[-1], 2)
                for label, dt in [('D-1', 1), ('W-1', 5), ('M-1', 21), ('M-3', 63), ('M-6', 126), ('Y-1', 252)]
            })
        return DataFrame(data, index=tickers)
 



if __name__ == "__main__":
    print(marketCap())
    print(multiple())
    print(ipo())
    # print(priceReturn())
