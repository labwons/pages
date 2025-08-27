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


class ARCHIVE:

    __slots__ = [
        "MACRO_FRED",
        "MARKET_BASELINE",
        "MARKET_DAILY",
        "MARKET_OVERVIEW",
        "MARKET_SECTORS",
        "STATEMENT_A",
        "STATEMENT_Q",
    ]
    def __init__(self, date:str):
        for __slot__ in self.__slots__:
            setattr(self, __slot__, os.path.join(PATH.ARCHIVE, date, f'{__slot__}.parquet'))
        return

    @classmethod
    def _get_latest_file(cls, file:str):
        for _date in sorted(os.listdir(PATH.ARCHIVE), reverse=True):
            _path = os.path.join(PATH.ARCHIVE, _date)
            if file in os.listdir(_path):
                return os.path.join(_path, file)
        raise FileNotFoundError

    @classmethod
    def read(cls, date:str) -> DD:
        """
        입력 날짜 기준, 가장 최신 파일 경로 부여
        """
        return DD(**{key: cls._get_latest_file(f'{key}.parquet') for key in cls.__slots__})

    @classmethod
    def write(cls, date:str) -> DD:
        """
        입력 날짜 기준, 파일 존재 여부와 무관하게 파일 경로 부여
        """
        path = os.path.join(PATH.ARCHIVE, date)
        os.makedirs(path, exist_ok=True)
        return DD(**{key: os.path.join(path, f'{key}.parquet') for key in cls.__slots__})

    @classmethod
    def push(cls, date:str) -> DD:
        return cls.write(date)

    @classproperty
    def LATEST(cls) -> DD:
        return cls.read(sorted(os.listdir(PATH.ARCHIVE), reverse=True)[0])


if __name__ == "__main__":
    print(ARCHIVE.push("20250830"))
    print(ARCHIVE.read('20250830'))
    print(ARCHIVE.LATEST)
    print(ARCHIVE("20250801").MARKET_SECTORS)

