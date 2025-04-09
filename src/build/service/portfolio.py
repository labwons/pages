try:
    from ...common.path import PATH
except ImportError:
    from src.common.path import PATH
from pandas import concat, read_json, isna, to_datetime, DataFrame, MultiIndex
from typing import List

# REFERENCED BY {config.py}
# HOW TO USE
# 1) 정규장 마감 이후 종목 선택
# 2) 다음 거래일 매수 체결 후, BUILD 실행 전
#    - 종목 정보 추가
# 3) 이력 삭제 시
#    - {MY_PORTFOLIO}에서 해당 종목 정보 삭제
MY_PORTFOLIO = [
    {"ticker": "251970", "start": "2025-03-28", "buy": 49200, "end": "2025-04-09", "sell": 49400}, # 펌텍코리아
    {"ticker": "053580", "start": "2025-04-02", "buy": 11000, "end": "2025-04-04", "sell": 15000}, # 웹케시
    {"ticker": "102710", "start": "2025-04-02", "buy": 26000}, # 이엔에프테크놀로지
    {"ticker": "005180", "start": "2025-04-03", "buy": 97000, "end": "2025-04-09", "sell": 90000}, # 빙그레
    {"ticker": "097520", "start": "2025-04-04", "buy": 24000, "end": "2025-04-09", "sell": 21500}, # 엠씨넥스
    {"ticker": "017960", "start": "2025-04-09", "buy": 17400}, # 한국카본
    {"ticker": "016590", "start": "2025-04-09", "buy": 7170}, # 신대양제지
]


