from labwons.util import DP
from labwons.fetch.macro.schema import FIELD_ECOS

from datetime import datetime
from pandas import concat, DataFrame, Series, to_datetime
from time import perf_counter
from typing import Dict, List
from xml.etree.ElementTree import ElementTree, fromstring
import requests


API = "CEW3KQU603E6GA8VX0O9"
class MacroEcos:
    """
    ECOS (Bank of Korea, Economic Statistics System) Provided data
    * API key required for this <class; ecos>
    """

    def __init__(self, api:str):
        self.api = api
        self.xml: Dict[str, BeautifulSoup] = {}
        return

    def __call__(self, symbol: str, *args):
        return self.fetch(symbol, *args)

    @property
    def FIELD(self) -> DataFrame:
        """
        type        : DataFrame
        description : listed economic index with implicit information
        example     :
                                                       name  cycle        by
            symbol
            102Y004   본원통화 구성내역(평잔, 계절조정계열)      M      None
            102Y002         본원통화 구성내역(평잔, 원계열)      M      None
            102Y003   본원통화 구성내역(말잔, 계절조정계열)      M      None
            ...                                       ...    ...       ...
            251Y001            북한의 경제활동별 국내총생산      A  한국은행
            252Y001                           시장물가지수      Q  한국은행
            252Y002                               시장환율      Q  한국은행
        """
        if not hasattr(self, '__FIELD__'):
            columns = {
                "STAT_CODE": "symbol",
                "STAT_NAME": "name",
                "CYCLE": "cycle",
                "ORG_NAME": "by"
            }
            url = f'http://ecos.bok.or.kr/api/StatisticTableList/{self.api}/xml/kr/1/10000/'
            data = self.xml2df(url=url)
            data = data[data['SRCH_YN'] == 'Y'].copy()
            data['STAT_NAME'] = data["STAT_NAME"].apply(lambda x: x[x.find(' ') + 1:])
            data = data.rename(columns=columns)
            self.__FIELD__ = data[columns.values()].set_index(keys='symbol')
        return self.__FIELD__

    def container(self, symbol: str) -> DataFrame:
        """
        type        : Callable
        description : layered list of @data
        example     :
            ''' self.container("252Y001") '''
                  이름     코드  주기    시점    종점  개수
            0   총지수  A110000     A    2006    2022    17
            1   총지수  A110000     Q  2006Q1  2022Q4    68
            2   식료품  A111000     A    2006    2022    17
            ..     ...      ...    ..     ...     ...    ..
            85  휘발유  B121300     Q  2006Q1  2022Q4    68
            86    경유  B121400     A    2006    2022    17
            87    경유  B121400     Q  2006Q1  2022Q4    68
        """
        columns = {
            "ITEM_NAME":'name',
            "ITEM_CODE":'code',
            "CYCLE":'freq',
            "START_TIME":'startdate',
            "END_TIME":'enddate',
            "DATA_CNT":'count'
        }
        url = f"http://ecos.bok.or.kr/api/StatisticItemList/{self.api}/xml/kr/1/10000/{symbol}"
        return self.xml2df(url=url)[columns.keys()].rename(columns=columns)


    def fetch(self, symbol: str, code: str) -> Series:
        """
        type        : Callable
        description : time-series data of given symbol
                      return priority to the data majority (the number of dataset), not controllable
        example     :
            ''' self.fetch("252Y001", "총지수") '''
            time
            2006-03-31      0.073
            2006-06-30      0.077
            2006-09-30      0.075
                           ...
            2022-06-30    127.600
            2022-09-30    121.700
            2022-12-31    120.600
            Freq: Q-DEC, Name: 총지수, Length: 68, dtype: float64
        """
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
        fetch = self.xml2df(url=url)
        dtype = {"A": "%Y", "Q": "%Y%m", "M": "%Y%m", "D": "%Y%m%d"}[layer["freq"]]

        if layer["freq"] == "Q":
            split = fetch.TIME.str.split("Q", expand=True).astype(int)
            split["time"] = split[0].astype(str) + (3 * split[1]).astype(str).str.zfill(2)
            index = to_datetime(split.time, format=dtype)
        else:
            index = to_datetime(fetch.TIME, format=dtype)
        series = Series(name=layer["name"], index=index, data=fetch.DATA_VALUE.values, dtype=float)
        if not layer["freq"] == "D":
            series.index = series.index.to_period("M").to_timestamp("M")
        return series


    def xml2df(self, url: str) -> DataFrame:
        """
        정보-100 : 인증키가 유효하지 않습니다.
                   인증키를 확인하십시오! 인증키가 없는 경우 인증키를 신청하십시오!
        정보-200 : 해당하는 데이터가 없습니다.
        에러-100 : 필수 값이 누락되어 있습니다.
                   필수 값을 확인하십시오! 필수 값이 누락되어 있으면 오류를 발생합니다.
                   요청 변수를 참고 하십시오!
        에러-101 : 주기와 다른 형식의 날짜 형식입니다.
        에러-200 : 파일타입 값이 누락 혹은 유효하지 않습니다.
                   파일타입 값을 확인하십시오!
                   파일타입 값이 누락 혹은 유효하지 않으면 오류를 발생합니다.
                   요청 변수를 참고 하십시오!
        에러-300 : 조회건수 값이 누락되어 있습니다.
                   조회시작건수/조회종료건수 값을 확인하십시오!
                   조회시작건수/조회종료건수 값이 누락되어 있으면 오류를 발생합니다.
        에러-301 : 조회건수 값의 타입이 유효하지 않습니다.
                   조회건수 값을 확인하십시오!
                   조회건수 값의 타입이 유효하지 않으면 오류를 발생합니다.
                   정수를 입력하세요.
        에러-400 : 검색범위가 적정범위를 초과하여 60초 TIMEOUT이 발생하였습니다.
                   요청조건 조정하여 다시 요청하시기 바랍니다.
        에러-500 : 서버 오류입니다.
                   OpenAPI 호출시 서버에서 오류가 발생하였습니다.
                   해당 서비스를 찾을 수 없습니다.
        에러-600 : DB Connection 오류입니다.
                   OpenAPI 호출시 서버에서 DB접속 오류가 발생했습니다.
        에러-601 : SQL 오류입니다.
                   OpenAPI 호출시 서버에서 SQL 오류가 발생했습니다.
        에러-602 : 과도한 OpenAPI호출로 이용이 제한되었습니다.
                   잠시후 이용해주시기 바랍니다.
        """
        exclude = ['row', 'P_STAT_CODE']
        if not url in self.xml:
            self.xml[url] = requests.get(url).text

        root = ElementTree(fromstring(self.xml[url])).getroot()
        data = list()
        for tag in root.findall('row'):
            getter = dict()
            for n, t in enumerate([inner for inner in tag.iter()]):
                if t.tag in exclude:
                    continue
                getter.update({t.tag: t.text})
            data.append(getter)
        return DataFrame(data=data) if data else DataFrame()

    def merge(self) -> DataFrame:
        conv = {'십억원': 1e+9, '억원': 1e+8, '천만원': 1e+7, '백만원': 1e+6}

        objs = {}
        for label, meta in FIELD_ECOS.items():
            code = f'{meta.symbol}{meta.code}'
            try:
                objs[code] = series = self.fetch(meta.symbol, meta.code)
            except Exception as reason:
                print(f'- FAILED TO FETCH: {label}: {reason}')
                continue

        #     if meta.unit in conv:
        #         objs[f'{code}Text'] = (conv[meta.unit] * objs[code]).apply(DP.krw2currency)
        #
        #     if meta.YoY:
        #         objs[f'{code}YoY'] = series.dropna().asfreq('M').pct_change(periods=12) * 100
        #         if label.startswith('신용대주'):
        #             objs[f'{code}YoY'] = objs[f'{code}YoY'].clip(upper=2000)
        #
        #     if meta["MoM"]:
        #         objs[f'{code}MoM'] = series.dropna().asfreq('M').pct_change(periods=1) * 100
        #
        #     if code == '121Y015BECBLB01':
        #         # 장단기금리차(10Y - 2Y)
        #         objs['T10MT2'] = objs['817Y002010210000'] - objs['817Y002010195000']
        #
        #         # 하이일드스프레드
        #         objs['HYSPREAD'] = objs['817Y002010320000'] - objs['817Y002010210000']
        #
        #         # 예대금리차(신규)
        #         objs['LBDIFFN'] = objs['121Y006BECBLA01'] - objs['121Y002BEABAA2']
        #
        #         # 예대금리차(잔액)
        #         objs['LBDIFFL'] = objs['121Y015BECBLB01'] - objs['121Y013BEABAB2']
        # data = concat(objs=objs, axis=1)
        # data = data[data.index >= datetime(1990, 1, 1)]
        #
        # self.log = f'  >> END: {perf_counter() - stime:.2f}s'
        return concat(objs=objs, axis=1)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ecos = MacroEcos(API)
    # print(ecos.FIELD)
    # print(ecos.container('252Y001'))
    # print(ecos.fetch('101Y003', 'BBHS00'))

    print(ecos.merge())
