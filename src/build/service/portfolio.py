try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH

from numpy import datetime_as_string
from pandas import concat, read_json, DataFrame, MultiIndex


MY_PORTFOLIO = {
    "251970": {"start": "2025-03-28", "name": "펌텍코리아"},
    "021240": {"start": "2025-03-28", "name": "코웨이"},
}


class Portfolio(DataFrame):

    def __init__(self, baseline:DataFrame):
        portfolio = read_json(PATH.PORTFOLIO, orient='index')
        portfolio.columns = [eval(col) for col in portfolio.columns]
        portfolio.index = portfolio.index.astype(str).str.zfill(6)

        baseline_date = f"{datetime_as_string(baseline['date'].values[0], unit='D')}"
        for ticker, info in PORTFOLIO_HISTORY.items():
            stock:DataFrame = baseline.loc[[ticker]]
            if stock.empty:
                # TODO
                # {onsite{의 ticker가 baseline에 없으면 logging
                continue

            if "end" in info:
                # IF THE INVESTMENT OF THIS TICKER IS ALREADY OVER,
                # CHECK THE END-DATE DATA IN PORTFOLIO HISTORY.
                # IF THE DATA IS NOT EXIST, APPEND THE DATA AND CONTINUE THE LOOP
                history = portfolio.loc[[ticker]]

                continue


            stock.columns = [(key, baseline_date) for key in stock.columns]
            axis = 1
            if not ticker in portfolio.index:
                # IF TICKER IS NOT IN PORTFOLIO LIST,
                # NEW STOCK DATA IS TO APPEND BY THE LATEST BASELINE DATE
                axis = 0
            else:
                # IF TICKER IS IN PORTFOLIO LIST,
                # THIS CODE PREVENT TO APPEND DUPLICATED-DATED-DATA
                stock = stock[[col for col in stock.columns if not col in portfolio.columns]]

            portfolio = concat([portfolio, stock], axis=axis)
            
            # TODO
            # 종목 당 날짜는 시작 날짜, 오늘 날짜 2개로 제한하는 코드 추가

        portfolio.columns = MultiIndex.from_tuples(portfolio.columns)
        portfolio = portfolio.T.drop_duplicates(keep='first')
        super().__init__(portfolio.T)
        self.to_json(PATH.PORTFOLIO, orient='index')
        return



if __name__ == "__main__":
    from src.build.service.baseline import MarketBaseline
    from pandas import set_option

    set_option('display.expand_frame_repr', False)

    ONSITE = {
        "251970": {"name": "펌텍코리아", "from": "2025-03-28"},
        "021240": {"name": "코웨이", "from": "2025-03-28"},
    }

    baseline = MarketBaseline(update=False)
    # print(baseline)
    portfolio = Portfolio(baseline, ONSITE)
    print(portfolio)
    print(portfolio[['close', 'marketCap', 'volume']])
