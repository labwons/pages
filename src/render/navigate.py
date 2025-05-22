try:
    from ..common.path import PATH
except ImportError:
    from src.common.path import PATH
from typing import Dict, List, Union
import os


CONTENT_NAMES = {
    "bubble": "종목 분포",
    "macro": "거시 경제",
    "portfolio": "투자 기록",
}

def navigate() -> List[Dict[str, Union[str, dict]]]:
    nav: List[Dict] = [{"href": f"/", "content": "시장 지도"}]
    for content in CONTENT_NAMES:
        if not content in os.listdir(PATH.DOCS):
            continue
        nav.append({'href': f'/{content}', 'content': CONTENT_NAMES[content]})
        if content == "portfolio":

            sub = []
            for sub_content in os.listdir(os.path.join(PATH.DOCS, content)):
                if sub_content.startswith('index'):
                    continue
                name = "" # TODO 
                          # Ticker에 해당하는 종목명 기입
                sub.append({'href': f'/{content}/{sub_content}', 'content': name})
            nav[-1].update({'sub': sub})
    return nav

if __name__ == "__main__":
    print(navigate())