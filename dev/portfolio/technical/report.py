# try:
#     from ..fetch.krx import krx
#     import calc
# except ImportError:
#     from dev.portfolio.fetch.krx import krx
#     from dev.portfolio.technical import calc
import calc
from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import json


class TechnicalReport(DataFrame):

    @classmethod
    def push(cls, a:DataFrame, b:DataFrame):
        b_ = b.drop(columns=a.columns.intersection(b.columns))
        return pd.merge(a, b_, left_index=True, right_index=True, how='outer')
    
    def __init__(self, ticker:str, period:int=10):
        # data = krx(ticker=ticker, period=period).ohlcv
        data = pd.read_csv("https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
                 .set_index(keys="Date") \
                 .drop(columns=["Adj Close"])
        data.index = pd.to_datetime(data.index)
        data['typical'] = calc.typicalPrice(data)
        data = data.astype(int)
        data = self.push(data, calc.bollingerBand(data))
        data.reset_index(level=0, inplace=True)
        data['Date'] = data['Date'].dt.strftime("%Y-%m-%d")
        super().__init__(data)
        return
    
    def write(self):
        jsonData = json.dumps({col: self[col].tolist() for col in self})
        syntax = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>문서 제목</title>
	
	<script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.1.min.js"></script>
</head>
<body>
    <header>
        <!-- 상단 내비게이션 바나 제목 -->
    </header>
    <main>
        <div class="service-app">
            <div class="plotly" id="plotly"></div>
          </div>
          <div style="clear:both;"></div>
    </main>
    <footer>
        <!-- 하단 정보 -->
    </footer>
    <script>
        $(document).ready(function() {
            const data = %s;
            const layout = {
                title: "%s 유형",
            }
            const candle = {
                x:data.Date,
                open:data.Open,
                high:data.High,
                low:data.Low,
                close:data.Close,
                xhoverformat:"%s",
                type:'candlestick'
            };
            Plotly.newPlot('plotly', [candle], layout);
        })
    </script>
</body>
</html>""" % (jsonData, '이름', "%Y/%m/%d")
        with open(r"C:\Users\Administrator\Desktop\report_copy.html", mode='w', encoding='utf-8') as file:
            file.write(syntax)
        return
    
if __name__ == "__main__":
    rep = TechnicalReport('005930')

    # print(rep)
    rep.write()