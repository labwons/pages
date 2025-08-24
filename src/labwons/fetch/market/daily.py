from labwons.logs import fetch_logger as logger
from labwons.util import DATETIME

from datetime import datetime, timedelta
from io import StringIO
from pandas import DataFrame, Series
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
from typing import Iterable
import pandas as pd


pd.set_option('future.no_silent_downcasting', True)
class DailyMarket:

    def __init__(self):
        stime = perf_counter()
        self.status = "FAILED"
        self.fname = "DAILYMARKET"

        logger.info("RUN [FETCH PYKRX DATA]")

        if DATETIME.TRADING is None:
            logger.error(f'- FAILED TO FETCH TRADING DATE')
            return

        try:
            marketCap = get_market_cap_by_ticker(date=DATETIME.TRADING, market='ALL', alternative=True)
            if marketCap.empty:
                raise Exception(f'Empty {{Market Cap}} DataFrame')
            logger.info(f'- SUCCEED IN FETCHING MARKET CAP')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH MARKET CAP: {reason}')
            return

        try:
            multiples = get_market_fundamental(date=DATETIME.TRADING, market='ALL', alternative=True)
            if multiples.empty:
                raise Exception(f'Empty {{Multiples}} DataFrame')
            logger.info(f'- SUCCEED IN FETCHING MULTIPLES')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH MULTIPLES: {reason}')
            return

        try:
            foreignRate = get_exhaustion_rates_of_foreign_investment(date=DATETIME.TRADING, market='ALL')
            if foreignRate.empty:
                raise Exception(f'Empty {{Foreign Rate}} DataFrame')
            logger.info(f'- SUCCEED IN FETCHING FOREIGN EXHAUST RATE')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH FOREIGN EXHAUST RATE: {reason}')
            return

        try:
            ipo = pd.read_html(
                io=StringIO(get('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download').text),
                encoding='euc-kr'
            )[0].set_index(keys='종목코드')
            ipo.index = ipo.index.astype(str).str.zfill(6)
            logger.info(f'- SUCCEED IN FETCHING IPO LIST')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH IPO LIST: {reason}')
            return

        try:
            ks = Series(index=get_market_ticker_list(date=DATETIME.TRADING, market='KOSPI')).fillna('KOSPI')
            kq = Series(index=get_market_ticker_list(date=DATETIME.TRADING, market='KOSDAQ')).fillna('KOSDAQ')
            marketType = pd.concat([ks, kq], axis=0)
            marketType.name = "market"
            logger.info(f'- SUCCEED IN FETCHING MARKET TYPE')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH MARKET TYPE: {reason}')
            return

        try:
            index = get_index_portfolio_deposit_file('2203') + get_index_portfolio_deposit_file('1028')
            largeCap = Series(index=index, data=['largeCap'] * len(index), name='capGroup')
            logger.info(f'- SUCCEED IN FETCHING LARGE CAPS')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH LARGE CAPS: {reason}')
            return

        merged = pd.concat([marketCap, multiples, foreignRate], axis=1)
        merged = merged.loc[:, ~merged.columns.duplicated(keep='first')]

        c_active_ipo = merged.index.isin(ipo.index)
        c_no_konex = ~merged.index.isin(get_market_cap_by_ticker(date=DATETIME.TRADING, market='KONEX').index)
        c_active_trade = merged['거래량'] > 0
        c_market_cap = merged['시가총액'] >= merged['시가총액'].median()

        merged = merged[c_active_ipo & c_no_konex & c_active_trade & c_market_cap]
        merged = merged.join(marketType, how='left')
        if not largeCap.empty:
            merged = merged.join(largeCap, how='left')
        merged.index.name = 'ticker'

        try:
            returns = self.fetchReturns(DATETIME.TRADING, merged.index)
            merged = merged.join(returns, how='left')
            logger.info(f'- SUCCEED IN FETCHING PERIODIC RETURNS')
        except Exception as reason:
            logger.error(f'- FAILED TO FETCH PERIODIC RETURNS: {reason}')
            return

        clock = DATETIME.CLOCK()
        time = "15:30" if clock.hour >= 15 and clock.minute >= 30 else clock.strftime("%H:%M")
        self.data:DataFrame = merged.sort_values(by='시가총액', ascending=False)
        self.data['date'] = f'{DATETIME.TRADING}{time}'
        self.status = "OK"
        logger.info(f'END [FETCH PYKRX DATA] {len(self.data)} ITEMS: {perf_counter() - stime:.2f}s')
        return

    @classmethod
    def fetchReturns(cls, date: str, tickers: Iterable = None) -> DataFrame:
        tdate = datetime.strptime(date, "%Y%m%d")
        intv, objs = {}, {}
        for key, val in {
            'D0': 0,
            'return1Day': 1, 'return1Week': 7,
            'return1Month': 30, 'return2Month': 61,
            'return3Month': 92, 'return6Month': 182, 'return1Year': 365
        }.items():
            fdate = (tdate - timedelta(val)).strftime("%Y%m%d")
            intv[key] = dt = get_nearest_business_day_in_a_week(fdate)
            objs[key] = get_market_cap_by_ticker(date=dt, market='ALL', alternative=True)

        base = pd.concat(objs, axis=1)
        base = base[base.index.isin(tickers)]
        returns = pd.concat({
            dt: base['D0']['종가'] / base[dt]['종가'] - 1 for dt in objs
        }, axis=1)
        returns.drop(columns=['D0'], inplace=True)

        diff = base[base['return1Year']['상장주식수'] != base['D0']['상장주식수']].index
        fdate = (tdate - timedelta(380)).strftime("%Y%m%d")

        ohlc = pd.concat({
            ticker: get_market_ohlcv_by_date(fromdate=fdate, todate=date, ticker=ticker)['종가']
            for ticker in diff
        }, axis=1)

        objs = {}
        for interval in returns.columns:
            ohlc_copy = ohlc[ohlc.index >= intv[interval]]
            _returns = ohlc_copy.iloc[-1] / ohlc_copy.iloc[0] - 1
            objs[interval] = _returns
        returns.update(pd.concat(objs=objs, axis=1))
        return round(100 * returns, 2)


