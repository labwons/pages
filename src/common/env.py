try:
    from .struct import dDict
except ImportError:
    from src.common.struct import dDict
from datetime import datetime, timezone, timedelta
import os


CLOCK = lambda: datetime.now(timezone(timedelta(hours=9)))
ENV   = "local"
if any([key.lower().startswith('colab') for key in os.environ]):
    ENV = 'google_colab'
if any([key.lower().startswith('github') for key in os.environ]):
    ENV = 'github_action'

ROOT = "https://raw.githubusercontent.com/labwons/pages/main/"
if not ENV == 'google_colab':
    ROOT = os.path.dirname(__file__)
    while not ROOT.endswith('pages'):
        ROOT = os.path.dirname(ROOT)

DOCS   = os.path.join(ROOT, r'docs')

FILE = dDict()
FILE.AFTER_MARKET       = os.path.join(ROOT, r'src/fetch/market/parquet/aftermarket.parquet')
FILE.ANNUAL_STATEMENT   = os.path.join(ROOT, r'src/fetch/market/parquet/annualstatement.parquet')
FILE.QUARTER_STATEMENT  = os.path.join(ROOT, r'src/fetch/market/parquet/quarterstatement.parquet')
FILE.STATEMENT_OVERVIEW = os.path.join(ROOT, r'src/fetch/market/parquet/statementoverview.parquet')
FILE.SECTOR_COMPOSITION = os.path.join(ROOT, r'src/fetch/market/parquet/sectorcomposition.parquet')
FILE.BASELINE           = os.path.join(ROOT, r'src/fetch/market/parquet/baseline.parquet')
FILE.MACRO_BASELINE     = os.path.join(ROOT, r'src/fetch/macro/parquet/baseline.parquet')
FILE.ECOS               = os.path.join(ROOT, r'src/fetch/macro/parquet/ecos.parquet')
FILE.FRED               = os.path.join(ROOT, r'src/fetch/macro/parquet/fred.parquet')
FILE.MACRO              = os.path.join(ROOT, r'src/fetch/macro/json/macro.json')

HTML = dDict()
HTML.MAP        = os.path.join(ROOT, r'docs/index.html')
HTML.BUBBLE     = os.path.join(ROOT, r'docs/bubble/index.html')
HTML.MACRO      = os.path.join(ROOT, r'docs/macro/index.html')

PATH = dDict()
PATH.DOCS = os.path.join(ROOT, r'docs')
PATH.TEMPLATES = os.path.join(ROOT, r'src/build/apps/templates')
if ENV == "local":
    PATH.DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    PATH.DOWNLOADS = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    PATH.STUB = os.path.join(PATH.DOWNLOADS, 'labwons')

GITHUB = dDict()
GITHUB.EVENT = os.environ.get("GITHUB_EVENT_NAME", "local")
GITHUB.CONFIG = dDict(
    AFTERMARKET = False,
    STATEMENT = False,
    SECTOR = False,
    ECOS = False,
    FRED = False
)
def _reset():
    for key, val in GITHUB.CONFIG:
        if not key == "RESET":
            GITHUB.CONFIG[key] = False
GITHUB.CONFIG.RESET = _reset



if __name__ == "__main__":
    print(ENV)
    # print(FILE.BASELINE)
    # print(FILE.GROUP)
    # print(FILE.ANNUAL_STATEMENT)
    print(GITHUB.CONFIG)
    GITHUB.CONFIG.RESET()
    print(GITHUB.CONFIG)
    GITHUB.CONFIG.ECOS = GITHUB.CONFIG.STATEMENT = True
    print(GITHUB.CONFIG)