try:
    from ..common.date import TradingDate
    import core
except ImportError:
    from app.common.date import TradingDate
    from app.sector import core
from pandas import concat, DataFrame
import requests
import time


wiseDate = TradingDate.wiseDate
def sector(code:str, try_count:int=5) -> DataFrame:
    for n in range(try_count):
        resp = requests.get(core.URL(wiseDate, code))
        if resp.status_code == 200:
            data = DataFrame(resp.json()['list'])[core.COLUMNS.keys()]
            return data.rename(columns=core.COLUMNS)
        time.sleep(5)
    raise TimeoutError(f'Unable to fetch WISE INDEX code: {code}')
