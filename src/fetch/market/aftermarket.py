from datetime import datetime, timedelta, timezone
from io import StringIO
from pandas import (
    concat,
    DataFrame,
    read_html,
    set_option,
    Series
)
from pykrx.stock import (
    get_exhaustion_rates_of_foreign_investment,
    get_index_portfolio_deposit_file,
    get_market_cap_by_ticker,
    get_market_fundamental,
    get_market_ohlcv_by_date,
    get_market_ticker_list,
    get_nearest_business_day_in_a_week,
)
from requests import get
from time import perf_counter
from typing import Dict, Iterable, List

set_option('future.no_silent_downcasting', True)

INTERVALS: Dict[str, int] = {
    'D0': 0,
    'return1Day': 1, 'return1Week': 7, 'return1Month': 30,
    'return3Month': 91, 'return6Month': 182, 'return1Year': 365
}


class AfterMarket:
    _log: List[str] = []
    state:str = "SUCCESS"
    def __init__(self):
        stime = perf_counter()

        self.log = f'  >> RUN [CACHING AFTER MARKET]'

        date = get_nearest_business_day_in_a_week()
        time = datetime.now(timezone(timedelta(hours=9)))
        time = "15:30" if time.hour >= 15 and time.minute >= 30 else time.strftime("%H:%M")

        try:
            marketCap = get_market_cap_by_ticker(date=date, market='ALL', alternative=True)
            self.log = f'     ... {"FAILED" if marketCap.empty else "Success"} fetching market cap'
        except Exception as reason:
            marketCap = DataFrame()
            self.log = f'     ... FAILED fetching market cap: {reason}'

        try:
            multiples = get_market_fundamental(date=date, market='ALL', alternative=True)
            self.log = f'     ... {"FAILED" if multiples.empty else "Success"} fetching multiples'
        except Exception as reason:
            multiples = DataFrame()
            self.log = f'     ... FAILED fetching multiples: {reason}'

        try:
            foreignRate = get_exhaustion_rates_of_foreign_investment(date=date, market='ALL')
            self.log = f'     ... {"FAILED" if foreignRate.empty else "Success"} fetching foreign rate'
        except Exception as reason:
            foreignRate = DataFrame()
            self.log = f'     ... FAILED fetching foreign rate: {reason}'

        try:
            ipo = read_html(
                io=StringIO(get('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download').text),
                encoding='euc-kr'
            )[0].set_index(keys='종목코드')
            ipo.index = ipo.index.astype(str).str.zfill(6)
            self.log = f'     ... {"FAILED" if ipo.empty else "Success"} fetching ipo list'
        except Exception as reason:
            ipo = DataFrame()
            self.log = f'     ... FAILED fetching ipo list: {reason}'

        try:
            ks = Series(index=get_market_ticker_list(date=date, market='KOSPI')).fillna('KOSPI')
            kq = Series(index=get_market_ticker_list(date=date, market='KOSDAQ')).fillna('KOSDAQ')
            marketType = concat([ks, kq], axis=0)
            marketType.name = "market"
            self.log = f'     ... {"FAILED" if marketType.empty else "Success"} fetching market type'
        except Exception as reason:
            marketType = DataFrame()
            self.log = f'     ... FAILED fetching market type: {reason}'

        try:
            index = get_index_portfolio_deposit_file('2203') + get_index_portfolio_deposit_file('1028')
            largeCap = Series(index=index, data=['largeCap'] * len(index), name='capGroup')
            self.log = f'     ... "Success" fetching largecaps'
        except Exception as reason:
            largeCap = Series()
            self.log = f'     ... FAILED fetching large caps: {reason}'

        merged = concat([marketCap, multiples, foreignRate], axis=1)
        merged = merged.loc[:, ~merged.columns.duplicated(keep='first')]

        c_active_ipo = merged.index.isin(ipo.index)
        c_no_konex = ~merged.index.isin(get_market_cap_by_ticker(date=date, market='KONEX').index)
        c_active_trade = merged['거래량'] > 0
        c_market_cap = merged['시가총액'] >= merged['시가총액'].median()

        merged = merged[c_active_ipo & c_no_konex & c_active_trade & c_market_cap]
        merged = merged.join(marketType, how='left')
        if not largeCap.empty:
            merged = merged.join(largeCap, how='left')
        merged.index.name = 'ticker'

        try:
            returns = self.fetchReturns(date, merged.index)
            merged = merged.join(returns, how='left')
            self.log = f'     ... {"FAILED" if returns.empty else "Success"} fetching returns'
        except Exception as reason:
            self.log = f'     ... FAILED fetching returns: {reason}'
        self.data = merged = merged.sort_values(by='시가총액', ascending=False)
        self.data['date'] = f'{date}{time}'

        self.log = f'  >> End: {perf_counter() - stime:.2f}s'
        self._log[0] += f': {len(self.data)} items'
        if "FAILED" in self.log:
            self.state = "PARTIALLY FAILED"
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @classmethod
    def fetchReturns(cls, date: str, tickers: Iterable = None) -> DataFrame:
        tdate = datetime.strptime(date, "%Y%m%d")
        intv, objs = {}, {}
        for key, val in INTERVALS.items():
            fdate = (tdate - timedelta(val)).strftime("%Y%m%d")
            intv[key] = dt = get_nearest_business_day_in_a_week(fdate)
            objs[key] = get_market_cap_by_ticker(date=dt, market='ALL', alternative=True)

        base = concat(objs, axis=1)
        base = base[base.index.isin(tickers)]
        returns = concat({
            dt: base['D0']['종가'] / base[dt]['종가'] - 1 for dt in objs
        }, axis=1)
        returns.drop(columns=['D0'], inplace=True)

        diff = base[base['return1Year']['상장주식수'] != base['D0']['상장주식수']].index
        fdate = (tdate - timedelta(380)).strftime("%Y%m%d")

        ohlc = concat({
            ticker: get_market_ohlcv_by_date(fromdate=fdate, todate=date, ticker=ticker)['종가']
            for ticker in diff
        }, axis=1)

        objs = {}
        for interval in returns.columns:
            ohlc_copy = ohlc[ohlc.index >= intv[interval]]
            _returns = ohlc_copy.iloc[-1] / ohlc_copy.iloc[0] - 1
            objs[interval] = _returns
        returns.update(concat(objs=objs, axis=1))
        return round(100 * returns, 2)


if __name__ == "__main__":
    afterMarket = AfterMarket()

    print(afterMarket.log)

