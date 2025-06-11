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
        calc='pykrx',
        origin='종가',
        # Adder
    ),
    marketCap=dDict(
        label='시가총액',
        unit='억원',
        dtype=int,
        digit=0,
        calc='pykrx',
        origin='시가총액',
        # Adder
    ),
    volume=dDict(
        label='거래량',
        unit='',
        dtype=int,
        digit=0,
        calc='pykrx',
        origin='거래량',
        # Adder
    ),
    amount=dDict(
        label='거래대금',
        unit='원',
        dtype=int,
        digit=0,
        calc='pykrx',
        origin='거래대금',
        # Adder
    ),
    shares=dDict(
        label='상장주식수',
        unit='',
        dtype=int,
        digit=0,
        calc='pykrx',
        origin='상장주식수',
        # Adder
    ),
    priceToBook=dDict(
        label='PBR',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='PBR',
        # Adder
    ),
    dividendYield=dDict(
        label='배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='DIV',
        # Adder
    ),
    foreignRate=dDict(
        label='외인보유율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='지분율',
        # Adder
    ),
    return1Day=dDict(
        label='1일 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@d-1 / close - 1',
        origin='',
        # Adder
    ),
    return1Week=dDict(
        label='1주 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@w-1 / close - 1',
        origin='',
        # Adder
    ),
    return1Month=dDict(
        label='1개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-1 / close - 1',
        origin='',
        # Adder
    ),
    return3Month=dDict(
        label='3개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-3 / close - 1',
        origin='',
        # Adder
    ),
    return6Month=dDict(
        label='6개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-6 / close - 1',
        origin='',
        # Adder
    ),
    return1Year=dDict(
        label='1년 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@y-1 / close - 1',
        origin='',
        # Adder
    ),
    fiftyTwoWeekHigh=dDict(
        label='52주최고가',
        unit='원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='high52week',
        # Adder
    ),
    fiftyTwoWeekLow=dDict(
        label='52주최저가',
        unit='원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='low52week',
        # Adder
    ),
    beta=dDict(
        label='베타',
        unit='',
        dtype=float,
        digit=4,
        calc='fnguide',
        origin='',
        # Adder
    ),
    floatShares=dDict(
        label='유동주식비율',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='ff_sher_rt',
        # Adder
    ),
    stockSplitDate=dDict(
        label='최근 액면분할일자',
        unit='',
        dtype=datetime,
        digit=0,
        calc='fnguide',
        origin='face_value_chg_dt',
        # Adder
    ),
    targetPrice=dDict(
        label='목표가',
        unit='원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='target_price',
        # Adder
    ),
    forwardEps=dDict(
        label='추정EPS',
        unit='원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='eps',
        # Adder
    ),
    numberOfEstimation=dDict(
        label='추정기관수',
        unit='',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='presume_organ_count',
        # Adder
    ),
    statementType=dDict(
        label='재무제표 종류',
        unit='',
        dtype=str,
        digit=0,
        calc='fnguide',
        origin='',
        # Adder
    ),
    fiscalDate=dDict(
        label='직전 회계연도',
        unit='',
        dtype=str,
        digit=0,
        calc='fnguide',
        origin='',
        # Adder
    ),
    fiscalRevenue=dDict(
        label='매출액(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='',
        # Adder
    ),
    fiscalProfit=dDict(
        label='영업이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='영업이익(억원)',
        # Adder
    ),
    fiscalNetProfit=dDict(
        label='당기순이익(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='당기순이익(억원)',
        # Adder
    ),
    fiscalProfitRatio=dDict(
        label='영업이익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='영업이익률(%)',
        # Adder
    ),
    fiscalAsset=dDict(
        label='총 자산(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='자산총계(억원)',
        # Adder
    ),
    fiscalCapital=dDict(
        label='총 자본(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='자본총계(억원)',
        # Adder
    ),
    fiscalDebt=dDict(
        label='총 부채(직전 회계연도 기준)',
        unit='억원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='부채총계(억원)',
        # Adder
    ),
    fiscalDebtRatio=dDict(
        label='부채비율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='부채비율(%)',
        # Adder
    ),
    fiscalRetentionRatio=dDict(
        label='유보율(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='유보율(%)',
        # Adder
    ),
    fiscalRoA=dDict(
        label='RoA(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='ROA(%)',
        # Adder
    ),
    fiscalRoE=dDict(
        label='RoE(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='ROE(%)',
        # Adder
    ),
    fiscalEps=dDict(
        label='EPS(직전 회계연도 기준)',
        unit='원',
        dtype=int,
        digit=0,
        calc='fnguide',
        origin='EPS(원)',
        # Adder
    ),
    fiscalDividendYield=dDict(
        label='배당수익률(직전 회계연도 기준)',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='배당수익률(%)',
        # Adder
    ),
    fiscalPE = dDict(
        label='PER(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='PER(배)',
        # Adder
    ),
    fiscalPriceToBook=dDict(
        label='PBR(직전 회계연도 기준)',
        unit='',
        dtype=float,
        digit=2,
        calc='fnguide',
        origin='PBR(배)',
        # Adder
    ),
    trailingRevenue=dDict(
        label='매출액',
        unit='억원',
        dtype=float,
        digit=0,
        calc='fnguide:q[-4:].sum()',
        origin='',
        # Adder
    ),
    trailingEps=dDict(
        label='EPS',
        unit='원',
        dtype=float,
        digit=1,
        calc='fnguide',
        origin='',
        # Adder
    ),
    trailingProfitRate=dDict(
        label='영업이익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    averageRevenueGrowth_A=dDict(
        label='연평균 매출성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    averageProfitGrowth_A=dDict(
        label='연평균 영업이익성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    averageEpsGrowth_A=dDict(
        label='연평균 EPS성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    RevenueGrowth_A=dDict(
        label='매출성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    RevenueGrowth_Q=dDict(
        label='매출성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    ProfitGrowth_A=dDict(
        label='영업이익성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    ProfitGrowth_Q=dDict(
        label='영업이익성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    EpsGrowth_A=dDict(
        label='EPS성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    EpsGrowth_Q=dDict(
        label='EPS성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    pct52wHigh=dDict(
        label='52주 최고가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    pct52wLow=dDict(
        label='52주 최저가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    pctEstimated=dDict(
        label='목표가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    estimatedPE=dDict(
        label='Forward PE',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    trailingPS=dDict(
        label='PSR',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    trailingPE=dDict(
        label='PER',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    turnoverRatio=dDict(
        label="거래회전율",
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        origin='',
        # Adder
    ),
    market=dDict(
        label='시장구분',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    name=dDict(
        label='종목명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    industryCode=dDict(
        label='산업코드',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    industryName=dDict(
        label='산업명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    sectorCode=dDict(
        label='섹터코드',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    sectorName=dDict(
        label='섹터명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    stockSize=dDict(
        label='대형주여부',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
    date=dDict(
        label='날짜',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        origin='',
        # Adder
    ),
)
METADATA.RENAME = dDict(**{item.origin: key for key, item in METADATA if item.origin})


if __name__ == "__main__":
    print(METADATA)
    print(METADATA.close)
    print(METADATA.close.unit)
    print(METADATA.RENAME)