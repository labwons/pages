# try:
#     from types import mapData
# except ImportError:
#     from app.barmap.types import mapData    
# from pandas import DataFrame

# def align(data:mapData) -> mapData:
    
    
#     # level = [col for col in frm.columns if col in ['ticker', 'sectorName', 'indexName']]
#     # ftr = [col for col in frm.columns if any([col.startswith(key) for key in ['R', 'B', 'P', 'D']])]

#     objs = list()
#     for n, level in enumerate(data.level):
#         # obj = pd.DataFrame() if n else frm.rename(columns={'섹터': '분류'})
#         if level == 'ticker':
#             obj = data.copy()
#         else:
#             layer = data.groupby(by=level[n:]).sum().reset_index()
#             obj = DataFrame()            
#             obj['ticker'] = layer[level] + f'_{self.name}{self.tag}'
#             obj['name'] = layer[l]
#             obj['classify'] = layer[lvl[n + 1]] if n < len(lvl) - 1 else self.name
#             obj['size'] = layer['size']
#             for name in obj['종목명']:
#                 df = frm[frm[l] == name]
#                 for f in ftr:
#                     if f == 'DIV':
#                         obj.loc[obj['종목명'] == name, f] = 0 if df.empty else df[f].mean()
#                     else:
#                         num = df[df['PER'] != 0].copy() if f == 'PER' else df
#                         obj.loc[obj['종목명'] == name, f] = (num[f] * num['크기'] / num['크기'].sum()).sum()
#         objs.append(obj)
#     objs.append(pd.DataFrame(
#         data=[[f'{self.name}{self.tag}', self.name, '', frm['크기'].sum()]],
#         columns=['종목코드', '종목명', '분류', '크기'], index=['Cover']
#     ))
#     aligned = pd.concat(objs=objs, axis=0, ignore_index=True)
#     dropper = [c for c in ['IPO', '거래량', '시가총액', '상장주식수', 'BPS', 'DPS', 'EPS'] if c in aligned.columns]
#     aligned = aligned.drop(columns=dropper)

#     key = aligned[aligned['종목명'] == aligned['분류']].copy()
#     if not key.empty:
#         aligned = aligned.drop(index=key.index)
#     return aligned