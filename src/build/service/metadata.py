try:
    from ...common.env import dDict
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
    fiscalProfitRatio=dDict(
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
    estimatedProfitRatio=dDict(
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
)
METADATA.RENAME = dDict(**{item.origin: key for key, item in METADATA if item.origin})


if __name__ == "__main__":
    print(METADATA)
    print(METADATA.close)
    print(METADATA.close.unit)
    print(METADATA.RENAME)
