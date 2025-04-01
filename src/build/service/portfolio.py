try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH
from pandas import concat, read_json, isna, DataFrame, MultiIndex
from typing import List


# REFERENCED BY {config.py}
MY_PORTFOLIO = [
    # {"ticker": "251970", "start": "2025-03-28", "end":"2025-03-31", "name": "펌텍코리아"},
    {"ticker": "251970", "start": "2025-03-28", "name": "펌텍코리아"},
    {"ticker": "021240", "start": "2025-03-28", "name": "코웨이"},
]


class Portfolio(DataFrame):

    _log: List[str] = []
    def __init__(self, baseline:DataFrame):
        self.log = f'RUN [Build Portfolio]'

        baseline = baseline.copy()
        if str(baseline["date"].dtype).startswith("datetime64"):
            baseline["date"] = baseline["date"].dt.strftime("%Y-%m-%d")
        baseline_date = baseline['date'].values[0]

        portfolio = read_json(PATH.PORTFOLIO, orient='index')
        portfolio.columns = MultiIndex.from_tuples([eval(col) for col in portfolio.columns])
        portfolio.index = portfolio.index.astype(str).str.zfill(6)
        portfolio_date = portfolio["date"]["Tracking"].values[0]
        if baseline_date == portfolio_date:
            super().__init__(portfolio)
            self.log = f'END [Build Portfolio] {len(self[self["date"]["End"].isna()])} / {len(self)} Stocks'
            return

        _new, _tracking, _complete = [], [], []
        for obj in MY_PORTFOLIO:
            ticker = obj["ticker"]
            if ticker in portfolio.index:

                # IF PORTFOLIO CONFIGURATION TICKER IS IN PORTFOLIO DATA, TWO CASES
                # ARE POSSIBLE. IF THE START DATE OF PORTFOLIO DATA AND CONFIGURATION
                # START DATE IS THE SAME, IT IS ON GOING(TRACKING) TICKER. ON THE OTHER
                # HAND, IF THE START DATES ARE NOT MATCHED, NEW INVESTMENT IS BEGINNING.
                if portfolio.loc[ticker]["date"]["Start"] == obj["start"]:
                    _tracking.append(ticker)
                if portfolio.loc[ticker]["date"]["Start"] != obj["start"]:
                    _new.append(ticker)
                    _tracking.append(ticker)

                # IF CONFIGURATION TICKER IS IN PORTFOLIO DATA, AND INVESTMENT {end} IS
                # CONFIGURED, CHECK PORTFOLIO DATA IS ENDED. IF NOT, TODAY'S BASELINE
                # DATA WILL BE RECORDED AS HISTORY.
                if "end" in obj:
                    if isna(portfolio.loc[ticker]["date"]["End"]):
                        _complete.append(ticker)
            else:
                _new.append(ticker)
                _tracking.append(ticker)

        new:DataFrame = baseline.loc[_new]
        new.columns = MultiIndex.from_tuples(zip(new.columns, ["Start"] * len(new.columns)))
        if not new.empty:
            portfolio = concat([portfolio, new], axis=0)

        tracking:DataFrame = baseline.loc[_tracking]
        tracking.columns = MultiIndex.from_tuples(zip(tracking.columns, ["Tracking"] * len(tracking.columns)))
        if not tracking.empty:
            portfolio.update(tracking)

        complete:DataFrame = baseline.loc[_complete]
        complete.columns = MultiIndex.from_tuples(zip(complete.columns, ["End"] * len(complete.columns)))
        if not complete.empty:
            portfolio.update(complete)

        # order = portfolio.columns.get_level_values(0).unique()
        # portfolio = portfolio.reindex(columns=
        #                               sorted(portfolio.columns, key=lambda x: (order.get_loc(x[0]), x[1])))

        super().__init__(portfolio)
        self.to_json(PATH.PORTFOLIO, orient='index')
        self.log = f'END [Build Portfolio] {len(self[self["date"]["End"].isna()])} / {len(self)} Stocks'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)



if __name__ == "__main__":
    from src.build.service.baseline import MarketBaseline
    from pandas import set_option
    from numpy import datetime_as_string
    set_option('display.expand_frame_repr', False)


    baseline = MarketBaseline(update=False)
    # print(baseline)
    # print(baseline.loc[['021240']])

    portfolio = Portfolio(baseline)
    print(portfolio.log)
    print("*" * 100)
    print(portfolio)
    print(portfolio[['close', 'marketCap', 'volume']])
