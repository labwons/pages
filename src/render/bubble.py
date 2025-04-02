try:
    from ..common.path import PATH
    from .config import templateKeys
except ImportError:
    from src.common.path import PATH
    from src.render.config import templateKeys
from jinja2 import Environment, FileSystemLoader
import os


defaultBubbleAttribute = {
    "title": "\uc885\ubaa9\u0020\ubd84\ud3ec BUBBLES",
    "script": [{"src": f"/src/js/bubble.min.js", "pos": "bottom"}],
    "service_opt_l": ('\n' + '\t' * 5).join([
        '',
        '\t<select name="x" class="bubble-select bubble-x"></select>',
        '\t<select name="y" class="bubble-select bubble-y"></select>',
        # '\t<div class="bubble-button bubble-edit"><i class="fa"></i></div>',
        # '\t<div class="bubble-button bubble-sizing"><i class="fa fa-compress"></i></div>',
        ''
    ]),
    "service_opt_r": ('\n' + '\t' * 5).join([
        '',
        '\t<select name="sectors" class="bubble-select bubble-sectors"></select>',
        '\t<select name="tickers" class="bubble-select bubble-searchbar"><option></option></select>',
        ''
    ]),
    "app_icon": '<span class="toolbox-on"><i class="fa fa-edit"></i></span>',
    # "service_items": '<span class="bubble-legend"></span>' * 7,
    "service_notice": (
        '모든 투자의 책임은 당사자에게 있습니다. '
        '*표시는 코스닥 종목입니다. '
        '한국거래소 상장 주식 중 시가총액 중위값 이상 종목들로 구성되었습니다. '
        '종목을 PC 환경에서 마우스 커서를 올리거나 모바일 기기에서 터치하면 세부 정보가 나타납니다. '
        '우측 상단 아이콘을 클릭하면 차트를 조작할 수 있습니다. '
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
                   .get_template('service.html') \
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
                   .get_template('bubble.js') \
                   .render(**kwargs) \
                   .replace("nan", "null").replace("NaN", "null")
        return

    def save(self, path:str):
        file = os.path.join(path, 'bubble.js')
        with open(file, mode='w', encoding='utf-8') as js:
            js.write(self.src)
        return

