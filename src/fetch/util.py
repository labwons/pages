from bs4 import BeautifulSoup
from numpy import nan
from pandas import DataFrame, isna
from urllib.request import urlopen
from typing import Dict
import requests, json, pandas, warnings

warnings.filterwarnings("ignore")


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

class multiframes(DataFrame):

    __mem__ = {}
    def __init__(self, frames:Dict[str, DataFrame]):
        base = list(frames.values())[0]
        self.__mem__ = frames.copy()
        super().__init__(data=base.values, index=base.index, columns=base.columns)
        return

    def __getattr__(self, item):
        if item in self.__mem__:
            return self.__mem__[item]
        return super().__getattr__(name=item)


def str2num(src: str) -> int or float:
    if isinstance(src, float):
        return src
    src = "".join([char for char in src if char.isdigit() or char == "."])
    if not src or src == ".":
        return nan
    if "." in src:
        return float(src)
    return int(src)

def cutString(string:str, deleter:list) -> str:
    _deleter = deleter.copy()
    while _deleter:
        string = string.replace(_deleter.pop(0), '')
    return string

def krwFormat(krw: int) -> str:
    if krw is nan or isna(krw):
        return krw
    zo, euk = int(krw // 10000), int(krw % 10000)
    return f'{zo}조 {euk}억' if zo else f'{euk}억'


# Alias
web = _web()