class StockPortfolio(DataFrame):

    _log: List[str] = []
    def __init__(self, baseline:DataFrame):
        self.log = f'RUN [Build Portfolio]'

        baseline = baseline.copy()
        if str(baseline["date"].dtype).startswith("datetime64"):
            baseline["date"] = baseline["date"].dt.strftime("%Y-%m-%d")
        baseline_date = baseline['date'].values[0]

        portfolio = read_json(PATH.PORTFOLIO, orient='index')
        portfolio.columns = MultiIndex.from_tuples([eval(col) for col in portfolio.columns])
        portfolio.index = portfolio.index.astype(str).str.zfill(6)
        portfolio = portfolio[
            portfolio.index.isin([o["ticker"] for o in MY_PORTFOLIO]) & \
            portfolio[("date", "Start")].isin([o["start"] for o in MY_PORTFOLIO])
        ]
        portfolio_date = portfolio["date"]["Tracking"].values[0]

        # if baseline_date == portfolio_date:
        #     super().__init__(portfolio)
        #     self.log = f'END [Build Portfolio] {len(self[self["date"]["End"].isna()])} / {len(self)} Stocks'
        #     return

        _new, _tracking, _complete = [], [], []
        for obj in MY_PORTFOLIO:
            ticker = obj["ticker"]
            if ticker in portfolio.index:

                # IF PORTFOLIO CONFIGURATION TICKER IS IN PORTFOLIO DATA, TWO CASES
                # ARE POSSIBLE. IF THE START DATE OF PORTFOLIO DATA AND CONFIGURATION
                # START DATE IS THE SAME, IT IS ON GOING(TRACKING) TICKER. ON THE OTHER
                # HAND, IF THE START DATES ARE NOT MATCHED, NEW INVESTMENT IS BEGINNING.
                if portfolio.loc[ticker]["date"]["Start"] == obj["start"]:
                    _tracking.append(ticker)
                if portfolio.loc[ticker]["date"]["Start"] != obj["start"]:
                    _new.append(ticker)
                    _tracking.append(ticker)

                # IF CONFIGURATION TICKER IS IN PORTFOLIO DATA, AND INVESTMENT {end} IS
                # CONFIGURED, CHECK PORTFOLIO DATA IS ENDED. IF NOT, TODAY'S BASELINE
                # DATA WILL BE RECORDED AS HISTORY.
                if "end" in obj:
                    if isna(portfolio.loc[ticker]["date"]["End"]):
                        _complete.append(ticker)
            else:
                _new.append(ticker)
                _tracking.append(ticker)

        new:DataFrame = baseline.loc[_new]
        new.columns = MultiIndex.from_tuples(zip(new.columns, ["Start"] * len(new.columns)))
        if not new.empty:
            portfolio = concat([portfolio, new], axis=0)

        tracking:DataFrame = baseline.loc[_tracking]
        tracking.columns = MultiIndex.from_tuples(zip(tracking.columns, ["Tracking"] * len(tracking.columns)))
        if not tracking.empty:
            portfolio.update(tracking)
        portfolio.loc[:, ("buy", "Start")] = [obj["buy"] for obj in MY_PORTFOLIO]

        complete:DataFrame = baseline.loc[_complete]
        complete.columns = MultiIndex.from_tuples(zip(complete.columns, ["End"] * len(complete.columns)))
        if not complete.empty:
            portfolio.update(complete)
            portfolio.loc[_complete, ("sell", "End")] = [obj["sell"] for obj in MY_PORTFOLIO if obj["ticker"] in _complete]

        # order = portfolio.columns.get_level_values(0).unique()
        # portfolio = portfolio.reindex(columns=
        #                               sorted(portfolio.columns, key=lambda x: (order.get_loc(x[0]), x[1])))
        super().__init__(portfolio)
        self.to_json(PATH.PORTFOLIO, orient='index')
        self.log = f'END [Build Portfolio] {len(self[self["date"]["End"].isna()])} / {len(self)} Stocks'
        return

    @property
    def log(self) -> str:
        return "\n".join(self._log)

    @log.setter
    def log(self, log: str):
        self._log.append(log)

    @classmethod
    def _format_cap(cls, market_cap: int) -> str:
        zo, euk = int(market_cap // 10000), int(market_cap % 10000)
        return f'{zo}조 {euk}억' if zo else f'{euk}억'

    def report(self) -> DataFrame:
        on = self[self["sell"]["End"].isna()].copy()
        return on[[
            ('date', 'Start'),
            ('date', 'Tracking'),
            ('buy', 'Start'),
            ('close', 'Tracking'),
            ('D-1', 'Tracking'),
            ('M-1', 'Tracking'),
            ('M-3', 'Tracking'),
            ('M-6', 'Tracking'),
            ('Y-1', 'Tracking'),
        ]]

    def status(self):
        BLUE2RED = [
            '#1861A8',  # R24 G97 B168
            '#228BE6',  # R34 G139 B230
            '#74C0FC',  # R116 G192 B252
            '#A6A6A6',  # R168 G168 B168
            '#FF8787',  # R255 G135 B135
            '#F03E3E',  # R240 G62 B62
            '#C92A2A'  # R201 G42 B42
        ]

        RED2GREEN = [
            '#F63538',  # R246 G53 B56
            '#BF4045',  # R191 G64 B69
            '#8B444E',  # R139 G68 B78
            '#414554',  # R65 G69 B84
            '#35764E',  # R53 G118 B78
            '#2F9E4F',  # R47 G158 B79
            '#30CC5A'  # R48 G204 B90
        ]
        HEX2RGB = lambda x: (int(x[1:3], 16), int(x[3:5], 16), int(x[5:], 16))
        CONNECT = lambda x, x1, y1, x2, y2: ((y2 - y1) / (x2 - x1)) * (x - x1) + y1

        def _paint(value, valueScale, colorScale) -> str:
            rgb = [HEX2RGB(s) for s in colorScale]
            if isna(value):
                return colorScale[3]
            if value <= valueScale[0]:
                return colorScale[0]
            if value > valueScale[-1]:
                return colorScale[-1]
            n = 0
            while n < len(colorScale) - 1:
                if valueScale[n] < value <= valueScale[n + 1]:
                    break
                n += 1
            r1, g1, b1 = rgb[n]
            r2, g2, b2 = rgb[n + 1]
            r = CONNECT(value, valueScale[n], r1, valueScale[n + 1], r2)
            g = CONNECT(value, valueScale[n], g1, valueScale[n + 1], g2)
            b = CONNECT(value, valueScale[n], b1, valueScale[n + 1], b2)
            return f'#{hex(int(r))[2:]}{hex(int(g))[2:]}{hex(int(b))[2:]}'.upper()


        on = self[self["sell"]["End"].isna()].copy()
        on = on[[('date', 'Start'), ('buy', 'Start')] + [c for c in on.columns if c[1] == "Tracking"]]
        on.columns = [f'{c[1].lower()}{c[0].capitalize()}' if c[1] == "Start" else c[0] for c in on]
        on["timeDiff"] = (to_datetime(on["date"]) - to_datetime(on["startDate"])).astype(str)
        on["yield"] = round(100 * (on["close"] / on["startBuy"] - 1), 2)
        on["marketCap"] = (on["marketCap"] / 1e+8).apply(self._format_cap)
        on["yieldColor"] = on["yield"].apply(_paint, valueScale=[-21, -14, -7, 0, 7, 14, 21], colorScale=BLUE2RED)
        on["profitColor"] = on["trailingProfitRate"].apply(_paint, valueScale=[-15, -10, -5, 0, 5, 10, 15], colorScale=RED2GREEN)
        on["peColor"] = on["trailingPE"].apply(_paint, valueScale=[6, 12, 18, 24, 30, 36, 42], colorScale=RED2GREEN[::-1])
        on["epeColor"] = on["estimatedPE"].apply(_paint, valueScale=[6, 12, 18, 24, 30, 36, 42], colorScale=RED2GREEN[::-1])
        on["meta1"] = "투자 시작일: " + on["startDate"].str.replace("-", "/") + \
                      "(" + on["timeDiff"].str.replace(" days", "일차") + ")<br>" + \
                      "투자 수익률: " + on["yield"].astype(str) + "%<br>"
        on["meta2"] = "영업이익률: " + on["trailingProfitRate"].astype(str) + "%<br>" + \
                      "섹터: " + on["sectorName"] + "<br>" + \
                      "업종: " + on["industryName"] + "<br>" + \
                      "시가총액: " + on["marketCap"] + "원<br>"

        return on

    def history(self) -> str:
        return ""


if __name__ == "__main__":
    from src.build.service.baseline import MarketBaseline
    from pandas import set_option
    from numpy import datetime_as_string
    set_option('display.expand_frame_repr', False)


    baseline = MarketBaseline(update=False)
    # print(baseline)
    # print(baseline.loc[['021240']])

    portfolio = StockPortfolio(baseline)
    print(portfolio.log)
    print("*" * 100)
    print(portfolio)
    # print(portfolio.report())
    # print(portfolio.status())

