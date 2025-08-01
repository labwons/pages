try:
    from .dtype import dDict
except ImportError:
    from src.common.dtype import dDict
from datetime import datetime, timezone, timedelta
import os


# DATETIME CLOCK: %Y-%m-%d %H:%M:%s+09:00
CLOCK = lambda: datetime.now(timezone(timedelta(hours=9)))

# ENVIRONMENT VARIABLE: DETECTING CURRENT RUNNER
ENV   = "local"
if any([key.lower().startswith('colab') for key in os.environ]):
    ENV = 'google_colab'
if any([key.lower().startswith('github') for key in os.environ]):
    ENV = 'github_action'

DOMAIN = ""
if "USERDOMAIN" in os.environ:
    DOMAIN = os.environ["USERDOMAIN"]

# ROOT DIRECTORY
ROOT = "https://raw.githubusercontent.com/labwons/pages/main/"
if not ENV == 'google_colab':
    ROOT = os.path.dirname(__file__)
    while not ROOT.endswith('pages'):
        ROOT = os.path.dirname(ROOT)

# DEPLOYMENT DIRECTORY
DOCS   = os.path.join(ROOT, r'docs')

# RESOURCE FILE DIRECTORIES
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
FILE.PRICE              = os.path.join(ROOT, r'src/fetch/stock/parquet/price.parquet')
FILE.MARKET_CAP         = os.path.join(ROOT, r'src/fetch/stock/parquet/marketcap.parquet')
FILE.FOREIGN_RATE       = os.path.join(ROOT, r'src/fetch/stock/parquet/foreignrate.parquet')
FILE.PER_BAND           = os.path.join(ROOT, r'src/fetch/stock/parquet/perband.parquet')

# RESOURCE DEPLOY DELIVERABLES
HTML = dDict()
HTML.MAP        = os.path.join(ROOT, r'docs/index.html')
HTML.BUBBLE     = os.path.join(ROOT, r'docs/bubble/index.html')
HTML.MACRO      = os.path.join(ROOT, r'docs/macro/index.html')

# RESOURCE PATH DIRECTORIES
PATH = dDict()
PATH.DOCS = os.path.join(ROOT, r'docs')
PATH.TEMPLATES = os.path.join(ROOT, r'src/build/apps/templates')
if ENV == "local":
    PATH.DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    PATH.DOWNLOADS = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    PATH.STUB = os.path.join(PATH.DOWNLOADS, 'labwons')

# GITHUB ENVIRONMENT PARAMETERS
GITHUB = dDict()
GITHUB.EVENT = os.environ.get("GITHUB_EVENT_NAME", "local")
GITHUB.CONFIG = dDict(
    AFTERMARKET = False,
    STATEMENT = False,
    SECTOR = False,
    ECOS = False,
    FRED = False,
    STOCKPRICE = True,
    STOCKDEPLOY = True,
)
def __RESET__():
    for key, val in GITHUB.CONFIG:
        if not key == "RESET":
            GITHUB.CONFIG[key] = False
GITHUB.CONFIG.RESET = __RESET__

TICKERS = [
    "023910", # 대한약품
    "062040", # 산일전기
    "214180", # 헥토이노베이션
    "012450", # 한화에어로스페이스
    "079550", # LIG넥스원
    "064350", # 현대로템
    "034020", # 두산에너빌리티
    "267260", # HD현대일렉트릭
    "298040", # 효성중공업
    "272210", # 한화시스템
    "329180", # HD현대중공업
    "042660", # 한화오션
    "009540", # HD한국조선해양
    "017960", # 한국카본
]

if __name__ == "__main__":
    print(CLOCK())
    print(ENV)
    print(FILE.BASELINE)
    print(FILE.GROUP)
    print(FILE.ANNUAL_STATEMENT)
    print(GITHUB.CONFIG)
    GITHUB.CONFIG.RESET()
    print(GITHUB.CONFIG)
    GITHUB.CONFIG.ECOS = GITHUB.CONFIG.STATEMENT = True
    print(GITHUB.CONFIG)

    for key, value in os.environ.items():
        print(key, value)
