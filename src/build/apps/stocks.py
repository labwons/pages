try:
    from ...common.env import FILE, dDict
    from ...common.util import krw2currency, str2num
    from ...fetch.stock.krx import PyKrx
except ImportError:
    from src.common.env import FILE, dDict
    from src.common.util import krw2currency, str2num
    from src.fetch.stock.krx import PyKrx
from datetime import timedelta
from json import dumps
from pandas import DataFrame, Series, DateOffset
from pandas import concat, read_parquet, to_datetime, isna
from requests.exceptions import ConnectionError
from scipy.stats import linregress
from ta.trend import MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from time import perf_counter
from typing import List


class UpdateStockPrice(DataFrame):
    _log: List[str] = []
    def __init__(self, *tickers):
        super().__init__()

        self.log = f'  >> RUN [CACHING STOCK PRICE]: '
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
            super().__init__(concat(objs, axis=1))

        self._log[0] += f'{len(self.columns):,d} items @{self.index.astype(str).values[-1]}'.replace("-", "/")
        self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)


class Stocks:

    _log: List[str] = []
    def __init__(self):
        stime = perf_counter()
        self.log = f'  >> BUILD [STOCK]: '
        self.basis = basis = read_parquet(FILE.BASELINE, engine='pyarrow')
        self.price = price = read_parquet(FILE.PRICE, engine='pyarrow')
        self.astat = astat = read_parquet(FILE.ANNUAL_STATEMENT, engine='pyarrow')
        self.qstat = qstat = read_parquet(FILE.QUARTER_STATEMENT, engine='pyarrow')

        tickers = price.columns.get_level_values(0).unique()
        xrange = [
            price[price.index >= (price.index[-1] - DateOffset(months=6))].index[0],
            to_datetime(price.index[-1])
        ]

        __mem__ = dDict()
        for ticker in tickers:
            if not ticker in basis.index:
                self.log = f'     ...TICKER NOT FOUND IN BASELINE: {ticker}'
                continue
            general = basis.loc[ticker]
            ohlcv = price[ticker].dropna().astype(int)
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3
            trend = self.calcTrend(typical)
            annual = astat[ticker]
            quarter = qstat[ticker]
            try:
                cap = PyKrx(ticker).getMarketCap()
            except ConnectionError:
                cap = DataFrame()

            __mem__[ticker] = dDict(
                name=general['name'],
                date=ohlcv.index.astype(str).tolist(),
                xrange=[ohlcv.index.get_loc(xrange[0]), len(ohlcv) - 1],
                ohlcv=self.convertOhlcv(ohlcv),
                sma=self.convertSma(typical),
                bollinger=self.convertBollinger(typical),
                trend=self.convertTrend(trend),
                macd=self.convertMacd(typical),
                rsi=self.convertRsi(typical),
                sales_y=self.convertSales(annual, cap),
                sales_q=self.convertSales(quarter, cap),
                asset=self.convertAsset(annual, quarter),
                pers=self.convertPer(general)
            )
            __mem__[ticker].deviation = self.convertDeviation(typical, trend)
        self.__mem__ = __mem__

        self._log[0] += f'{len(tickers):,d} items @{price.index.astype(str).values[-1]}'.replace("-", "/")
        self.log = f'  >> BUILD END: {perf_counter() - stime:.2f}s'
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

    @classmethod
    def calcTrend(cls, typical:Series) -> DataFrame:
        def _regression(subdata: Series, newName: str = '') -> Series:
            newName = newName if newName else subdata.name
            subdata.index.name = 'date'
            subdata = subdata.reset_index(level=0)
            xrange = (subdata['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

            slope, intercept, _, _, _ = linregress(x=xrange, y=subdata[subdata.columns[-1]])
            fitted = slope * xrange + intercept
            fitted.name = newName
            return concat(objs=[subdata, fitted], axis=1).set_index(keys='date')[fitted.name]

        objs = [_regression(typical, '10년')]
        for yy in [5, 2, 1, 0.5, 0.25]:
            col = f"{yy}년" if isinstance(yy, int) else f"{int(yy * 12)}개월"
            date = typical.index[-1] - timedelta(int(yy * 365))
            if typical.index[0] > date:
                objs.append(Series(name=col, index=typical.index))
            else:
                objs.append(_regression(typical[typical.index >= date], col))
        return concat(objs, axis=1)

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
            # 'width': 100 * 4 * typical.rolling(20).std() / typical.rolling(20).mean()
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertTrend(cls, trend:DataFrame) -> str:
        obj = {}
        for col in trend:
            series = trend[col].dropna()
            obj[col] = {
                'x': 'srcDate' if col == "10년" else  series.index.strftime("%Y-%m-%d").tolist(),
                'y': round(series, 1).tolist()
            }
        return dumps(obj).replace(" ", "").replace("NaN", "null").replace('"srcDate"', 'srcDate')

    @classmethod
    def convertMacd(cls, typical:Series):
        macd = MACD(close=typical)
        obj ={
            'macd': macd.macd().tolist(),
            'signal': macd.macd_signal().tolist(),
            'diff': macd.macd_diff().tolist()
        }
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertRsi(cls, typical:Series):
        rsi = RSIIndicator(close=typical)
        obj = {
            'rsi': rsi.rsi().tolist()
        }
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertSales(cls, statement:DataFrame, marketcap:DataFrame) -> str:
        sales = statement[statement.columns.tolist()[:3] + ['영업이익률(%)']].dropna(how='all')
        sales = sales.map(str2num)
        sales = sales.sort_index()
        for n, date in enumerate(sales.index):
            if "(" in date:
                sales = sales.iloc[:n + 1]
                if len(sales) > 5:
                    sales = sales.iloc[-5:]
        if not "(" in sales.index[-1]:
            if len(sales) > 4:
                sales = sales.iloc[-4:]

        columns = sales.columns
        if not marketcap.empty:
            marketcap.index = to_datetime(marketcap.index).strftime("%Y/%m")
            marketcap = marketcap[marketcap.index.isin(sales.index) | (marketcap.index == marketcap.index[-1])]
            if "(" in sales.index[-1]:
                marketcap = marketcap.rename(index={marketcap.index[-1]:sales.index[-1]})

            marketcap = Series(index=marketcap.index, data=marketcap['시가총액'] / 1e8, dtype=int)
            sales = concat([marketcap, sales], axis=1)

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
            obj['marketcapText'][-1] = f"(현재){obj['marketcapText'][-1]}"
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertAsset(cls, a:DataFrame, q:DataFrame) -> str:
        cols = ['자산총계(억원)', '부채총계(억원)', '자본총계(억원)', '부채비율(%)']
        def _asset(_df_:DataFrame) -> DataFrame:
            _df_ = _df_[cols]
            _df_.columns = [col.replace("(억원)", "") for col in _df_]
            return _df_.dropna(how='all')

        a_asset = _asset(a)
        a_asset = a_asset[~a_asset.index.str.endswith("(E)")]
        q_asset = _asset(q)
        if q_asset.index[-1] == a_asset.index[-1]:
            asset = a_asset
        else:
            asset = concat([a_asset, q_asset.iloc[[-1]]], axis=0)
        asset = asset.iloc[-5:].map(str2num)
        obj = {
            "index": asset.index.tolist(),
            "asset": asset["자산총계"].tolist(),
            "assetText": [krw2currency(1e8 * v) for v in asset["자산총계"]],
            "capital": asset["자본총계"].tolist(),
            "capitalText": [krw2currency(1e8 * v) for v in asset["자본총계"]],
            "debt": asset["부채총계"].tolist(),
            "debtText": [krw2currency(1e8 * v) for v in asset["부채총계"]],
            "debtRatio": asset['부채비율(%)'].tolist()
        }
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertDeviation(cls, typical:Series, trend:DataFrame) -> str:
        df = concat([typical, trend], axis=1)
        objs = {}
        for col in df.columns[1:]:
            align = df[[df.columns[0], col]].dropna(how='all')
            if align.empty:
                objs[col] = align
                continue
            avg = (abs(align[df.columns[0]] - align[col]).sum() / len(align))
            objs[col] = (align[df.columns[0]] - align[col]) / avg
        dev = concat(objs=objs, axis=1)
        obj = {}
        for col in dev:
            data = dev[col].dropna()
            if data.empty:
                obj[col] = {'empty': 'true'}
            obj[col] = {
                'date': data.index.strftime("%Y-%m-%d").tolist(),
                'data': data.tolist(),
                'empty': 'false'
            }
        return dumps(obj).replace("NaN", "null")

    def convertPer(self, baseline:Series) -> str:
        y = []
        text = []
        meta = []

        if isna(baseline["fiscalPE"]):
            y.append(0)
            text.append("적자" if baseline["fiscalEps"] <= 0 else "미제공")
        else:
            y.append(float(baseline["fiscalPE"]))
            text.append(f'{float(baseline["fiscalPE"])}')
        meta.append(f'직전회계연도({baseline["fiscalDate"]}) EPS 대비 종가')

        if isna(baseline["trailingPE"]):
            y.append(0)
            text.append("적자" if baseline["trailingEps"] <= 0 else "미제공")
        else:
            y.append(round(baseline["trailingPE"], 2))
            text.append(f'{round(baseline["trailingPE"], 2)}')
        meta.append(f'4분기연속EPS합산 대비 현재가(종가)')

        if isna(baseline["estimatedPE"]):
            y.append(0)
            if baseline["estimatedEps"] <= 0:
                text.append("적자")
                meta.append(f'추정회계연도({baseline["estimatedDate"].replace("(E)", "")}) EPS 대비 현재가(종가)')
            else:
                text.append("미제공")
                meta.append(f'증권사 추정치 미제공')
        else:
            y.append(round(baseline["estimatedPE"], 2))
            text.append(f'{round(baseline["estimatedPE"], 2)}')
            meta.append(f'추정회계연도({baseline["estimatedDate"].replace("(E)", "")}) EPS 대비 현재가(종가)')

        if isna(baseline["weightedAverageEps"]):
            y.append(0)
            text.append("적자" if baseline["weightedAverageEps"] <= 0 else "미제공")
        else:
            y.append(float(round(baseline["close"] / baseline["weightedAverageEps"], 2)))
            text.append(f'{float(round(baseline["close"] / baseline["weightedAverageEps"], 2))}')
        meta.append(f'{int(baseline["numberOfAnnualStatement"])}개 회계연도의 EPS 가중 평균 대비 현재가(종가)')

        y.append(round(self.basis[self.basis["industryCode"] == baseline["industryCode"]]["trailingPE"].mean(), 2))
        text.append(f'{y[-1]}')
        meta.append(f'{baseline["industryName"]} 업종 4분기연속 PE에 대한 평균')

        obj = {
            "x": ["직전회계연도PE", "4분기연속PE", "추정PE", "가중평균PE", "업종평균PE"],
            "y": y,
            "text": text,
            "meta": meta
        }
        return dumps(obj).replace("NaN", "null")


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    stocks = Stocks()
    # for t, stock in stocks:
    #     print(t)
    #     print(stock.trend)
