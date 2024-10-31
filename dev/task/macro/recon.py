try:
    from ...common.path import PATH
    from ...module.ecos.core import METADATA
except ImportError:
    from dev.common.path import PATH
    from dev.module.ecos.core import METADATA
from pandas import DataFrame, Series
import pandas as pd
import json


def fromEcos() -> DataFrame:
    with open(PATH.ECOS, 'r') as file:
        load = json.load(file)
        objs = {key: Series(index=data["date"], data=data["data"]) for key, data in load.items()}
        data = pd.concat(objs=objs, axis=1)
        data.index = pd.to_datetime(data.index)
        data = data.astype(float).sort_index()

    align = []
    for name, meta in METADATA.items():
        align.append(name)
        if meta["YoY"]:
            label = f'{name}(YoY)'
            data[label] = data[name].dropna().asfreq('M').pct_change(periods=12) * 100
            if label.startswith('신용대주'):
                data[label] = data[label].clip(upper=2000)
            align.append(label)
        if meta["MoM"]:
            data[f'{name}(MoM)'] = data[name].dropna().asfreq('M').pct_change(periods=1) * 100
            align.append(f'{name}(MoM)')
        if name == '은행대출금리(잔액)':
            data['장단기금리차(10Y-2Y)'] = data['국고채10년'] - data['국고채2년']
            data['하이일드스프레드'] = data['회사채3년(BBB-)'] - data['국고채10년']
            data['예대금리차(신규)'] = data['은행대출금리(신규)'] - data['은행수신금리(신규)']
            data['예대금리차(잔액)'] = data['은행대출금리(잔액)'] - data['은행수신금리(잔액)']
            align.append('장단기금리차(10Y-2Y)')
            align.append('하이일드스프레드')
            align.append('예대금리차(신규)')
            align.append('예대금리차(잔액)')
    return data[align]

def fromWise():
    data = pd.read_json(PATH.INDEX, orient='index')
    return data


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    import plotly.graph_objects as go


    ecos = fromEcos()
    wise = fromWise()

    fig = go.Figure()
    fig.set_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        specs=[[{"secondary_y": True, "r":-0.06}]]
    )
    traces = [go.Scatter(
        name=col,
        x=ecos[col].dropna().index,
        y=ecos[col].dropna(),
        visible=True if not n else False
    ) for n, col in enumerate(ecos)]
    traces += [go.Scatter(
        name='KS',
        x=wise.index,
        y=wise['KOSPI'],
        visible=True
    )]

    buttons = [{
        'label': trace.name,
        'method': 'update',
        'args': [{
            'visible': [True if n == m else False for m in range(len(traces) - 1)] + [True]
        }]
    } for n, trace in enumerate(traces)]

    fig.add_traces(traces, secondary_ys=[False] * (len(traces) - 1) + [True])
    fig.update_layout(
        plot_bgcolor="white",
        hovermode="x unified",
        legend=dict(
            orientation='h',
            xanchor='right',
            x=1.0,
            yanchor='top',
            y=1.0
        ),
        updatemenus=[{
            'buttons':buttons,
            'direction':'down',
            'showactive':True,
            'xanchor': 'left',
            'yanchor': 'bottom',
            'x': 0.0, 'y': 1.0
        }],
        xaxis=dict(
            gridcolor='lightgrey',
            showline=True,
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor='grey',
            linecolor="grey",
            mirror=False
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            showline=True,
            linecolor="grey",
            mirror=True
        ),
        yaxis2=dict(
            showgrid=False
        )

    )
    fig.show()
