try:
    import fetch
except ImportError:
    from __py__.sector import fetch
from datetime import datetime
from pandas import DataFrame
from pykrx.stock import get_index_portfolio_deposit_file, get_index_ohlcv_by_date
from pytz import timezone
from typing import List
import pandas, os, json


class Sector(DataFrame):

    # A class variable is initialized only once when the class is loaded.
    # Therefore, if a class variable is the result of a complex and time-consuming computation,
    # that computation is performed only once, when the class is defined or first used.
    # After that, the value of the variable is shared among all instances,
    # so the computation is not repeated every time a new instance is created.

    # KOSDAQ LIST
    __kq__:List[str] = get_index_portfolio_deposit_file('2001')

    # KOSPI200, KOSDAQ150 LIST
    __lg__:List[str] = get_index_portfolio_deposit_file('2203') + get_index_portfolio_deposit_file('1028')

    # WISE INDEX VALID DATE
    __dt__ = fetch.index_date()

    def __init__(self, auto_update:bool=False):
        # _name = fetch.index_name(index)

        try:
            _path = os.path.join(os.path.dirname(__file__), rf'../../src/json/market/sector.json')
        except NameError:
            _path = f"https://raw.githubusercontent.com/labwons/pages/main/src/json/market/sector.json"

        if auto_update:
            print(f"Fetching WISE INDEX GROUP...", end="")
            objs = [fetch.index_component(self.__dt__, cd) for cd in fetch.KEYS]
            print("Success")

            _data = pandas.concat(objs=objs, axis=0, ignore_index=False)

            __kq__ = [ticker for ticker in _data.index if ticker in self.__kq__]
            __lg__ = [ticker for ticker in _data.index if ticker in self.__lg__]
            _data.loc[__kq__, 'name'] = _data.loc[__kq__, 'name'] + '*'
            _data.loc[__lg__, 'stockSize'] = 'large'
            _data.to_json(_path, orient='index')
            # _data['indexName'] = _name
            super().__init__(_data)
            return

        super().__init__(pandas.read_json(_path, orient='index'))
        self.index = self.index.astype(str).str.zfill(6)
        self.index.name = 'ticker'
        # if not 'indexName' in self:
        #     self['indexName'] = _name
        return  
    
    
class Index(object):
    
    # WISE INDEX VALID DATE
    __dt__ = fetch.index_date()
    __td__ = datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d")
    def __init__(self):
        try:
            _path = os.path.join(os.path.dirname(__file__), rf'../../src/json/macro/index.json')
        except NameError:
            _path = f"https://raw.githubusercontent.com/labwons/pages/main/src/json/macro/index.json"
        print("Fetching KS/KQ...", end="")
        ks = get_index_ohlcv_by_date(ticker="1001", fromdate="20000101", todate=self.__td__, name_display=False)
        ks = ks.rename(columns={'종가':'KOSPI'})[['KOSPI']]
        ks.index = pandas.to_datetime(ks.index).strftime('%Y-%m-%d')
        kq = get_index_ohlcv_by_date(ticker="2001", fromdate="20000101", todate=self.__td__, name_display=False)
        kq = kq.rename(columns={'종가':'KOSDAQ'})[['KOSDAQ']]
        kq.index = pandas.to_datetime(kq.index).strftime('%Y-%m-%d')
        data1 = pandas.concat([ks, kq], axis=1)
        print("Success")
        
        print(f"Fetching WISE INDEX...", end="")
        data2 = pandas.concat([fetch.index_data(self.__dt__, cd) for cd in fetch.KEYS], axis=1)
        print("Success")
        
        data = pandas.concat([data1, data2], axis=1)
        data.index.name = 'date'
        data = data.reset_index(level=0)
        src = json.dumps(data.to_dict(orient='list'), separators=(',', ':'))
        with open(_path, mode='w') as file:
            file.write(src)
        return
        
    
if __name__ == "__main__":
    
    print(Sector('WICS'))