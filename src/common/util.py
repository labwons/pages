from bs4 import BeautifulSoup
from numpy import nan
from pandas import DataFrame, isna
from urllib.request import urlopen
from typing import Dict
from numpy import isnan, nan
from pandas import isna
from typing import Union
import requests, json, pandas, warnings

class _web(object):

    def req(self, url:str):
        attr = f"_req_{url}_"
        if not hasattr(self, attr):
            req = requests.get(url, verify=False)
            if not req.status_code == 200:
                raise ConnectionError
            self.__setattr__(attr, req)
        return self.__getattribute__(attr)

    def html(self, url:str, parser:str="") -> BeautifulSoup:
        attr = f"_html_{url}_"
        if not hasattr(self, attr):
            parser = parser if parser else 'xml' if url.endswith('.xml') else 'lxml'
            self.__setattr__(attr, BeautifulSoup(self.req(url).text, parser))
        return self.__getattribute__(attr)

    def list(self, url:str, encoding:str='utf-8', displayed_only:bool=False) -> list:
        attr = f"_list_{url}_"
        if not hasattr(self, attr):
            encoding = "euc-kr" if "naver" in url else encoding
            self.__setattr__(attr, pandas.read_html(io=url, header=0, encoding=encoding, displayed_only=displayed_only))
        return self.__getattribute__(attr)

    def json(self, url:str) -> json:
        attr = f"_json_{url}_"
        if not hasattr(self, attr):
            data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
            self.__setattr__(attr, data)
        return self.__getattribute__(attr)

    def data(self, url:str, key:str=""):
        if url.endswith('.json'):
            return pandas.DataFrame(self.json(url)[key] if key else self.json(url))
        elif url.endswith('.csv'):
            return pandas.read_csv(url, encoding='utf-8')
        elif url.endswith('.pkl'):
            return pandas.read_pickle(url)
        else:
            raise KeyError(f"Unknown data type: {url}")

def krw2currency(krw: int) -> Union[str, float]:
    """
    KRW (원화) 입력 시 화폐 표기 법으로 변환(자동 계산)
    @krw 단위는 원 일 것
    """
    if isna(krw) or isnan(krw):
        return nan
    if krw >= 1e+12:
        krw /= 1e+8
        return f'{int(krw // 10000)}조 {int(krw % 10000)}억'
    if krw >= 1e+8:
        krw /= 1e+4
        return f'{int(krw // 10000)}억 {int(krw % 10000)}만'
    return f'{int(krw // 10000)}만'



# Alias
web = _web()