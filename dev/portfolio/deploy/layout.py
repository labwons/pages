import json


class layout:
    def _xaxis(self, **kwargs) -> str:
        axis = {
            "autorange": True,              # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                            #                       "max reversed" | "min" | "max" )
            "color": "#444",                # [str]
            "showgrid": True,               # [bool]
            "gridcolor": "lightgrey",       # [str]
            "griddash": "solid",            # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,               # [float]
            "showline": True,               # [bool]
            "linecolor": "grey",            # [str]
            "linewidth": 1,                 # [float]
            "mirror": False,                # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "rangeslider": {
                "visible": False            # [bool]
            },
            "rangeselector": {
                "visible": True,            # [bool]
                "bgcolor": "#eee",          # [str]
                "bordercolor": "#444",      # [str]
                "borderwidth": 0,           # [float]
                "buttons": [
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all")
                ],
                "xanchor" : "left",         # [str] one of ( "auto" | "left" | "center" | "right" )
                "x" : 0.005,                # [float]
                "yanchor" : "bottom",       # [str] one of ( "auto" | "top" | "middle" | "bottom" )
                "y" : 1.0                   # [float]
            },
            "showticklabels": True,         # [bool]
            "tickformat": "%Y/%m/%d",       # [str]
            "zeroline": True,               # [bool]
            "zerolinecolor": "lightgrey",   # [str]
            "zerolinewidth": 1              # [float]
        }
        axis.update(kwargs)
        return json.dumps(axis)