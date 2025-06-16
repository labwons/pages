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
        apps=[],
        # Adder
    ),
    marketCap=dDict(
        label='시가총액',
        unit='억원',
        dtype=int,
        digit=0,
        origin='시가총액',
        limit=False,
        apps=[],
        # Adder
    ),
    volume=dDict(
        label='거래량',
        unit='',
        dtype=int,
        digit=0,
        origin='거래량',
        limit=False,
        apps=[],
        # Adder
    ),
    amount=dDict(
        label='거래대금',
        unit='원',
        dtype=int,
        digit=0,
        origin='거래대금',
        limit=False,
        apps=[],
        # Adder
    ),
    shares=dDict(
        label='상장주식수',
        unit='',
        dtype=int,
        digit=0,
        origin='상장주식수',
        limit=False,
        apps=[],
        # Adder
    ),
    priceToBook=dDict(
        label='PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR',
        limit=False,
        apps=[],
        # Adder
    ),
    dividendYield=dDict(
        label='배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='DIV',
        limit=False,
        apps=[],
        # Adder
    ),
    foreignRate=dDict(
        label='외인보유율',
        unit='%',
        dtype=float,
        digit=2,
        origin='지분율',
        limit=False,
        apps=[],
        # Adder
    ),
    return1Day=dDict(
        label='1일 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    return1Week=dDict(
        label='1주 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    return1Month=dDict(
        label='1개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    return3Month=dDict(
        label='3개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    return6Month=dDict(
        label='6개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    return1Year=dDict(
        label='1년 수익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiftyTwoWeekHigh=dDict(
        label='52주최고가',
        unit='원',
        dtype=int,
        digit=0,
        origin='high52week',
        limit=False,
        apps=[],
        # Adder
    ),
    fiftyTwoWeekLow=dDict(
        label='52주최저가',
        unit='원',
        dtype=int,
        digit=0,
        origin='low52week',
        limit=False,
        apps=[],
        # Adder
    ),
    beta=dDict(
        label='베타',
        unit='',
        dtype=float,
        digit=4,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    floatShares=dDict(
        label='유동주식비율',
        unit='%',
        dtype=float,
        digit=2,
        origin='ff_sher_rt',
        limit=False,
        apps=[],
        # Adder
    ),
    stockSplitDate=dDict(
        label='최근 액면분할일자',
        unit='',
        dtype=datetime,
        digit=0,
        origin='face_value_chg_dt',
        limit=False,
        apps=[],
        # Adder
    ),
    targetPrice=dDict(
        label='목표가',
        unit='원',
        dtype=int,
        digit=0,
        origin='target_price',
        limit=False,
        apps=[],
        # Adder
    ),
    forwardEps=dDict(
        label='추정EPS',
        unit='원',
        dtype=int,
        digit=0,
        origin='eps',
        limit=False,
        apps=[],
        # Adder
    ),
    numberOfEstimation=dDict(
        label='추정기관수',
        unit='',
        dtype=int,
        digit=0,
        origin='presume_organ_count',
        limit=False,
        apps=[],
        # Adder
    ),
    statementType=dDict(
        label='재무제표 종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalDate=dDict(
        label='직전 회계연도',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalRevenue=dDict(
        label='매출액(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    fiscalProfit=dDict(
        label='영업이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='영업이익(억원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalNetProfit=dDict(
        label='당기순이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='당기순이익(억원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalProfitRatio=dDict(
        label='영업이익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='영업이익률(%)',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    fiscalAsset=dDict(
        label='총 자산(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자산총계(억원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalCapital=dDict(
        label='총 자본(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='자본총계(억원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalDebt=dDict(
        label='총 부채(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='부채총계(억원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalDebtRatio=dDict(
        label='부채비율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='부채비율(%)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalRetentionRatio=dDict(
        label='유보율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='유보율(%)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalRoA=dDict(
        label='RoA(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROA(%)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalRoE=dDict(
        label='RoE(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='ROE(%)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalEps=dDict(
        label='EPS(직전 회계연도 기준)',
        unit='원',
        dtype=int,
        digit=0,
        origin='EPS(원)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalDividendYield=dDict(
        label='배당수익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='배당수익률(%)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalPE = dDict(
        label='PER(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PER(배)',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    fiscalPriceToBook=dDict(
        label='PBR(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        origin='PBR(배)',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalRevenueGrowth=dDict(
        label='매출성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalProfitGrowth=dDict(
        label='영업이익성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalEpsGrowth=dDict(
        label='EPS성장율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),

    averageRevenueGrowth=dDict(
        label='연평균 매출성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    averageProfitGrowth=dDict(
        label='연평균 영업이익성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    averageEpsGrowth=dDict(
        label='연평균 EPS성장율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        apps=[],
        # Adder
    ),
    trailingRevenue=dDict(
        label='매출액',
        unit='억원',
        dtype=float,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    trailingEps=dDict(
        label='EPS',
        unit='원',
        dtype=float,
        digit=1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    trailingProfitRate=dDict(
        label='영업이익률',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedPE=dDict(
        label='Forward PE',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    trailingPS=dDict(
        label='PSR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=[0, 200],
        apps=[],
        # Adder
    ),
    trailingPE=dDict(
        label='PER',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        apps=[],
        # Adder
    ),
    turnoverRatio=dDict(
        label="거래회전율",
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    market=dDict(
        label='시장구분',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    name=dDict(
        label='종목명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    industryCode=dDict(
        label='산업코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    industryName=dDict(
        label='산업명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    sectorCode=dDict(
        label='섹터코드',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    sectorName=dDict(
        label='섹터명',
        unit='',
        dtype=str,
        digit=-1,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalProfitState=dDict(
        label='영업이익현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    fiscalEpsState=dDict(
        label='EPS현황',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedDate=dDict(
        label='추정 월',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedRevenue=dDict(
        label='매출(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedProfit=dDict(
        label='영업이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedNetProfit=dDict(
        label='당기순이익(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedAsset=dDict(
        label='총 자산(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedDebt=dDict(
        label='총 부채(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedCapital=dDict(
        label='총 자본(추정치)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedDebtRatio=dDict(
        label='부채율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedProfitRatio=dDict(
        label='영업이익율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedRoA=dDict(
        label='RoA(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedRoE=dDict(
        label='RoE(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedEps=dDict(
        label='EPS(추정치)',
        unit='원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedPriceToBook=dDict(
        label='추정PBR',
        unit='',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedRevenueGrowth=dDict(
        label='매출성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedProfitGrowth=dDict(
        label='영업이익성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    estimatedEpsGrowth=dDict(
        label='EPS성장율(추정치)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    revenueType=dDict(
        label='매출종류',
        unit='',
        dtype=str,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    recentAsset=dDict(
        label='총 자산',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    recentCapital=dDict(
        label='총 자본',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    recentDebt=dDict(
        label='총 부채',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    recentDebtRatio=dDict(
        label='부채율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    recentProfitRate=dDict(
        label='영업이익율',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    trailingProfit=dDict(
        label='영업이익(4분기 연속)',
        unit='억원',
        dtype=int,
        digit=0,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    pctFiftyTwoWeekHigh=dDict(
        label='52주최고가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    pctFiftyTwoWeekLow=dDict(
        label='52주최저가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    pctTargetPrice=dDict(
        label='목표가대비',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyRevenue=dDict(
        label='매출액(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    yoyProfit=dDict(
        label='영업이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyNetProfit=dDict(
        label='당기순이익(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:2',
        apps=[],
        # Adder
    ),
    yoyAsset=dDict(
        label='총 자산(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyDebt=dDict(
        label='총 부채(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyCapital=dDict(
        label='총 자본(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyDebtRatio=dDict(
        label='부채비율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyRetentionRatio=dDict(
        label='유보율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyProfitRatio=dDict(
        label='영업이익율(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyRoA=dDict(
        label='RoA(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyRoE=dDict(
        label='RoE(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyEps=dDict(
        label='EPS(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit='statistic:1',
        apps=[],
        # Adder
    ),
    yoyPriceToBook=dDict(
        label='PBR(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
    yoyDividendYield=dDict(
        label='배당수익률(YoY)',
        unit='%',
        dtype=float,
        digit=2,
        origin='',
        limit=False,
        apps=[],
        # Adder
    ),
)
METADATA.RENAME = dDict(**{item.origin: key for key, item in METADATA if item.origin})



MARKETMAP = dDict(
    COLORS=dDict(
        BLUE2RED = [
            '#1861A8', # R24 G97 B168
            '#228BE6', # R34 G139 B230
            '#74C0FC', # R116 G192 B252
            '#A6A6A6', # R168 G168 B168
            '#FF8787', # R255 G135 B135
            '#F03E3E', # R240 G62 B62
            '#C92A2A'  # R201 G42 B42
        ],
        RED2GREEN = [
            '#F63538', # R246 G53 B56
            '#BF4045', # R191 G64 B69
            '#8B444E', # R139 G68 B78
            '#414554', # R65 G69 B84
            '#35764E', # R53 G118 B78
            '#2F9E4F', # R47 G158 B79
            '#30CC5A'  # R48 G204 B90
        ]
    )
)


if __name__ == "__main__":
    print(METADATA)
    print(METADATA.close)
    print(METADATA.close.unit)
    print(METADATA.RENAME)
