# try:
#     from ..fetch.krx import krx
#     import calc
# except ImportError:
#     from dev.portfolio.fetch.krx import krx
#     from dev.portfolio.technical import calc
import calc
from pandas import DataFrame, Series
from typing import Union
import pandas as pd
import json





class Report(DataFrame):
    ticker:str = ''

    @classmethod
    def push(cls, a:DataFrame, b:DataFrame):
        b_ = b.drop(columns=a.columns.intersection(b.columns))
        return pd.merge(a, b_, left_index=True, right_index=True, how='outer')
    
    @classmethod
    def dump(cls, data:dict) -> str:
        return json.dumps(data).replace("NaN", "null")
    
    def __init__(self, ticker:str, period:int=10):
        # data = krx(ticker=ticker, period=period).ohlcv
        data = pd.read_csv("https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
                 .set_index(keys="Date") \
                 .drop(columns=["Adj Close"])
        data.index = pd.to_datetime(data.index)

        data['typical'] = calc.typicalPrice(data)
        data = data.astype(int)
        data = self.push(data, calc.bollingerBand(data))
        data = self.push(data, calc.simpleMA(data, 5, 20, 60, 120, 200))
        data = self.push(data, calc.regression(data, 5, 2, 1, 0.5, 0.25))
        data.reset_index(level=0, inplace=True)
        data['Date'] = data['Date'].dt.strftime("%Y-%m-%d")
        super().__init__(data)
        self.ticker = ticker
        return
    
    def __getitem__(self, item) -> list:
        return super().__getitem__(item).tolist()
    
    # def serialize(self) -> str:
    #     return self.dump({col:self[col].tolist() for col in self})
    
    def candlestick(self, **kwargs) -> str:
        _trace = {
            "open": self["Open"],
            "high": self["High"],
            "low": self["Low"],
            "close": self["Close"],
            "increasing": {
                "line": {
                    "color":'red'
                }
            },
            "decreasing": {
                "line": {
                    "color":'royalblue'
                }
            },
            "showlegend": False,
            "hoverinfo": 'x+y',
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ",d",
            "type": 'candlestick'
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def volume(self, **kwargs) -> str:
        _color = self.apply(lambda r: "red" if r.Close >= r.Open else "royalblue", axis=1).tolist()
        _trace = {
            "y":self["Volume"],
            "marker":{
                "color":_color
            },
            "showlegend":False,
            "xhoverformat":"%Y/%m/%d",
            "yhoverformat":",d",
            "hovertemplate":"거래량: %{y}<extra></extra>",
            "yaxis":"y2",
            "type":'bar'
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def ma(self, **kwargs) -> str:
        _trace = {
            # "y":self[],
            "mode": "lines",
            "visible": "legendonly",
            "showlegend": True,
            "line": {
                "dash": "dot"
            },
            "connectgaps": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            # "hovertemplate": ""
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def upperband(self, **kwargs) -> str:
        _trace = {
            "name": "x2 Band",
            "y": self["upperband"],
            "mode": "lines",
            "line": {
                "dash": "dash",
                "color": "maroon"
            },
            "showlegend": True,
            "legendgroup": "x2",
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".1f",
            "hovertemplate": "x2 상단: %{y}원<extra></extra>"
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def uppertrend(self, **kwargs) -> str:
        _trace = {
            "name": "x1 Band",
            "y": self["uppertrend"],
            "mode": "lines",
            "line": {
                "dash": "dash",
                "color": "green"
            },
            "showlegend": True,
            "legendgroup": "x1",
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".1f",
            "hovertemplate": "x1 상단: %{y}원<extra></extra>"
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def lowerband(self, **kwargs) -> str:
        _trace = {
            "name": "x2 Band",
            "y": self["lowerband"],
            "mode": "lines",
            "line": {
                "dash": "dash",
                "color": "maroon"
            },
            "showlegend": False,
            "legendgroup": "x2",
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".1f",
            "hovertemplate": "x2 하단: %{y}원<extra></extra>"
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def lowertrend(self, **kwargs) -> str:
        _trace = {
            "name": "x1 Band",
            "y": self["lowertrend"],
            "mode": "lines",
            "line": {
                "dash": "dash",
                "color": "green"
            },
            "showlegend": False,
            "legendgroup": "x1",
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".1f",
            "hovertemplate": "x1 하단: %{y}원<extra></extra>"
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def bandwidth(self, **kwargs) -> str:
        _trace = {
            "name": "밴드폭",
            "y": self["width"],
            "mode": "lines",
            "line": {
                "color": "grey"
            },
            "showlegend": False,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            "hovertemplate": "폭: %{y}%<extra></extra>",
            "yaxis":"y3",
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def trend(self, **kwargs) -> str:
        _trace = {
            "mode": "lines",
            "visible": "legendonly",
            "showlegend": True,
            "line": {
                "dash": "dash",
                "color": "black"
            },
            "connectgaps": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            # "hovertemplate": ""
        }
        _trace.update(**kwargs)
        return self.dump(_trace)
    
    def write(self):
        with open(r"C:\Users\Administrator\Desktop\report_copy.html", mode='w', encoding='utf-8') as file:
            file.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>LAB￦ONS :: ({self.ticker})</title>
	
	<!-- <script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script> --> 
    <script src="https://cdn.jsdelivr.net/gh/labwons/pages/src/js/plotly-0.1.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.1.min.js"></script>
</head>
<body>
    <header>

    </header>
    <main>
        <div class="service-app">
            <div class="service-nav">
                <div class="service-options">
                    <select name="technical" class="service-t">
                        <option value="default">기본</option>
                        <option value="bollingerBand">밴드</option>
                        <option value="trend">추세</option>
                    </select>
                    <select name="fundamental" class="service-f"></select>
                </div>
            </div>
            <div class="plotly" id="plotly"></div>
        </div>
        <div style="clear:both;"></div>
    </main>
    <footer>
        <!-- 하단 정보 -->
    </footer>
    <script>
        var date = {self["Date"]};
        var candle = {self.candlestick()};
        var volume = {self.volume()};
        var ma5 = {self.ma(name='MA5', y=self['MA5'])};
        var ma20 = {self.ma(name='MA20', y=self['MA20'])};
        var ma60 = {self.ma(name='MA60', y=self['MA60'])};
        var ma120 = {self.ma(name='MA120', y=self['MA120'])};
        var ma200 = {self.ma(name='MA200', y=self['MA200'])};
        var upperBand = {self.upperband()};
        var upperTrend = {self.uppertrend()};
        var lowerBand = {self.lowerband()};
        var lowerTrend = {self.lowertrend()};
        var bandWidth = {self.bandwidth()};
        var trendAll = {self.trend(name='전기간 추세', y=self['전체'])};
        var trend5y = {self.trend(name="5년 추세", y=self["5Y"])};
        var trend2y = {self.trend(name="2년 추세", y=self["2Y"])};
        var trend1y = {self.trend(name="1년 추세", y=self["1Y"])};
        var trend6m = {self.trend(name="6개월 추세", y=self["6M"])};
        var trend3m = {self.trend(name="3개월 추세", y=self["3M"])};
        var layout = {{
            title: "이름({self.ticker})",
            hovermode: "x unified",
            xaxis: {Layout.xaxis()},
            yaxis: {Layout.yaxis()},
            legend: {Layout.legend()}
        }};
        var option = {{
            displayModeBar:false,
            responsive:true,
            showTips:false
        }};

        function viewHeight() {{
            return 0.7 * $(window).height();
        }};

        function sma(){{
            var data = [candle, volume, ma5, ma20, ma60, ma120, ma200];
            data.forEach(item => {{item.x = date;}});
            layout.grid = {{
                rows:2,
                columns:1,
                rowheights:[0.8, 0.2],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('plotly', data, layout, option);
        }};

        function bollingerBand(){{
            var data = [candle, volume, upperBand, lowerBand, upperTrend, lowerTrend, bandWidth];
            data.forEach(item => {{item.x = date;}});
            layout.grid = {{
                rows:3,
                columns:1,
                rowheights:[0.7, 0.15, 0.15],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('plotly', data, layout, option);
        }};

        function trend(){{
            var data = [candle, volume, trendAll, trend5y, trend2y, trend1y, trend6m, trend3m];
            data.forEach(item => {{item.x = date;}});
            layout.grid = {{
                rows:2,
                columns:1,
                rowheights:[0.8, 0.2],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('plotly', data, layout, option);
        }}
        
        $(document).ready(function() {{
            sma();
            $('.service-t').on('change', function() {{
                $('#plotly').empty();
                if ($(this).val() == "default") {{
                    sma();
                }} else if ($(this).val() == "bollingerBand") {{
                    bollingerBand();
                }}
            }})
    
        }})
    </script>
</body>
</html>""")
        return
    
if __name__ == "__main__":
    rep = TechnicalReport('005930')

    print(rep)
    rep.write()