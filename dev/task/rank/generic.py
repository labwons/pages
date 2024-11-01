try:
    from ...common.path import PATH
    from ...common.calendar import Calendar
    from ..treemap.core import KEYS
    from ..treemap.color import paint
except ImportError:
    from dev.common.path import PATH
    from dev.common.calendar import Calendar
    from dev.task.treemap.core import KEYS
    from dev.task.treemap.color import paint
from pandas import DataFrame
from typing import Dict
import pandas as pd
import json


class Rank(object):

    KEY = ['D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1']
    def __init__(self, basis:DataFrame=DataFrame()):
        if basis.empty:
            basis = pd.read_json(PATH.SPECS, orient='index')
            basis.index = basis.index.astype(str).str.zfill(6)
        basis = basis.copy()
        basis['meta'] = basis['name'] + '(' + basis.index + ')<br>' \
                         + '시가총액: ' + basis['marketCap'] + '원<br>' \
                         + '종가: ' + basis['close'].apply(lambda x: f"{x:,d}") + '원'
        basis = basis[[
            'name', 'industryCode', 'industryName', 'sectorCode', 'sectorName', 'meta',
            'D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1'
        ]]
        for col in self.KEY:
            basis[f'{col}-C'] = paint(basis[col], KEYS[col], False)
        keys = {key: KEYS[key] for key in self.KEY}

        self.objs = {
            'Date': str(Calendar),
            'Data': {
                'ALL': {col: self.align(basis, col) for col in self.KEY},
            },
            'Meta': keys,
        }
        self.objs['Data']['ALL']['label'] = '전체'
        for (code, label, ), group in basis.groupby(by=['industryCode', 'industryName']):
            self.objs['Data'][code] = {col: self.align(group, col) for col in self.KEY}
            self.objs['Data'][code]['label'] = label
        return

    def __getitem__(self, item):
        return self.objs[item]

    def dump(self):
        string = json.dumps(self.objs)
        if not PATH.RANK.startswith('http'):
            with open(PATH.RANK, 'w') as f:
                f.write(string)
        return string

    @staticmethod
    def align(data:DataFrame, by:str) -> dict:
        data = data.sort_values(by=by, ascending=False)
        upper = data[data[by] >= 0].iloc[:10]
        lower = data[data[by] < 0].iloc[-10:]
        return {
            'upper': {
                'name': upper['name'].tolist(),
                'meta': upper['meta'].tolist(),
                'text': round(upper[by], 2).tolist(),
                'color': upper[f'{by}-C'].tolist(),
                'x': upper[by].abs().tolist(),
                'y': [n for n in range(1, len(lower) + 1)][::-1]
            },
            'lower': {
                'name': lower['name'].tolist(),
                'meta': lower['meta'].tolist(),
                'text': round(lower[by], 2).tolist(),
                'color': lower[f'{by}-C'].tolist(),
                'x': (-1 * lower[by].abs()).tolist(),
                'y': [n for n in range(1, len(lower) + 1)][::-1]
            }
        }



if __name__ == "__main__":
    from pandas import set_option
    import plotly.graph_objects as go
    set_option('display.expand_frame_repr', False)

    # 'WI100', 'WI110', 'WI200', 'WI210', 'WI220', 'WI230',
    # 'WI240', 'WI250', 'WI260', 'WI300', 'WI310', 'WI320', 'WI330', 'WI340',
    # 'WI400', 'WI410', 'WI500', 'WI510', 'WI520', 'WI600', 'WI610', 'WI620',
    # 'WI630', 'WI640', 'WI700', 'WI800', 'ALL'
    rank = Rank()
    rank.dump()


    # test = rank['WI100']
    # label = 'D-1'
    #
    # fig = go.Figure()
    # low = go.Bar(
    #     orientation='h',
    #     x=test[label]['lower']['x'],
    #     y=test[label]['lower']['y'],
    #     text=test[label]['lower']['text'],
    #     texttemplate='%{text}%',
    #     textposition= 'outside',
    #     marker={
    #         'color': test[label]['lower']['color']
    #     },
    #     hovertemplate=test[label]['lower']['meta'],
    #     showlegend=False
    # )
    # lowlabel = go.Scatter(
    #     x=[-0.1] * len(test[label]['lower']['y']),
    #     y=test[label]['lower']['y'],
    #     mode='text',
    #     text=test[label]['lower']['name'],
    #     texttemplate='%{text}',
    #     textposition='middle left',
    #     textfont={'color':'white'},
    #     showlegend=False
    # )
    # high = go.Bar(
    #     orientation='h',
    #     x=test[label]['upper']['x'],
    #     y=test[label]['upper']['y'],
    #     text=test[label]['upper']['text'],
    #     texttemplate='%{text}%',
    #     textposition='outside',
    #     marker={
    #         'color': test[label]['upper']['color']
    #     },
    #     hovertemplate=test[label]['upper']['meta'],
    #     showlegend=False
    # )
    #
    # fig.add_traces([low, lowlabel, high])
    # fig.update_layout(
    #     plot_bgcolor='white',
    #     barmode='relative'
    # )
    # fig.show()
