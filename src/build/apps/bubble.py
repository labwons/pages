try:
    from ...common.env import TICKERS
    from ...common.util import krw2currency
    from ..baseline.metadata import METADATA, BUBBLES
except ImportError:
    from src.common.env import TICKERS
    from src.common.util import krw2currency
    from src.build.baseline.metadata import METADATA, BUBBLES
from datetime import datetime
from numpy import nan
from pandas import DataFrame, Series, concat
from pandas.errors import IntCastingNaNError
from time import perf_counter
from typing import List


class MarketBubble:

    _log: List[str] = []
    specials = [
        "name",
        "return1Day",
        "return1Week",
        "return1Month",
        "return3Month",
        "return6Month",
        "return1Year",
        "pctFiftyTwoWeekHigh",
        "pctFiftyTwoWeekLow"
    ]

    def __init__(self, baseline:DataFrame):
        stime = perf_counter()
        self.log = f'  >> BUILD [BUBBLES]'

        resource = baseline.copy()

        # TYPE CASTING BEFORE FACTORIZE BUBBLE DATA.
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
                           + '시가총액: ' + baseline['marketCap'].apply(krw2currency, limit='억') + '원<br>' \
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
            refactor[f'{key}Text'] = (1e8 * refactor[key]).apply(krw2currency)
        self.data = refactor

        # SECTOR DATA
        self.sectors = baseline[['sectorCode', 'sectorName', 'color']] \
                       .drop_duplicates().dropna() \
                       .set_index(keys="sectorCode")
        self.sectors = concat([
            DataFrame({'sectorName': "전체", 'color': 'royalblue'}, index=['ALL']),
            self.sectors
        ])

        # METADATA
        meta = {}
        for key in BUBBLES.SELECTOR:
            _meta = METADATA[key]
            mean = self.data[key].mean() if  _meta.dtype != str and _meta.dtype != datetime else nan
            meta[key] = {
                "label": _meta.label,
                "unit": _meta.unit,
                "mean": round(mean, 4),
                "dtype": "int" if "int" in str(_meta.dtype) else "float" if "float" in str(_meta.dtype) else "str",
                "digit": _meta.digit,
                "text": key in BUBBLES.KRW
            }
        self.meta = meta

        self.log = f'  >> BUILD END: {perf_counter() - stime:.2f}s'
        self._log[0] += f': {len(self.data):,d} items'
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

    @property
    def todaySpecials(self) -> list:
        data = self.data.copy()
        filtered = data[
            (data['return3Month'] >= data['return3Month'].mean()) & \
            (data['return1Month'] >= data['return1Month'].mean()) & \
            (data['return1Week'] >= data['return1Week'].mean()) & \
            (data['pctFiftyTwoWeekHigh'] >= data['pctFiftyTwoWeekHigh'].mean()) & \

            (data['pctFiftyTwoWeekLow'] <= data['pctFiftyTwoWeekLow'].mean()) & \
            (data['estimatedPE'] <= data['estimatedPE'].mean()) & \
            (data['trailingPE'] <= data['trailingPE'].mean())
        ]
        specials = filtered.index.tolist()
        if len(specials) > 20:
            specials = specials[:20]
        return specials

    @property
    def specialSLabel(self) -> list:
        return [
            f"{self.meta[key]['label']}({self.meta[key]['unit']})" if not key == "name" else f"{self.meta[key]['label']}"
            for key in self.specials]

    def selectSpecials(self, tickers:list) -> list:
        filtered = self.data.loc[tickers][self.specials]
        rows = []
        for row in filtered.itertuples(index=True):
            row = list(row)
            row[1] = f'{row[1]}<br>({row[0]})'
            rows.append(row)
        return rows


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    from src.common.env import FILE
    from pandas import read_parquet

    marketBubble = MarketBubble(read_parquet(FILE.BASELINE, engine='pyarrow'))
    # print(marketBubble.data)
    # print(marketBubble.data.columns)
    # print(marketBubble.sectors)
    # print(marketBubble.meta)