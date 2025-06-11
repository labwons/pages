try:
    from ...common.env import dDict
except ImportError:
    from src.common.env import dDict


METADATA = dDict(
    close=dDict(
        label='종가',
        unit='원',
        dtype=int,
        digit=0,
        calc='pykrx',
        # Adder
    ),
    marketCap=dDict(
        label='시가총액',
        unit='억원',
        dtype=int,
        digit=0,
        calc='pykrx',
        # Adder
    ),
    volume=dDict(
        label='거래량',
        unit='',
        dtype=int,
        digit=0,
        calc='pykrx',
        # Adder
    ),
    amount=dDict(
        label='거래대금',
        unit='원',
        dtype=int,
        digit=0,
        calc='pykrx',
        # Adder
    ),
    priceToBook=dDict(
        label='PBR',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    dividendYield=dDict(
        label='예상 배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    foreignRate=dDict(
        label='외인보유율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    return1Day=dDict(
        label='1일 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@d-1 / close - 1',
        # Adder
    ),
    return1Week=dDict(
        label='1주 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@w-1 / close - 1',
        # Adder
    ),
    return1Month=dDict(
        label='1개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-1 / close - 1',
        # Adder
    ),
    return3Month=dDict(
        label='3개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-3 / close - 1',
        # Adder
    ),
    return6Month=dDict(
        label='6개월 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@m-6 / close - 1',
        # Adder
    ),
    return1Year=dDict(
        label='1년 수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx:close@y-1 / close - 1',
        # Adder
    ),
    beta=dDict(
        label='베타',
        unit='',
        dtype=float,
        digit=4,
        calc='fnguide',
        # Adder
    ),
    shares=dDict(
        label='상장주식수',
        unit='',
        dtype=float,
        digit=0,
        calc='pykrx',
        # Adder
    ),
    floatShares=dDict(
        label='유동주식비율',
        unit='%',
        dtype=float,
        digit=2,
        calc='fnguide',
        # Adder
    ),
    trailingRevenue=dDict(
        label='매출액',
        unit='억원',
        dtype=float,
        digit=0,
        calc='fnguide:q[-4:].sum()',
        # Adder
    ),
    trailingEps=dDict(
        label='EPS',
        unit='원',
        dtype=float,
        digit=1,
        calc='fnguide',
        # Adder
    ),
    trailingProfitRate=dDict(
        label='영업이익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    averageRevenueGrowth_A=dDict(
        label='연평균 매출성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    averageProfitGrowth_A=dDict(
        label='연평균 영업이익성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    averageEpsGrowth_A=dDict(
        label='연평균 EPS성장율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    RevenueGrowth_A=dDict(
        label='매출성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    RevenueGrowth_Q=dDict(
        label='매출성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    ProfitGrowth_A=dDict(
        label='영업이익성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    ProfitGrowth_Q=dDict(
        label='영업이익성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    EpsGrowth_A=dDict(
        label='EPS성장율(연간)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    EpsGrowth_Q=dDict(
        label='EPS성장율(분기)',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    fiscalDividendYield=dDict(
        label='배당수익률',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    fiscalDebtRatio=dDict(
        label='부채율',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    pct52wHigh=dDict(
        label='52주 최고가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    pct52wLow=dDict(
        label='52주 최저가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    pctEstimated=dDict(
        label='목표가 대비',
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    estimatedPE=dDict(
        label='Forward PE',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    trailingPS=dDict(
        label='PSR',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    trailingPE=dDict(
        label='PER',
        unit='',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    turnoverRatio=dDict(
        label="거래회전율",
        unit='%',
        dtype=float,
        digit=2,
        calc='pykrx',
        # Adder
    ),
    market=dDict(
        label='시장구분',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    name=dDict(
        label='종목명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    industryCode=dDict(
        label='산업코드',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    industryName=dDict(
        label='산업명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    sectorCode=dDict(
        label='섹터코드',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    sectorName=dDict(
        label='섹터명',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    stockSize=dDict(
        label='대형주여부',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),
    date=dDict(
        label='날짜',
        unit='',
        dtype=str,
        digit=-1,
        calc='pykrx',
        # Adder
    ),


)

if __name__ == "__main__":
    print(METADATA)
    print(METADATA.close)
    print(METADATA.close.unit)