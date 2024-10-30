try:
    from ...common.web import Web
except ImportError:
    from dev.common.web import Web
from pandas import DataFrame
from xml.etree.ElementTree import  ElementTree, fromstring


__all__ = ["PREDEF", "xml2df"]

PREDEF = {
    "731Y003" : {
        'name': '원달러환율',
        'code': {
            "0000002":'시가',
            "0000005":'고가',
            "0000004":'저가',
            "0000003":'종가'
        },
        'category': '통화공급',
        'unit': '원',
    },
    "403Y001": {
        "name": '수출지수', # 금액
        "code": {
            '*AA': '총지수',
            '3091AA': '반도체',
            '31124AA': '반도체및디스플레이제조기계',
            '309512AA': '이동전화기',
            '3121AA': '자동차',
            '31213AA': '자동차부품',
            '310131AA': '전지',
            '31015AA': '가정용전기기기'
        },
        'category': '수출입',
        'unit': '-'
    },
    "403Y003": {
        "name": '수입지수', # 금액
        "code": {
            '*AA': '총지수',
        },
        'category': '수출입',
        'unit': '-'
    },
    "101Y003": {
        "name": "M2",
        "code" :{
            'BBHS00': '계절조정'
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "101Y004": {
        "name": "M2",
        "code" :{
            'BBHA00': '원계열'
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "104Y013" : {
        "name": "은행수신",
        "code": {
            "BCB8": "말잔",
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "104Y014" : {
        "name": "은행수신",
        "code": {
            "BCA8": "평잔",
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "111Y008" : {
        "name": "비은행수신",
        "code": {
            "1000000": "평잔"
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "111Y007": {
        "name": "비은행수신",
        "code": {
            "1000000": "말잔"
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "104Y016": {
        "name": "은행여신",
        "code": {
            "BDCA1": "말잔"
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "111Y009": {
        "name": "비은행여신",
        "code": {
            "1000000": "말잔"
        },
        "category": "통화공급",
        "unit": "십억원"
    },
    "722Y001": {
        "name": "기준금리",
        "code": {
            "0101000": "일간"
        },
        "category": "금리",
        "unit": "십억원"
    },
    "817Y002" : {
        "name": "시장금리",
        "code": {
            "010101000": "콜금리",
            "010151000": "KORIBOR(6M)",
            "010190000": "국고채1년",
            "010195000": "국고채2년",
            "010200001": "국고채5년",
            "010210000": "국고채10년",
            "010300000": "회사채3년(AA-)",
            "010320000": "회사채3년(BBB-)"
        },
        "category": "금리",
        "unit": "%"
    },
    "121Y002": {
        "name": "은행수신금리",
        "code": {
            "BEABAA2": "신규기준",
            "BEABAA1": "신규기준(금융채제외)"
        },
        "category": "금리",
        "unit": "%"
    },
    "121Y013": {
        "name": "은행수신금리",
        "code": {
            "BEABAB2": "잔액기준",
            "BEABAB1": "잔액기준(금융채제외)"
        },
        "category": "금리",
        "unit": "%"
    },
    "121Y006": {
        "name": "은행대출금리",
        "code": {
            "BECBLA01": "신규기준",
            "BECBLA02": "신규기준(기업)",
            "BECBLA03": "신규기준(가계)"
        },
        "category": "금리",
        "unit": "%"
    },
    "121Y015": {
        "name": "은행대출금리",
        "code": {
            "BECBLB01": "잔액기준",
            "BECBLB0201": "잔액기준(기업)",
            "BECBLB0202": "잔액기준(가계)"
        },
        "category": "금리",
        "unit": "%"
    },
    "901Y056":  {
        "name": "증시자금",
        "code": {
            "S23A": "예탁금",
            "S23E": "신용융자잔고",
            "S23F": "신용대주잔고"
        },
        "category": "통화공급",
        "unit": "백만원"
    },
    "404Y014": {
        "name": "생산자물가지수",
        "code": {
            "*AA": "전체"
        },
        "category": "물가",
        "unit": "-"
    },
    "901Y009": {
        "name": "소비자물가지수",
        "code": {
            "0": "전체"
        },
        "category": "물가",
        "unit": "-"
    },
    "901Y062": {
        "name": "KB부동산매매지수",
        "code": {
            "P63AC": "아파트(전국)",
            "P63ACA": "아파트(서울)",
        },
        "category": "부동산",
        "unit": "-"
    },
    "901Y063": {
        "name": "KB부동산전세지수",
        "code": {
            "P64AC": "아파트(전국)",
            "P64ACA": "아파트(서울)",
        },
        "category": "부동산",
        "unit": "-"
    },
    "901Y089": {
        "name": "아파트실거래지수",
        "code": {
            "100": "전국",
            "200": "서울",
            "210": "서울도심",
            "220": "서울동북",
            "230": "서울동남",
            "240": "서울서북",
            "250": "서울서남",
            "300": "수도권",
            "C00": "경기",
            "B00": "세종",
            "400": "지방",
            "M00": "지방광역시"
        },
        "category": "부동산",
        "unit": "-"
    },
    "512Y014": {
        "name": "경기전망",
        "code": {
            "C0000/BA": "제조업업황전망",
            "C0000/BD": "제조업신규수주전망",
            "C0000/BM": "제조업수출전망",
            "C0000/BY": "제조업심리지수",
            "X8000/BA": "수출기업업황전망",
            "X8000/BD": "수출기업신규수주전망",
            "X8000/BM": "수출기업수출전망",
        },
        "category": "심리지수",
        "unit": "-"
    },
    "511Y002": {
        "name": "소비자동향",
        "code": {
            "FME/99988": "심리지수"
        },
        "category": "심리지수",
        "unit": "-"
    },
    "513Y001": {
        "name": "경제심리지수",
        "code": {
            "E2000": "순환변동"
        },
        "category": "심리지수",
        "unit": "-"
    },
    "521Y001": {
        "name": "뉴스심리지수",
        "code": {
            "A001": "실험통계"
        },
        "category": "심리지수",
        "unit": "-"
    },
    "901Y067": {
        "name": "경기종합지수",
        "code": {
            "I16E": "선행지수순환변동",
            "I16D": "동행지수순환변동",
        },
        "category": "종합지수",
        "unit": "-"
    },
    "901Y027": {
        "name": "실업률",
        "code": {
            "I61BC/I28A": "원계열",
            "I61BC/I28B": "계절조정"
        },
        "category": "기타",
        "unit": "%"
    },
    "901Y014": {
        "name": "월별주가지수",
        "code": {
            "1070000": "코스피",
            "2090000": "코스닥"
        },
        "category": "주가지수",
        "unit": "-"
    }
}


def xml2df(url: str, parser:str="") -> DataFrame:
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
    resp = Web.text(url, parser=parser)
    root = ElementTree(fromstring(str(resp))).getroot()
    if root.find('CODE'):
        raise ConnectionError(f'{root.find("CODE").text} / {root.find("MESSAGE").text}')

    data = list()
    for tag in root.findall('row'):
        getter = dict()
        for n, t in enumerate([inner for inner in tag.iter()]):
            if t.tag in exclude:
                continue
            getter.update({t.tag: t.text})
        data.append(getter)
    return DataFrame(data=data) if data else DataFrame()