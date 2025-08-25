import os


PROJECT_NAME = 'labwons'
class PATH:
    if not os.environ.get("GITHUB_EVENT_NAME", ""):
        find = os.path.dirname(__file__).split(os.sep).index(PROJECT_NAME)
        ROOT = os.sep.join(os.path.dirname(__file__).split(os.sep)[:find + 1])
    else:
        ROOT = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    DOCS = os.path.join(ROOT, r'docs')
    SRC = os.path.join(ROOT, r'src')
    DATA = os.path.join(ROOT, r'src/data')
    LOGS = os.path.join(DATA, r'logs')
    ARCHIVE = os.path.join(DATA, r'archive')
    TEMPLATE = os.path.join(DATA, r'template')


class Archive:
    
    ROOT = PATH.ARCHIVE

    def __init__(self, date:str=''):
        if not date:
            date = f"{max(int(date) for date in os.listdir(self.ROOT))}"

        self.LATEST = latest = os.path.join(self.ROOT, date)
        self.MARKET_BASELINE = os.path.join(latest, 'MARKET_BASELINE.parquet')
        self.MARKET_DAILY = os.path.join(latest, 'MARKET_DAILY.parquet')
        self.MARKET_OVERVIEW = os.path.join(latest, 'MARKET_OVERVIEW.parquet')
        self.MARKET_SECTORS = os.path.join(latest, 'MARKET_SECTORS.parquet')
        self.STATEMENT_A = os.path.join(latest, 'STATEMENT_A.parquet')
        self.STATEMENT_Q = os.path.join(latest, 'STATEMENT_Q.parquet')
        return

    def create(self, date:str=''):
        if not date:
            from datetime import datetime
            date = datetime.today().strftime("%Y%m%d")
        os.makedirs(os.path.join(self.ROOT, date), exist_ok=True)
        self.__init__(date)
        return

    def replace_to(self, date:str):
        path = os.path.join(self.ROOT, date)
        if not os.path.isdir(path):
            raise FileExistsError
        self.__init__(date)
        return
    
    @property
    def recentBaseline(self) -> str:
        for _dir in sorted((int(date) for date in os.listdir(self.ROOT)), reverse=True):
            baseline = os.path.join(self.ROOT, str(_dir), 'MARKET_BASELINE.parquet')
            if os.path.isfile(baseline):
                return baseline
        return ""
        

# Alias
ARCHIVE = Archive()

if __name__ == "__main__":
    print(PROJECT_NAME)
    print(ARCHIVE.recentBaseline)