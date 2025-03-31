try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH
from numpy import datetime_as_string
from pandas import concat, read_json, to_datetime, DataFrame, MultiIndex


# REFERENCED BY {config.py}
MY_PORTFOLIO = {
    "251970": {"start": "2025-03-28", "name": "펌텍코리아"},
    "021240": {"start": "2025-03-28", "name": "코웨이"},
}


class Portfolio(DataFrame):

    def __init__(self, baseline:DataFrame, baseline_date:str):
        baseline_date = baseline_date.replace("/", "-")

        portfolio = read_json(PATH.PORTFOLIO, orient='index')
        portfolio.columns = MultiIndex.from_tuples([eval(col) for col in portfolio.columns])
        portfolio.index = portfolio.index.astype(str).str.zfill(6)
        portfolio['date'] = portfolio['date'] \
                            .apply(to_datetime, unit='ms') \
                            .apply(lambda x: x.dt.strftime("%Y-%m-%d"))
        portfolio_date = portfolio["date"]["Tracking"].values[0]
        if baseline_date == portfolio_date:
            super().__init__(portfolio)
            return

        objs = []
        for ticker, info in MY_PORTFOLIO.items():
            stock:DataFrame = baseline.loc[[ticker]]
            stock.columns = [(key, "Tracking") for key in stock.columns]
            stock[("date", "Tracking")] = stock[("date", "Tracking")].dt.strftime("%Y-%m-%d")
            objs.append(stock)
        today = concat(objs, axis=0)
        today.columns = MultiIndex.from_tuples(today.columns)
        portfolio.update(today)


        super().__init__(portfolio)
        self.to_json(PATH.PORTFOLIO, orient='index')
        return



if __name__ == "__main__":
    from src.build.service.baseline import MarketBaseline
    from pandas import set_option
    from numpy import datetime_as_string
    set_option('display.expand_frame_repr', False)

    ONSITE = {
        "251970": {"name": "펌텍코리아", "from": "2025-03-28"},
        "021240": {"name": "코웨이", "from": "2025-03-28"},
    }

    baseline = MarketBaseline(update=False)
    TRADING_DATE = baseline['date'].values[0]
    if not isinstance(TRADING_DATE, str):
        TRADING_DATE = f"{datetime_as_string(TRADING_DATE, unit='D').replace('-', '/')}"
    # print(baseline)
    # print(baseline.loc[['021240']])


    portfolio = Portfolio(baseline, TRADING_DATE)
    print(portfolio)
    print(portfolio[['close', 'marketCap', 'volume']])
