from pandas import DataFrame
from plotly.graph_objs import Scatter
from typing import Any, Dict, Union
from json import dumps

class Trace:

    mode:str = 'python'
    def __init__(self, data:DataFrame):
        self.data = data.copy()
        return

    def __getitem__(self, item):
        return self.data[item].tolist()

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
        return Scatter(**attrib)

