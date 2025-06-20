from pandas import DataFrame, Series


class Stocks:
    def __init__(self, baseline:DataFrame, *tickers):
        self.baseline = baseline.copy()
        self.tickers = [ticker for ticker in tickers if ticker]
        return

    def __iter__(self):
        for ticker in self.tickers:
            yield self.baseline.loc[ticker]

