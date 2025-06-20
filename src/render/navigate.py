try:
    from ..common.env import DOCS
except ImportError:
    from src.common.env import DOCS
from typing import Dict, List, Union
import csscompressor, rjsmin, os


CONTENT_NAMES = {
    "bubble": "종목 분포",
    "macro": "경제 지표",
    "portfolio": "투자 기록",
}

def navigate() -> List[Dict[str, Union[str, dict]]]:
    nav: List[Dict] = [{"href": f"/", "content": "시장 지도"}]
    for content in CONTENT_NAMES:
        if not content in os.listdir(DOCS):
            continue
        nav.append({'href': f'/{content}', 'content': CONTENT_NAMES[content]})
        if content == "portfolio":

            sub = []
            for sub_content in os.listdir(os.path.join(DOCS, content)):
                if sub_content.startswith('index'):
                    continue
                name = "" # TODO 
                          # Ticker에 해당하는 종목명 기입
                sub.append({'href': f'/{content}/{sub_content}', 'content': name})
            nav[-1].update({'sub': sub})
    return nav


def minify():
    for _dir, _folder, _files in os.walk(DOCS):
        for _file in _files:
            if _file.endswith('js') and not _file.endswith('.min.js'):
                js = os.path.join(_dir, _file)
                with open(js, 'r', encoding='utf-8') as file:
                    src = file.read()
                with open(js.replace(".js", ".min.js"), "w", encoding='utf-8') as file:
                    file.write(rjsmin.jsmin(src))
            elif _file.endswith('css') and not _file.endswith('.min.css'):
                css = os.path.join(_dir, _file)
                with open(css, 'r', encoding='utf-8') as file:
                    src = file.read()
                with open(css.replace(".css", ".min.css"), "w", encoding='utf-8') as file:
                    file.write(csscompressor.compress(src))
            else:
                continue
    return


if __name__ == "__main__":
    print(navigate())
    minify()