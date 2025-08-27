from labwons.logs import logger
from labwons.path import ARCHIVE
from labwons.util import DD, DP
from labwons.build.schema import FIELD

from datetime import datetime
from numpy import nan
from pandas import DataFrame, Series
from pandas import concat, read_parquet
from time import perf_counter


FIELD_RENAME = DD(**{item.origin: key for key, item in FIELD.items() if item.origin})
class MarketBaseline:

    BASELINE_DATE:str = ''

    @classmethod
    def build(cls, stdout:bool=False, to_clipboard:bool=False):
        ARCHIVE.refresh()

        stime = perf_counter()
        logger.info('RUN [BUILD MARKET BASELINE]')
        logger.info(f'- FROM ARCHIVE @{ARCHIVE.DATE}')

        number = read_parquet(ARCHIVE.MARKET_DAILY, engine="pyarrow")
        n_date = datetime.strptime(str(number.pop('date').values[-1]), "%Y%m%d%H:%M")
        number = cls.number(number)
        number['date'] = n_date.strftime("%Y-%m-%d")
        logger.info(f'- READ AFTER MARKET: {cls.BASELINE_DATE}')

        overview = read_parquet(ARCHIVE.MARKET_OVERVIEW, engine="pyarrow")
        overview_date = overview.pop('date').value_counts(dropna=False)
        statement_yy = overview.pop('reportYears')
        statement_qq = overview.pop('reportQuarters')
        if len(overview_date) == 1:
            logger.info(f'- READ STATEMENT OVERVIEW: {overview_date.index[0]}')
        else:
            report = ", ".join([f'{d}({n})' for d, n in overview_date.items()])
            logger.info(f'- READ STATEMENT OVERVIEW: LOW RELIABILITY :: {report}')
        overview = cls.overview(overview)
        # print(overview)

        statementA = read_parquet(ARCHIVE.STATEMENT_A, engine="pyarrow")
        logger.info(f'- READ ANNUAL STATEMENT')
        statementA = cls.statementA(statementA, statement_yy)
        # # print(statementA)

        statementQ = read_parquet(ARCHIVE.STATEMENT_Q, engine="pyarrow")
        logger.info(f'- READ QUARTER STATEMENT')
        statementQ = cls.statementQ(statementQ, statement_qq)
        # print(statementQ)

        sector = read_parquet(ARCHIVE.MARKET_SECTORS, engine="pyarrow")
        s_date = datetime.strptime(str(sector.pop('date').values[-1]), "%Y%m%d").strftime("%Y/%m/%d")
        logger.info(f'- READ SECTOR COMPOSITION: {s_date}')
        sector = cls.sector(sector)
        # print(sector)

        merge = cls.merge(number, overview, statementA, statementQ, sector)
        cls.checkMetadata(merge)

        merge.to_parquet(ARCHIVE.write(ARCHIVE.DATE).MARKET_BASELINE, engine='pyarrow')

        if stdout:
            print(merge)
        if to_clipboard:
            merge.to_clipboard()

        cls.BASELINE_DATE = n_date.strftime("%Y/%m/%d")

        logger.info(f'END [BUILD MARKET BASELINE] {len(merge):,d} ITEMS: {perf_counter() - stime:.2f}s')
        return

    @classmethod
    def number(cls, number:DataFrame) -> DataFrame:
        # RENAME AND DROP
        number = number.rename(columns={p: c for p, c in FIELD_RENAME.items() if p in number.columns})
        number = number.drop(columns=[col for col in number if not col in FIELD])
        return number

    @classmethod
    def overview(cls, overview:DataFrame) -> DataFrame:
        overview = overview.rename(columns={p: c for p, c in FIELD_RENAME.items() if p in overview.columns})
        overview = overview.drop(columns=[col for col in overview if not col in FIELD])
        typecast = overview.columns.difference(['stockSplitDate', 'statementType'])
        overview[typecast] = overview[typecast].map(DP.typeCast)
        return overview

    @classmethod
    def sector(cls, sector:DataFrame) -> DataFrame:
        # NOTHING TO MODIFY
        return sector

    @classmethod
    def statementA(cls, statementA:DataFrame, yy:Series) -> DataFrame:
        tickers = statementA.columns.get_level_values(0).unique()
        objs = []
        for ticker in tickers:
            statement = statementA[ticker].loc[yy[ticker].split(",")]
            statement = statement.dropna(how='all', axis=0)
            statement = statement.map(DP.typeCast)
            statement = statement.drop(columns=['BPS(원)', 'DPS(원)'])
            estimated = statement[statement.index.str.contains('\\(E\\)')].copy()
            provision = statement[statement.index.str.contains('\\(P\\)')].copy()
            statement = statement[~statement.index.isin(estimated.index)]

            recentStatement = statement.loc[statement.index[-1]]
            if not provision.empty:
                # IF THERE IS PROVISIONAL STATEMENT(잠정치), BASICALLY PROVISIONAL VALUE WILL BE USED,
                # NaN VALUES OF PROVISIONAL WILL BE REPLACED TO RECENT FISCAL YEAR STATEMENT
                recentStatement = recentStatement.combine_first(statement.iloc[-2])

            obj = Series()
            _revenueKey = statement.columns[0]
            obj['fiscalDate'] = recentStatement.name
            obj['fiscalRevenue'] = recentStatement[_revenueKey]
            obj = concat([obj, recentStatement.drop(index=[_revenueKey])])

            revenueGrowth = 100 * statement[_revenueKey].pct_change(fill_method=None).dropna()
            if not revenueGrowth.empty:
                obj['fiscalRevenueGrowth'] = revenueGrowth.values[-1]
                obj['averageRevenueGrowth'] = revenueGrowth.mean()
                pg = Series(
                    index=['fiscalProfitGrowth', 'fiscalProfitState', 'averageProfitGrowth'],
                    data=DP.profitGrowth(statement['영업이익(억원)'])
                )
                eg = Series(
                    index=['fiscalEpsGrowth', 'fiscalEpsState', 'averageEpsGrowth'],
                    data= DP.profitGrowth(statement['EPS(원)'])
                )
                obj = concat([obj, pg, eg])

            if not estimated.empty:
                # IF THERE IS ESTIMATED STATEMENT(추정치), CLOSEST ESTIMATION DATE WILL BE USED.
                # ESTIMATIONG FOR GROWTH IS ONLY USED FOR REVENUE, PROFIT, AND EPS.

                est = concat([recentStatement, estimated.iloc[0]], axis=1).T
                est = est.rename(columns={p: c.replace("fiscal", "estimated") for p, c in FIELD_RENAME.items() if p in est})
                est = est.rename(columns={est.columns[0]:'estimatedRevenue'})
                obj['estimatedDate'] = est.index[-1]
                obj = concat([obj, est.iloc[-1]])

                if recentStatement[_revenueKey] < 5:
                    obj['estimatedRevenueGrowth'] = nan
                else:
                    obj['estimatedRevenueGrowth'] = 100 * est.pct_change(fill_method=None).iloc[-1]['estimatedRevenue']

                pg = DP.profitGrowth(est['estimatedProfit'])
                obj['estimatedProfitGrowth'] = pg[0]
                obj['estimatedProfitState'] = pg[1]

                eg = DP.profitGrowth(est['estimatedEps'])
                obj['estimatedEpsGrowth'] = eg[0]
                obj['estimatedEpsState'] = eg[1]

            obj['revenueType'] = _revenueKey.replace("(억원)", "")
            obj['numberOfAnnualStatement'] = len(statement)
            obj['averageEps'] = statement['EPS(원)'].mean()
            if len(statement) <= 1:
                obj['weightedAverageEps'] = obj['averageEps']
            else:
                weight = list(range(0, len(statement), 1))
                obj['weightedAverageEps'] = sum(eps * w for eps, w in zip(statement['EPS(원)'], weight)) / sum(weight)
            obj.name = ticker
            objs.append(obj)

        merge = concat(objs=objs, axis=1).T
        merge = merge.rename(columns={p: c for p, c in FIELD_RENAME.items() if p in merge.columns})
        return merge

    @classmethod
    def statementQ(cls, statementQ:DataFrame, qq:Series) -> DataFrame:
        from numpy import seterr
        seterr(all='raise')
        tickers = statementQ.columns.get_level_values(0).unique()
        objs = []
        for ticker in tickers:
            statement = statementQ[ticker].loc[qq[ticker].split(",")]
            statement = statement.dropna(how='all', axis=0)
            statement = statement.map(DP.typeCast)
            statement = statement.drop(columns=['BPS(원)', 'DPS(원)'])
            estimated = statement[statement.index.str.contains('\\(E\\)')].copy()
            provision = statement[statement.index.str.contains('\\(P\\)')].copy()
            statement = statement[~statement.index.isin(estimated.index)]
            recentQuarter = statement.loc[statement.index[-1]]
            if not provision.empty:
                recentQuarter = statement.iloc[-1].combine_first(statement.iloc[-2])

            obj = Series()
            obj['recentAsset'] = recentQuarter['자산총계(억원)']
            obj['recentCapital'] = recentQuarter['자본총계(억원)']
            obj['recentDebt'] = recentQuarter['부채총계(억원)']
            obj['recentDebtRatio'] = recentQuarter['부채비율(%)']
            obj['recentProfitRate'] = recentQuarter['영업이익률(%)']
            if recentQuarter[statement.columns[0]] < 5:
                # IF REVENUE IS LESS THAN 5억원, PROFIT RATE IS NOT USED.
                obj['recentProfitRate'] = nan

            if len(statement) >= 4:
                for key, label in {
                    statement.columns[0]: 'trailingRevenue',
                    '영업이익(억원)': 'trailingProfit',
                    '당기순이익(억원)': 'trailingNetProfit',
                    'EPS(원)': 'trailingEps'
                }.items():
                    trailer = statement[key].iloc[-4:]
                    if trailer.isnull().sum():
                        trailer = statement[key].iloc[-5:-1]
                        if trailer.isnull().sum():
                            # IF THE NUMBER OF TRAILING VALUES IS LESS THAN FOUR,
                            # TRAILING VALUES ARE TO BE REGARD AS UNRELIABLE DATA.
                            break
                    obj[label] = trailer.sum()
            if 'trailingRevenue' in obj and 'trailingProfit' in obj:
                obj['trailingProfitRate'] = 100 * obj['trailingProfit'] / obj['trailingRevenue']

            lastQ = str(recentQuarter.name).replace("(P)", "").split("/")
            yearAgo = statement[statement.index == f'{int(lastQ[0]) - 1}/{lastQ[-1]}']
            if not yearAgo.empty:
                frm = concat([yearAgo.iloc[0], recentQuarter], axis=1).T
                yoy = 100 * frm.pct_change(fill_method=None)
                yoy = yoy.rename(columns={p: c.replace("fiscal", "yoy") for p, c in FIELD_RENAME.items() if p in yoy})
                yoy = yoy.rename(columns={yoy.columns[0]: "yoyRevenue"})
                obj = concat([obj, yoy.iloc[-1]], axis=0)
                ps = DP.profitGrowth(frm['영업이익(억원)'])
                es = DP.profitGrowth(frm['EPS(원)'])
                obj['yoyProfit'] = ps[0]
                obj['yoyProfitState'] = ps[1]
                obj['yoyEps'] = es[0]
                obj['yoyEpsState'] = es[1]

            obj.name = ticker
            objs.append(obj)
        merge = concat(objs=objs, axis=1).T
        return merge

    @classmethod
    def merge(cls, base:DataFrame, *dataframes:DataFrame) -> DataFrame:
        merge = base.join(concat(list(dataframes), axis=1))
        merge = merge[~merge['name'].isna()]
        merge = merge.dropna(how='all', axis=1)

        # CUSTOMIZE SECTION
        merge['fiftyTwoWeekHigh'] = merge[['close', 'fiftyTwoWeekHigh']].max(axis=1)
        merge['fiftyTwoWeekLow'] = merge[['close', 'fiftyTwoWeekLow']].min(axis=1)
        merge['pctFiftyTwoWeekHigh'] = 100 * (merge['close'] / merge['fiftyTwoWeekHigh'] - 1)
        merge['pctFiftyTwoWeekLow'] = 100 * (merge['close'] / merge['fiftyTwoWeekLow'] - 1)
        merge['pctTargetPrice'] = 100 * (merge['close'] / merge['targetPrice'] - 1)
        merge['estimatedPE'] = merge['close'] / merge['estimatedEps'].apply(lambda x: x if x > 0 else nan)
        merge['trailingPS'] = (merge['marketCap'] / 1e+8) / merge['trailingRevenue']
        merge['trailingPE'] = merge['close'] / merge['trailingEps'].apply(lambda x: x if x > 0 else nan)
        merge['turnoverRatio'] = 100 * merge['volume'] / (merge['shares'] * merge['floatShares'] / 100)
        merge['PEG'] = merge['trailingPE'] / merge['estimatedEpsGrowth']
        merge['PEG'] = merge['PEG'].apply(lambda x: x if x > 0 else nan)
        return merge

    @classmethod
    def checkMetadata(cls,base:DataFrame):
        ndef = [c for c in base if c not in FIELD]
        if ndef:
            print("FIELD 미정의 항목")
            for c in ndef:
                print(f'{c}=dDict(')
                print(f"\tlabel='label',")
                print(f"\tunit='%',")
                print(f"\tdtype=float,")
                print(f"\tdigit=2,")
                print(f"\torigin='',")
                print(f"\tlimit=False,")
                print(f"\t# Adder")
                print(f"),")

        ddef = [m for m, v in FIELD.items() if m not in base and not "RENAME" == m]
        if ddef:
            print("불필요 FIELD 항목")
            for m in ddef:
                print(m)
        return

    @classmethod
    def gaussian(cls, data:DataFrame, col:str):
        # INTERNAL
        import plotly.graph_objs as go
        from scipy.stats import norm
        from pandas import concat, Series


        y = Series(index=data.index, data=norm.pdf(data[col], data[col].mean(), data[col].std()), name='y')
        m = data['name'] + '(' + data.index + ')'
        m.name = 'm'
        subset = concat([data[col], y, m], axis=1).sort_values(by=col)

        # print(data[data.index.isin(subset.tail(5).index)])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=subset[col],
            y=subset.y,
            mode='lines+markers',
            showlegend=False,
            meta=subset.m,
            hovertemplate="%{meta}: %{x}<extra></extra>"
        ))

        xs = [
            [subset[col].mean() - 2 * subset[col].std()] * len(subset),
            [subset[col].mean() - 1 * subset[col].std()] * len(subset),
            [subset[col].mean() + 1 * subset[col].std()] * len(subset),
            [subset[col].mean() + 2 * subset[col].std()] * len(subset),
            [subset[col].mean()] * len(subset)
        ]
        for x in xs:
            fig.add_trace(go.Scatter(
                x=x,
                y=subset.y,
                mode='lines',
                showlegend=False,
                line={
                    'color':'black',
                    'dash':'dot'
                },
                hoverinfo='skip'
            ))

        fig.update_layout(
            xaxis_title="Value",
            yaxis_title="Density",
        )
        fig.show('browser')
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    MarketBaseline.build(
        save=False,
        stdout=False,
        to_clipboard=True
    )
