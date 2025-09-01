from labwons.util import DD
from datetime import datetime


FIELD = DD(
    close=DD(
        label='종가',
        unit='원',
        dtype=int,
        digit=0,
        origin='종가',
        limit=False,
        # Adder
    ),
    marketCap=DD(
        label='시가총액',
        unit='억원',
        dtype=int,
        digit=0,
        origin='시가총액',
        limit=False,
        # Adder
    ),
    volume=DD(
        label='거래량',
        unit='',
        dtype=int,
        digit=0,
        origin='거래량',
        limit=False,
        # Adder
    ),
    amount=DD(
        label='거래대금',
        unit='원',
        dtype=int,
        digit=0,
        origin='거래대금',
        limit=False,
        # Adder
    ),
    shares=DD(
        label='상장주식수',
        unit='',
        dtype=int,
        digit=0,
        origin='상장주식수',
        limit=False,
        # Adder
    ),
    priceToBook=DD(
        label='PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR',
        limit=False,
        # Adder
    ),
    recentBPS=DD(
        label='BPS',
        unit='원',
        dtype=int,
        digit=0,
        origin='BPS',
        limit=False,
        # Adder
    ),
    dividendYield=DD(
        label='배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='DIV',
        limit=False,
        # Adder
    ),
    foreignRate=DD(
        label='외인보유율',
        unit='%',
        dtype=float,
        digit=2,
        origin='지분율',
        limit=False,
        # Adder
    ),
    return1Day=DD(
        label='1일 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Week=DD(
        label='1주 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Month=DD(
        label='1개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return2Month=DD(
        label='2개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return3Month=DD(
        label='3개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return6Month=DD(
        label='6개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Year=DD(
        label='1년 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    capGroup=DD(
        label='추종 지수 분류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiftyTwoWeekHigh=DD(
        label='52주최고가',
        unit='원',
        dtype=int,
        digit=0,
        origin='high52week',
        limit=False,
        # Adder
    ),
    fiftyTwoWeekLow=DD(
        label='52주최저가',
        unit='원',
        dtype=int,
        digit=0,
        origin='low52week',
        limit=False,
        # Adder
    ),
    date=DD(
        label='최근거래일',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    beta=DD(
        label='베타',
        unit='',
        dtype=float,
        digit=4,
        origin='',
        limit=False,
        # Adder
    ),
    floatShares=DD(
        label='유동주식비율',
        unit='%',
        dtype=float,
        digit=2,
        origin='ff_sher_rt',
        limit=False,
        # Adder
    ),
    stockSplitDate=DD(
        label='최근 액면분할일자',
        unit='',
        dtype=datetime,
        digit=0,
        origin='face_value_chg_dt',
        limit=False,
        # Adder
    ),
    targetPrice=DD(
        label='목표가',
        unit='원',
        dtype=int,
        digit=0,
        origin='target_price',
        limit=False,
        # Adder
    ),
    forwardEps=DD(
        label='추정EPS',
        unit='원',
        dtype=int,
        digit=0,
        origin='eps',
        limit=False,
        # Adder
    ),
    numberOfEstimation=DD(
        label='추정기관수',
        unit='',
        dtype=int,
        digit=0,
        origin='presume_organ_count',
        limit=False,
        # Adder
    ),
    statementType=DD(
        label='재무제표 종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalDate=DD(
        label='직전 회계연도',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalRevenue=DD(
        label='매출액(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalProfit=DD(
        label='영업이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='영업이익(억원)',
        limit=False,
        # Adder
    ),
    fiscalNetProfit=DD(
        label='당기순이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='당기순이익(억원)',
        limit=False,
        # Adder
    ),
    fiscalProfitRate=DD(
        label='영업이익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='영업이익률(%)',
        limit='statistic:1',
        # Adder
    ),
    fiscalAsset=DD(
        label='총 자산(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자산총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalCapital=DD(
        label='총 자본(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자본총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalDebt=DD(
        label='총 부채(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='부채총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalDebtRatio=DD(
        label='부채비율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='부채비율(%)',
        limit=False,
        # Adder
    ),
    fiscalRetentionRatio=DD(
        label='유보율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='유보율(%)',
        limit=False,
        # Adder
    ),
    fiscalRoA=DD(
        label='RoA(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROA(%)',
        limit=False,
        # Adder
    ),
    fiscalRoE=DD(
        label='RoE(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROE(%)',
        limit=False,
        # Adder
    ),
    fiscalEps=DD(
        label='EPS(직전 회계연도 기준)',
        unit='원',
        dtype=int,
        digit=0,
        origin='EPS(원)',
        limit=False,
        # Adder
    ),
    fiscalDividendYield=DD(
        label='배당수익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='배당수익률(%)',
        limit=False,
        # Adder
    ),
    fiscalPE = DD(
        label='PER(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PER(배)',
        limit='statistic:1',
        # Adder
    ),
    fiscalPriceToBook=DD(
        label='PBR(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR(배)',
        limit=False,
        # Adder
    ),
    fiscalRevenueGrowth=DD(
        label='매출성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalProfitGrowth=DD(
        label='영업이익성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalEpsGrowth=DD(
        label='EPS성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),

    averageRevenueGrowth=DD(
        label='연평균 매출성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    averageProfitGrowth=DD(
        label='연평균 영업이익성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    averageEpsGrowth=DD(
        label='연평균 EPS성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    trailingRevenue=DD(
        label='매출액',
        unit='억원',
        dtype=float,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    trailingEps=DD(
        label='EPS',
        unit='원',
        dtype=float,
        digit=1,
        origin='',
        limit=False,
        # Adder
    ),
    trailingProfitRate=DD(
        label='영업이익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedPE=DD(
        label='Forward PE',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    trailingPS=DD(
        label='PSR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=[0, 200],
        # Adder
    ),
    trailingPE=DD(
        label='PER',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    turnoverRatio=DD(
        label="거래회전율",
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    market=DD(
        label='시장구분',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    name=DD(
        label='종목명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    industryCode=DD(
        label='산업코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    industryName=DD(
        label='산업명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    sectorCode=DD(
        label='섹터코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    sectorName=DD(
        label='섹터명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalProfitState=DD(
        label='영업이익현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalEpsState=DD(
        label='EPS현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDate=DD(
        label='추정 월',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRevenue=DD(
        label='매출(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfit=DD(
        label='영업이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedNetProfit=DD(
        label='당기순이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedAsset=DD(
        label='총 자산(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDebt=DD(
        label='총 부채(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedCapital=DD(
        label='총 자본(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDebtRatio=DD(
        label='부채율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitRate=DD(
        label='영업이익율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRoA=DD(
        label='RoA(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRoE=DD(
        label='RoE(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEps=DD(
        label='EPS(추정치)',
        unit='원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedPriceToBook=DD(
        label='추정PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRevenueGrowth=DD(
        label='매출성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitGrowth=DD(
        label='영업이익성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEpsGrowth=DD(
        label='EPS성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitState=DD(
        label='영업이익성장율(추정치) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEpsState=DD(
        label='EPS성장율(추정치) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    revenueType=DD(
        label='매출종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentAsset=DD(
        label='총 자산',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentCapital=DD(
        label='총 자본',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentDebt=DD(
        label='총 부채',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentDebtRatio=DD(
        label='부채율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    recentProfitRate=DD(
        label='영업이익율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    trailingProfit=DD(
        label='영업이익(4분기 연속)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    trailingNetProfit=DD(
        label='당기순이익(4분기 연속)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    pctFiftyTwoWeekHigh=DD(
        label='52주최고가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    pctFiftyTwoWeekLow=DD(
        label='52주최저가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    pctTargetPrice=DD(
        label='목표가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRevenue=DD(
        label='매출액(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    yoyProfit=DD(
        label='영업이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyNetProfit=DD(
        label='당기순이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    yoyAsset=DD(
        label='총 자산(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDebt=DD(
        label='총 부채(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyCapital=DD(
        label='총 자본(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDebtRatio=DD(
        label='부채비율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRetentionRatio=DD(
        label='유보율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyProfitRate=DD(
        label='영업이익율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRoA=DD(
        label='RoA(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRoE=DD(
        label='RoE(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyEps=DD(
        label='EPS(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    yoyPriceToBook=DD(
        label='PBR(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDividendYield=DD(
        label='배당수익률(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyProfitState=DD(
        label='영업이익율(YoY) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    yoyEpsState=DD(
        label='EPS(YoY) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    numberOfAnnualStatement=DD(
        label='재무개수(연)',
        unit='',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    averageEps=DD(
        label='평균EPS',
        unit='원',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    weightedAverageEps=DD(
        label='가중평균EPS',
        unit='원',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    PEG=DD(
        label='PEG',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
)
FIELD.rename = lambda container: DD({item.origin: key for key, item in FIELD.items() if item.origin in container})
FIELD.rename_all = lambda : DD({item.origin: key for key, item in FIELD.items() if item.origin})

PROPERTY = DD(
    MARKET_MAP=DD(
        return1Day=DD(
            scale=[-3, -2, -1, 0, 1, 2, 3],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return1Week=DD(
            scale=[-6, -4, -2, 0, 2, 4, 6],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return1Month=DD(
            scale=[-10, -6.7, -3.3, 0, 3.3, 6.7, 10],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return2Month=DD(
            scale=[-15, -10, -5, 0, 5, 10, 15],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return3Month=DD(
            scale=[-21, -14, -7, 0, 7, 14, 21],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return6Month=DD(
            scale=[-27, -18, -9, 0, 9, 18, 27],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        return1Year=DD(
            scale=[-36, -24, -12, 0, 12, 24, 36],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        pctFiftyTwoWeekHigh=DD(
            scale=[-45, -30, -15, 0, 0, 0, 0],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        pctFiftyTwoWeekLow=DD(
            scale=[0, 0, 0, 0, 15, 30, 45],
            color='BLUE2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        pctTargetPrice=DD(
            scale=[-20, -10, -5, 0, 5, 10, 20],
            color='GREEN2RED',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        dividendYield=DD(
            scale=[0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            color='RED2GREEN',
            index=0,
            iconMax='bi-hand-thumbs-up',
            iconMin='bi-hand-thumbs-down',
            # map-attribute
        ),
        foreignRate=DD(
            scale=[0, 0, 0, 0, 20, 40, 60],
            color='RED2GREEN',
            index=3,
            iconMax='bi-person-up',
            iconMin='bi-person-down',
            # map-attribute
        ),
        yoyRevenue=DD(
            scale=[-30, -20, -10, 0, 10, 20, 30],
            color='RED2GREEN',
            index=3,
            iconMax='bi-building-up',
            iconMin='bi-building-down',
            # map-attribute
        ),
        yoyProfit=DD(
            scale=[-120, -80, -40, 0, 40, 80, 120],
            color='RED2GREEN',
            index=3,
            iconMax='bi-database-up',
            iconMin='bi-database-down',
            # map-attribute
        ),
        yoyEps=DD(
            scale=[-90, -60, -30, 0, 30, 60, 90],
            color='RED2GREEN',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        trailingPS=DD(
            scale=[0.5, 2, 3.5, 5, 6.5, 8, 9.5],
            color='GREEN2RED',
            index=3,
            iconMax='bi-arrow-up-square',
            iconMin='bi-arrow-down-square',
            # map-attribute
        ),
        trailingPE=DD(
            scale=[5, 10, 20, 30, 40, 50, 60],
            color='GREEN2RED',
            index=3,
            iconMax='bi-arrow-up-square',
            iconMin='bi-arrow-down-square',
            # map-attribute
        ),
        trailingProfitRate=DD(
            scale=[-15, -10, -5, 0, 5, 10, 15],
            color='RED2GREEN',
            index=3,
            iconMax='bi-building-up',
            iconMin='bi-building-down',
            # map-attribute
        ),
        estimatedRevenueGrowth=DD(
            scale=[-10, -5, 0, 5, 10, 15, 20],
            color='RED2GREEN',
            index=3,
            iconMax='bi-building-up',
            iconMin='bi-building-down',
            # map-attribute
        ),
        estimatedProfitRate=DD(
            scale=[-15, -10, -5, 0, 5, 10, 15],
            color='RED2GREEN',
            index=3,
            iconMax='bi-database-up',
            iconMin='bi-database-down',
            # map-attribute
        ),
        estimatedProfitGrowth=DD(
            scale=[-50, -25, 0, 25, 50, 75, 100],
            color='RED2GREEN',
            index=3,
            iconMax='bi-database-up',
            iconMin='bi-database-down',
            # map-attribute
        ),
        estimatedEpsGrowth=DD(
            scale=[-50, -25, 0, 25, 50, 75, 100],
            color='RED2GREEN',
            index=3,
            iconMax='bi-graph-up-arrow',
            iconMin='bi-graph-down-arrow',
            # map-attribute
        ),
        estimatedPE=DD(
            scale=[5, 10, 20, 30, 40, 50, 60],
            color='GREEN2RED',
            index=3,
            iconMax='bi-arrow-up-square',
            iconMin='bi-arrow-down-square',
            # map-attribute
        ),
    ),)

SELECTOR = DD(
    # MARKET_MAP=[
    #     'return1Day', 'return1Week', 'return1Month', 'return2Month', 'return3Month', 'return6Month', 'return1Year',
    #     'pctFiftyTwoWeekHigh', 'pctFiftyTwoWeekLow', 'pctTargetPrice', 'dividendYield', 'foreignRate',
    #     'yoyRevenue', 'yoyProfit', 'yoyEps', 'trailingPS', 'trailingPE', 'trailingProfitRate',
    #     'estimatedRevenueGrowth', 'estimatedProfitRate', 'estimatedProfitGrowth', 'estimatedEpsGrowth', 'estimatedPE',
    #     'meta', 'ceiling', 'size', 'name'
    # ],
    MARKET_MAP = list(PROPERTY.MARKET_MAP.keys()) + ['meta', 'ceiling', 'size', 'name'],
    MARKET_BUBBLE=[
        # 수익률 지표
        'return1Day', 'return1Week', 'return1Month', 'return2Month', 'return3Month', 'return6Month', 'return1Year',
        'pctFiftyTwoWeekHigh', 'pctFiftyTwoWeekLow', 'pctTargetPrice', 'dividendYield',

        # 수급 지표
        'volume', 'turnoverRatio', 'foreignRate',

        # Multiples
        'trailingPS', 'trailingPE', 'priceToBook',
        'estimatedPE', 'estimatedPriceToBook',

        # 재무
        'fiscalRevenue', 'fiscalProfit', 'fiscalNetProfit',
        'estimatedRevenue', 'estimatedProfit', 'estimatedNetProfit',
        'trailingRevenue', 'trailingProfit',

        # 재무 비율
        'fiscalProfitRate', 'fiscalRoA', 'fiscalRoE',
        'fiscalRevenueGrowth', 'fiscalProfitGrowth', 'fiscalProfitState',
        'estimatedRevenueGrowth', 'estimatedProfitGrowth', 'estimatedProfitState',
        'recentProfitRate', 'trailingProfitRate',
        'averageRevenueGrowth', 'averageProfitGrowth',
        'estimatedProfitRate', 'estimatedRoA', 'estimatedRoE',
        'fiscalDebtRatio', 'estimatedDebtRatio', 'recentDebtRatio',
        'yoyRevenue', 'yoyProfit', 'yoyNetProfit', 'yoyProfitState',
        'yoyAsset', 'yoyDebt',

        # 투자 지표
        'fiscalEps', 'forwardEps', 'estimatedEps',
        'fiscalEpsGrowth', 'fiscalEpsState',
        'trailingEps',
        'estimatedEpsGrowth', 'estimatedEpsState',
        'averageEpsGrowth',
        'beta', 'yoyEps', 'yoyEpsState', 'PEG',

        # 기타
        'revenueType', 'name', 'sectorCode'
    ]
)

COLORS = DD(
    BLUE2RED = [
        (24, 97, 168), #1861A8
        (34, 139, 230), #228BE6
        (116, 192, 252), #74C0FC
        (168, 168, 168), #A6A6A6
        (255, 135, 135), #FF8787
        (240, 62, 62), #F03E3E
        (201, 42, 42) #C92A2A
    ],
    RED2BLUE = [
        (201, 42, 42), #C92A2A
        (240, 62, 62), #F03E3E
        (255, 135, 135), #FF8787
        (168, 168, 168), #A6A6A6
        (116, 192, 252), #74C0FC
        (34, 139, 230), #228BE6
        (24, 97, 168) #1861A8
    ],
    RED2GREEN = [
        (246, 53, 56), #F63538
        (191, 64, 69), #BF4045
        (139, 68, 78), #8B444E
        (65, 69, 84), #414554
        (53, 118, 78), #35764E
        (47, 158, 79), #2F9E4F
        (48, 204, 90) #30CC5A
    ],
    GREEN2RED = [
        (48, 204, 90), #30CC5A
        (47, 158, 79), #2F9E4F
        (53, 118, 78), #35764E
        (65, 69, 84), #414554
        (139, 68, 78), #8B444E
        (191, 64, 69), #BF4045
        (246, 53, 56) #F63538
    ],
    SECTORS = DD(
        G10=(92, 168, 155),
        G15=(86, 152, 168),
        G20=(96, 103, 184),
        G25=(195, 102, 56),
        G30=(96, 185, 120),
        G35=(94, 156, 59),
        G40=(142, 182, 77),
        G45=(207, 90, 92),
        G50=(210, 145, 65),
        G55=(86, 80, 199),
        G99=(132, 62, 173)
    )
)



# FIELD_BUBBLES = DD(
#     COLORS=DD(
#         G10=(92,168,155),
#         G15=(86, 152, 168),
#         G20=(96, 103, 184),
#         G25=(195, 102, 56),
#         G30=(96, 185, 120),
#         G35=(94, 156, 59),
#         G40=(142, 182, 77),
#         G45=(207, 90, 92),
#         G50=(210, 145, 65),
#         G55=(86, 80, 199),
#         G99=(132, 62, 173)
#     ),
#     SELECTOR=[
#         # 수익률 지표
#         'return1Day', 'return1Week', 'return1Month', 'return2Month', 'return3Month', 'return6Month', 'return1Year',
#         'pctFiftyTwoWeekHigh', 'pctFiftyTwoWeekLow', 'pctTargetPrice', 'dividendYield',
#
#         # 수급 지표
#         'volume', 'turnoverRatio', 'foreignRate',
#
#         # Multiples
#         'trailingPS', 'trailingPE', 'priceToBook',
#         'estimatedPE', 'estimatedPriceToBook',
#
#         # 재무
#         'fiscalRevenue', 'fiscalProfit', 'fiscalNetProfit',
#         'estimatedRevenue', 'estimatedProfit', 'estimatedNetProfit',
#         'trailingRevenue', 'trailingProfit',
#
#         # 재무 비율
#         'fiscalProfitRate', 'fiscalRoA', 'fiscalRoE',
#         'fiscalRevenueGrowth', 'fiscalProfitGrowth', 'fiscalProfitState',
#         'estimatedRevenueGrowth', 'estimatedProfitGrowth', 'estimatedProfitState',
#         'recentProfitRate', 'trailingProfitRate',
#         'averageRevenueGrowth', 'averageProfitGrowth',
#         'estimatedProfitRate', 'estimatedRoA', 'estimatedRoE',
#         'fiscalDebtRatio', 'estimatedDebtRatio', 'recentDebtRatio',
#         'yoyRevenue', 'yoyProfit', 'yoyNetProfit', 'yoyProfitState',
#         'yoyAsset', 'yoyDebt',
#
#         # 투자 지표
#         'fiscalEps', 'forwardEps', 'estimatedEps',
#         'fiscalEpsGrowth', 'fiscalEpsState',
#         'trailingEps',
#         'estimatedEpsGrowth', 'estimatedEpsState',
#         'averageEpsGrowth',
#         'beta', 'yoyEps', 'yoyEpsState', 'PEG',
#
#         # 기타
#         'revenueType', 'name', 'sectorCode'
#     ],
#     KRW=[
#         'fiscalRevenue', 'fiscalProfit', 'fiscalNetProfit',
#         'estimatedRevenue', 'estimatedProfit', 'estimatedNetProfit',
#         'trailingRevenue', 'trailingProfit',
#     ]
#
# )



if __name__ == "__main__":
    print(FIELD)
    for k, m in FIELD.items():
        print(k, m.dtype)

