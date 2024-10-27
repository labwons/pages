try:
    from ...common.path import PATH
    from .fetch import fetchIpo, fetchOverviewSpec, fetchOverviewStatement
except ImportError:
    from dev.module.fng.fetch import fetchIpo, fetchOverviewSpec, fetchOverviewStatement
    from dev.common.path import PATH
from pandas import DataFrame
from typing import Iterable
import numpy as np
import pandas as pd


class Stat(DataFrame):

    def __init__(self):
        read = pd.read_json(PATH.STATE, orient='index')
        read.index = read.index.astype(str).str.zfill(6)
        super().__init__(read)
        return

    def dataUpdate(self, *tickers):
        if not tickers:
            tickers = self.index

        for ticker in tickers:
            base = fetchOverviewSpec(ticker)

            ifrs = 'con'
            quarter = fetchOverviewStatement(ticker, ifrs, 'q', False).iloc[1:]
            if quarter.empty:
                self.loc[ticker, base.index] = base.values
                continue
            debt = quarter.iloc[-1]['부채비율(%)']
            if np.isnan(debt):
                ifrs = 'sep'
                quarter = fetchOverviewStatement(ticker, ifrs, 'q', False).iloc[1:]

            base['trailingSales'] = quarter[quarter.columns[0]].sum()
            base['trailingEarning'] = quarter['영업이익(억원)'].sum()
            base['trailingNetIncome'] = quarter['당기순이익(억원)'].sum()
            base['trailingEarningRatio'] = round(quarter['영업이익률(%)'].mean(), 2)
            base['trailingEps'] = quarter['EPS(원)'].sum()

            annual = fetchOverviewStatement(ticker, ifrs, 'a', False)

            base['fiscalSales'] = annual.iloc[-1][annual.columns[0]]
            base['fiscalEarning'] = annual['영업이익(억원)'].sum()
            base['fiscalNetIncome'] = annual['당기순이익(억원)'].sum()
            base['fiscalEarningRatio'] = annual.iloc[-1]['영업이익률(%)']
            base['fiscalEps'] = annual.iloc[-1]['EPS(원)']
            base['fiscalDividends'] = annual.iloc[-1]['배당수익률(%)']
            base['debtRatio'] = quarter.iloc[-1]['부채비율(%)']
            self.loc[ticker] = base
        return

    def remove(self, tickers:Iterable):
        self.drop(index=tickers, inplace=True)
        return

    def dump(self) -> str:
        string = self.to_json(orient='index').replace("nan", "")
        if not PATH.STATE.startswith('http'):
            with open(PATH.STATE, 'w') as f:
                f.write(string)
        return string


if __name__ == "__main__":
    df = Stat()
    df.dataUpdate(['395400'])
    df.dump()