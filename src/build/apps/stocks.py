try:
    from ...common.env import FILE, dDict
    from ...common.util import krw2currency, str2num
    from ...fetch.stock.krx import PyKrx
except ImportError:
    from src.common.env import FILE, dDict
    from src.common.util import krw2currency, str2num
    from src.fetch.stock.krx import PyKrx
from json import dumps
from pandas import DataFrame, Series, DateOffset
from pandas import concat, read_parquet
from time import perf_counter
from typing import List


# from ta import

class Stocks:

    _log: List[str] = []
    def __init__(self):
        self.basis = basis = read_parquet(FILE.BASELINE, engine='pyarrow')
        self.price = price = read_parquet(FILE.PRICE, engine='pyarrow')
        self.astat = astat = read_parquet(FILE.ANNUAL_STATEMENT, engine='pyarrow')
        # self.qstat = qstat = read_parquet(FILE.QUARTER_STATEMENT, engine='pyarrow')
        tickers = price.columns.get_level_values(0).unique()
        xrange = [price.index[-1] - DateOffset(months=6), price.index[-1]]
        self.xrange = [x.strftime("%Y-%m-%d") for x in xrange]

        __mem__ = dDict()
        for ticker in tickers:
            if not ticker in basis.index:
                self.log = f'     ...TICKER NOT FOUND IN BASELINE: {ticker}'
                continue
            general = basis.loc[ticker]
            ohlcv = price[ticker].dropna().astype(int)
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3

            annual = astat[ticker]
            cap = PyKrx(ticker).getMarketCap()

            __mem__[ticker] = dDict(
                name=general['name'],
                date=ohlcv.index.astype(str).tolist(),
                ohlcv=self.convertOhlcv(ohlcv),
                sma=self.convertSma(typical),
                bollinger=self.convertBollinger(typical),
                sales_y=self.convertAnnualSales(annual, cap)
            )
        self.__mem__ = __mem__
        return

    def __iter__(self):
        for ticker, attr in self.__mem__:
            yield ticker, attr

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    def update(self, *tickers):
        self._log = [f'  >> RUN [CACHING STOCK PRICE]: ']
        stime = perf_counter()
        objs = {}
        for ticker in tickers:
            if not ticker:
                continue
            try:
                objs[ticker] = PyKrx(ticker).ohlcv
            except Exception as reason:
                self.log = f'     ...FAILED TO FETCH PRICE: {ticker} / {reason}'

        if objs:
            self.price = concat(objs, axis=1)
        self._log[0] += f'{len(tickers):,d} items @{self.price.index.astype(str).values[-1]}'.replace("-", "/")
        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return

    @classmethod
    def convertOhlcv(cls, ohlcv:DataFrame) -> str:
        obj = {
            'open': ohlcv['open'],
            'high': ohlcv['high'],
            'low': ohlcv['low'],
            'close': ohlcv['close'],
            'volume': ohlcv['volume'],
        }
        for key in obj:
            obj[key] = obj[key].tolist()
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertSma(cls, typical:Series) -> str:
        obj = {
            'sma5': typical.rolling(5).mean(),
            'sma20': typical.rolling(20).mean(),
            'sma60': typical.rolling(60).mean(),
            'sma120': typical.rolling(120).mean(),
            'sma200': typical.rolling(200).mean(),
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertBollinger(cls, typical:Series) -> str:
        obj = {
            'upper': typical.rolling(20).mean() + 2 * typical.rolling(20).std(),
            'upperTrend': typical.rolling(20).mean() + 1 * typical.rolling(20).std(),
            'middle': typical.rolling(20).mean(),
            'lower': typical.rolling(20).mean() - 2 * typical.rolling(20).std(),
            'lowerTrend': typical.rolling(20).mean() - 1 * typical.rolling(20).std(),
            'width': 100 * 4 * typical.rolling(20).std() / typical.rolling(20).mean()
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertAnnualSales(cls, statement:DataFrame, marketcap:DataFrame) -> str:
        sales = statement[statement.columns.tolist()[:3] + ['영업이익률(%)']].dropna(how='all')
        if len(sales.index) > 6:
            sales = sales.iloc[:6]
        sales = sales.map(str2num)
        columns = sales.columns
        settleMonth = sales.index[0].split("/")[-1]
        if not marketcap.empty:
            marketcap = marketcap[
                marketcap.index.astype(str).str.contains(settleMonth) | \
                (marketcap.index == marketcap.index[-1])
            ]
            marketcap.index = marketcap.index.strftime("%Y/%m")
            if "(" in sales.index[-1]:
                marketcap = marketcap.rename(index={marketcap.index[-1]:sales.index[-1]})
            marketcap = marketcap[marketcap.index.isin(sales.index)]
            marketcap = Series(index=marketcap.index, data=marketcap['시가총액'] / 1e8, dtype=int)
            try:
                sales = concat([marketcap, sales], axis=1)
            except Exception:
                print("오류")
                print(sales)
                print(marketcap)
            sales = sales.iloc[-6:]
        e_sales = 1e8 * sales
        obj = {
            'index': sales.index.tolist(),
            'sales': sales[columns[0]].tolist(),
            'salesLabel': columns[0].replace("(억원)", ""),
            'salesText': [krw2currency(v) for v in e_sales[columns[0]]],
            'profit': sales[columns[1]].tolist(),
            'profitLabel': columns[1].replace("(억원)", ""),
            'profitText': [krw2currency(v) for v in e_sales[columns[1]]],
            'netProfit': sales[columns[2]].tolist(),
            'netProfitLabel': columns[2].replace("(억원)", ""),
            'netProfitText': [krw2currency(v) for v in e_sales[columns[2]]],
            'profitRate': sales['영업이익률(%)'].tolist(),
            'profitRateLabel': '영업이익률(%)'
        }
        if not marketcap.empty:
            obj['marketcap'] = sales['시가총액'].tolist()
            obj['marketcapLabel'] = '시가총액'
            obj['marketcapText'] = [krw2currency(v) for v in e_sales['시가총액']]
            obj['marketcapText'][-1] = f"{obj['marketcapText'][-1]}(최근)"
        return dumps(obj).replace("NaN", "null")


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    stocks = Stocks()
    for t, stock in stocks:
        print(t)
        print(stock.sales_y)
