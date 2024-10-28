try:
    from .core import xml2df
except ImportError:
    from dev.module.ecos.core import xml2df
from pandas import DataFrame, Index, Series
from typing import Dict, Union
import pandas as pd


class _ecos:

    def __init__(self, api:str=""):
        self.__api__:str = api
        self.__mem__:Dict[str, Union[DataFrame, Series]] = {}
        self.__sym__:DataFrame = DataFrame()
        return

    def __call__(self) -> DataFrame:
        return self.metadata

    def __contains__(self, item):
        return item in self.metadata.index

    def __repr__(self) -> repr:
        return repr(self.metadata)

    @property
    def api(self):
        return self.__api__

    @api.setter
    def api(self, api:str):
        self.__api__ = api
        return

    @property
    def metadata(self) -> DataFrame:
        """
        return:
                                                   name cycle        by
        symbol
        102Y004   본원통화 구성내역(평잔, 계절조정계열)     M      None
        102Y002         본원통화 구성내역(평잔, 원계열)     M      None
        102Y003   본원통화 구성내역(말잔, 계절조정계열)     M      None
        102Y001         본원통화 구성내역(말잔, 원계열)     M  한국은행
        101Y018  M1 상품별 구성내역(평잔, 계절조정계열)     M      None
        ...                                         ...   ...       ...
        251Y003                                    총량     A      None
        251Y002                          한국/북한 배율     A      None
        251Y001            북한의 경제활동별 국내총생산     A  한국은행
        252Y001                            시장물가지수     Q  한국은행
        252Y002                                시장환율     Q  한국은행
        """
        if self.__sym__.empty:
            columns = {
                "STAT_CODE": "symbol",
                "STAT_NAME": "name",
                "CYCLE": "cycle",
                "ORG_NAME": "by"
            }
            url = f'http://ecos.bok.or.kr/api/StatisticTableList/{self.api}/xml/kr/1/10000/'
            data = xml2df(url=url, parser="xml")
            data = data[data.SRCH_YN == 'Y'].copy()
            data['STAT_NAME'] = data["STAT_NAME"].apply(lambda x: x[x.find(' ') + 1:])
            data = data.rename(columns=columns)
            self.__sym__ = data[columns.values()].set_index(keys='symbol')
        return self.__sym__

    @property
    def symbols(self) -> Index:
        return self.metadata.index

    def container(self, symbol:str, **kwargs):
        columns = {
            "ITEM_NAME": 'name',
            "ITEM_CODE": 'code',
            "CYCLE": 'freq',
            "START_TIME": 'startdate',
            "END_TIME": 'enddate',
            "DATA_CNT": 'count'
        }
        url = f"http://ecos.bok.or.kr/api/StatisticItemList/{self.api}/xml/kr/1/10000/{symbol}"
        get = xml2df(url=url, parser="xml")
        if get.empty:
            return get
        fetch = xml2df(url=url, parser="xml")[columns.keys()].rename(columns=columns)
        for key, value in kwargs.items():
            fetch = fetch[fetch[key] == value]
        return fetch

    def data(self, symbol:str, code:str) -> Series:
        layer = self.container(symbol)
        if layer.empty:
            return Series()
        layer = layer.set_index(keys="code")
        if len(layer) > 1:
            for _freq in ['D', 'M', 'Q', 'A']:
                if _freq in layer['freq'].values:
                    layer = layer[layer['freq'] == _freq]
                    break
        layer = layer.loc[code].to_dict()

        url = f'http://ecos.bok.or.kr/api/StatisticSearch/{self.api}/' \
              f'xml/' \
              f'kr/' \
              f'1/' \
              f'100000/' \
              f'{symbol}/' \
              f'{layer["freq"]}/' \
              f'{layer["startdate"]}/' \
              f'{layer["enddate"]}/' \
              f'{code}'
        fetch = xml2df(url=url, parser="xml")
        dtype = {"A": "%Y", "Q": "%Y%m", "M": "%Y%m", "D": "%Y%m%d"}[layer["freq"]]

        if layer["freq"] == "Q":
            split = fetch.TIME.str.split("Q", expand=True).astype(int)
            split["time"] = split[0].astype(str) + (3 * split[1]).astype(str).str.zfill(2)
            index = pd.to_datetime(split.time, format=dtype)
        else:
            index = pd.to_datetime(fetch.TIME, format=dtype)
        series = Series(name=layer["name"], index=index, data=fetch.DATA_VALUE.values, dtype=float)
        if not layer["freq"] == "D":
            series.index = series.index.to_period("M").to_timestamp("M")
        return series


# Alias
Ecos = _ecos()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    import time

    Ecos.api = "CEW3KQU603E6GA8VX0O9"
    # print(Ecos)
    cont = Ecos.container('403Y001')
    print(cont[cont["name"] == '가정용전기기기'])
    # print(Ecos.container('403Y001'))
    # print(Ecos.data('731Y003', '0000002'))
    # print(Ecos.data('403Y001', '31211AA'))
    # print(Ecos.data('403Y001', '3121AA'))