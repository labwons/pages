try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH

from pandas import concat, read_json, DataFrame, MultiIndex


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

        print(portfolio)
        print("-" * 100)

        objs = []
        for ticker, info in MY_PORTFOLIO.items():
            stock:DataFrame = baseline.loc[[ticker]]
            stock.columns = [(key, baseline_date) for key in stock.columns]
            objs.append(stock)
        today = concat(objs, axis=0)
        today.columns = MultiIndex.from_tuples(today.columns)
        print(today)
        print("-" * 100)

        portfolio = concat([portfolio, today], axis=1)
        order = portfolio.columns.get_level_values(0).unique()
        portfolio = portfolio.reindex(
            columns=sorted(portfolio.columns, key=lambda x: (order.get_loc(x[0]), x[1]))
        )

            # if stock.empty:
            #     # TODO
            #     # {onsite{의 ticker가 baseline에 없으면 logging
            #     continue
            #
            # if "end" in info:
            #     # IF THE INVESTMENT OF THIS TICKER IS ALREADY OVER,
            #     # CHECK THE END-DATE DATA IN PORTFOLIO HISTORY.
            #     # IF THE DATA IS NOT EXIST, APPEND THE DATA AND CONTINUE THE LOOP
            #     history = portfolio.loc[[ticker]]
            #
            #     continue
            #
            # axis = 1
            # if not ticker in portfolio.index:
            #     # IF TICKER IS NOT IN PORTFOLIO LIST,
            #     # NEW STOCK DATA IS TO APPEND BY THE LATEST BASELINE DATE
            #     axis = 0
            # # else:
            #     # IF TICKER IS IN PORTFOLIO LIST,
            #     # THIS CODE PREVENT TO APPEND DUPLICATED-DATED-DATA
            #
            #     # stock = stock[[col for col in stock.columns if not col in portfolio.columns]]
            #
            # portfolio = concat([portfolio, stock], axis=axis)
            
            # TODO
            # 종목 당 날짜는 시작 날짜, 오늘 날짜 2개로 제한하는 코드 추가

        # portfolio.columns = MultiIndex.from_tuples(portfolio.columns)
        # portfolio = portfolio.T.drop_duplicates(keep='first')
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
