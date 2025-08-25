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
# FIELD.RENAME = DD(**{item.origin: key for key, item in FIELD.items() if item.origin})



MARKETMAP = DD(
    COLORS=DD(
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
    beta=DD(
        scale=[0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        color='RED2GREEN',
        index=3,
        iconMax='bi-graph-up-arrow',
        iconMin='bi-graph-down-arrow',
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
    turnoverRatio=DD(
        scale=[0.5, 1, 2, 3, 4, 5, 6],
        color='GREEN2RED',
        index=3,
        iconMax='bi-arrow-repeat',
        iconMin='bi-slash-circle',
        # map-attribute
    ),

)


BUBBLES = DD(
    COLORS=DD(
        G10=(92,168,155),
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
    ),
    SELECTOR=[
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
    ],
    KRW=[
        'fiscalRevenue', 'fiscalProfit', 'fiscalNetProfit',
        'estimatedRevenue', 'estimatedProfit', 'estimatedNetProfit',
        'trailingRevenue', 'trailingProfit',
    ]

)

ECOSMETA = DD(**{
	'한국은행 기준금리': DD(
		symbol='722Y001',
		code='0101000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'KORIBOR(3개월)': DD(
		symbol='817Y002',
		code='010150000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'KORIBOR(6개월)': DD(
		symbol='817Y002',
		code='010151000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'국고채1년': DD(
		symbol='817Y002',
		code='010190000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'국고채2년': DD(
		symbol='817Y002',
		code='010195000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'국고채5년': DD(
		symbol='817Y002',
		code='010200001',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'국고채10년': DD(
		symbol='817Y002',
		code='010210000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'회사채3년(AA-)': DD(
		symbol='817Y002',
		code='010300000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'회사채3년(BBB-)': DD(
		symbol='817Y002',
		code='010320000',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}%<extra></extra>',
    ),
	'은행수신금리(신규)': DD(
		symbol='121Y002',
		code='BEABAA2',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'은행수신금리(잔액)': DD(
		symbol='121Y013',
		code='BEABAB2',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'은행대출금리(신규)': DD(
		symbol='121Y006',
		code='BECBLA01',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),
	'은행대출금리(잔액)': DD(
		symbol='121Y015',
		code='BECBLB01',
		unit='%',
		category='금리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}%<extra></extra>',
    ),

	'원/달러환율': DD(
		symbol='731Y003',
		code='0000003',
		unit='원',
		category='통화/유동성지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=1,
		hover=': %{y:,.1f}원<extra></extra>',
    ),
	'M2(평잔, 원계열)': DD(
		symbol='101Y004',
		code='BBHA00',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'M2(평잔, 계절조정)': DD(
		symbol='101Y003',
		code='BBHS00',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'은행수신(말잔)': DD(
		symbol='104Y013',
		code='BCB8',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'은행수신(평잔)': DD(
		symbol='104Y014',
		code='BCA8',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'비은행수신(말잔)': DD(
		symbol='111Y007',
		code='1000000',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'비은행수신(평잔)': DD(
		symbol='111Y008',
		code='1000000',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'은행여신(말잔)': DD(
		symbol='104Y016',
		code='BDCA1',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'비은행여신(말잔)': DD(
		symbol='111Y009',
		code='1000000',
		unit='십억원',
		category='통화/유동성지표',
		YoY=True,
		MoM=True,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'증시예탁금': DD(
		symbol='901Y056',
		code='S23A',
		unit='백만원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'신용융자잔고': DD(
		symbol='901Y056',
		code='S23E',
		unit='백만원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),
	'신용대주잔고': DD(
		symbol='901Y056',
		code='S23F',
		unit='백만원',
		category='통화/유동성지표',
		YoY=True,
		MoM=False,
        dtype=int,
        digit=0,
		hover=': %{text}원<extra></extra>',
    ),

	'수출지수': DD(
		symbol='403Y001',
		code='*AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'반도체수출': DD(
		symbol='403Y001',
		code='3091AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'반도체/디스플레이장비수출': DD(
		symbol='403Y001',
		code='3091AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'스마트폰/무선전화기수출': DD(
		symbol='403Y001',
		code='309512AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'자동차수출': DD(
		symbol='403Y001',
		code='3121AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'자동차부품수출': DD(
		symbol='403Y001',
		code='31213AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'음식료품수출': DD(
		symbol='403Y001',
		code='301AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'석탄및석유제품수출': DD(
		symbol='403Y001',
		code='304AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'철강수출': DD(
		symbol='403Y001',
		code='3071AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'전지수출': DD(
		symbol='403Y001',
		code='31013AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'가전수출': DD(
		symbol='403Y001',
		code='31015AA',
		unit='',
		category='수출지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),

	'소비자물가지수': DD(
		symbol='901Y009',
		code='0',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'소비자물가지수(식료품 및 에너지 제외)': DD(
		symbol='901Y010',
		code='DB',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'소비자물가지수(서비스)': DD(
		symbol='901Y010',
		code='22',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'생산자물가지수': DD(
		symbol='404Y014',
		code='*AA',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'생산자물가지수(식료품 및 에너지 제외)': DD(
		symbol='404Y015',
		code='S620AA',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'생산자물가지수(서비스)': DD(
		symbol='404Y014',
		code='5AA',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),

	'KB부동산매매지수(아파트, 전국)': DD(
		symbol='901Y062',
		code='P63AC',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}<extra></extra>',
    ),
	'KB부동산매매지수(아파트, 서울)': DD(
		symbol='901Y062',
		code='P63ACA',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}<extra></extra>',
    ),
	'KB부동산전세지수(아파트, 전국)': DD(
		symbol='901Y063',
		code='P64AC',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}<extra></extra>',
    ),
	'KB부동산전세지수(아파트, 서울)': DD(
		symbol='901Y063',
		code='P64ACA',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=3,
		hover=': %{y:.3f}<extra></extra>',
    ),
	'아파트실거래지수(전국)': DD(
		symbol='901Y089',
		code='100',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'아파트실거래지수(서울)': DD(
		symbol='901Y089',
		code='200',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}%<extra></extra>',
    ),
	'아파트실거래지수(수도권)': DD(
		symbol='901Y089',
		code='300',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'아파트실거래지수(경기)': DD(
		symbol='901Y089',
		code='C00',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'아파트실거래지수(지방광역시)': DD(
		symbol='901Y089',
		code='M00',
		unit='',
		category='물가/부동산지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),

	'경기선행지수순환변동': DD(
		symbol='901Y067',
		code='I16E',
		unit='',
		category='경제/심리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'경기동행지수순환변동': DD(
		symbol='901Y067',
		code='I16D',
		unit='',
		category='경제/심리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'제조업업황전망': DD(
		symbol='512Y014',
		code='C0000/BA',
		unit='',
		category='경제/심리지표',
		YoY=True,
		MoM=True,
        dtype=int,
        digit=0,
		hover=': %{y:,d}<extra></extra>',
    ),
	'제조업신규수주전망': DD(
		symbol='512Y014',
		code='C0000/BD',
		unit='',
		category='경제/심리지표',
		YoY=True,
		MoM=True,
        dtype=int,
        digit=0,
		hover=': %{y:,d}<extra></extra>',
    ),
	'제조업수출전망': DD(
		symbol='512Y014',
		code='C0000/BM',
		unit='',
		category='경제/심리지표',
		YoY=True,
		MoM=True,
        dtype=int,
        digit=0,
		hover=': %{y:,d}<extra></extra>',
    ),
	'제조업심리지수': DD(
		symbol='512Y014',
		code='C0000/BY',
		unit='',
		category='경제/심리지표',
		YoY=True,
		MoM=True,
        dtype=int,
        digit=0,
		hover=': %{y:,d}<extra></extra>',
    ),
	'소비자심리지수': DD(
		symbol='511Y002',
		code='FME/99988',
		unit='',
		category='경제/심리지표',
		YoY=True,
		MoM=True,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}<extra></extra>',
    ),
	'뉴스심리지수(실험통계)': DD(
		symbol='521Y001',
		code='A001',
		unit='',
		category='경제/심리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=2,
		hover=': %{y:.2f}<extra></extra>',
    ),
	'실업률(원계열)': DD(
		symbol='901Y027',
		code='I61BC/I28A',
		unit='%',
		category='경제/심리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}%<extra></extra>',
    ),
	'실업률(계절조정)': DD(
		symbol='901Y027',
		code='I61BC/I28B',
		unit='%',
		category='경제/심리지표',
		YoY=False,
		MoM=False,
        dtype=float,
        digit=1,
		hover=': %{y:.1f}%<extra></extra>',
    ),
})

FREDMETA = DD(**{
    # Bond and Interest Rate
    '연준 기준금리':DD(
        symbol='FEDFUNDS',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='Federal Funds Effective Rate (Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채10년':DD(
        symbol='DGS10',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채5년':DD(
        symbol='DGS5',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채2년':DD(
        symbol='DGS2',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채1년':DD(
        symbol='DGS1',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채장단기금리차(10Y-2Y)':DD(
        symbol='T10Y2Y',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국채장단기금리차(10Y-3M)':DD(
        symbol='T10Y3M',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 하이일드 스프레드':DD(
        symbol='BAMLH0A0HYM2',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='ICE BofA US High Yield Index Option-Adjusted Spread (Daily)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 30년고정주택담보대출':DD(
        symbol='MORTGAGE30US',
        quoteType='INDICATOR',
        category='금리지표',
        unit='%',
        comment='30-Year Fixed Rate Mortgage Average in the United States (Weekly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),

    # Monetary
    '미국 M2':DD(
        symbol='M2SL',
        quoteType='INDICATOR',
        category='통화/유동성지표',
        unit='USD(xB)',
        comment='M2: Billions of Dollars (Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}$(xB)<extra></extra>',
    ),
    '미국 M2통화유동속도':DD(
        symbol='M2V',
        quoteType='INDICATOR',
        category='통화/유동성지표',
        unit='%',
        comment='Velocity of M2 Money Stock (Seasonally Adjusted, Quarterly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),

    # Inflation
    '미국 CPI(계절조정)':DD(
        symbol='CPIAUCSL',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='',
        comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Seasonally Adjusted, Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}<extra></extra>',
    ),
    '미국 CPI(계절조정 미반영)':DD(
        symbol='CPIAUCNS',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='',
        comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Not Seasonally Adjusted, Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}<extra></extra>',
    ),
    '미국 CPI(경직물가, YoY)':DD(
        symbol='CORESTICKM159SFRBATL',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='%',
        comment='Sticky Price Consumer Price Index less Food and Energy (Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 CPI(식음료 에너지 제외)':DD(
        symbol='CPILFESL',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='',
        comment='Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average (Seasonally Adjusted, Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}<extra></extra>',
    ),
    '미국 10년 기대인플레이션율':DD(
        symbol='T10YIE',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='%',
        comment='10-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 5년 기대인플레이션율':DD(
        symbol='T5YIE',
        quoteType='INDICATOR',
        category='물가 / 부동산지표',
        unit='%',
        comment='5-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),

    # Labor, GDP, Saving and Others
    '미국 실업률':DD(
        symbol='UNRATE',
        quoteType='INDICATOR',
        category='경제 / 심리지표',
        unit='%',
        comment='Unemployment Rate(Seasonally Adjusted, Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 명목GDP':DD(
        symbol='GDP',
        quoteType='INDICATOR',
        category='경제 / 심리지표',
        unit='USD(xB)',
        comment='Gross Domestic Product (Seasonally Adjusted, Quarterly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}$(xB)<extra></extra>',
    ),
    '미국 실질GDP':DD(
        symbol='GDPC1',
        quoteType='INDICATOR',
        category='경제 / 심리지표',
        unit='USD(xB)',
        comment='Real Gross Domestic Product (Seasonally Adjusted, Quarterly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}$(xB)<extra></extra>',
    ),
    '미국 가계저축율':DD(
        symbol='PSAVERT',
        quoteType='INDICATOR',
        category='경제 / 심리지표',
        unit='%',
        comment='Personal Saving Rate (Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}%<extra></extra>',
    ),
    '미국 소비자 심리지수(미시간 대학교)':DD(
        symbol='UMCSENT',
        quoteType='INDICATOR',
        category='경제 / 심리지표',
        unit='',
        comment='University of Michigan: Consumer Sentiment (Monthly)',
        digit=2,
        dtype=float,
        hover=': %{y:.2f}<extra></extra>',
    ),
})

KRXMETA = DD(
    KOSPI=DD(
        symbol='1001',
        unit= '',
        digit=2,
        dtype=float,
        category='지수',
        hover= ': %{y:.2f}<extra></extra>',
    ),
    KOSDAQ=DD(
        symbol='2001',
        unit= '',
        digit=2,
        dtype=float,
        category='지수',
        hover= ': %{y:.2f}<extra></extra>',
    ),
)

MACRO = DD(
    STATUS=DD(**{
        '1001':DD(
            icon='bi-graph-up',
            digit=2,
        ),
        '2001':DD(
            icon='bi-graph-up',
            digit=2,
        ),
        '731Y0030000003':DD(
            icon='bi-currency-exchange',  # 원/달러 환율
            digit=1,
        ),
        '817Y002010195000':DD(
            icon='bi-percent',  # 국고채2년
            digit=3,
        ),
        '817Y002010210000':DD(
            icon='bi-percent',  # 국고채10년
            digit=3,
        ),
        '901Y056S23A':DD(
            icon='bi-piggy-bank-fill',  # 증시예탁금
            digit=0,
        ),
        '901Y056S23E':DD(
            icon='bi-cash-stack',  # 신용융자잔고
            digit=0,
        ),
        '901Y056S23F':DD(
            icon='bi-credit-card',  # 신용대주잔고
            digit=0,
        ),
        '403Y001*AA':DD(
            icon='bi-truck',  # 수출지수
            digit=2,
        ),
        '901Y062P63AC':DD(
            icon='bi-house-up-fill',  # KB부동산매매지수(아파트, 전국)
            digit=2,
        ),
        '901Y063P64AC':DD(
            icon='bi-house-up-fill',  # KB부동산전세지수(아파트, 전국)
            digit=2,
        ),
        '901Y067I16E':DD(
            icon='bi-graph-up-arrow',  # 경기선행지수순환변동
            digit=1,
        ),

    })
)

if __name__ == "__main__":
    # print(FIELD)
    # print(FIELD.close)
    # print(FIELD.close.unit)
    # print(FIELD.RENAME)

    print(ECOSMETA)
    print(FREDMETA)