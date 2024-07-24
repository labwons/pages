from pandas import DataFrame
from pykrx import stock


class mapData(DataFrame):

    _kq = stock.get_index_portfolio_deposit_file('2001')
    _ks200 = stock.get_index_portfolio_deposit_file('1028')
    _kq150 = stock.get_index_portfolio_deposit_file('2203')
    def __init__(self, wiseIndex:DataFrame, properties:DataFrame):
        if not str(wiseIndex.index.name) == 'ticker':
            wiseIndex = wiseIndex.set_index(keys='ticker')
        super().__init__(wiseIndex.join(properties, how='left'))

        # self.drop(columns=self.dropper, inplace=True)
        self.sort_values(by='marketCap', ascending=False, inplace=True)
        self['indexName'] = self['indexName'].str.replace("WICS ", "")
        self['name'] = self['name'].apply(lambda x: f"*{x}" if x in self._kq else x)
        self['close'] = self['close'].apply(lambda x: f"{x:,}원")
        self['size'] = self['marketCap'] / 100000000
        self['marketCap'] = self['size'].apply(self._format_cap)
        self[['DIV', 'PER', 'PBR']] = round(self[['DIV', 'PBR', 'PER']], 2)
        return

    @staticmethod
    def _format_cap(x:int) -> str:
        mod, res = int(x // 10000), int(x % 10000)
        return f'{mod}조 {res}억원' if mod else f'{res}억원'

    # @property
    # def dropper(self) -> list:
    #     return [
    #         'indexCode', 'sectorCode', 'sectorCap', 'sectorWeight',
    #         'shares', 'ipo', 'settlementMonth', 'D+0'
    #     ]    
    
    @property
    def largeCap(self) -> DataFrame:
        return self[self.index.isin(self._ks200 + self._kq150)]

    @property
    def midCap(self) -> DataFrame:
        return self[~self.index.isin(self._ks200 + self._kq150)].head(500)