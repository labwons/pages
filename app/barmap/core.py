from pandas import DataFrame
from typing import List
import pandas as pd


def align(data:DataFrame, level:List[str]):
    base = data.reset_index(level=0).copy()
    keys = ['PBR', 'D-1', 'W-1', 'M-1', 'M-3', 'M-6', 'Y-1']
    objs = []
    for n, lev in enumerate(level):
        if lev == 'ticker':
            base['cover'] = base['sectorName']
            objs.append(base)
            continue
        obj = DataFrame()
        cover = base.groupby(by=level[n:]).sum().reset_index()
        obj['ticker'] = cover[lev]
        obj['name'] = cover['name']
        obj['cover'] = cover[level[n + 1]] if (n + 1) < len(level) else "전체"
        obj['size'] = cover['size']
        for name in obj['name']:
            np = base[base[lev] == name].copy()
            pe = base[(base[lev] == name) & (base['PER'] != 0)].copy()
            
            np['weight'] = np['size'] / np['size'].sum()
            pe['weight'] = pe['size'] / pe['size'].sum()
            obj.loc[obj['name'] == name, 'DIV'] = 0 if np.empty else np['DIV'].mean()            
            obj.loc[obj['name'] == name, 'PER'] = (pe['PER'] * pe['weight']).sum()
            obj.loc[obj['name'] == name, keys] = (np[keys] * np['weight']).sum()
        objs.append(obj)
    # top = DataFrame()
    # objs.append()
    return pd.concat(objs=objs, axis=0, ignore_index=True)
            
        
            