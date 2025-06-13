try:
    from src.build.service.metadata import METADATA
    from src.common.env import FILE
except ImportError:
    from src.build.service.metadata import METADATA
    from src.common.env import FILE
from datetime import datetime
from numpy import nan
from pandas import DataFrame, Series, isna
from pandas import concat, read_parquet
from time import perf_counter
from typing import List


class Tools:

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
    def profitGrowth(cls, profit:Series) -> List:
        prev = profit.values[0]
        if 0 <= prev <= 1:
            prev = nan
        value, label = [], []
        for curr in profit.iloc[1:]:
            if 0 < curr <= 1:
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
        return [value[-1], label[-1], average]



class Baseline:

    _log: List[str] = []

    def __init__(self):
        stime = perf_counter()
        self.log = f'RUN [BUILD BASELINE]'

        number = read_parquet(FILE.AFTER_MARKET, dtype_backend="pyarrow")
        n_date = datetime.strptime(str(number.pop('date').values[-1]), "%Y%m%d%H:%M")
        self.log = f'- READ AFTER MARKET NUMBERS: {str(n_date).replace("-", "/")}'
        number = self.number(number)
        # print(number)

        overview = read_parquet(FILE.STATEMENT_OVERVIEW, dtype_backend="pyarrow")
        overview_date = overview.pop('date').value_counts(dropna=False)
        statement_yy = overview.pop('reportYears')
        statement_qq = overview.pop('reportQuarters')
        if len(overview_date) == 1:
            self.log = f'- READ STATEMENT OVERVIEW: {overview_date.index[0]}'
        else:
            report = '\n'.join(f'  {line}' for line in str(overview_date).split('\n')[1:-1])
            self.log = f'- READ STATEMENT OVERVIEW: LOW RELIABILITY'
            self.log = f'{report}'
        overview = self.overview(overview)
        # print(overview)

        statementA = read_parquet(FILE.ANNUAL_STATEMENT)
        self.log = f'- READ ANNUAL STATEMENT'
        statementA = self.statementA(statementA, statement_yy)
        # print(statementA)

        statementQ = read_parquet(FILE.QUARTER_STATEMENT)
        self.log = f'- READ QUARTER STATEMENT'
        statementQ = self.statementQ(statementQ, statement_qq)
        # print(statementQ)

        sector = read_parquet(FILE.SECTOR_COMPOSITION)
        s_date = datetime.strptime(str(sector.pop('date').values[-1]), "%Y%m%d").strftime("%Y/%m/%d")
        self.log = f'- READ SECTOR COMPOSITION: {s_date}'
        sector = self.sector(sector)
        # print(sector)

        merge = self.merge(number, overview, statementA, statementQ, sector)
        self.data = merge
        # print(merge)
        # merge.to_clipboard()

        self.tradingDate = n_date.strftime("%Y/%m/%d")

        self.log = f'END [BUILD BASELINE] {len(merge)} Stocks / Elapsed: {perf_counter() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

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
                EST_GROWTH_COLUMNS = ['estimatedRevenue', 'estimatedProfit', 'estimatedEps']
                est = concat([recentStatement, estimated.iloc[0]], axis=1).T
                est = est.rename(
                    columns={p: c.replace("fiscal", "estimated") for p, c in METADATA.RENAME if p in est.columns}
                )
                est = est.rename(columns={est.columns[0]:'estimatedRevenue'})
                estRated = 100 * est.pct_change(fill_method=None)[EST_GROWTH_COLUMNS]
                estRated = estRated.rename(columns={c: f'{c}Growth' for c in estRated.columns})

                obj['estimatedDate'] = est.index[-1]
                obj = concat([obj, est.iloc[-1], estRated.iloc[-1]])

            obj['revenueType'] = _revenueKey.replace("(억원)", "")
            obj.name = ticker
            objs.append(obj)
        merge = concat(objs=objs, axis=1).T
        merge = merge.rename(columns={p: c for p, c in METADATA.RENAME if p in merge.columns})
        return merge

    @classmethod
    def statementQ(cls, statementQ:DataFrame, qq:Series) -> DataFrame:
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

            # TODO
            # YoY 계산 및 추가

            obj = Series()
            obj['recentAsset'] = recentQuarter['자산총계(억원)']
            obj['recentCapital'] = recentQuarter['자본총계(억원)']
            obj['recentDebt'] = recentQuarter['부채총계(억원)']
            obj['recentDebtRatio'] = recentQuarter['부채비율(%)']
            obj['recentProfitRate'] = recentQuarter['영업이익률(%)']

            for key, label in {
                statement.columns[0]: 'trailingRevenue',
                '영업이익(억원)': 'trailingProfit',
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


    # def show_gaussian(self, col:str):
    #     # INTERNAL
    #     import plotly.graph_objs as go
    #     from scipy.stats import norm
    #     from pandas import concat, Series
    #
    #     # x = self[[col, 'name']]
    #     y = Series(index=self.index, data=norm.pdf(self[col], self[col].mean(), self[col].std()), name='y')
    #     m = self['name'] + '(' + self.index + ')'
    #     m.name = 'm'
    #     subset = concat([self[col], y, m], axis=1).sort_values(by=col)
    #     print(subset)
    #     fig = go.Figure()
    #
    #     fig.add_trace(go.Scatter(
    #         x=subset[col],
    #         y=subset.y,
    #         mode='lines+markers',
    #         showlegend=False,
    #         meta=subset.m,
    #         hovertemplate="%{meta}: %{x}<extra></extra>"
    #     ))
    #     fig.add_trace(go.Scatter(
    #         x=[subset[col].mean() - 2 * subset[col].std()] * len(subset),
    #         y=subset.y,
    #         mode='lines',
    #         showlegend=False,
    #         line={
    #             'color':'black',
    #             'dash':'dot'
    #         },
    #         hoverinfo='skip'
    #     ))
    #     fig.add_trace(go.Scatter(
    #         x=[subset[col].mean() + 2 * subset[col].std()] * len(subset),
    #         y=subset.y,
    #         mode='lines',
    #         showlegend=False,
    #         line={
    #             'color': 'black',
    #             'dash': 'dot'
    #         },
    #         hoverinfo='skip'
    #     ))
    #
    #     fig.update_layout(
    #         xaxis_title="Value",
    #         yaxis_title="Density",
    #     )
    #     fig.show('browser')
    #     return


if __name__ == "__main__":
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    # baseline = Baseline()
    # print(baseline)
    # print(baseline.log)
    # baseline.show_gaussian('M-1')

    from pandas import read_parquet
    from src.common.env import FILE

    df = read_parquet(FILE.BASELINE, engine='pyarrow')
    # print(df)

    for c in df:
        if c not in METADATA:
            print(f'{c}=dDict(')
            print(f"\tlabel='label',")
            print(f"\tunit='%',")
            print(f"\tdtype=float,")
            print(f"\tdigit=2,")
            print(f"\torigin='',")
            print(f"\t# Adder")
            print(f"),")

    for m, v in METADATA:
        if m not in df:
            print(m)