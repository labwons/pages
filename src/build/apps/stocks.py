try:
    from ...common.env import FILE, dDict
    from ...common.util import krw2currency, str2num
    from ...fetch.stock.fnguide import fnguide
except ImportError:
    from src.common.env import FILE, dDict
    from src.common.util import krw2currency, str2num
    from src.fetch.stock.fnguide import fnguide
from datetime import timedelta
from json import dumps
from pandas import DataFrame, Series, DateOffset
from pandas import concat, read_parquet, to_datetime, isna
from scipy.stats import linregress
from ta.trend import MACD
from ta.momentum import RSIIndicator
from time import perf_counter
from typing import List



class Stocks:

    _log: List[str] = []
    def __init__(self):
        stime = perf_counter()
        self.log = f'  >> BUILD [STOCK]: '
        self.basis = basis = read_parquet(FILE.BASELINE, engine='pyarrow')
        self.price = price = read_parquet(FILE.PRICE, engine='pyarrow')
        self.mcap = mcap = read_parquet(FILE.MARKET_CAP, engine='pyarrow')
        self.band = band = read_parquet(FILE.PER_BAND, engine='pyarrow')
        self.foreignRage = foreignRate = read_parquet(FILE.FOREIGN_RATE, engine='pyarrow')
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
            fng = fnguide(ticker)
            try:
                product = self.convertProduct(fng.products)
            except Exception as reason:
                product = 'null'
                self.log = f'     ...PRODUCT FOR: {ticker} NOT FOUND: {reason}'
            general = basis.loc[ticker]
            ohlcv = price[ticker].dropna().astype(int)
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3
            monthlyClose = ohlcv["close"].resample('M').nearest()
            monthlyClose.index = monthlyClose.index.strftime("%Y/%m")
            annualClose = monthlyClose[
                monthlyClose.index.str.endswith('/12') | \
                (monthlyClose.index == monthlyClose.index[-1])
            ].rename(index={monthlyClose.index[-1]:f'{monthlyClose.index[-1][:4]}/현재'})

            trend = self.calcTrend(typical)
            annual = astat[ticker].map(str2num)
            quarter = qstat[ticker].map(str2num)
            cap = mcap[ticker]
            multipleBand = band[ticker] if ticker in band else DataFrame()
            foreignExhaustRate = foreignRate[ticker] if ticker in foreignRate else DataFrame()

            __mem__[ticker] = dDict(
                name=general['name'],
                date=ohlcv.index.astype(str).tolist(),
                spec=self.convertOverview(general),
                xrange=[ohlcv.index.get_loc(xrange[0]), len(ohlcv) - 1],
                ohlcv=self.convertOhlcv(ohlcv),
                sma=self.convertSma(typical),
                bollinger=self.convertBollinger(typical),
                envelope=self.convertEnvelope(ohlcv, typical),
                trend=self.convertTrend(trend),
                macd=self.convertMacd(typical),
                rsi=self.convertRsi(typical),
                # deviation=self.convertDeviation(typical, trend),
                sales_y=self.convertSales(annual, cap),
                sales_q=self.convertSales(quarter, cap),
                asset=self.convertAsset(annual, quarter),
                growth=self.convertGrowth(annual),
                per=self.convertPer(general),
                pbr=self.convertPbr(annual, general),
                div=self.convertDiv(annual, general),
                peg = self.convertPeg(annual, general, annualClose),
                perBand=self.convertPerBand(multipleBand, general),
                foreignRate=self.convertForeignRate(foreignExhaustRate, general),
                product=product
            )
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
    def convertEnvelope(cls, ohlcv:DataFrame, typical:Series) -> str:
        ma = typical.rolling(window=20).mean()
        adr = (ohlcv["high"] - ohlcv["low"]).rolling(window=14).mean()
        pct = 6 # [%]
        obj = {
            'adr': adr,
            # 'upper': ma + 1.5 * adr,
            # 'lower': ma - 1.5 * adr
            'upper': ma * (1 + pct / 100),
            'lower': ma * (1 - pct / 100)
        }
        for key in obj:
            obj[key] = round(obj[key], 1).tolist()
        return  dumps(obj).replace(" ", "").replace("NaN", "null")

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
            'macd': round(macd.macd(), 1).tolist(),
            'signal': round(macd.macd_signal(), 1).tolist(),
            'diff': round(macd.macd_diff(), 1).tolist()
        }
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertRsi(cls, typical:Series):
        rsi = RSIIndicator(close=typical)
        obj = {
            'rsi': round(rsi.rsi(), 1).tolist()
        }
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertSales(cls, statement:DataFrame, marketcap:DataFrame) -> str:
        sales = statement[statement.columns.tolist()[:3] + ['영업이익률(%)']].dropna(how='all')
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
        asset = asset.iloc[-5:]
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
    def convertGrowth(cls, a:DataFrame) -> str:
        yy = a.copy()
        yy = yy[yy.columns[:2].tolist() + ['EPS(원)']]
        yy = yy.dropna(how='all', axis=0)
        est = yy[yy.index.str.endswith('(E)')]
        yy = yy.drop(index=est.index)
        if not est.empty:
            yy = concat([yy, est.iloc[[0]]], axis=0)
        yy = round(100 * yy.pct_change().dropna(how='all', axis=0), 2)
        obj = {
            "date": yy.index.tolist(),
            "revenue": yy[yy.columns[0]].tolist(),
            "profit": yy[yy.columns[1]].tolist(),
            "eps": yy[yy.columns[2]].tolist(),
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
                'date': 'srcDate' if col == "10년" else f'srcTrend["{col}"].x',
                'data': round(data, 2).tolist(),
                'empty': 'false'
            }
        return dumps(obj).replace(" ", "").replace("NaN", "null") \
                         .replace('"srcDate"', 'srcDate') \
                         .replace('"srcTrend', 'srcTrend') \
                         .replace('].x"', '].x') \
                         .replace('\\"', '"')

    @classmethod
    def convertPerBand(cls, perBand:DataFrame, general:Series) -> str:
        if perBand.empty:
            return "null"

        perBand.index = perBand.index.strftime("%Y-%m-%d")
        perBand.loc[str(general["date"])] = [int(general["close"])] + [None] * (len(perBand.columns) - 1)
        perBand = perBand.sort_index()
        obj = {'x': perBand.index.tolist()}
        obj.update({col: perBand[col].dropna().tolist() for col in perBand})
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertForeignRate(cls, foreignRate:DataFrame, general:Series) -> str:
        if foreignRate.empty:
            return "null"
        obj = {}
        for col in foreignRate:
            date, name = col
            if not date in obj:
                obj[date] = {}
            obj[date]['x'] = foreignRate[col].dropna().index.strftime("%Y-%m-%d").tolist()
            obj[date][name] = foreignRate[col].dropna().tolist()
            if not str(general["date"]) in obj[date]['x']:
                obj[date]['x'].append(str(general["date"]))
                if "종가" in name:
                    obj[date][name].append(int(general["close"]))
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertPbr(cls, yy:DataFrame, general:Series) -> str:
        yy = yy.dropna(how='all', axis=0)[['PBR(배)', 'BPS(원)']]
        est = yy[yy.index.str.endswith('(E)')]
        yy = yy.drop(index=est.index)
        yy.loc[f'{general["date"][:4]}/현재'] = [general["close"]/general["recentBPS"], general["recentBPS"]]
        yy = yy.iloc[-4:]
        if not est.empty:
            yy.loc[est.index.values[0]] = [general["close"]/est.iloc[0]['BPS(원)'], est.iloc[0]['BPS(원)']]
        obj = {
            'x': yy.index.tolist(),
            'pbr': yy['PBR(배)'].tolist(),
            'bps': yy['BPS(원)'].tolist()
        }
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertDiv(cls, yy:DataFrame, general:Series) -> str:
        yy = yy.dropna(how='all', axis=0)[['배당수익률(%)', 'DPS(원)']]
        est = yy[yy.index.str.endswith('(E)')]
        yy = yy.drop(index=est.index)
        if not est.empty:
            yy.loc[est.index.values[0]] = [round(100 * est.iloc[0]['DPS(원)']/general["close"], 2), est.iloc[0]['DPS(원)']]

        obj = {
            'x': yy.index.tolist(),
            'div': yy['배당수익률(%)'].tolist(),
            'dps': yy['DPS(원)'].tolist(),
            'meta': ('배당수익률: ' + yy['배당수익률(%)'].astype(str) + '%').tolist(),
        }
        if not est.empty:
            obj['meta'][-1] += '<br>* 최근 종가 대비 추정 DPS'
        return dumps(obj).replace("NaN", "null")

    @classmethod
    def convertPeg(cls, yy:DataFrame, general:Series, price:Series):
        yy = yy.dropna(how='all', axis=0)
        est = yy[yy.index.str.endswith('(E)')]
        yy = yy.drop(index=est.index)

        pe = yy["PER(배)"]
        epsR = 100 * yy["EPS(원)"].pct_change().shift(-1)
        recp = concat([pe, epsR], axis=1)
        if not est.empty:
            recp.iloc[-1, -1] = 100 * (est.iloc[0]['EPS(원)'] - yy.iloc[-1]['EPS(원)']) / yy.iloc[-1]['EPS(원)']
        recp["PEG"] = recp.apply(lambda r: r["PER(배)"]/r["EPS(원)"] if r["EPS(원)"] > 0 else None, axis=1)
        recp.loc[f'{general["date"][:4]}/현재'] = [general["trailingPE"], general["estimatedEpsGrowth"], general["PEG"]]
        recp = round(recp.iloc[-5:], 2)

        recp["적자"] = recp["PER(배)"].apply(lambda x: "적자" if isna(x) else "")
        recp["성장"] = recp["EPS(원)"].apply(lambda x: "미제공" if isna(x) else "역성장" if x <= 0 else "")

        text = []
        for n, r in recp.iterrows():
            if not isna(r["PEG"]):
                text.append(r["PEG"])
            else:
                if r["적자"] and r["성장"]:
                    text.append(f'{r["적자"]}/{r["성장"]}')
                else:
                    text.append(f'{r["적자"]}{r["성장"]}')

        recp['text'] = text
        recp = recp.join(price)
        obj = {
            'x': recp.index.tolist(),
            'peg': recp["PEG"].tolist(),
            'text': recp['text'].tolist(),
            'close': recp['close'].tolist()
        }
        return dumps(obj).replace("NaN", "null")


    @classmethod
    def convertProduct(cls, product: DataFrame) -> str:
        product = product.iloc[-1]
        product = product[product != 0]
        etc = product[product.index.str.contains("기타(계)")]
        if len(etc) == 1 and etc.sum() < 0:
            product.drop(labels=etc.index, inplace=True)
            product = product + (etc.sum() / len(product))
            product = round(product, 2)
            diff = round((100 - product.sum()), 2)
            if diff > 0:
                product.iloc[0] += diff
            else:
                product.iloc[0] -= diff
        if (len(etc) > 1) or (product.sum() != 100):
            return "null"
        obj = {'label': product.index.tolist(), 'value': product.values.tolist()}
        return dumps(obj).replace(" ", "").replace("NaN", "null")

    @classmethod
    def convertOverview(cls, baseline:Series) -> dict:
        obj = {
            'sector':  f'{baseline["sectorName"]}',
            'industry': f'{baseline["industryName"]}',
            'close': f'{baseline["close"]:,d}원',
            'marketCap': f'{krw2currency(baseline["marketCap"])}원',
            'volume': f'{baseline["volume"]:,d}주',
            'foreignRate': f'{baseline["foreignRate"]:.2f}%',
            'revenueType': f'{baseline["revenueType"]}',
            'revenue': f'{krw2currency(1e8 * baseline["trailingRevenue"])}원',
            'profit': f'{krw2currency(1e8 * baseline["trailingProfit"])}원',
            'profitRate': f'{baseline["trailingProfitRate"]:.2f}%',
            'estProfitRate': f'{baseline["estimatedProfitRate"]:.2f}%',
            'h52': f'{int(baseline["fiftyTwoWeekHigh"]):,d}원',
            'l52': f'{int(baseline["fiftyTwoWeekLow"]):,d}원',
            'return1Day': f'{"▼" if baseline["return1Day"] < 0 else "▲"}{baseline["return1Day"]:.2f}%',
            'color1Day': '#1861A8' if baseline["return1Day"] < 0 else '#C92A2A',
            'return1Week': f'{"▼" if baseline["return1Week"] < 0 else "▲"}{baseline["return1Week"]:.2f}%',
            'color1Week': '#1861A8' if baseline["return1Week"] < 0 else '#C92A2A',
            'return1Month': f'{"▼" if baseline["return1Month"] < 0 else "▲"}{baseline["return1Month"]:.2f}%',
            'color1Month': '#1861A8' if baseline["return1Month"] < 0 else '#C92A2A',
            'return3Month': f'{"▼" if baseline["return3Month"] < 0 else "▲"}{baseline["return3Month"]:.2f}%',
            'color3Month': '#1861A8' if baseline["return3Month"] < 0 else '#C92A2A',
            'return6Month': f'{"▼" if baseline["return6Month"] < 0 else "▲"}{baseline["return6Month"]:.2f}%',
            'color6Month': '#1861A8' if baseline["return6Month"] < 0 else '#C92A2A',
            'return1Year': f'{"▼" if baseline["return1Year"] < 0 else "▲"}{baseline["return1Year"]:.2f}%',
            'color1Year': '#1861A8' if baseline["return1Year"] < 0 else '#C92A2A',
            'eps': '미제공' if isna(baseline["trailingEps"]) else f'{int(baseline["trailingEps"]):,d}원',
            'estEps': "미제공",
            'bps': f'{int(baseline["recentBPS"]):,d}원',
            'per': f'{baseline["trailingPE"]:.2f}',
            'estPer': "미제공",
            'pbr': f'{baseline["priceToBook"]:.2f}',
        }
        if obj["close"] == obj["h52"]:
            obj['pct52h'] = "최고가"
            obj['pct52hColor'] = '#C92A2A'
        else:
            obj['pct52h'] = f'▼{baseline["pctFiftyTwoWeekHigh"]:.2f}%'
            obj['pct52hColor'] = '#1861A8'
        if obj["close"] == obj["l52"]:
            obj['pct52l'] = "최저가"
            obj['pct52lColor'] = '#1861A8'
        else:
            obj['pct52l'] = f'▲{baseline["pctFiftyTwoWeekLow"]:.2f}%'
            obj['pct52lColor'] = '#C92A2A'
        if not baseline["estimatedProfitRate"]:
            obj['estProfitRate'] = "미제공"
        if (not baseline["estimatedEps"] is None) and (not isna(baseline["estimatedEps"])):
            obj['estEps'] = f'{int(baseline["estimatedEps"]):,d}원'
            obj['estPer'] = f'{baseline["estimatedPE"]:.2f}'
        return obj

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
    # for ticker, stock in stocks:
    #     print(stock.perBand)

