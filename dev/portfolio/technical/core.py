from json import dumps
from numpy import nan
from pandas import DataFrame, Series
from ta.trend import MACD as taMACD
from typing import Any, Dict
BASE_PRICE:str = "Typical"
PRINT_MODE:str = "json"


class OHLCV_T(DataFrame):

    __slot__ = {}

    @classmethod
    def dump(cls, attr:dict) -> str:
        attr_copy = attr.copy()
        for key, val in attr.items():
            if isinstance(val, Series):
                attr_copy[key] = val.tolist()
        return dumps(attr_copy)

    def __init__(self, ohlcv:DataFrame):
        super().__init__(ohlcv)
        self["Date"] = self.index.astype(str)
        self["Typical"] = ((ohlcv.High + ohlcv.Low + ohlcv.Close) / 3).astype(int)

        __slot__ = self.__slot__ = {}
        __slot__["trace"] = {
            "ohlc": {
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
            },
            # 'typicalPrice': {
            #     "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
            #     "y": self["Typical"].astype(int),
            #     "mode": "lines",
            #     "line": {
            #         "color": "black"
            #     },
            #     "visible": False,
            #     "showlegend": True,
            #     "xhoverformat": "%Y/%m/%d",
            #     "yhoverformat": ",d",
            #     "hovertemplate": "표준주가:%{y}원<extra></extra>",
            #     "type": "scatter"
            # },
            'volume': {
                "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                "y": self["Volume"],
                "marker": {
                    "color": self.apply(lambda r: "red" if r.Close >= r.Open else "royalblue", axis=1).tolist()
                },
                "showlegend": False,
                "xhoverformat": "%Y/%m/%d",
                "yhoverformat": ",d",
                "hovertemplate": "거래량: %{y}<extra></extra>",
                "yaxis": "y2",
                "type": 'bar'
            }
        }
        __slot__["label"] = list(__slot__["trace"].keys())
        __slot__["const"] = "\n".join([
            f"const {label} = {self.dump(attr)};" for label, attr in __slot__["trace"].items()
        ])
        return

    @property
    def const(self) -> str:
        return self.__slot__["const"]

    @property
    def label(self) -> list:
        return self.__slot__['label']

    @property
    def trace(self) -> dict:
        return self.__slot__["trace"]


class MovingAverage(OHLCV_T):

    WINDOWS = [5, 20, 60, 120, 200]

    def __init__(self, ohlcv:DataFrame):
        super().__init__(ohlcv)
        self._construct()

        __slot__ = {
            'trace': {
                col.lower(): {
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self[col], 1),
                    "mode": "lines",
                    "visible": True,
                    "showlegend": True,
                    "line": {
                        "dash": "dot"
                    },
                    "connectgaps": True,
                    "xhoverformat": "%Y/%m/%d",
                    "yhoverformat": ".1f",
                    "hovertemplate": f"{col.replace('MA', '')}일: %%{{y}}<extra></extra>"
                } for col in self if col.startswith('MA')
            }
        }
        __slot__['label'] = list(__slot__['trace'].keys())
        __slot__['const'] = "\n".join([
            f"const {label} = {self.dump(attr)};" for label, attr in __slot__['trace'].items()
        ])
        if PRINT_MODE.startswith('js'):
            self.__slot__ = __slot__
        else:
            self.__slot__['trace'].update(__slot__['trace'])
            self.__slot__['label'] += __slot__['label']
            self.__slot__['const'] += __slot__['const']
        return

    def _construct(self):
        for win in self.WINDOWS:
            self[f'MA{win}'] = self[BASE_PRICE].rolling(win).mean()
        return


