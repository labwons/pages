try:
    from src.common.env import dDict
except ImportError:
    from src.common.env import dDict
from datetime import datetime


METADATA = dDict(
    close=dDict(
        label='종가',
        unit='원',
        dtype=int,
        digit=0,
        origin='종가',
        limit=False,
        # Adder
    ),
    marketCap=dDict(
        label='시가총액',
        unit='억원',
        dtype=int,
        digit=0,
        origin='시가총액',
        limit=False,
        # Adder
    ),
    volume=dDict(
        label='거래량',
        unit='',
        dtype=int,
        digit=0,
        origin='거래량',
        limit=False,
        # Adder
    ),
    amount=dDict(
        label='거래대금',
        unit='원',
        dtype=int,
        digit=0,
        origin='거래대금',
        limit=False,
        # Adder
    ),
    shares=dDict(
        label='상장주식수',
        unit='',
        dtype=int,
        digit=0,
        origin='상장주식수',
        limit=False,
        # Adder
    ),
    priceToBook=dDict(
        label='PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR',
        limit=False,
        # Adder
    ),
    dividendYield=dDict(
        label='배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='DIV',
        limit=False,
        # Adder
    ),
    foreignRate=dDict(
        label='외인보유율',
        unit='%',
        dtype=float,
        digit=2,
        origin='지분율',
        limit=False,
        # Adder
    ),
    return1Day=dDict(
        label='1일 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Week=dDict(
        label='1주 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Month=dDict(
        label='1개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return3Month=dDict(
        label='3개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return6Month=dDict(
        label='6개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    return1Year=dDict(
        label='1년 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    fiftyTwoWeekHigh=dDict(
        label='52주최고가',
        unit='원',
        dtype=int,
        digit=0,
        origin='high52week',
        limit=False,
        # Adder
    ),
    fiftyTwoWeekLow=dDict(
        label='52주최저가',
        unit='원',
        dtype=int,
        digit=0,
        origin='low52week',
        limit=False,
        # Adder
    ),
    beta=dDict(
        label='베타',
        unit='',
        dtype=float,
        digit=4,
        origin='',
        limit=False,
        # Adder
    ),
    floatShares=dDict(
        label='유동주식비율',
        unit='%',
        dtype=float,
        digit=2,
        origin='ff_sher_rt',
        limit=False,
        # Adder
    ),
    stockSplitDate=dDict(
        label='최근 액면분할일자',
        unit='',
        dtype=datetime,
        digit=0,
        origin='face_value_chg_dt',
        limit=False,
        # Adder
    ),
    targetPrice=dDict(
        label='목표가',
        unit='원',
        dtype=int,
        digit=0,
        origin='target_price',
        limit=False,
        # Adder
    ),
    forwardEps=dDict(
        label='추정EPS',
        unit='원',
        dtype=int,
        digit=0,
        origin='eps',
        limit=False,
        # Adder
    ),
    numberOfEstimation=dDict(
        label='추정기관수',
        unit='',
        dtype=int,
        digit=0,
        origin='presume_organ_count',
        limit=False,
        # Adder
    ),
    statementType=dDict(
        label='재무제표 종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalDate=dDict(
        label='직전 회계연도',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalRevenue=dDict(
        label='매출액(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    fiscalProfit=dDict(
        label='영업이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='영업이익(억원)',
        limit=False,
        # Adder
    ),
    fiscalNetProfit=dDict(
        label='당기순이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='당기순이익(억원)',
        limit=False,
        # Adder
    ),
    fiscalProfitRate=dDict(
        label='영업이익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='영업이익률(%)',
        limit='statistic:1',
        # Adder
    ),
    fiscalAsset=dDict(
        label='총 자산(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자산총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalCapital=dDict(
        label='총 자본(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자본총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalDebt=dDict(
        label='총 부채(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='부채총계(억원)',
        limit=False,
        # Adder
    ),
    fiscalDebtRatio=dDict(
        label='부채비율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='부채비율(%)',
        limit=False,
        # Adder
    ),
    fiscalRetentionRatio=dDict(
        label='유보율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='유보율(%)',
        limit=False,
        # Adder
    ),
    fiscalRoA=dDict(
        label='RoA(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROA(%)',
        limit=False,
        # Adder
    ),
    fiscalRoE=dDict(
        label='RoE(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROE(%)',
        limit=False,
        # Adder
    ),
    fiscalEps=dDict(
        label='EPS(직전 회계연도 기준)',
        unit='원',
        dtype=int,
        digit=0,
        origin='EPS(원)',
        limit=False,
        # Adder
    ),
    fiscalDividendYield=dDict(
        label='배당수익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='배당수익률(%)',
        limit=False,
        # Adder
    ),
    fiscalPE = dDict(
        label='PER(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PER(배)',
        limit='statistic:1',
        # Adder
    ),
    fiscalPriceToBook=dDict(
        label='PBR(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR(배)',
        limit=False,
        # Adder
    ),
    fiscalRevenueGrowth=dDict(
        label='매출성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalProfitGrowth=dDict(
        label='영업이익성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalEpsGrowth=dDict(
        label='EPS성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),

    averageRevenueGrowth=dDict(
        label='연평균 매출성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    averageProfitGrowth=dDict(
        label='연평균 영업이익성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    averageEpsGrowth=dDict(
        label='연평균 EPS성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    trailingRevenue=dDict(
        label='매출액',
        unit='억원',
        dtype=float,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    trailingEps=dDict(
        label='EPS',
        unit='원',
        dtype=float,
        digit=1,
        origin='',
        limit=False,
        # Adder
    ),
    trailingProfitRate=dDict(
        label='영업이익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedPE=dDict(
        label='Forward PE',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    trailingPS=dDict(
        label='PSR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=[0, 200],
        # Adder
    ),
    trailingPE=dDict(
        label='PER',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    turnoverRatio=dDict(
        label="거래회전율",
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    market=dDict(
        label='시장구분',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    name=dDict(
        label='종목명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    industryCode=dDict(
        label='산업코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    industryName=dDict(
        label='산업명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    sectorCode=dDict(
        label='섹터코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    sectorName=dDict(
        label='섹터명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalProfitState=dDict(
        label='영업이익현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    fiscalEpsState=dDict(
        label='EPS현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDate=dDict(
        label='추정 월',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRevenue=dDict(
        label='매출(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfit=dDict(
        label='영업이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedNetProfit=dDict(
        label='당기순이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedAsset=dDict(
        label='총 자산(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDebt=dDict(
        label='총 부채(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedCapital=dDict(
        label='총 자본(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedDebtRatio=dDict(
        label='부채율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitRate=dDict(
        label='영업이익율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRoA=dDict(
        label='RoA(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRoE=dDict(
        label='RoE(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEps=dDict(
        label='EPS(추정치)',
        unit='원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedPriceToBook=dDict(
        label='추정PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedRevenueGrowth=dDict(
        label='매출성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitGrowth=dDict(
        label='영업이익성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEpsGrowth=dDict(
        label='EPS성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedProfitGrowthState=dDict(
        label='영업이익성장율(추정치) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    estimatedEpsGrowthState=dDict(
        label='EPS성장율(추정치) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    revenueType=dDict(
        label='매출종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentAsset=dDict(
        label='총 자산',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentCapital=dDict(
        label='총 자본',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentDebt=dDict(
        label='총 부채',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    recentDebtRatio=dDict(
        label='부채율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    recentProfitRate=dDict(
        label='영업이익율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    trailingProfit=dDict(
        label='영업이익(4분기 연속)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    pctFiftyTwoWeekHigh=dDict(
        label='52주최고가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    pctFiftyTwoWeekLow=dDict(
        label='52주최저가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    pctTargetPrice=dDict(
        label='목표가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRevenue=dDict(
        label='매출액(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    yoyProfit=dDict(
        label='영업이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyNetProfit=dDict(
        label='당기순이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        # Adder
    ),
    yoyAsset=dDict(
        label='총 자산(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDebt=dDict(
        label='총 부채(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyCapital=dDict(
        label='총 자본(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDebtRatio=dDict(
        label='부채비율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRetentionRatio=dDict(
        label='유보율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyProfitRate=dDict(
        label='영업이익율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRoA=dDict(
        label='RoA(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyRoE=dDict(
        label='RoE(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyEps=dDict(
        label='EPS(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        # Adder
    ),
    yoyPriceToBook=dDict(
        label='PBR(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyDividendYield=dDict(
        label='배당수익률(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        # Adder
    ),
    yoyProfitState=dDict(
        label='영업이익율(YoY) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
    yoyEpsState=dDict(
        label='EPS(YoY) 상태',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        # Adder
    ),
)
METADATA.RENAME = dDict(**{item.origin: key for key, item in METADATA if item.origin})



MARKETMAP = dDict(
    COLORS=dDict(
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
    ),
    return1Day=dDict(
        scale=[-3, -2, -1, 0, 1, 2, 3],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    return1Week=dDict(
        scale=[-6, -4, -2, 0, 2, 4, 6],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    return1Month=dDict(
        scale=[-10, -6.7, -3.3, 0, 3.3, 6.7, 10],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    return3Month=dDict(
        scale=[-18, -12, -6, 0, 6, 12, 18],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    return6Month=dDict(
        scale=[-24, -16, -8, 0, 8, 16, 24],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    return1Year=dDict(
        scale=[-30, -20, -10, 0, 10, 20, 30],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    pctFiftyTwoWeekHigh=dDict(
        scale=[-30, -20, -10, 0, 0, 0, 0],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    pctFiftyTwoWeekLow=dDict(
        scale=[0, 0, 0, 0, 10, 20, 30],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    pctTargetPrice=dDict(
        scale=[-20, -10, -5, 0, 5, 10, 15],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    dividendYield=dDict(
        scale=[0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        color='BLUE2RED',
        index=3,
        iconMax='bi-hand-thumbs-up',
        iconMin='bi-hand-thumbs-down',
        # map-attribute
    ),
    foreignRate=dDict(
        scale=[0, 0, 0, 0, 20, 40, 60],
        color='BLUE2RED',
        index=3,
        iconMax='bi-person-up',
        iconMin='bi-person-down',
        # map-attribute
    ),
    beta=dDict(
        scale=[0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    yoyRevenue=dDict(
        scale=[-30, -20, -10, 0, 10, 20, 30],
        color='BLUE2RED',
        index=3,
        iconMax='bi-building-up',
        iconMin='bi-building-down',
        # map-attribute
    ),
    yoyProfit=dDict(
        scale=[-120, -80, -40, 0, 40, 80, 120],
        color='BLUE2RED',
        index=3,
        iconMax='bi-database-up',
        iconMin='bi-database-down',
        # map-attribute
    ),
    yoyEps=dDict(
        scale=[-90, -60, -30, 0, 30, 60, 90],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    trailingPS=dDict(
        scale=[0.5, 2, 3.5, 5, 6.5, 8, 9.5],
        color='BLUE2RED',
        index=3,
        iconMax='bi-arrow-up-square',
        iconMin='bi-arrow-down-square',
        # map-attribute
    ),
    trailingPE=dDict(
        scale=[5, 10, 20, 30, 40, 50, 60],
        color='BLUE2RED',
        index=3,
        iconMax='bi-arrow-up-square',
        iconMin='bi-arrow-down-square',
        # map-attribute
    ),
    trailingProfitRate=dDict(
        scale=[-15, -10, -5, 0, 5, 10, 15],
        color='BLUE2RED',
        index=3,
        iconMax='bi-building-up',
        iconMin='bi-building-down',
        # map-attribute
    ),
    estimatedRevenueGrowth=dDict(
        scale=[-10, -5, 0, 5, 10, 15, 20],
        color='BLUE2RED',
        index=3,
        iconMax='bi-building-up',
        iconMin='bi-building-down',
        # map-attribute
    ),
    estimatedProfitRate=dDict(
        scale=[-15, -10, -5, 0, 5, 10, 15],
        color='BLUE2RED',
        index=3,
        iconMax='bi-database-up',
        iconMin='bi-database-down',
        # map-attribute
    ),
    estimatedProfitGrowth=dDict(
        scale=[-50, -25, 0, 25, 50, 75, 100],
        color='BLUE2RED',
        index=3,
        iconMax='bi-database-up',
        iconMin='bi-database-down',
        # map-attribute
    ),
    estimatedEpsGrowth=dDict(
        scale=[-50, -25, 0, 25, 50, 75, 100],
        color='BLUE2RED',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
        # map-attribute
    ),
    estimatedPE=dDict(
        scale=[5, 10, 20, 30, 40, 50, 60],
        color='BLUE2RED',
        index=3,
        iconMax='bi-arrow-up-square',
        iconMin='bi-arrow-down-square',
        # map-attribute
    ),
    turnoverRatio=dDict(
        scale=[0.5, 1, 2, 3, 4, 5, 6],
        color='BLUE2RED',
        index=3,
        iconMax='bi-arrow-repeat',
        iconMin='bi-slash-circle',
        # map-attribute
    ),

)


if __name__ == "__main__":
    print(METADATA)
    print(METADATA.close)
    print(METADATA.close.unit)
    print(METADATA.RENAME)
