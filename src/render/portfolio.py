try:
    from ..common.path import PATH
    from .config import templateKeys
except ImportError:
    from src.common.path import PATH
    from src.render.config import templateKeys
from jinja2 import Environment, FileSystemLoader
import os


defaultPortfolioAttribute = {
    "title": "포트폴리오 PORTFOLIO",
    "script": [{"src": f"/src/js/portfolio.min.js", "pos": "bottom"}],

    "service_notice": (
        '모든 투자의 책임은 당사자에게 있습니다. '
        '*표시는 코스닥 종목 입니다. '
        '코스피200, 코스닥150 종목으로 구성하였습니다. '
        'PC환경에서 마우스를 올리거나 모바일에서 종목을 길게 누르면 세부 정보가 나타납니다. '
        '종목이나 섹터를 클릭(탭)하면 확대/재편됩니다. '
        '재편된 지도에서 상단 분류를 클릭(탭)하면 상위 분류 기준으로 재편됩니다. '
    ),
    "faq": [
        {'q': '실시간 업데이트는 안 되나요?', 'a': '안타깝지만 제공되지 않습니다.<i class="fa fa-frown-o"></i>'},
        {'q': '제가 찾는 종목이 없어요.', 'a': '가독성을 위해 대형주는 코스피200 지수와 코스닥150 지수 종목으로 구성하였으며 이외 종목은 제외됩니다.'},
        {'q': '언제 업데이트 되나요?', 'a': '정규장 시간 마감(15:30) 이후 15분~30분 내로 업데이트 됩니다. 휴장일에는 마지막 개장일 데이터가 유지됩니다.'},
        {'q': '자료 출처가 어디인가요?',
         'a': '섹터/업종 분류는 GICS 산업 분류 및 WISE INDEX를 참고하여 재구성하였습니다. 수익률은 한국거래소(KRX) 데이터를 참고하였으며 기타 지표는 네이버 및 에프앤가이드를 참고하였습니다.'},
        {'q': 'NXT 거래소 정보는 반영 안 되나요?',
         'a': 'NXT 거래소의 가격 정보는 반영되지 않으며 한국거래소(KRX) 기준 가격만 반영됩니다.'},
        {'q': '정보 수정이 필요해요.',
         'a': '고장 신고, 정보 정정 및 기타 문의는 snob.labwons@gmail.com 으로 연락주세요!<i class="fa fa-smile-o"></i>'},
    ]
}

class html:

    def __init__(self, **kwargs):
        self.src = Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                   .get_template('portfolio.html') \
                   .render(**kwargs)
        return

    def save(self, path:str):
        file = os.path.join(path, 'index.html')
        with open(file, mode='w', encoding='utf-8') as index:
            index.write(self.src)
        return


class javascript:

    def __init__(self, **kwargs):
        self.src = Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                   .get_template('portfolio.js') \
                   .render(**kwargs) \
                   .replace("nan", "null").replace("NaN", "null")
        return

    def save(self, path:str):
        file = os.path.join(path, 'portfolio.js')
        with open(file, mode='w', encoding='utf-8') as js:
            js.write(self.src)
        return
