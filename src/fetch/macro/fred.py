from datetime import datetime, timedelta
from pandas import concat, DataFrame, Series
from pandas_datareader import get_data_fred
from requests.exceptions import SSLError
import time


class Fred(DataFrame):
    predef = {
        # Bond and Interest Rate
        'FEDFUNDS': dict(
            symbol='FEDFUNDS',
            name='연준 기준금리',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='Federal Funds Effective Rate (Monthly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'DGS10': dict(
            symbol='DGS10',
            name='미국채10년',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'DGS5': dict(
            symbol='DGS5',
            name='미국채5년',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'DGS2': dict(
            symbol='DGS2',
            name='미국채2년',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'DGS1': dict(
            symbol='DGS1',
            name='미국채1년',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'T10Y2Y': dict(
            symbol='T10Y2Y',
            name='미국채장단기금리차(10Y-2Y)',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'T10Y3M': dict(
            symbol='T10Y3M',
            name='미국채장단기금리차(10Y-3M)',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'BAMLH0A0HYM2': dict(
            symbol='BAMLH0A0HYM2',
            name='미국 하이일드 스프레드',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='ICE BofA US High Yield Index Option-Adjusted Spread (Daily)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'MORTGAGE30US': dict(
            symbol='MORTGAGE30US',
            name='미국 30년고정주택담보대출',
            quoteType='INDICATOR',
            category='금리지표',
            unit='%',
            comment='30-Year Fixed Rate Mortgage Average in the United States (Weekly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),

        # Monetary
        'M2SL': dict(
            symbol='M2SL',
            name='미국 M2',
            quoteType='INDICATOR',
            category='통화/유동성지표',
            unit='USD(xB)',
            comment='M2: Billions of Dollars (Monthly)',
            hoverTemplate=': %{y:.2f}$(xB)<extra></extra>',
        ),
        'M2V': dict(
            symbol='M2V',
            name='미국 M2통화유동속도',
            quoteType='INDICATOR',
            category='통화/유동성지표',
            unit='%',
            comment='Velocity of M2 Money Stock (Seasonally Adjusted, Quarterly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),

        # Inflation
        'CPIAUCSL': dict(
            symbol='CPIAUCSL',
            name='미국 CPI(계절조정)',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='',
            comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Seasonally Adjusted, Monthly)',
            hoverTemplate=': %{y:.2f}<extra></extra>',
        ),
        'CPIAUCNS': dict(
            symbol='CPIAUCNS',
            name='미국 CPI(계절조정 미반영)',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='',
            comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Not Seasonally Adjusted, Monthly)',
            hoverTemplate=': %{y:.2f}<extra></extra>',
        ),
        'CORESTICKM159SFRBATL': dict(
            symbol='CORESTICKM159SFRBATL',
            name='미국 CPI(경직물가, YoY)',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='%',
            comment='Sticky Price Consumer Price Index less Food and Energy (Monthly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'CPILFESL': dict(
            symbol='CPILFESL',
            name='미국 CPI(식음료 에너지 제외)',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='',
            comment='Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average (Seasonally Adjusted, Monthly)',
            hoverTemplate=': %{y:.2f}<extra></extra>',
        ),
        'T10YIE': dict(
            symbol='T10YIE',
            name='미국 10년 기대인플레이션율',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='%',
            comment='10-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'T5YIE': dict(
            symbol='T5YIE',
            name='미국 5년 기대인플레이션율',
            quoteType='INDICATOR',
            category='물가 / 부동산지표',
            unit='%',
            comment='5-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),

        # Labor, GDP, Saving and Others
        'UNRATE': dict(
            symbol='UNRATE',
            name='미국 실업률',
            quoteType='INDICATOR',
            category='경제 / 심리지표',
            unit='%',
            comment='Unemployment Rate(Seasonally Adjusted, Monthly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'GDP': dict(
            symbol='GDP',
            name='미국 명목GDP',
            quoteType='INDICATOR',
            category='경제 / 심리지표',
            unit='USD(xB)',
            comment='Gross Domestic Product (Seasonally Adjusted, Quarterly)',
            hoverTemplate=': %{y:.2f}$(xB)<extra></extra>',
        ),
        'GDPC1': dict(
            symbol='GDPC1',
            name='미국 실질GDP',
            quoteType='INDICATOR',
            category='경제 / 심리지표',
            unit='USD(xB)',
            comment='Real Gross Domestic Product (Seasonally Adjusted, Quarterly)',
            hoverTemplate=': %{y:.2f}$(xB)<extra></extra>',
        ),
        'PSAVERT': dict(
            symbol='PSAVERT',
            name='미국 가계저축율',
            quoteType='INDICATOR',
            category='경제 / 심리지표',
            unit='%',
            comment='Personal Saving Rate (Monthly)',
            hoverTemplate=': %{y:.2f}%<extra></extra>',
        ),
        'UMCSENT': dict(
            symbol='UMCSENT',
            name='미국 소비자 심리지수(미시간 대학교)',
            quoteType='INDICATOR',
            category='경제 / 심리지표',
            unit='',
            comment='University of Michigan: Consumer Sentiment (Monthly)',
            hoverTemplate=': %{y:.2f}<extra></extra>',
        ),
    }

    def __init__(self):
        super().__init__(concat([self.fetch(item) for item in self.predef], axis=1))
        return

    def __call__(self, symbol:str, period:int=10):
        return self.fetch(symbol, period)

    @classmethod
    def fetch(cls, symbol: str, period:int=10, fs:int=5) -> Series:
        while fs > 0:
            try:
                fetched = get_data_fred(
                    symbols=symbol,
                    start=datetime.today() - timedelta(365 * period),
                    end=datetime.today()
                )
                return Series(name=symbol, index=fetched.index, data=fetched[symbol], dtype=float)
            except SSLError:
                print(f"SSL Error: Retry for {symbol}... {fs}")
                fs -= 1
                time.sleep(5)
        print(f"SSL Error confirmed: {symbol}")
        return Series()



if __name__ == "__main__":
    fred = Fred()
    print(fred)
    for col in fred:
        data = fred[col]
        if data.empty:
            print(col, "empty")
        else:
            data = data.dropna()
            print(col, data.values[-1], f'@{data.index[-1]}')