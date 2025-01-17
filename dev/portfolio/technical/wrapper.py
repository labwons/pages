try:
    from . import core
except ImportError:
    from dev.portfolio.technical import core
from json import dumps
from pandas import DataFrame


class TechnicalReporter:

    def __init__(self, ohlcv:DataFrame, to:str='js'):
        core.PRINT_MODE = to
        self.ohlcv_t = core.OHLCV_T(ohlcv)
        self.sma = core.MovingAverage(ohlcv)
        self.bb = core.BollingerBand(ohlcv)
        self.macd = core.MACD(ohlcv)
        return

    def __iter__(self):
        for item in [
            self.ohlcv_t,
            self.sma,
            self.bb,
            self.macd
        ]:
            yield item

    @property
    def const(self) -> str:
        return "\n".join([item.const for item in self]) \
                .replace('"ohlc.x"', 'ohlc.x') \
                .replace("NaN", "null")

    @property
    def predef(self) -> str:
        return f"""
const BELOW_INDICATORS = ["volume", "macd"];
const VARIABLE_MAPPING = {{
    ohlc:[ohlc],
    volume:[volume],
    sma:{str(self.sma.label).replace("'", "").replace('"', '')},
    bb:{str(self.bb.label).replace("'", "").replace('"', '')},
    macd:{str(self.macd.label).replace("'", "").replace('"', '')},
}};
const GRID_RATIO = {{
    2:[0.8, 0.2],
    3:[0.6, 0.2, 0.2],
    4:[0.55, 0.15, 0.15, 0.15]
}};"""[1:]

    def xaxis(self, **kwargs):
        attr = {
            "autorange": True,  # [str | bool] one of ( True | False | "reversed" | "min reversed" |
            #                       "max reversed" | "min" | "max" )
            "color": "#444",  # [str]
            "showgrid": True,  # [bool]
            "gridcolor": "lightgrey",  # [str]
            "griddash": "solid",  # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,  # [float]
            "showline": True,  # [bool]
            "linecolor": "black",  # [str]
            "linewidth": 2,  # [float]
            "mirror": False,  # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "rangeslider": {
                "visible": False  # [bool]
            },
            "rangeselector": {
                "visible": True,  # [bool]
                "bgcolor": "#eee",  # [str]
                "bordercolor": "#444",  # [str]
                "borderwidth": 0,  # [float]
                "buttons": [
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all")
                ],
                "xanchor": "left",  # [str] one of ( "auto" | "left" | "center" | "right" )
                "x": 0.005,  # [float]
                "yanchor": "bottom",  # [str] one of ( "auto" | "top" | "middle" | "bottom" )
                "y": 1.0  # [float]
            },
            "showticklabels": True,  # [bool]
            "tickformat": "%Y/%m/%d",  # [str]
            "zeroline": True,  # [bool]
            "zerolinecolor": "lightgrey",  # [str]
            "zerolinewidth": 1  # [float]
        }
        attr.update(kwargs)
        return dumps(attr)

    def yaxis(self, **kwargs):
        attr = {
            "domain":[0, 1],
            "side":"right",
            "showticklabels": True,  # [bool]
            "tickformat": ',d',
            "autorange": True,  # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                #  "max reversed" | "min" | "max" )
            "color": "#444",  # [str]
            "showgrid": True,  # [bool]
            "gridcolor": "lightgrey",  # [str]
            "griddash": "solid",  # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,  # [float]
            "showline": True,  # [bool]
            "linecolor": "grey",  # [str]
            "linewidth": 1,  # [float]
            "mirror": False,  # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "zeroline": True,  # [bool]
            "zerolinecolor": "lightgrey",  # [str]
            "zerolinewidth": 1  # [float]
        }
        attr.update(kwargs)
        return dumps(attr)
