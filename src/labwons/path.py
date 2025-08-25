import os


PROJECT_NAME = 'labwons'
class PATH:
    if os.environ.get("GITHUB_EVENT_NAME", "localhost") == "localhost":
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


class FILE:
    AFTER_MARKET = os.path.join(PATH.ARCHIVE, 'aftermarket.parquet')
    ANNUAL_STATEMENT = os.path.join(PATH.ARCHIVE, 'annualstatement.parquet')
    BASELINE = os.path.join(PATH.ARCHIVE, 'baseline.parquet')
    SECTOR_COMPOSITION = os.path.join(PATH.ARCHIVE, 'sectorcomposition.parquet')
    STATEMENT_OVERVIEW = os.path.join(PATH.ARCHIVE, 'statementoverview.parquet')
    QUARTER_STATEMENT = os.path.join(PATH.ARCHIVE, 'quarterstatement.parquet')

if __name__ == "__main__":
    # print(PROJECT_NAME)
    print(os.getcwd())
    print(PATH.ROOT)
    print(PATH.ARCHIVE)
    print(PATH.LOGS)
    print(os.path.isdir(PATH.ARCHIVE))
    print(os.path.join(PATH.ARCHIVE, f"{max(int(date) for date in os.listdir(PATH.ARCHIVE))}/BASELINE.parquet"))
