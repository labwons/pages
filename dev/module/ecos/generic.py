try:
    from ...common.path import PATH
    from .core import PREDEF, xml2df
except ImportError:
    from dev.common.path import PATH
    from dev.module.ecos.core import PREDEF, xml2df
from pandas import DataFrame, Series
import pandas as pd
import json


class _ecos:

    def __init__(self, api:str=""):
        self.__api__:str = api
        return

    def __call__(self) -> DataFrame:
        return self.serviceData

    def __getitem__(self, item: str) -> Series:
        return self.userDefine[item]

    def __repr__(self) -> repr:
        return repr(self.serviceData)

    @property
    def api(self):
        return self.__api__

    @api.setter
    def api(self, api:str):
        self.__api__ = api
        return

    @property
    def serviceData(self) -> DataFrame:
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
        if not hasattr(self, "__meta__"):
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
            self.__setattr__("__meta__", data[columns.values()].set_index(keys='symbol'))
        return self.__getattribute__("__meta__")

    @property
    def userDefine(self) -> DataFrame:
        if not hasattr(self, "__user__"):
            objs = {}
            for symbol, attr in PREDEF.items():
                for code, name in attr["code"].items():
                    objs[f"{symbol}_{code}"] = self.data(symbol, code)
            self.__setattr__("__user__", pd.concat(objs=objs, axis=1))
        return self.__getattribute__("__user__")

    @property
    def METADATA(self) -> dict:
        meta = {}
        for symbol, attr in PREDEF.items():
            for code, name in attr["code"].items():
                meta[f'{symbol}_{code.replace("*", "")}'] = {
                    "name": f"{attr['name']}/{name}",
                    "unit": attr["unit"],
                    "category": attr["category"]
                }
        return meta

    def container(self, symbol:str, **kwargs):
        columns = {
            "ITEM_NAME": 'name',
            "ITEM_CODE": 'code',
            "CYCLE": 'freq',
            "START_TIME": 'startdate',
            "END_TIME": 'enddate',
            "DATA_CNT": 'count',
            "UNIT_NAME": "unit"
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
        layer = layer.loc[code.split("/")[0]].to_dict()

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

    def dump(self):
        objs = {}
        for col in self.userDefine:
            series = self.userDefine[col].dropna()
            objs[col] = {
                'date': series.index.strftime("%Y-%m-%d").tolist(),
                'data': series.tolist()
            }
        string = json.dumps(objs)
        if not PATH.ECOS.startswith('http'):
            with open(PATH.ECOS, 'w') as f:
                f.write(string)
        return objs


# Alias
Ecos = _ecos()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    import time

    Ecos.api = "CEW3KQU603E6GA8VX0O9"
    # print(Ecos)
    # cont = Ecos.container('901Y027')
    # print(cont)
    # print(cont[cont["name"] == '가정용전기기기'])

    # print(Ecos.data('731Y003', '0000002'))
    # print(Ecos.data('403Y001', '31211AA'))
    # print(Ecos.data('101Y003', 'BBHS00'))
    # print(Ecos.data('512Y014', 'C0000/BY'))
    # print(Ecos.data('511Y002', "FME/99988"))
    # print(Ecos.userDefine)
    # print(Ecos.METADATA)
    print(Ecos.dump())