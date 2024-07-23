from pandas import DataFrame
from typing import List


class mapData(DataFrame):
    
    mapType:str = ''
    mapLevel:List[str] = []
    aligned:DataFrame = DataFrame()
    
    def __init__(self, data:DataFrame):
        super().__init__(data.copy())
        
        if self.iloc[0]['indexName'].startswith("WICS"):
            self.mapType = 'WICS'
            self.mapLevel = ['ticker', 'sectorName', 'indexName']
        elif self.iloc[0]['indexName'].startswith("WI26"):
            self.mapType = 'WI26'
            self.mapLevel = ['ticker', 'sectorName']
            self.drop(columns=['indexCode', 'indexName'], inplace=True)
        else:
            raise KeyError(f'Unalbe to discreminate index Type')
    
        self.reset_index(level=0, inplace=True)
        self['size'] = self['marketCap'] / 100000000
        return