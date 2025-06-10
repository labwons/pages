try:
    from .metadata import METADATA
    from ...common.env import FILE
except ImportError:
    from src.build.service.metadata import METADATA
    from src.common.env import FILE
from datetime import datetime
from numpy import nan, datetime_as_string
from pandas import DataFrame, read_json
from time import time
from typing import Any, Dict, List




class MarketBaseline(DataFrame):

    _log: List[str] = []

    def __init__(self):
        stime = time()
        self.log = f'RUN [BUILD BASELINE]'


        super().__init__()




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
        self.log = f'END [BUILD BASELINE] {len(self)} Stocks / Elapsed: {time() - stime:.2f}s'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    def show_gaussian(self, col:str):
        # INTERNAL
        import plotly.graph_objs as go
        from scipy.stats import norm
        from pandas import concat, Series

        # x = self[[col, 'name']]
        y = Series(index=self.index, data=norm.pdf(self[col], self[col].mean(), self[col].std()), name='y')
        m = self['name'] + '(' + self.index + ')'
        m.name = 'm'
        subset = concat([self[col], y, m], axis=1).sort_values(by=col)
        print(subset)
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=subset[col],
            y=subset.y,
            mode='lines+markers',
            showlegend=False,
            meta=subset.m,
            hovertemplate="%{meta}: %{x}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=[subset[col].mean() - 2 * subset[col].std()] * len(subset),
            y=subset.y,
            mode='lines',
            showlegend=False,
            line={
                'color':'black',
                'dash':'dot'
            },
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=[subset[col].mean() + 2 * subset[col].std()] * len(subset),
            y=subset.y,
            mode='lines',
            showlegend=False,
            line={
                'color': 'black',
                'dash': 'dot'
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

    baseline = MarketBaseline()
    # print(baseline)
    # print(baseline.log)
    # baseline.show_gaussian('M-1')




