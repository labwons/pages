try:
    from ..baseline.metadata import METADATA, BUBBLES
    from ..baseline.baseline import Tools
except ImportError:
    from src.build.baseline.metadata import METADATA, BUBBLES
    from src.build.baseline.baseline import Tools
from datetime import datetime
from numpy import nan
from pandas import DataFrame, Series
from pandas.errors import IntCastingNaNError
from time import perf_counter
from typing import Any, Dict, List


class MarketBubble:

    _log: List[str] = []

    # meta: Dict[str, Dict[str, Any]] = {}
    # sector: Dict[str, Dict[str, str]] = {"ALL": {"label": "전체", "color": "royalblue"}}
    def __init__(self, baseline:DataFrame):
        stime = perf_counter()
        self.log = f'BUILD [MARKET BUBBLE]'

        resource = baseline.copy()

        # TYPE CASTING BEFORE FACTORIZE MAP DATA.
        baseline = baseline.copy()
        for col, meta in METADATA:
            if col == "RENAME":
                continue
            if meta.dtype != str and meta.dtype != datetime:
                try:
                    baseline[col] = baseline[col].astype(meta.dtype)
                except (IntCastingNaNError, ValueError):
                    baseline[col] = baseline[col].astype(float)

        # SIZING, NAMING, HOVER INFORMATION FACTORIZE
        baseline['size'] = self.normalize(baseline['marketCap'], 7, 100)
        baseline['name'] = baseline[['name', 'market']].apply(lambda r: f'{r["name"]}*' if r.market == 'KOSDAQ' else r['name'], axis=1)
        baseline['meta'] = baseline.name + '(' + baseline.index + ')<br>' \
                           + '시가총액: ' + baseline['marketCap'].apply(Tools.krw2currency, div=1e+8) + '원<br>' \
                           + '종가: ' + baseline.close.apply(lambda x: f"{x:,d}원")
        baseline['color'] = baseline['sectorCode'].apply(lambda code: self.rgb2hex(*BUBBLES.COLORS[code]))

        # FACTORIZE
        refactor = baseline.copy()
        for key, meta in METADATA:
            if key == "RENAME":
                continue
            if not meta.limit:
                continue
            if str(meta.limit).startswith('statistic'):
                lower = refactor[key].mean() - int(meta.limit.split(":")[-1]) * refactor[key].std()
                upper = refactor[key].mean() + int(meta.limit.split(":")[-1]) * refactor[key].std()
                refactor[key] = refactor[key].apply(lambda x: x if lower < x < upper else nan)
            if type(meta.limit) == list:
                refactor[key] = refactor[key].clip(lower=meta.limit[0], upper=meta.limit[1])

        for key, meta in METADATA:
            if key == "RENAME":
                continue
            if meta.dtype == float:
                refactor[key] = round(refactor[key], meta.digit)
        refactor = refactor[BUBBLES.SELECTOR + ['size', 'meta', 'color']]
        for key in BUBBLES.KRW:
            refactor[f'{key}Text'] = refactor[key].apply(Tools.krw2currency)
        self.data = refactor

        # SECTOR DATA
        self.sectors = baseline[['sectorCode', 'sectorName', 'color']] \
                       .drop_duplicates().dropna() \
                       .set_index(keys="sectorCode")

        # METADATA
        meta = {}
        for key in BUBBLES.SELECTOR:
            _meta = METADATA[key]
            mean = self.data[key].mean() if  _meta.dtype != str and _meta.dtype != datetime else '',
            meta[key] = {
                "label": _meta.label,
                "unit": _meta.unit,
                "mean": mean,
                "digit": _meta.digit,
            }



        # sectors['colors'] = sectors['sectorCode'].apply(lambda code: self.rgb2hex(*BUBBLES.COLORS[code]))




        # for code, name in self[["sectorCode", "sectorName"]].drop_duplicates().dropna().itertuples(index=False):
        #     self.sector[code] = {'label': name, 'color': colors[code]}
        #
        # self.drop(inplace=True, index=abnormal.index)
        # self.drop(inplace=True, columns=[
        #     "close", "marketCap", "amount", "market", "date",
        #     "industryCode", "industryName", "sectorName", "stockSize",
        # ])
        #
        # meta = {}
        # for col in self.meta:
        #     if col in self:
        #         meta[col] = self.meta[col]
        #         if not self.meta[col]['round'] == -1:
        #             meta[col]['mean'] = round(self[col].mean(), 2)
        # self.meta = meta
        #
        # self._round_up()
        #
        # self.log = f'END [Build Market Bubble] {len(self)} Items / Elapsed: {time() - stime:.2f}s'
        return

    @classmethod
    def rgb2hex(cls, r, g, b) -> str:
        return f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'

    @classmethod
    def normalize(cls, series:Series, mn, mx) -> Series:
        return mn + (series - series.min()) * (mx - mn) / (series.max() - series.min())

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from src.common.env import FILE
    from pandas import read_parquet

    marketBubble = MarketBubble(read_parquet(FILE.BASELINE, engine='pyarrow'))
    print(marketBubble.data)
    # print(marketBubble.data.columns)
    # print(marketBubble.sectors)
    # print(marketBubble.meta)



    # def filterUpper(df, col, factor:int=2) -> DataFrame:
    #     return df[
    #         (df[col] >= df[col].mean()) & \
    #         (df[col] < (df[col].mean() + factor * df[col].std()))
    #     ]
    #
    # def filterLower(df, col, factor:int=2) -> DataFrame:
    #     return df[
    #         (df[col] < df[col].mean()) & \
    #         (df[col] >= (df[col].mean() - factor * df[col].std()))
    #     ]
    #
    #
    # choice = marketBubble.copy()
    # choice = filterUpper(choice, 'M-3')
    # choice = filterUpper(choice, 'M-1')
    # choice = filterUpper(choice, 'pct52wLow')
    # print(choice)
