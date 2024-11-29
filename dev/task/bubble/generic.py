try:
    from ...common.path import PATH
    from ...common.calendar import Calendar
except ImportError:
    from dev.common.path import PATH
    from dev.common.calendar import Calendar
from pandas import DataFrame
from typing import Dict
import pandas as pd
import json


class Bubble(DataFrame):
    DUMP = {
        'DATE': f"{Calendar} 기준",
        'LABEL': {            
            'D-1':'1일 수익률',
            'W-1':'1주 수익률', 
            'M-1':'1개월 수익률', 
            'M-3':'3개월 수익률', 
            'M-6':'6개월 수익률', 
            'Y-1':'1년 수익률', 
            'high52PR':'52주 최고가 대비', 
            'low52PR':'52주 최저가 대비', 
            'estimatedPR':'목표가 대비',
            'volume':'거래량',
            'foreignRate':'외국인 지분율', 
            'beta':'베타', 
            'floatShares':'유동주식비율', 
            'trailingPS':'PSR', 
            'trailingPE':'PER',
            'estimatedPE':'추정PER', 
            'PBR':'PBR', 
            'trailingEarningRatio':'영업이익률',
            'fiscalDividends':'배당수익률', 
            'DIV':'예상배당수익률',
            'debtRatio':'부채비율',
        }
    }
    def __init__(self, basis:DataFrame=DataFrame()):
        normalize = lambda x, mn, mx: mn + (x - x.min()) * (mx - mn) / (x.max() - x.min())
        if basis.empty:
            basis = pd.read_json(PATH.SPECS, orient='index')
            basis.index = basis.index.astype(str).str.zfill(6)
        basis = basis.copy()
        basis = basis.sort_values(by='size', ascending=True)
        basis['size'] = normalize(basis['size'], 5, 100)
        keys = ['name', 'size', 'meta'] + list(self.DUMP['LABEL'].keys())
        
        super().__init__(basis[keys])
        category = basis[["sectorCode", "sectorName"]] \
                   .drop_duplicates() \
                   .set_index(keys="sectorCode") \
                   .to_dict()["sectorName"]
        category.update(basis[["industryCode", "industryName"]] \
                        .drop_duplicates() \
                        .set_index(keys="industryCode") \
                        .to_dict()["industryName"])
        self.DUMP["CATEGORY"] = category
        self.DUMP["DATA"] = self.to_dict(orient="index")
        return

    def dump(self):
        string = json.dumps(self.DUMP).replace("NaN", "null")
        if not PATH.BUBBLE.startswith('http'):
            with open(PATH.BUBBLE, 'w') as f:
                f.write(string)
        return string


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
