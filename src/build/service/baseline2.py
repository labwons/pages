try:
    from .metadata import METADATA
    from ...common.env import FILE
except ImportError:
    from src.build.service.metadata import METADATA
    from src.common.env import FILE
from datetime import datetime
from numpy import nan, datetime_as_string
from pandas import DataFrame, Series
from pandas import concat, read_parquet
from time import perf_counter
from typing import Any, Dict, List, Union



class Tools:

    @classmethod
    def typeCast(cls, value):
        value = str(value).lower().replace(",", "")
        if "n" in value:
            return nan
        if not any([char.isdigit() for char in value]):
            return nan
        return float(value) if "." in value or "-" in value else int(value)

    # @classmethod
    # def meanGrowthRate(cls, series:Series) -> Union[Any, float]:
    #     if len(series) != len(series.dropna()):
    #         return nan
    #     return (100 * series.pct_change()).mean()



class MarketBaseline:

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
        statementA = self.statementA(statementA)
        print(statementA)

        sector = read_parquet(FILE.SECTOR_COMPOSITION)
        s_date = datetime.strptime(str(sector.pop('date').values[-1]), "%Y%m%d").strftime("%Y/%m/%d")
        self.log = f'- READ SECTOR COMPOSITION: {s_date}'
        sector = self.sector(sector)
        # print(sector)

        merge = number \
                .join(overview) \
                .join(sector)
        merge = merge[~merge['name'].isna()]
        # print(merge)

        self.tradingDate = n_date.strftime("%Y/%m/%d")

        # baseline = read_json(PATH.BASE, orient='index')
        # basedate = baseline['date'].values[0]
        # if not isinstance(basedate, str):
        #     basedate = f"{datetime_as_string(basedate, unit='D')}"
        # else:
        #     basedate = basedate.replace("/", "-")
        #
        # if (not update) or basedate == datetime.today().strftime("%Y-%m-%d"):
        #     super().__init__(baseline[["date"] + [col for col in baseline.columns if not col == 'date']])
        #     self.index = self.index.astype(str).str.zfill(6)
        #     self.log = f'END [Build Market Baseline] {len(self)} Stocks / Elapsed: {time() - stime:.2f}s'
        #     return
        #
        # spec = MarketSpec(update=False)
        # group = MarketGroup(update=False)
        # state = MarketState(debug=False)
        # merge = state.join(spec).join(group)
        # if state.log:
        #     self.log = state.log
        #
        # try:
        #     merge['high52'] = merge[['close', 'high52']].max(axis=1)
        #     merge['low52'] = merge[['close', 'low52']].min(axis=1)
        #     merge['pct52wHigh'] = 100 * (merge['close'] / merge['high52'] - 1)
        #     merge['pct52wLow'] = 100 * (merge['close'] / merge['low52'] - 1)
        #     merge['pctEstimated'] = 100 * (merge['close'] / merge['estPrice'] - 1)
        #     merge['estEps'] = merge['estEps'].apply(lambda x: x if x > 0 else nan)
        #     merge['estimatedPE'] = merge['close'] / merge['estEps']
        #     merge.drop(columns=["high52", "low52", "estPrice", "estEps"], inplace=True)
        #
        #     merge['trailingEps'] = merge['trailingEps'].apply(lambda x: x if x > 0 else nan)
        #     merge['trailingPS'] = (merge['marketCap'] / 1e+8) / merge['trailingRevenue']
        #     merge['trailingPE'] = merge['close'] / merge['trailingEps']
        #     merge['turnoverRatio'] = 100 * merge['volume'] / (merge['shares'] * merge['floatShares'] / 100)
        #     self.log = f'- No-Labeled Keys: {[key for key in merge if key not in METADATA]}'
        #
        #     merge = merge[METADATA.keys()]
        #     for key, meta in METADATA.items():
        #         if not meta['round'] == -1:
        #             merge[key] = round(merge[key], meta['round'])
        # except Exception as report:
        #     self.log = f" * [FAILED] Error while customizing data: {report}"

        # super().__init__(merge[["date"] + [col for col in merge.columns if not col == 'date']])
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
        return overview

    @classmethod
    def sector(cls, sector:DataFrame) -> DataFrame:
        # NOTHING TO MODIFY
        return sector

    @classmethod
    def statementA(cls, statementA:DataFrame) -> DataFrame:
        tickers = statementA.columns.get_level_values(0).unique()
        objs = []
        # for ticker in ['005930', '361390']:
        for ticker in tickers:
            c = statementA[ticker]['연결']
            s = statementA[ticker]['별도']
            obj = Series()
            obj['statementType'] = 'separate' if s.count().sum() > c.count().sum() else 'Consolidated'

            statement = s if obj.statementType == "separate" else c
            statement = statement[statement.index.str.contains('/12') & (~statement.index.str.contains('\\(E\\)'))]
            statement = statement.map(Tools.typeCast)

            latestStatement = statement.iloc[-1]
            obj['fiscalDate'] = latestStatement.name
            obj['fiscalRevenue'] = latestStatement[statement.columns[0]]
            obj = concat([obj, latestStatement.drop(index=[statement.columns[0]])])

            ratedStatement = 100 * statement.pct_change(fill_method=None).iloc[1:]
            # print(ratedStatement)
            # obj['averageRevenueGrowth']
            # obj['averageProfitGrowth']
            # obj['averageEpsGrowth']
            # obj['fiscalRevenueGrowth']
            # obj['fiscalProfitGrowth']
            # obj['fiscalEpsGrowth']
            # obj['fiscalDividendGrowth']

            obj.name = ticker
            objs.append(obj)
        merge = concat(objs=objs, axis=1).T
        merge = merge.rename(columns={p: c for p, c in METADATA.RENAME if p in merge.columns})
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

    baseline = MarketBaseline()
    # print(baseline)
    print(baseline.log)
    # baseline.show_gaussian('M-1')





