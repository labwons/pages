from labwons.deco import classproperty
from labwons.util import DD
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


class Archive(DD):

    __slots__ = [
        "MARKET_BASELINE",
        "MARKET_DAILY",
        "MARKET_SECTORS",
        "MARKET_MAP",
        "DATE",
        "PATH",
    ]
    REPORTS:str=os.path.join(PATH.ARCHIVE, 'reports')

    def __init__(self, date:str='', alloc:bool=False):
        super().__init__()

        if not date:
            date = sorted(os.listdir(PATH.ARCHIVE), reverse=True)[0]
        self["DATE"] = date
        self["PATH"] = path = os.path.join(PATH.ARCHIVE, date)

        if alloc:
            os.makedirs(path, exist_ok=True)

        for __slot__ in self.__slots__:
            if __slot__ in self:
                continue
            if alloc:
                self[__slot__] = os.path.join(path, f'{__slot__}.parquet')
            else:
                self[__slot__] = self._get_latest_file(date, f'{__slot__}.parquet')
        return

    def __call__(self, date:str, alloc:bool):
        self.__init__(date, alloc)

    @classmethod
    def _get_latest_file(cls, date:str, file:str):
        dates = sorted(os.listdir(PATH.ARCHIVE), reverse=True)
        if not date in dates:
            raise FileExistsError(f'ARCHIVE HAS NO DATA FOR {date}')

        dates = dates[dates.index(date):]
        for _date in dates:
            _path = os.path.join(PATH.ARCHIVE, _date)
            if file in os.listdir(_path):
                return os.path.join(_path, file)
        raise FileNotFoundError(f'File: {file} @{date}')

    def dateof(self, fullpath:str) -> str:
        return [sp for sp in fullpath.split(os.sep) if len(sp) == 8 and sp.startswith('20')][0]

    def at(self, date:str):
        if date.lower() == "latest":
            date = ''
        return Archive(date)

    def refresh(self):
        self.__init__()

    def report(self, ticker:str) -> str:
        file = os.path.join(self.REPORTS, f'{ticker}.xml')
        if not os.path.isfile(file):
            raise FileNotFoundError(f'NO Report for ticker: {ticker}')
        return file

    def to(self, date:str=""):
        return Archive(date, True)



# Alias
ARCHIVE = Archive()

if __name__ == "__main__":
    print(ARCHIVE)
    print(ARCHIVE.new('20250827'))
    print(ARCHIVE.at('20250825'))
    # print(ARCHIVE.push("20250830"))
    # print(ARCHIVE.read('20250830'))
    # print(ARCHIVE.LATEST)
    # print(ARCHIVE("20250801").MARKET_SECTORS)

