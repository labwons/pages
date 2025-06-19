try:
    from .metadata import METADATA
    from src.common.env import FILE
except ImportError:
    from src.build.baseline.metadata import METADATA
    from src.common.env import FILE
from datetime import datetime
from numpy import nan
from pandas import DataFrame, Series
from pandas import concat, isna, read_parquet
from time import perf_counter
from typing import List, Union


class Tools:

    @classmethod
    def krw2currency(cls, krw:int, div:int=0) -> Union[str, float]:
        if isna(krw):
            return nan
        if div:
            krw = krw / div
        zo, euk = int(krw // 10000), int(krw % 10000)
        return f'{zo}조 {euk}억' if zo else f'{euk}억'

    @classmethod
    def typeCast(cls, value):
        value = str(value).lower().replace(",", "")
        if value in ['separate', 'consolidated']:
            return value
        if "n" in value:
            return nan
        if not any([char.isdigit() for char in value]):
            return nan
        return float(value) if "." in value or "-" in value else int(value)

    @classmethod
    def profitGrowth(cls, profit:Series, debug:bool=False) -> List:
        prev = profit.values[0]
        if -1 <= prev <= 1:
            prev = nan
        value, label = [], []
        for curr in profit.iloc[1:]:
            if -1 <= curr <= 1:
                curr = nan
            if prev is None or isna(prev) or isna(curr):
                value.append(nan)
                label.append(nan)
            elif prev < 0 <= curr:
                value.append(nan)
                label.append("흑자 전환")
            elif curr < 0 <= prev:
                value.append(nan)
                label.append("적자 전환")
            else:
                value.append(100 * (curr - prev) / abs(prev))
                label.append(nan)
            prev = curr
        values = Series(value)
        average = values.mean() if len(values.dropna()) >= 2 else nan
        if debug:
            print(values)
            print(average)
        return [value[-1], label[-1], average]



class Baseline:

    _log: List[str] = []

    def __init__(self):
        stime = perf_counter()
        self.log = f'  >> BUILD [BASELINE]'

        number = read_parquet(FILE.AFTER_MARKET, dtype_backend="pyarrow")
        n_date = datetime.strptime(str(number.pop('date').values[-1]), "%Y%m%d%H:%M")
        self.log = f'     READ AFTER MARKET NUMBERS: {str(n_date).replace("-", "/")}'
        number = self.number(number)
        # print(number)

        overview = read_parquet(FILE.STATEMENT_OVERVIEW, dtype_backend="pyarrow")
        overview_date = overview.pop('date').value_counts(dropna=False)
        statement_yy = overview.pop('reportYears')
        statement_qq = overview.pop('reportQuarters')
        if len(overview_date) == 1:
            self.log = f'     READ STATEMENT OVERVIEW: {overview_date.index[0]}'
        else:
            report = '\n'.join(f'     {line}' for line in str(overview_date).split('\n')[1:-1])
            self.log = f'     READ STATEMENT OVERVIEW: LOW RELIABILITY'
            self.log = f'{report}'
        overview = self.overview(overview)
        # print(overview)

        statementA = read_parquet(FILE.ANNUAL_STATEMENT)
        self.log = f'     READ ANNUAL STATEMENT'
        statementA = self.statementA(statementA, statement_yy)
        # # print(statementA)

        statementQ = read_parquet(FILE.QUARTER_STATEMENT)
        self.log = f'     READ QUARTER STATEMENT'
        statementQ = self.statementQ(statementQ, statement_qq)
        # print(statementQ)

        sector = read_parquet(FILE.SECTOR_COMPOSITION)
        s_date = datetime.strptime(str(sector.pop('date').values[-1]), "%Y%m%d").strftime("%Y/%m/%d")
        self.log = f'     READ SECTOR COMPOSITION: {s_date}'
        sector = self.sector(sector)
        # print(sector)

        merge = self.merge(number, overview, statementA, statementQ, sector)
        self.checkMetadata(merge)
        self.data = merge

        # print(merge)
        # merge.to_clipboard()

        self.tradingDate = n_date.strftime("%Y/%m/%d")

        self.log = f'  >> BUILD END: {perf_counter() - stime:.2f}s'
        self._log[0] += f'{len(merge)} items'
        return

    @property
    def log(self) -> str:
        return "  \n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @classmethod
    def number(cls, number:DataFrame) -> DataFrame:
        # RENAME AND DROP
        number = number.rename(columns={p: c for p, c in METADATA.RENAME if p in number.columns})
        number = number.drop(columns=[col for col in number if not col in METADATA])
        return number

    @classmethod
    def overview(cls, overview:DataFrame) -> DataFrame:
        overview = overview.rename(columns={p: c for p, c in METADATA.RENAME if p in overview.columns})
        overview = overview.drop(columns=[col for col in overview if not col in METADATA])
        typecast = overview.columns.difference(['stockSplitDate', 'statementType'])
        overview[typecast] = overview[typecast].map(Tools.typeCast)
        return overview

    @classmethod
    def sector(cls, sector:DataFrame) -> DataFrame:
        # NOTHING TO MODIFY
        return sector

    @classmethod
    def statementA(cls, statementA:DataFrame, yy:Series) -> DataFrame:
        tickers = statementA.columns.get_level_values(0).unique()
        objs = []
        for ticker in tickers:
            statement = statementA[ticker].loc[yy[ticker].split(",")]
            statement = statement.dropna(how='all', axis=0)
            statement = statement.map(Tools.typeCast)
            estimated = statement[statement.index.str.contains('\\(E\\)')].copy()
            provision = statement[statement.index.str.contains('\\(P\\)')].copy()
            statement = statement[~statement.index.isin(estimated.index)]

            recentStatement = statement.loc[statement.index[-1]]
            if not provision.empty:
                # IF THERE IS PROVISIONAL STATEMENT(잠정치), BASICALLY PROVISIONAL VALUE WILL BE USED,
                # NaN VALUES OF PROVISIONAL WILL BE REPLACED TO RECENT FISCAL YEAR STATEMENT
                recentStatement = recentStatement.combine_first(statement.iloc[-2])

            obj = Series()
            _revenueKey = statement.columns[0]
            obj['fiscalDate'] = recentStatement.name
            obj['fiscalRevenue'] = recentStatement[_revenueKey]
            obj = concat([obj, recentStatement.drop(index=[_revenueKey])])

            revenueGrowth = 100 * statement[_revenueKey].pct_change(fill_method=None).dropna()
            if not revenueGrowth.empty:
                obj['fiscalRevenueGrowth'] = revenueGrowth.values[-1]
                obj['averageRevenueGrowth'] = revenueGrowth.mean()
                profitGrowth = Series(
                    index=['fiscalProfitGrowth', 'fiscalProfitState', 'averageProfitGrowth'],
                    data=Tools.profitGrowth(statement['영업이익(억원)'])
                )
                epsGrowth = Series(
                    index=['fiscalEpsGrowth', 'fiscalEpsState', 'averageEpsGrowth'],
                    data= Tools.profitGrowth(statement['EPS(원)'])
                )
                obj = concat([obj, profitGrowth, epsGrowth])

            if not estimated.empty:
                # IF THERE IS ESTIMATED STATEMENT(추정치), CLOSEST ESTIMATION DATE WILL BE USED.
                # ESTIMATIONG FOR GROWTH IS ONLY USED FOR REVENUE, PROFIT, AND EPS.

                est = concat([recentStatement, estimated.iloc[0]], axis=1).T
                est = est.rename(columns={p: c.replace("fiscal", "estimated") for p, c in METADATA.RENAME if p in est})
                est = est.rename(columns={est.columns[0]:'estimatedRevenue'})
                obj['estimatedDate'] = est.index[-1]
                obj = concat([obj, est.iloc[-1]])

                if recentStatement[_revenueKey] < 5:
                    obj['estimatedRevenueGrowth'] = nan
                else:
                    obj['estimatedRevenueGrowth'] = 100 * est.pct_change(fill_method=None).iloc[-1]['estimatedRevenue']

                pg = Tools.profitGrowth(est['estimatedProfit'])
                obj['estimatedProfitGrowth'] = pg[0]
                obj['estimatedProfitState'] = pg[1]

                eg = Tools.profitGrowth(est['estimatedEps'])
                obj['estimatedEpsGrowth'] = eg[0]
                obj['estimatedEpsState'] = eg[1]

            obj['revenueType'] = _revenueKey.replace("(억원)", "")
            obj.name = ticker
            objs.append(obj)
        merge = concat(objs=objs, axis=1).T
        merge = merge.rename(columns={p: c for p, c in METADATA.RENAME if p in merge.columns})
        return merge

    @classmethod
    def statementQ(cls, statementQ:DataFrame, qq:Series) -> DataFrame:
        from numpy import seterr
        seterr(all='raise')
        tickers = statementQ.columns.get_level_values(0).unique()
        objs = []
        for ticker in tickers:
            statement = statementQ[ticker].loc[qq[ticker].split(",")]
            statement = statement.dropna(how='all', axis=0)
            statement = statement.map(Tools.typeCast)
            estimated = statement[statement.index.str.contains('\\(E\\)')].copy()
            provision = statement[statement.index.str.contains('\\(P\\)')].copy()
            statement = statement[~statement.index.isin(estimated.index)]
            recentQuarter = statement.loc[statement.index[-1]]
            if not provision.empty:
                recentQuarter = statement.iloc[-1].combine_first(statement.iloc[-2])

            obj = Series()
            obj['recentAsset'] = recentQuarter['자산총계(억원)']
            obj['recentCapital'] = recentQuarter['자본총계(억원)']
            obj['recentDebt'] = recentQuarter['부채총계(억원)']
            obj['recentDebtRatio'] = recentQuarter['부채비율(%)']
            obj['recentProfitRate'] = recentQuarter['영업이익률(%)']
            if recentQuarter[statement.columns[0]] < 5:
                # IF REVENUE IS LESS THAN 5억원, PROFIT RATE IS NOT USED.
                obj['recentProfitRate'] = nan

            if len(statement) >= 4:
                for key, label in {
                    statement.columns[0]: 'trailingRevenue',
                    '영업이익(억원)': 'trailingProfit',
                    '당기순이익(억원)': 'trailingNetProfit',
                    'EPS(원)': 'trailingEps'
                }.items():
                    trailer = statement[key].iloc[-4:]
                    if trailer.isnull().sum():
                        trailer = statement[key].iloc[-5:-1]
                        if trailer.isnull().sum():
                            # IF THE NUMBER OF TRAILING VALUES IS LESS THAN FOUR,
                            # TRAILING VALUES ARE TO BE REGARD AS UNRELIABLE DATA.
                            break
                    obj[label] = trailer.sum()
            if 'trailingRevenue' in obj and 'trailingProfit' in obj:
                obj['trailingProfitRate'] = 100 * obj['trailingProfit'] / obj['trailingRevenue']

            lastQ = str(recentQuarter.name).replace("(P)", "").split("/")
            yearAgo = statement[statement.index == f'{int(lastQ[0]) - 1}/{lastQ[-1]}']
            if not yearAgo.empty:
                frm = concat([yearAgo.iloc[0], recentQuarter], axis=1).T
                yoy = 100 * frm.pct_change(fill_method=None)
                yoy = yoy.rename(columns={p: c.replace("fiscal", "yoy") for p, c in METADATA.RENAME if p in yoy})
                yoy = yoy.rename(columns={yoy.columns[0]: "yoyRevenue"})
                obj = concat([obj, yoy.iloc[-1]], axis=0)
                ps = Tools.profitGrowth(frm['영업이익(억원)'])
                es = Tools.profitGrowth(frm['EPS(원)'])
                obj['yoyProfit'] = ps[0]
                obj['yoyProfitState'] = ps[1]
                obj['yoyEps'] = es[0]
                obj['yoyEpsState'] = es[1]

            obj.name = ticker
            objs.append(obj)
        merge = concat(objs=objs, axis=1).T
        return merge

    @classmethod
    def merge(cls, base:DataFrame, *dataframes:DataFrame) -> DataFrame:
        merge = base.join(concat(list(dataframes), axis=1))
        merge = merge[~merge['name'].isna()]
        merge = merge.dropna(how='all', axis=1)

        # CUSTOMIZE SECTION
        merge['fiftyTwoWeekHigh'] = merge[['close', 'fiftyTwoWeekHigh']].max(axis=1)
        merge['fiftyTwoWeekLow'] = merge[['close', 'fiftyTwoWeekLow']].min(axis=1)
        merge['pctFiftyTwoWeekHigh'] = 100 * (merge['close'] / merge['fiftyTwoWeekHigh'] - 1)
        merge['pctFiftyTwoWeekLow'] = 100 * (merge['close'] / merge['fiftyTwoWeekLow'] - 1)
        merge['pctTargetPrice'] = 100 * (merge['close'] / merge['targetPrice'] - 1)
        merge['estimatedPE'] = merge['close'] / merge['estimatedEps'].apply(lambda x: x if x > 0 else nan)
        merge['trailingPS'] = (merge['marketCap'] / 1e+8) / merge['trailingRevenue']
        merge['trailingPE'] = merge['close'] / merge['trailingEps'].apply(lambda x: x if x > 0 else nan)
        merge['turnoverRatio'] = 100 * merge['volume'] / (merge['shares'] * merge['floatShares'] / 100)
        return merge

    @classmethod
    def checkMetadata(cls,base:DataFrame):
        ndef = [c for c in base if c not in METADATA]
        if ndef:
            print("METADATA 미정의 항목")
            for c in ndef:
                print(f'{c}=dDict(')
                print(f"\tlabel='label',")
                print(f"\tunit='%',")
                print(f"\tdtype=float,")
                print(f"\tdigit=2,")
                print(f"\torigin='',")
                print(f"\tlimit=False,")
                print(f"\t# Adder")
                print(f"),")

        ddef = [m for m, v in METADATA if m not in base and not "RENAME" == m]
        if ddef:
            print("불필요 METADATA 항목")
            for m in ddef:
                print(m)
        return

    @classmethod
    def gaussian(cls, data:DataFrame, col:str):
        # INTERNAL
        import plotly.graph_objs as go
        from scipy.stats import norm
        from pandas import concat, Series


        y = Series(index=data.index, data=norm.pdf(data[col], data[col].mean(), data[col].std()), name='y')
        m = data['name'] + '(' + data.index + ')'
        m.name = 'm'
        subset = concat([data[col], y, m], axis=1).sort_values(by=col)

        # print(data[data.index.isin(subset.tail(5).index)])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=subset[col],
            y=subset.y,
            mode='lines+markers',
            showlegend=False,
            meta=subset.m,
            hovertemplate="%{meta}: %{x}<extra></extra>"
        ))

        xs = [
            [subset[col].mean() - 2 * subset[col].std()] * len(subset),
            [subset[col].mean() - 1 * subset[col].std()] * len(subset),
            [subset[col].mean() + 1 * subset[col].std()] * len(subset),
            [subset[col].mean() + 2 * subset[col].std()] * len(subset),
            [subset[col].mean()] * len(subset)
        ]
        for x in xs:
            fig.add_trace(go.Scatter(
                x=x,
                y=subset.y,
                mode='lines',
                showlegend=False,
                line={
                    'color':'black',
                    'dash':'dot'
                },
                hoverinfo='skip'
            ))

        fig.update_layout(
            xaxis_title="Value",
            yaxis_title="Density",
        )
        fig.show('browser')
        return


if __name__ == "__main__":
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    from src.common.env import FILE
    from pandas import read_parquet

    baseline = Baseline()
    print(baseline.log)
    baseline.data.to_parquet(FILE.BASELINE, engine='pyarrow')
    baseline.data.to_clipboard()
    # print(baseline.data)
    # print(baseline.data.columns)

    # df = read_parquet(FILE.BASELINE, engine='pyarrow')
    # df.to_clipboard()
    # print(df.columns)
    # Baseline.gaussian(df, 'turnoverRatio')