class BollingerBand(OHLCV_T):

    WINDOW:int = 20
    FACTOR:int = 2

    def __init__(self, ohlcv:DataFrame):
        super().__init__(ohlcv)
        self._construct()

        __slot__:Dict[str, Any] = {
            'trace': {
                'bb_middle': {
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["bb_middle"], 1),
                    "mode": "lines",
                    "visible": True,
                    "showlegend": False,
                    "line": {
                        "dash": "dot"
                    },
                    "connectgaps": True,
                    "xhoverformat": "%Y/%m/%d",
                    "yhoverformat": ".1f",
                    "hovertemplate": f"{self.WINDOW}일: %%{{y}}<extra></extra>"
                },
                'bb_upperband': {
                    "name": "x2 Band",
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["bb_upperband"], 1),
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
                },
                'bb_uppertrend': {
                    "name": "x1 Band",
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["bb_uppertrend"], 1),
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
            }
        }
        __slot__['trace']['bb_lowerband'] = __slot__['trace']['bb_upperband'].copy()
        __slot__['trace']['bb_lowerband'].update({
            "y": round(self["bb_lowerband"], 1),
            "showlegend": False,
            "hovertemplate": "x2 하단: %{y}원<extra></extra>"
        })
        __slot__['trace']['bb_lowertrend'] = __slot__['trace']['bb_uppertrend'].copy()
        __slot__['trace']['bb_lowertrend'].update({
            "y": round(self["bb_lowertrend"], 1),
            "showlegend": False,
            "hovertemplate": "x1 하단: %{y}원<extra></extra>"
        })

        __slot__['label'] = list(__slot__['trace'].keys())
        __slot__['const'] = "\n".join([
            f"const {label} = {self.dump(attr)};" for label, attr in __slot__['trace'].items()
        ])
        if PRINT_MODE.startswith('js'):
            self.__slot__ = __slot__
        else:
            self.__slot__['trace'].update(__slot__['trace'])
            self.__slot__['label'] += __slot__['label']
            self.__slot__['const'] += __slot__['const']
        return

    def _construct(self):
        basePrice = self[BASE_PRICE]
        self['bb_middle'] = middle = basePrice.rolling(self.WINDOW).mean()
        self['bb_stddev'] = stddev = basePrice.rolling(self.WINDOW).std()
        self['bb_upperband'] = upperband = middle + self.FACTOR * stddev
        self['bb_lowerband'] = lowerband = middle - self.FACTOR * stddev
        self['bb_uppertrend'] = uppertrend = middle + (self.FACTOR / 2) * stddev
        self['bb_lowertrend'] = lowertrend = middle - (self.FACTOR / 2) * stddev
        self['bb_width'] = 100 * (2 * self.FACTOR * stddev) / middle
        self['bb_pctb'] = ((basePrice - lowerband) / (upperband - lowerband)).where(upperband != lowerband, nan)
        self['bb_pctt'] = ((basePrice - lowertrend) / (uppertrend - lowertrend)).where(uppertrend != lowertrend, nan)
        return


class MACD(OHLCV_T):

    def __init__(self, ohlcv: DataFrame):
        super().__init__(ohlcv)
        self._construct()

        __slot__: Dict[str, Any] = {
            'trace': {
                'macd': {
                    "name": "MACD",
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["macd"], 2),
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
                },
                'macd_sig': {
                    "name": "Signal",
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["signal"], 2),
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
                },
                'macd_diff': {
                    "name": "Diff",
                    "x": "ohlc.x" if PRINT_MODE.startswith("js") else self["Date"],
                    "y": round(self["diff"], 2),
                    "type":"bar",
                    "marker":{
                        "color": self["diff"].diff().apply(lambda x: 'red' if x > 0 else 'royalblue').tolist()
                    },
                    "visible": True,
                    "showlegend": True,
                    "xhoverformat": "%Y/%m/%d",
                    "yhoverformat": ".2f",
                    "hovertemplate": "Diff: %{y}<extra></extra>",
                    "yaxis": "y3",
                }
            }
        }
        __slot__['label'] = list(__slot__['trace'].keys())
        __slot__['const'] = "\n".join([
            f"const {label} = {self.dump(attr)};" for label, attr in __slot__['trace'].items()
        ])
        if PRINT_MODE.startswith('js'):
            self.__slot__ = __slot__
        else:
            self.__slot__['trace'].update(__slot__['trace'])
            self.__slot__['label'] += __slot__['label']
            self.__slot__['const'] += __slot__['const']
        return

    def _construct(self):
        macd = taMACD(close=self[BASE_PRICE])
        self['macd'] = macd.macd()
        self['signal'] = macd.macd_signal()
        self['diff'] = macd.macd_diff()
        return


if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv(
        "https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
        .set_index(keys="Date") \
        .drop(columns=["Adj Close"])
    data.index = pd.to_datetime(data.index)

    # PRINT_MODE = 'python'

    ohlcv_t = OHLCV_T(data)
    # print(ohlcv_t.trace)
    print(ohlcv_t.label)
    print(ohlcv_t.const)

    ma = MovingAverage(data)
    # print(ma.trace)
    print(ma.label)
    print(ma.const)