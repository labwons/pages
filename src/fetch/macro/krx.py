from datetime import datetime, timezone, timedelta
from pandas import concat, DataFrame
from pykrx.stock import get_index_ohlcv_by_date


def krxIndex() -> DataFrame:
    tz = timezone(timedelta(hours=9))
    ck = datetime.now(tz)
    ks = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '1001')['종가']
    kq = get_index_ohlcv_by_date('20000101', ck.strftime("%Y%m%d"), '2001')['종가']
    ks.name = '1001'
    kq.name = '2001'
    return concat([ks, kq], axis=1)