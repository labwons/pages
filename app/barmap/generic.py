try:
    from ..sector.generic import Wise
    from ..market.generic import Market
    from core import bmFrame
    import fetch
except ImportError:
    from app.sector.generic import Wise
    from app.market.generic import Market
    from app.barmap.core import bmFrame
    from app.barmap import fetch
from datetime import date, datetime, timedelta
from pandas import DataFrame
from pykrx import stock
from requests.exceptions import JSONDecodeError, SSLError
from typing import Dict, List, Union, Iterable
import pandas as pd


class MarketMap(DataFrame):
    
    def __init__(self, index:str):
        wise = Wise(index, auto_update=False)
        data = Market(auto_update=True)
        data = data.drop(columns=[col for col in data if col in wise])
        merged = wise.join(data, how='left')
        return