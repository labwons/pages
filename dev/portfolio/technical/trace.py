try:
    from .calc import TechnicalFrame
    from .layout import Layout
    from ..fetch.krx import krx
except ImportError:
    from dev.portfolio.technical.calc import TechnicalFrame
    from dev.portfolio.technical.layout import Layout
    from dev.portfolio.fetch.krx import krx
from datetime import datetime
from pandas import DataFrame
from plotly.graph_objs import Bar, Scatter
from typing import Any, Dict, Union
from jsmin import jsmin
from json import dumps

class TechnicalTrace:

    mode:str = 'python'
    def __init__(self, ticker_or_ohlcv_or_tf:Union[str, DataFrame, TechnicalFrame], **kwargs):
        if isinstance(ticker_or_ohlcv_or_tf, str):
            self.data = krx(ticker_or_ohlcv_or_tf, period=kwargs['period'] if 'period' in kwargs else 10)
        elif isinstance(ticker_or_ohlcv_or_tf, DataFrame):
            if len(ticker_or_ohlcv_or_tf.columns) <= 5:
                self.data = TechnicalFrame(ticker_or_ohlcv_or_tf)
            else:
                self.data = ticker_or_ohlcv_or_tf
        else:
            raise TypeError()
        return

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item].tolist()

    def to_js(
        self,
        option_id:str="service-option",
        plotly_id:str="plotly",
        minify:bool=True
    ) -> str:
        ma_defs = "\n\t\t".join([
            f"var {col.lower()} = {self.ma(name=col[2:] + '일', x='ohlc.x', y=self[col])};"
            for col in self if col.startswith('MA')
        ])
        ma_vars = ", ".join([col.lower() for col in self if col.startswith('MA')])
        tr_defs = "\n\t\t".join([
            f"var tr{col.replace('추세', '').replace('전구간', 'all')} = {self.trend(name=col, x='ohlc.x', y=self[col])};"
            for col in self if col.endswith('추세')
        ])
        tr_vars = ", ".join([
            f"tr{col.replace('추세', '').replace('전구간', 'all')}"
            for col in self if col.endswith('추세')
        ])


        context = f"""/* Copyright@LAB￦ONS 2024-{datetime.now().year} All rights reserved. */
        var layout = {{
            margin: {{
                t:10, r:80, b:20, l:10,
            }},
            hovermode: "x unified",
            legend: {Layout.legend()}
        }};
        var option = {{
            displayModeBar:false,
            responsive:true,
            showTips:false
        }};
        var ohlc = {self.ohlc()};
        var volume = {self.volume(x="ohlc.x")};
        {ma_defs}
        var upperBand = {self.upperband(x="ohlc.x")};
        var upperTrend = {self.uppertrend(x="ohlc.x")};
        var lowerBand = {self.lowerband(x="ohlc.x")};
        var lowerTrend = {self.lowertrend(x="ohlc.x")};
        var bandWidth = {self.bandwidth(x="ohlc.x")};
        {tr_defs}
        var macd = {self.macd(x="ohlc.x")};
        var macd_sig = {self.macd_signal(x="ohlc.x")};
        var macd_diff = {self.macd_diff(x="ohlc.x")};

        function viewHeight() {{
            return 0.7 * $(window).height();
        }};

        function sma(){{
            var data = [ohlc, volume, {ma_vars}];
            layout.grid = {{
                rows:2,
                columns:1,
                roworder: 'top to bottom',
                xaxes:['x'],
            }};
            
            layout.height = viewHeight();
            Plotly.newPlot('{plotly_id}', data, layout, option);
        }};

        function bollingerBand(){{
            var data = [ohlc, volume, upperBand, lowerBand, upperTrend, lowerTrend, bandWidth];
            layout.grid = {{
                rows:3,
                columns:1,
                rowheights:[0.7, 0.15, 0.15],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('{plotly_id}', data, layout, option);
        }};

        function macd(){{
            var data = [ohlc, volume, macd, macd_sig, macd_diff];
            layout.grid = {{
                rows:3,
                columns:1,
                rowheights:[0.6, 0.15, 0.25],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('{plotly_id}', data, layout, option);
        }};

        function trend(){{
            var data = [ohlc, volume, {tr_vars}];
            layout.grid = {{
                rows:2,
                columns:1,
                rowheights:[0.8, 0.2],
                xaxes:['x'],
            }}
            layout.height = viewHeight();
            Plotly.newPlot('{plotly_id}', data, layout, option);
        }}
        
        $(document).ready(function() {{
            $('.{option_id}')
            .append('<optgroup label="[기술차트 / Technical]">')
            .append('<option value="sma">이동평균선</option>')
            .append('<option value="bb">볼린저밴드</option>')
            .append('<option value="macd">MACD</option>')
            sma();
            
            $('.{option_id}').on('change', function() {{
                $('#plotly').empty();
                if ($(this).val() == "sma") {{
                    sma();
                }} else if ($(this).val() == "bb") {{
                    bollingerBand();
                }} else if ($(this).val() == "macd") {{
                    macd();
                }}
            }})
    
        }})
""".replace('"ohlc.x"', 'ohlc.x').replace("NaN", "null")
        return jsmin(context) if minify else context

    def ohlc(self, **kwargs) -> Union[Dict[str, Any], Scatter, str]:
        attrib = {
            "x": self["Date"],
            "open": self["Open"],
            "high": self["High"],
            "low": self["Low"],
            "close": self["Close"],
            "increasing": {
                "line": {
                    "color": 'red'
                }
            },
            "decreasing": {
                "line": {
                    "color": 'royalblue'
                }
            },
            "showlegend": False,
            "hoverinfo": 'x+y',
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ",d",
            "type": 'candlestick'
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def volume(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        _color = self.data.apply(lambda r: "red" if r.Close >= r.Open else "royalblue", axis=1).tolist()
        attrib = {
            "x": self["Date"],
            "y": self["Volume"],
            "marker": {
                "color": _color
            },
            "showlegend": False,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ",d",
            "hovertemplate": "거래량: %{y}<extra></extra>",
            "yaxis": "y2",
            "type": 'bar'
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def ma(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "x": self["Date"],
            "mode": "lines",
            "visible": True,
            "showlegend": True,
            "line": {
                "dash": "dot"
            },
            "connectgaps": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            # "hovertemplate": ""
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def upperband(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "x2 Band",
            "x": self["Date"],
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
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def uppertrend(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "x1 Band",
            "x": self["Date"],
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
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def lowerband(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "x2 Band",
            "x": self["Date"],
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
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def lowertrend(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "x1 Band",
            "x": self["Date"],
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
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def bandwidth(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "밴드폭",
            "x": self["Date"],
            "y": self["width"],
            "mode": "lines",
            "line": {
                "color": "grey"
            },
            "showlegend": False,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            "hovertemplate": "폭: %{y}%<extra></extra>",
            "yaxis": "y3",
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def trend(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "x": self["Date"],
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
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def macd(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "MACD",
            "x": self["Date"],
            "mode": "lines",
            "visible": True,
            "showlegend": True,
            "line": {
                "color": "royalblue"
            },
            "connectgaps": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            "hovertemplate": "MACD: %{y}<extra></extra>",
            "yaxis": "y3",
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def macd_signal(self, **kwargs) -> Union[Dict[str, Any], str, Scatter]:
        attrib = {
            "name": "Signal",
            "x": self["Date"],
            "mode": "lines",
            "visible": True,
            "showlegend": True,
            "line": {
                "color": "red"
            },
            "connectgaps": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            "hovertemplate": "Signal: %{y}<extra></extra>",
            "yaxis": "y3",
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Scatter(**attrib)

    def macd_diff(self, **kwargs) -> Union[Dict[str, Any], str, Bar]:
        attrib = {
            "name": "Diff",
            "x": self["Date"],
            "y": self["diff"],
            "type":"bar",
            "marker":{
                "color": self.data["diff"].diff().apply(lambda x: 'red' if x > 0 else 'royalblue').tolist()
            },
            "visible": True,
            "showlegend": True,
            "xhoverformat": "%Y/%m/%d",
            "yhoverformat": ".2f",
            "hovertemplate": "Diff: %{y}<extra></extra>",
            "yaxis": "y3",
        }
        attrib.update(kwargs)
        if self.mode == "json":
            return dumps(attrib)
        elif self.mode == 'dict':
            return attrib
        return Bar(**attrib)

if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv(
        "https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
        .set_index(keys="Date") \
        .drop(columns=["Adj Close"])
    data.index = pd.to_datetime(data.index)

    tt = TechnicalTrace(data)
    tt.mode = 'json'
    print(tt.to_js(False))