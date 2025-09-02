from labwons.path import Archive
from labwons.util import DP
from labwons.logs import logger
from labwons.build.schema import FIELD, SELECTOR, PROPERTY, COLORS

from datetime import datetime
from pandas import concat, DataFrame
from pandas.errors import IntCastingNaNError
from pykrx.stock import get_index_portfolio_deposit_file
from time import perf_counter
from typing import List
import pandas as pd



class MarketMap:

    @classmethod
    def build(cls, archive:Archive):
        logger.info('RUN [BUILD MARKET MAP]')

        stime = perf_counter()
        baseline = pd.read_parquet(archive.MARKET_BASELINE, engine='pyarrow')
        b = baseline.copy()

        # PRE-PROCESS: RESIZE DATAFRAME TO LARGE CAPS.
        # TYPE CASTING BEFORE FACTORIZE MAP DATA.
        b = b[b["capGroup"] == "largeCap"]
        for col, meta in FIELD.items():
            if meta.dtype != str and meta.dtype != datetime:
                try:
                    b[col] = b[col].astype(meta.dtype)
                except (IntCastingNaNError, ValueError):
                    b[col] = b[col].astype(float)

        # SIZING, NAMING, HOVER INFORMATION FACTORIZE
        b['size'] = (b['marketCap'] / 1e+8).astype(int)
        b['name'] = b[['name', 'market']].apply(lambda r: f'{r["name"]}*' if r.market == 'KOSDAQ' else r['name'], axis=1)
        b['ceiling'] = b['industryName']
        b['meta'] = b.name + '(' + b.index + ')<br>' + '시가총액: ' + b['marketCap'].apply(DP.krw2currency) + '원<br>' \
                    + '종가: ' + b.close.apply(lambda x: f"{x:,d}원")

        # IF INDUSTRY == SECTOR, INDUSTRY INFORMATION WILL BE DROPPED.
        _duplicated = b[b.industryName == b.sectorName]["sectorName"].drop_duplicates().tolist()

        # INCLUDE SAMSUNG(005930) CASE
        ws_industry = cls.grouping(b, "industryName")
        ws_industry.index = ws_industry.index.str.pad(width=6, side="left", fillchar='W')
        ws_industry = ws_industry[~ws_industry["name"].isin(_duplicated)]

        ws_sector = cls.grouping(b, "sectorName")
        ws_sector["ceiling"] = "대형주"
        ws_sector.index = ws_sector.index.str.pad(width=6, side="left", fillchar='W')

        ws_top = DataFrame(b.select_dtypes(include=['int']).sum()).T
        ws_top[['name', 'meta']] = ['대형주', DP.krw2currency(ws_top.iloc[0]['marketCap'])]
        ws_top.index = ['WS0000']

        # EXCLUDE SAMSUNG(005930) CASE
        ns_industry = cls.grouping(b, "industryName", "005930")
        ns_industry.index = ns_industry.index.str.pad(width=6, side="left", fillchar='N')
        ns_industry = ns_industry[~ns_industry["name"].isin(_duplicated)]

        ns_sector = cls.grouping(b, "sectorName", "005930")
        ns_sector["ceiling"] = "대형주(삼성전자 제외)"
        ns_sector.index = ns_sector.index.str.pad(width=6, side="left", fillchar='N')

        ns_top = DataFrame(b[~b.index.isin(['005930'])].select_dtypes(include=['int']).sum()).T
        ns_top[['name', 'meta']] = ["대형주(삼성전자 제외)", DP.krw2currency(ns_top.iloc[0]['marketCap'])]
        ns_top.index = ['NS0000']

        base = concat([b, ws_industry, ns_industry, ws_sector, ns_sector, ws_top, ns_top], axis=0)
        base = base[SELECTOR.MARKET_MAP]
        base = base.join(cls.paint(base), how='left')

        # CONVERT BASE DATA TO DISPLAYABLE FORMAT: HOVER, STATIC TEXT
        for key, meta in FIELD.items():
            if key in PROPERTY.MARKET_MAP:
                if meta.dtype == int:
                    base[key] = base[key].astype(int).astype(str) + meta.unit
                if meta.dtype == float:
                    base[key] = round(base[key], meta.digit).astype(str) + meta.unit

        for key in PROPERTY.MARKET_MAP:
            if key == 'pctFiftyTwoWeekHigh':
                base.loc[base[key] == '0.0%', key] = '52주 최고가'
            elif key == 'pctFiftyTwoWeekLow':
                base.loc[base[key] == '0.0%', key] = '52주 최저가'
            else:
                base.loc[(base[key] == 'nan%') | (base[key] == 'nan'), key] = '미제공'
            base.loc[["WS0000", "NS0000"], key] = ""

        ingredient = ['estimatedProfitState', 'estimatedEpsState', 'yoyProfitState', 'yoyEpsState', 'trailingEps']
        base = base.join(baseline[ingredient])
        base['estimatedProfitGrowth'] = base['estimatedProfitState'].combine_first(base['estimatedProfitGrowth'])
        base['estimatedEpsGrowth'] = base['estimatedEpsState'].combine_first(base['estimatedEpsGrowth'])
        base['trailingPE'] = base.apply(lambda r: '적자' if r.trailingEps <= 0 else r.trailingPE , axis=1)
        base['yoyProfit'] = base['yoyProfitState'].combine_first(base['yoyProfit'])
        base['yoyEps'] = base['yoyEpsState'].combine_first(base['yoyEps'])

        # advance = ['estimatedProfitState', 'estimatedEpsState', 'trailingEps',
        #            'yoyProfitState', 'yoyEpsState']
        # refactor = refactor.join(resource[advance])
        # refactor['estimatedProfitGrowth'] = refactor['estimatedProfitState'].combine_first(refactor['estimatedProfitGrowth'])
        # refactor['estimatedEpsGrowth'] = refactor['estimatedEpsState'].combine_first(refactor['estimatedEpsGrowth'])
        # refactor['trailingPE'] = refactor[['trailingPE', 'trailingEps']].apply(lambda r: '적자' if r.trailingEps <= 0 else r.trailingPE , axis=1)
        # refactor['yoyProfit'] = refactor['yoyProfitState'].combine_first(refactor['yoyProfit'])
        # refactor['yoyEps'] = refactor['yoyEpsState'].combine_first(refactor['yoyEps'])
        # refactor = refactor.drop(columns=advance)
        # self.data = data = refactor.join(self.paint(base))
        # # self.data.to_clipboard()
        #
        # meta = {}
        # for key, _meta in MARKETMAP:
        #     if key == "COLORS":
        #         continue
        #     meta[key] = {
        #         'label': METADATA[key].label,
        #         'unit': METADATA[key].unit,
        #         'scale': _meta.scale,
        #         'color': [self.rgb2hex(*rgb) for rgb in MARKETMAP.COLORS[_meta.color]],
        #     }
        # self.meta = meta
        #
        # self.stat = self.minmax(base)

        base.to_parquet(archive.to().MARKET_MAP, engine='pyarrow')

        logger.info(f'END [BUILD MARKET MAP] {len(base):,d} ITEMS: {perf_counter() - stime:.2f}s')
        return

    @classmethod
    def rgb2hex(cls, r, g, b) -> str:
        return f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'

    @classmethod
    def interpolate(cls, x, x1, y1, x2, y2):
        return ((y2 - y1) / (x2 - x1)) * (x - x1) + y1

    @classmethod
    def grouping(cls, frm:DataFrame, key:str, *exclude:str) -> DataFrame:
        objs = []
        for name, group in frm.groupby(by=key):
            if exclude:
                group = group[~group.index.isin(exclude)]
            '''
            Default Grouping Factors: 
            Weighted Mean
            '''
            size = group['size'].sum()
            w = group['size'] / size
            obj = {col: (w * group[col]).sum() for col in group if group[col].dtype in [float, int]}
            obj.update({
                "ticker": group.iloc[0][key.replace("Name", "Code")],
                "name": name,
                "size": size,
                "ceiling": 'TBD' if key.startswith('sector') else group.iloc[0]['sectorName'],
                'meta': f'{name}<br>시가총액: {DP.krw2currency(size)}원'
            })
            '''
            Exception Grouping Factors:
            Arithmetic Mean
            '''
            # Not Defined Yet

            objs.append(obj)
        return DataFrame(data=objs).set_index(keys='ticker')

    @classmethod
    def paint(cls, frm:DataFrame) -> DataFrame:

        def _paint_(_value, _scale, _color, _index):
            if _value <= _scale[0]:
                return cls.rgb2hex(*_color[0])
            if _value >= _scale[-1]:
                return cls.rgb2hex(*_color[-1])

            n = 0
            while n < len(_scale) - 1:
                if _scale[n] < _value <= _scale[n + 1]:
                    break
                n += 1

            if n == len(_scale) - 1:
                return cls.rgb2hex(*_color[_index])

            r1, g1, b1 = _color[n]
            r2, g2, b2 = _color[n + 1]
            return cls.rgb2hex(
                cls.interpolate(_value, _scale[n], r1, _scale[n + 1], r2),
                cls.interpolate(_value, _scale[n], g1, _scale[n + 1], g2),
                cls.interpolate(_value, _scale[n], b1, _scale[n + 1], b2)
            )

        objs = {}
        for key, meta in PROPERTY.MARKET_MAP.items():
            if "scale" in meta:
                objs[f'{key}_C'] = frm[key].apply(_paint_,
                                                  _scale=meta.scale,
                                                  _color=COLORS[meta.color],
                                                  _index=meta.index)
        colors = concat(objs, axis=1)
        colors.iloc[-2:] = "#C8C8C8"
        return colors

    @classmethod
    def minmax(cls, frm:DataFrame) -> DataFrame:
        objs = {}
        cols = ["min", "max", "minT", "maxT", "minC", "maxC", "minI", "maxI", "label", "minTicker", "maxTicker"]
        for key, meta in MARKETMAP:
            if key == 'COLORS' or not key in cls.specials:
                continue
            data = frm[key]
            _min = frm[frm[key] == data.min()]
            _max = frm[frm[key] == data.max()]
            minv = METADATA[key].dtype(data.min())
            maxv = METADATA[key].dtype(data.max())
            if METADATA[key].dtype == float:
                minv = f'{minv:.2f}' if key == 'beta' else f'{minv:,.1f}'
                maxv = f'{maxv:.2f}' if key == 'beta' else f'{maxv:,.1f}'
            objs[key] = [
                f'{"-" if len(_min) > 1 else minv}{METADATA[key].unit}',
                f'{"-" if len(_max) > 1 else maxv}{METADATA[key].unit}',
                "(복수 종목)" if len(_min) > 1 else _min.iloc[0]['name'],
                "(복수 종목)" if len(_max) > 1 else _max.iloc[0]['name'],
                cls.rgb2hex(*MARKETMAP.COLORS[meta.color][0]),
                cls.rgb2hex(*MARKETMAP.COLORS[meta.color][-1]),
                meta.iconMin,
                meta.iconMax,
                METADATA[key].label,
                None if len(_min) > 1 else _min.index[0],
                None if len(_max) > 1 else _max.index[0],
            ]
        return DataFrame(data=objs, index=cols)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    MarketMap.build(archive=False)