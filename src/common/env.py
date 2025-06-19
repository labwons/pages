from datetime import datetime, timezone, timedelta
import os, shutil


class dDict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = dDict(**value)
            self[key] = value

    def __iter__(self):
        return iter(self.items())

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

CLOCK = lambda: datetime.now(timezone(timedelta(hours=9)))

if any([key.lower().startswith('colab') for key in os.environ]):
    ENV = 'google_colab'
elif any([key.lower().startswith('github') for key in os.environ]):
    ENV = 'github_action'
else:
    ENV = 'local'

GITHUB_ACTION_EVENT = os.environ.get("GITHUB_EVENT_NAME", "local")

ROOT = "https://raw.githubusercontent.com/labwons/pages/main/"
if not ENV == 'google_colab':
    ROOT = os.path.dirname(__file__)
    while not ROOT.endswith('pages'):
        ROOT = os.path.dirname(ROOT)

if ENV == "local":
    DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    DOWNLOADS = os.path.join(os.environ['USERPROFILE'], 'Downloads')

DOCS   = os.path.join(ROOT, r'docs')
FILE = dDict()
FILE.AFTER_MARKET       = os.path.join(ROOT, r'src/fetch/market/parquet/aftermarket.parquet')
FILE.ANNUAL_STATEMENT   = os.path.join(ROOT, r'src/fetch/market/parquet/annualstatement.parquet')
FILE.QUARTER_STATEMENT  = os.path.join(ROOT, r'src/fetch/market/parquet/quarterstatement.parquet')
FILE.STATEMENT_OVERVIEW = os.path.join(ROOT, r'src/fetch/market/parquet/statementoverview.parquet')
FILE.SECTOR_COMPOSITION = os.path.join(ROOT, r'src/fetch/market/parquet/sectorcomposition.parquet')
FILE.BASELINE           = os.path.join(ROOT, r'src/fetch/market/parquet/baseline.parquet')
FILE.MACRO              = os.path.join(ROOT, r'src/fetch/macro/json/macro.json')

HTML = dDict()
HTML.MAP        = os.path.join(ROOT, r'docs/index.html')
HTML.BUBBLE     = os.path.join(ROOT, r'docs/bubble/index.html')
HTML.MACRO      = os.path.join(ROOT, r'docs/macro/index.html')
HTML.TEMPLATES  = os.path.join(ROOT, r'src/render/templates')




if __name__ == "__main__":
    print(ENV)
    # print(FILE.BASELINE)
    # print(FILE.GROUP)
    # print(FILE.ANNUAL_STATEMENT)
