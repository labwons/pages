try:
    from ...common.tradingdate import TradingDate
    import key
except ImportError:
    from app.common.tradingdate import TradingDate
    from app.sector.core import key
from pandas import concat, DataFrame
import requests
import time


wiseDate = TradingDate.wiseDate
def sector(code:str, try_count:int=5) -> DataFrame:
    for n in range(try_count):
        resp = requests.get(key.URL(wiseDate, code))
        if resp.status_code == 200:
            data = DataFrame(resp.json()['list'])[key.COLUMNS.keys()]
            return data.rename(columns=key.COLUMNS)
        time.sleep(5)
    raise TimeoutError(f'Unable to fetch WISE INDEX code: {code}')
