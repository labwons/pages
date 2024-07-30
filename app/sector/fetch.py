try:
    from ..common.date import TradingDate
except ImportError:
    from app.common.date import TradingDate
from dataclasses import dataclass
from pandas import DataFrame
from typing import Dict, Union
import pandas as pd
import requests
import time


def index_name(name:str) -> str:
    if not name.upper() in ['WICS', 'WI26']:
        raise KeyError(f'Unknown INDEX type: {name}')
    return name.upper()

def index_date() -> str:
    html = requests.get('https://www.wiseindex.com/Index/Index#/G1010.0.Components').text
    pin1 = html.find("기준일")
    pin2 = pin1 + html[pin1:].find("</p>")
    return html[pin1 + 6 : pin2].replace(".", "")

def index_component(date:str, code:str, try_count:int=5) -> DataFrame:
    columns = {
        'CMP_CD': 'ticker', 'CMP_KOR': 'name',        
        'SEC_CD': 'sectorCode', 'SEC_NM_KOR': 'sectorName', 'ALL_MKT_VAL': 'sectorCap', 'WGT': 'sectorWeight',
        'IDX_CD': 'industryCode', 'IDX_NM_KOR': 'industryName',        
    }
    url = f'http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={date}&sec_cd={code}'
    for n in range(try_count):
        resp = requests.get(url)
        if resp.status_code == 200:
            data = DataFrame(resp.json()['list'])[columns.keys()]
            return data.rename(columns=columns).set_index(keys='ticker')
        time.sleep(5)
    raise TimeoutError(f'Unable to fetch WISE INDEX url: {url}')

KEYS = {
    "WICS": {
        'G1010': '에너지',
        'G1510': '소재',
        'G2010': '자본재',
        'G2020': '상업서비스와공급품',
        'G2030': '운송',
        'G2510': '자동차와부품',
        'G2520': '내구소비재와의류',
        'G2530': '호텔,레스토랑,레저 등',
        'G2550': '소매(유통)',
        'G2560': '교육서비스',
        'G3010': '식품과기본식료품소매',
        'G3020': '식품,음료,담배',
        'G3030': '가정용품과개인용품',
        'G3510': '건강관리장비와서비스',
        'G3520': '제약과생물공학',
        'G4010': '은행',
        'G4020': '증권',
        'G4030': '다각화된금융',
        'G4040': '보험',
        'G4050': '부동산',
        'G4510': '소프트웨어와서비스',
        'G4520': '기술하드웨어와장비',
        'G4530': '반도체와반도체장비',
        'G4535': '전자와 전기제품',
        'G4540': '디스플레이',
        'G5010': '전기통신서비스',
        'G5020': '미디어와엔터테인먼트',
        'G5510': '유틸리티'
    },
    "WI26": {
        'WI100': '에너지',
        'WI110': '화학',
        'WI200': '비철금속',
        'WI210': '철강',
        'WI220': '건설',
        'WI230': '기계',
        'WI240': '조선',
        'WI250': '상사,자본재',
        'WI260': '운송',
        'WI300': '자동차',
        'WI310': '화장품,의류',
        'WI320': '호텔,레저',
        'WI330': '미디어,교육',
        'WI340': '소매(유통)',
        'WI400': '필수소비재',
        'WI410': '건강관리',
        'WI500': '은행',
        'WI510': '증권',
        'WI520': '보험',
        'WI600': '소프트웨어',
        'WI610': 'IT하드웨어',
        'WI620': '반도체',
        'WI630': 'IT가전',
        'WI640': '디스플레이',
        'WI700': '통신서비스',
        'WI800': '유틸리티',
    }
}
# def fetch(key:Union[str, Dict]) -> DataFrame:
#     def _fetch(code:str, try_count:int=5) -> DataFrame:
#         for n in range(try_count):
#             resp = requests.get(KEY.URL(TradingDate.wiseDate, code))
#             if resp.status_code == 200:
#                 data = DataFrame(resp.json()['list'])[KEY.COLUMNS.keys()]
#                 return data.rename(columns=KEY.COLUMNS)
#             time.sleep(5)
#         raise TimeoutError(f'Unable to fetch WISE INDEX code: {code}')

#     if isinstance(key, str):
#         if key.upper() == 'WICS':
#             index = KEY.WICS
#         elif key.upper() == 'WI26':
#             index = KEY.WI26
#         else:
#             raise KeyError(f'Unknown MAP Type: {key}')
#     elif isinstance(key, Dict):
#         index = key
#     return pd.concat(
#         objs=[_fetch(code) for code in index],
#         axis=0,
#         ignore_index=True
#     ).set_index(keys='ticker', inplace=True)
        