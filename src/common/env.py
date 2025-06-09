from datetime import datetime, timezone, timedelta
import os, shutil



class Dict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = Dict(**value)
            self[key] = value

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"No such attribute: {attr}")

    def __setattr__(self, attr, value):
        self[attr] = value


def copy(src:str, dst:str, rename:str=""):
    if not os.path.exists(src):
        raise FileNotFoundError(f"원본 파일이 존재하지 않습니다: {src}")

    ext = f".{src.split('.')[-1]}"
    new = os.path.basename(src) if not rename else f"{rename}{ext}"
    dst = os.path.join(dst, new)
    if not os.path.isfile(dst):
        shutil.copy2(src=src, dst=dst)
    return dst


def copytree(src:str, dst:str):
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return


if 'COLAB_GPU' in os.environ or 'COLAB_RELEASE_TAG' in os.environ:
    ENV = 'google_colab'
elif os.environ.get('GITHUB_ACTIONS') == 'true':
    ENV = 'github_action'
else:
    ENV = 'local'

GITHUB_ACTION_EVENT = os.environ.get("GITHUB_EVENT_NAME", "local")


if ENV == 'GOOGLE_COLAB' or ENV == 'GITHUB_ACTION':
    DESKTOP = DOWNLOADS = ROOT = 'https://raw.githubusercontent.com/labwons/pages/main/'
else:
    ROOT = os.path.dirname(__file__)
    while not ROOT.endswith('pages'):
        ROOT = os.path.dirname(ROOT)

    DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    DOWNLOADS = os.path.join(os.environ['USERPROFILE'], 'Downloads')

DOCS   = os.path.join(ROOT, r'docs')
FILE = Dict()
FILE.BASELINE           = os.path.join(ROOT, r'src/fetch/market/json/baseline.json')
FILE.GROUP              = os.path.join(ROOT, r'src/fetch/market/json/group.json')
FILE.ANNUAL_STATEMENT   = os.path.join(ROOT, r'src/fetch/market/parquet/annualstatement.parquet')
FILE.QUARTER_STATEMENT  = os.path.join(ROOT, r'src/fetch/market/parquet/quarterstatement.parquet')
FILE.STATEMENT_OVERVIEW = os.path.join(ROOT, r'src/fetch/market/parquet/statementoverview.parquet')
FILE.MACRO              = os.path.join(ROOT, r'src/fetch/macro/json/macro.json')


HTML = Dict()
HTML.MAP        = os.path.join(ROOT, r'docs/index.html')
HTML.BUBBLE     = os.path.join(ROOT, r'docs/bubble/index.html')
HTML.MACRO      = os.path.join(ROOT, r'docs/macro/index.html')
HTML.TEMPLATES  = os.path.join(ROOT, r'src/render/templates')


CLOCK = lambda: datetime.now(timezone(timedelta(hours=9)))



if __name__ == "__main__":

    print(ENV)
    print(FILE.BASELINE)
    print(FILE.GROUP)
    print(FILE.ANNUAL_STATEMENT)