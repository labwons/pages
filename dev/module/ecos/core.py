try:
    from ...common.web import Web
except ImportError:
    from dev.common.web import Web
from pandas import DataFrame
from xml.etree.ElementTree import  ElementTree, fromstring


PREDEF = {
    "731Y003" : {
        'name': '원/달러환율',
        'code': {
            "0000002":'시가',
            "0000005":'고가',
            "0000004":'저가',
            "0000003":'종가'
        },
        'unit': '원',
    },
    "403Y001": {
        "name": '수출액지수',
        "code": {
            '*AA': '총지수',
            '3091AA': '반도체',
            '31124AA': '반도체및디스플레이제조용기계',
            '309512AA': '이동전화기',
            '3121AA': '자동차',
            '31213AA': '자동차부품',
            '310131AA': '전지',
            '31015AA': '가정용전기기기'
        },
        'unit': '-'
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