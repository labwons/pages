from bs4 import BeautifulSoup
from pandas import DataFrame
from typing import List
import pandas as pd
import requests, re


class Web:

    __req__:dict = {}
    __tbl__:dict = {}

    @classmethod
    def get(cls, url:str, encoding:str='', **kwargs):
        if not url in cls.__req__:
            resp = requests.get(url)
            if not resp.status_code == 200:
                return
            if encoding:
                resp.encoding = encoding
            cls.__req__[url] = resp
        return cls.__req__[url]

    @classmethod
    def text(cls, url:str, **kwargs):
        resp = cls.get(url, **kwargs)
        if resp is None:
            return
        text = resp.text.replace("<![CDATA[", "").replace("]]>", "")
        text = re.sub(r'<business_summary>.*?</business_summary>', '', text, flags=re.DOTALL)
        return text

    @classmethod
    def parser(cls, url:str, parser:str='', **kwargs) -> BeautifulSoup:
        if not parser:
            parser = "xml" if url.endswith('xml') else "lxml"
        return BeautifulSoup(cls.text(url, **kwargs), parser)

    @classmethod
    def tables(cls, url:str, **kwargs) -> List[DataFrame]:
        if url in cls.__tbl__:
            return cls.__tbl__[url]
        df = pd.read_html(io=cls.text(url), **kwargs)
        cls.__tbl__[url] = df
        return df

    @classmethod
    def refresh(cls, url:str, encoding:str=''):
        resp = requests.get(url)
        if resp.status_code != 200:
            return
        cls.__req__[url] = resp
        return cls.__req__[url]
