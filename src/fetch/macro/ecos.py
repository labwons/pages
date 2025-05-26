try:
    from ..web import web
except ImportError:
    from src.fetch.web import web
from datetime import datetime
from pandas import concat, DataFrame, Series, to_datetime
from xml.etree.ElementTree import ElementTree, fromstring


class Ecos(DataFrame):
    """
    ECOS (Bank of Korea, Economic Statistics System) Provided data
    * API key required for this <class; ecos>

    @data:
        type        : DataFrame
        description : listed economic index with implicit information
        example     :
                                                       name  cycle        by
            symbol
            102Y004   본원통화 구성내역(평잔, 계절조정계열)      M      None
            102Y002         본원통화 구성내역(평잔, 원계열)      M      None
            102Y003   본원통화 구성내역(말잔, 계절조정계열)      M      None
            102Y001         본원통화 구성내역(말잔, 원계열)      M  한국은행
            101Y018  M1 상품별 구성내역(평잔, 계절조정계열)      M      None
            ...                                         ...    ...       ...
            251Y003                                    총량      A      None
            251Y002                          한국/북한 배율      A      None
            251Y001            북한의 경제활동별 국내총생산      A  한국은행
            252Y001                            시장물가지수      Q  한국은행
            252Y002                                시장환율      Q  한국은행

    @container:
        type        : Callable
        description : layered list of @data
        example     :
            ''' self.container("252Y001") '''
                  이름     코드  주기    시점    종점  개수
            0   총지수  A110000     A    2006    2022    17
            1   총지수  A110000     Q  2006Q1  2022Q4    68
            2   식료품  A111000     A    2006    2022    17
            3   식료품  A111000     Q  2006Q1  2022Q4    68
            4     곡물  A111100     A    2006    2022    17
            ..     ...      ...    ..     ...     ...    ..
            83    석탄  B121200     Q  2006Q1  2022Q4    68
            84  휘발유  B121300     A    2006    2022    17
            85  휘발유  B121300     Q  2006Q1  2022Q4    68
            86    경유  B121400     A    2006    2022    17
            87    경유  B121400     Q  2006Q1  2022Q4    68

    @fetch:
        type        : Callable
        description : time-series data of given symbol
                      return priority to the data majority (the number of dataset), not controllable
        example     :
            ''' self.fetch("252Y001", "총지수") '''
            time
            2006-03-31      0.073
            2006-06-30      0.077
            2006-09-30      0.075
            2006-12-31      0.082
            2007-03-31      0.101
                           ...
            2021-12-31    116.100
            2022-03-31    107.600
            2022-06-30    127.600
            2022-09-30    121.700
            2022-12-31    120.600
            Freq: Q-DEC, Name: 총지수, Length: 68, dtype: float64
    """
    api:str = ""
    src:DataFrame = DataFrame()
    meta = {}
    raw = {
        '기준금리': {
            'symbol': '722Y001',
            'code': '0101000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        'KORIBOR(3개월)': {
            'symbol': '817Y002',
            'code': '010150000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        'KORIBOR(6개월)': {
            'symbol': '817Y002',
            'code': '010151000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '국고채1년': {
            'symbol': '817Y002',
            'code': '010190000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '국고채2년': {
            'symbol': '817Y002',
            'code': '010195000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '국고채5년': {
            'symbol': '817Y002',
            'code': '010200001',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '국고채10년': {
            'symbol': '817Y002',
            'code': '010210000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '회사채3년(AA-)': {
            'symbol': '817Y002',
            'code': '010300000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '회사채3년(BBB-)': {
            'symbol': '817Y002',
            'code': '010320000',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '은행수신금리(신규)': {
            'symbol': '121Y002',
            'code': 'BEABAA2',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '은행수신금리(잔액)': {
            'symbol': '121Y013',
            'code': 'BEABAB2',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '은행대출금리(신규)': {
            'symbol': '121Y006',
            'code': 'BECBLA01',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },
        '은행대출금리(잔액)': {
            'symbol': '121Y015',
            'code': 'BECBLB01',
            'unit': '%',
            'category': '금리지표',
            'YoY': False,
            'MoM': False
        },

        '원/달러환율': {
            'symbol': '731Y003',
            'code': '0000003',
            'unit': '원',
            'category': '통화/유동성지표',
            'YoY': False,
            'MoM': False
        },
        'M2(평잔, 원계열)': {
            'symbol': '101Y004',
            'code': 'BBHA00',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        'M2(평잔, 계절조정)': {
            'symbol': '101Y003',
            'code': 'BBHS00',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '은행수신(말잔)': {
            'symbol': '104Y013',
            'code': 'BCB8',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '은행수신(평잔)': {
            'symbol': '104Y014',
            'code': 'BCA8',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '비은행수신(말잔)': {
            'symbol': '111Y007',
            'code': '1000000',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '비은행수신(평잔)': {
            'symbol': '111Y008',
            'code': '1000000',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '은행여신(말잔)': {
            'symbol': '104Y016',
            'code': 'BDCA1',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '비은행여신(말잔)': {
            'symbol': '111Y009',
            'code': '1000000',
            'unit': '십억원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': True
        },
        '증시예탁금': {
            'symbol': '901Y056',
            'code': 'S23A',
            'unit': '백만원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '신용융자잔고': {
            'symbol': '901Y056',
            'code': 'S23E',
            'unit': '백만원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },
        '신용대주잔고': {
            'symbol': '901Y056',
            'code': 'S23F',
            'unit': '백만원',
            'category': '통화/유동성지표',
            'YoY': True,
            'MoM': False
        },

        '수출지수': {
            'symbol': '403Y001',
            'code': '*AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '반도체수출': {
            'symbol': '403Y001',
            'code': '3091AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '반도체/디스플레이장비수출': {
            'symbol': '403Y001',
            'code': '3091AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '스마트폰/무선전화기수출': {
            'symbol': '403Y001',
            'code': '309512AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '자동차수출': {
            'symbol': '403Y001',
            'code': '3121AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '자동차부품수출': {
            'symbol': '403Y001',
            'code': '31213AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '음식료품수출': {
            'symbol': '403Y001',
            'code': '301AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '석탄및석유제품수출': {
            'symbol': '403Y001',
            'code': '304AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '철강수출': {
            'symbol': '403Y001',
            'code': '3071AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '전지수출': {
            'symbol': '403Y001',
            'code': '31013AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },
        '가전수출': {
            'symbol': '403Y001',
            'code': '31015AA',
            'unit': '-',
            'category': '수출지표',
            'YoY': True,
            'MoM': False
        },

        '소비자물가지수': {
            'symbol': '901Y009',
            'code': '0',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },
        '소비자물가지수(식료품 및 에너지 제외)': {
            'symbol': '901Y010',
            'code': 'DB',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },
        '소비자물가지수(서비스)': {
            'symbol': '901Y010',
            'code': '22',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },
        '생산자물가지수': {
            'symbol': '404Y014',
            'code': '*AA',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },
        '생산자물가지수(식료품 및 에너지 제외)': {
            'symbol': '404Y015',
            'code': 'S620AA',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },
        '생산자물가지수(서비스)': {
            'symbol': '404Y014',
            'code': '5AA',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': False
        },

        'KB부동산매매지수(아파트, 전국)': {
            'symbol': '901Y062',
            'code': 'P63AC',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        'KB부동산매매지수(아파트, 서울)': {
            'symbol': '901Y062',
            'code': 'P63ACA',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        'KB부동산전세지수(아파트, 전국)': {
            'symbol': '901Y063',
            'code': 'P64AC',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        'KB부동산전세지수(아파트, 서울)': {
            'symbol': '901Y063',
            'code': 'P64ACA',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        '아파트실거래지수(전국)': {
            'symbol': '901Y089',
            'code': '100',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        '아파트실거래지수(서울)': {
            'symbol': '901Y089',
            'code': '200',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        '아파트실거래지수(수도권)': {
            'symbol': '901Y089',
            'code': '300',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        '아파트실거래지수(경기)': {
            'symbol': '901Y089',
            'code': 'C00',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },
        '아파트실거래지수(지방광역시)': {
            'symbol': '901Y089',
            'code': 'M00',
            'unit': '-',
            'category': '물가/부동산지표',
            'YoY': True,
            'MoM': True
        },

        '경기선행지수순환변동': {
            'symbol': '901Y067',
            'code': 'I16E',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': False,
            'MoM': False
        },
        '경기동행지수순환변동': {
            'symbol': '901Y067',
            'code': 'I16D',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': False,
            'MoM': False
        },
        '제조업업황전망': {
            'symbol': '512Y014',
            'code': 'C0000/BA',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': True,
            'MoM': True
        },
        '제조업신규수주전망': {
            'symbol': '512Y014',
            'code': 'C0000/BD',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': True,
            'MoM': True
        },
        '제조업수출전망': {
            'symbol': '512Y014',
            'code': 'C0000/BM',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': True,
            'MoM': True
        },
        '제조업심리지수': {
            'symbol': '512Y014',
            'code': 'C0000/BY',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': True,
            'MoM': True
        },
        '소비자심리지수': {
            'symbol': '511Y002',
            'code': 'FME/99988',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': True,
            'MoM': True
        },
        '뉴스심리지수(실험통계)': {
            'symbol': '521Y001',
            'code': 'A001',
            'unit': '-',
            'category': '경제/심리지표',
            'YoY': False,
            'MoM': False
        },
        '실업률(원계열)': {
            'symbol': '901Y027',
            'code': 'I61BC/I28A',
            'unit': '%',
            'category': '경제/심리지표',
            'YoY': False,
            'MoM': False
        },
        '실업률(계절조정)': {
            'symbol': '901Y027',
            'code': 'I61BC/I28B',
            'unit': '%',
            'category': '경제/심리지표',
            'YoY': False,
            'MoM': False
        },
    }

    def __init__(self):
        self.src = self.fetchSrc()

        objs = {}
        for name, meta in self.raw.items():
            code = f'{meta["symbol"]}{meta["code"]}'
            data = self.fetch(meta['symbol'], meta['code'])
            self.meta[code] = {
                'name': name,
                'unit': meta['unit'],
                'category': meta['category']
            }
            objs[code] = data.copy()
            if meta["YoY"]:
                self.meta[f'{code}YoY'] = {
                    'name': f'{name}(YoY)',
                    'unit': '%',
                    'category': meta['category']
                }
                objs[f'{code}YoY'] = data.dropna().asfreq('M').pct_change(periods=12) * 100
                if name.startswith('신용대주'):
                    objs[f'{code}YoY'] = objs[f'{code}YoY'].clip(upper=2000)

            if meta["MoM"]:
                self.meta[f'{code}MoM'] = {
                    'name': f'{name}(MoM)',
                    'unit': '%',
                    'category': meta['category']
                }
                objs[f'{name}(MoM)'] = data.dropna().asfreq('M').pct_change(periods=1) * 100

            if code == '121Y015BECBLB01':
                self.meta['T10MT2'] = {
                    'name': '장단기금리차(10Y-2Y)',
                    'unit': '%',
                    'category': '금리지표'
                }
                objs['T10MT2'] = objs['817Y002010210000'] - objs['817Y002010195000']
                self.meta['HYSPREAD'] = {
                    'name': '하이일드스프레드',
                    'unit': '%',
                    'category': '금리지표'
                }
                objs['HYSPREAD'] = objs['817Y002010320000'] - objs['817Y002010210000']
                self.meta['LBDIFFN'] = {
                    'name': '예대금리차(신규)',
                    'unit': '%',
                    'category': '금리지표'
                }
                objs['LBDIFFN'] = objs['121Y006BECBLA01'] - objs['121Y002BEABAA2']
                self.meta['LBDIFFL'] = {
                    'name': '예대금리차(잔액)',
                    'unit': '%',
                    'category': '금리지표'
                }
                objs['LBDIFFL'] = objs['121Y015BECBLB01'] - objs['121Y013BEABAB2']

        df = concat(objs=objs, axis=1)
        super().__init__(df[df.index >= datetime(1990, 1, 1)])
        return

    def __call__(self, symbol: str, *args):
        return self.fetch(symbol, *args)

    @classmethod
    def container(cls, symbol: str) -> DataFrame:
        columns = {
            "ITEM_NAME":'name',
            "ITEM_CODE":'code',
            "CYCLE":'freq',
            "START_TIME":'startdate',
            "END_TIME":'enddate',
            "DATA_CNT":'count'
        }
        url = f"http://ecos.bok.or.kr/api/StatisticItemList/{cls.api}/xml/kr/1/10000/{symbol}"
        return cls.xml2df(url=url, parser="xml")[columns.keys()].rename(columns=columns)

    @classmethod
    def fetchSrc(cls) -> DataFrame:
        columns = {
            "STAT_CODE": "symbol",
            "STAT_NAME": "name",
            "CYCLE": "cycle",
            "ORG_NAME": "by"
        }
        url = f'http://ecos.bok.or.kr/api/StatisticTableList/{cls.api}/xml/kr/1/10000/'
        data = cls.xml2df(url=url, parser="xml")
        data = data[data.SRCH_YN == 'Y'].copy()
        data['STAT_NAME'] = data["STAT_NAME"].apply(lambda x: x[x.find(' ') + 1:])
        data = data.rename(columns=columns)
        return data[columns.values()].set_index(keys='symbol')

    @classmethod
    def fetch(cls, symbol: str, code: str) -> Series:
        layer = cls.container(symbol)
        if layer.empty:
            return Series()
        layer = layer.set_index(keys="code")
        if len(layer) > 1:
            for _freq in ['D', 'M', 'Q', 'A']:
                if _freq in layer['freq'].values:
                    layer = layer[layer['freq'] == _freq]
                    break
        layer = layer.loc[code.split("/")[0]].to_dict()

        url = f'http://ecos.bok.or.kr/api/StatisticSearch/{cls.api}/' \
              f'xml/' \
              f'kr/' \
              f'1/' \
              f'100000/' \
              f'{symbol}/' \
              f'{layer["freq"]}/' \
              f'{layer["startdate"]}/' \
              f'{layer["enddate"]}/' \
              f'{code}'
        fetch = cls.xml2df(url=url, parser="xml")
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

    @classmethod
    def xml2df(cls, url: str, parser: str = "") -> DataFrame:
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
        resp = web.html(url, parser)
        root = ElementTree(fromstring(str(resp))).getroot()
        data = list()
        for tag in root.findall('row'):
            getter = dict()
            for n, t in enumerate([inner for inner in tag.iter()]):
                if t.tag in exclude:
                    continue
                getter.update({t.tag: t.text})
            data.append(getter)
        return DataFrame(data=data) if data else DataFrame()



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    Ecos.api = "CEW3KQU603E6GA8VX0O9"
    Ecos = Ecos()
    # print(Ecos.container("252Y001"))
    # print(Ecos("252Y001", "총지수"))
    print(Ecos)




