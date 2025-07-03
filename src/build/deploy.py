"""
TITLE   : BUILD LABWONS
AUTHOR  : SNOB
CONTACT : snob.labwons@gmail.com
ROUTINE : 15:30+09:00UTC on weekday
"""
if __name__ == "__main__":
    try:
        from ..common.env import *
        from ..fetch.market.aftermarket import AfterMarket
        from ..fetch.market.finances import FinancialStatement
        from ..fetch.market.sector import SectorComposition
        from ..fetch.macro.ecos import Ecos
        from ..fetch.macro.fred import Fred
        from ..fetch.stock.krx import PyKrx
        from .baseline.metadata import ECOSMETA, FREDMETA
        from .baseline.market import MarketBaseline
        from .baseline.macro import MacroBaseline
        from .apps.marketmap import MarketMap
        from .apps.bubble import MarketBubble
        from .apps.macro import Macro
        from .apps.stocks import Stocks
        from .apps.sitemap import rss, sitemap
        from .util import navigate, minify, eMail, clearPath
    except ImportError:
        from src.common.env import *
        from src.fetch.market.aftermarket import AfterMarket
        from src.fetch.market.finances import FinancialStatement
        from src.fetch.market.sector import SectorComposition
        from src.fetch.macro.ecos import Ecos
        from src.fetch.macro.fred import Fred
        from src.fetch.stock.krx import PyKrx
        from src.build.baseline.metadata import ECOSMETA, FREDMETA
        from src.build.baseline.market import MarketBaseline
        from src.build.baseline.macro import MacroBaseline
        from src.build.apps.marketmap import MarketMap
        from src.build.apps.bubble import MarketBubble
        from src.build.apps.macro import Macro
        from src.build.apps.stocks import Stocks
        from src.build.apps.sitemap import rss, sitemap
        from src.build.util import navigate, minify, eMail, clearPath
    from jinja2 import Environment, FileSystemLoader
    from json import dumps
    import os

    # ---------------------------------------------------------------------------------------
    # ENVIRONMENT SETTINGS
    # ---------------------------------------------------------------------------------------
    SYSTEM_NAV = navigate(DOCS)
    if ENV == "local":
        # FOR LOCAL HOST TESTING, EXTERNAL DIRECTORY IS RECOMMENDED AND USED. USING THE SAME
        # LOCAL HOSTING DIRECTORY WITH DEPLOYMENT DIRECTORY, DEPLOYMENT MIGHT BE CORRUPTED.
        # IF YOU WANT TO USE DIFFERENT PATH FOR LOCAL HOST TESTING, BELOW {ROOT} VARIABLE ARE
        # TO BE CHANGED.
        from shutil import copytree
        if os.path.isdir(PATH.STUB):
            clearPath(PATH.STUB)
        copytree(DOCS, PATH.STUB, dirs_exist_ok=True)
        PATH.DOCS = PATH.STUB
        GITHUB.CONFIG.RESET()

    if GITHUB.EVENT == "schedule":
        # ON GITHUB ACTIONS, SYSTEM EXITS WHEN THE LATEST TRADING DATE AND CURRENT DATETIME
        # IS NOT MATCHED. THIS CODE IS IMPLEMENTED IN ORDER TO AVOID RUNNING ON WEEKDAY WHILE
        # HOLIDAYS OF THE MARKET.
        from pykrx.stock import get_nearest_business_day_in_a_week
        if get_nearest_business_day_in_a_week() != CLOCK().strftime("%Y%m%d"):
            raise SystemExit

        # ON GITHUB ACTIONS, IF SCHEDULED TIME IS ACTIVATED BEFORE THE MARKET IS CLOSED,
        # WHICH HARDLY HAPPENS, BUILD AND DEPLOY WILL HOLD UNTIL THE MARKET IS CLOSED.
        now = CLOCK()
        from time import sleep
        while (now.hour == 15) and (15 <= now.minute < 31):
            sleep(30)
            now = CLOCK()

        GITHUB.CONFIG.RESET()
        if now.hour >= 20:
            GITHUB.CONFIG.ECOS = GITHUB.CONFIG.FRED = GITHUB.CONFIG.STATEMENT = True
        else:
            GITHUB.CONFIG.AFTERMARKET = GITHUB.CONFIG.STOCKPRICE = True

    if GITHUB.EVENT == "workflow_dispatch":
        # CLEAN-UP DEPLOYMENT
        GITHUB.CONFIG.RESET()

    if GITHUB.EVENT == "push":
        # EXTERNAL CONFIGURATION FOR BUILD CACHING. CONFIGURATION SCRIPT AT //src/common/env.py
        # IF CONFIGURED AND PUSHED, GITHUB ACTION AUTOMATICALLY RUNS AND DEPLOY.
        pass


    context = ["DETAILS"]
    # ---------------------------------------------------------------------------------------
    # UPDATE MACRO: ECOS
    # ---------------------------------------------------------------------------------------
    if GITHUB.CONFIG.ECOS:
        try:
            Ecos.api = "CEW3KQU603E6GA8VX0O9"
            ecos = Ecos()
            ecos.data(ECOSMETA).to_parquet(path=FILE.ECOS, engine='pyarrow')
            context += [f"- [SUCCESS] UPDATE ECOS: ", ecos.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE ECOS: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE ECOS: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE MACRO: FRED
    # ---------------------------------------------------------------------------------------
    if GITHUB.CONFIG.FRED:
        try:
            fred = Fred()
            fred.data(FREDMETA).to_parquet(path=FILE.FRED, engine='pyarrow')
            context += [f"- [SUCCESS] UPDATE FRED: ", fred.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE FRED: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE FRED: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE SECTOR COMPOSITION
    # ---------------------------------------------------------------------------------------
    if GITHUB.CONFIG.SECTOR:
        try:
            sector = SectorComposition()
            if sector.state == "SUCCESS":
                sector.data.to_parquet(path=FILE.SECTOR_COMPOSITION, engine='pyarrow')
            context += [f"- [{sector.state}] UPDATE SECTOR COMPOSITION: ", sector.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE SECTOR COMPOSITION: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE SECTOR COMPOSITION: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE FINANCIAL STATEMENT
    # ---------------------------------------------------------------------------------------
    if GITHUB.CONFIG.STATEMENT:
        tickers = FinancialStatement.checkTickers(FILE.BASELINE)
        try:
            financialStatement = FinancialStatement(*tickers)
            if not financialStatement.state == "PASSED":
                financialStatement.overview.to_parquet(path=FILE.STATEMENT_OVERVIEW, engine='pyarrow')
                financialStatement.annual.to_parquet(path=FILE.ANNUAL_STATEMENT, engine='pyarrow')
                financialStatement.quarter.to_parquet(path=FILE.QUARTER_STATEMENT, engine='pyarrow')
            context += [f"- [{financialStatement.state}] UPDATE FINANCIAL STATEMENT: ", financialStatement.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE FINANCIAL STATEMENT: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE FINANCIAL STATEMENT: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE AFTER MARKET DATA
    # ---------------------------------------------------------------------------------------
    if GITHUB.CONFIG.AFTERMARKET:
        try:
            afterMarket = AfterMarket()
            afterMarket.data.to_parquet(FILE.AFTER_MARKET, engine='pyarrow')
            context += [f"- [{afterMarket.state}] UPDATE AFTER MARKET: ", afterMarket.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE AFTER MARKET: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE AFTER MARKET: ", ""]

    # ---------------------------------------------------------------------------------------
    # BUILD BASELINE: THIS PROCESS IS MANDATORY
    # ---------------------------------------------------------------------------------------
    if ENV == "local":
        from pandas import read_parquet
        marketData = read_parquet(FILE.BASELINE, engine='pyarrow')
        TRADING_DATE = "LOCAL"
        context += [f"- [PASSED] BUILD MARKET BASELINE:", "  >> READ ON LOCAL ENV.", ""]

        macroData = read_parquet(FILE.MACRO_BASELINE, engine='pyarrow')
        context += [f"- [PASSED] BUILD MACRO BASELINE:", "  >> READ ON LOCAL ENV.", ""]
    else:
        baseline = MarketBaseline()
        marketData = baseline.data
        marketData.to_parquet(FILE.BASELINE, engine='pyarrow')
        TRADING_DATE = baseline.tradingDate
        context += [f"- [SUCCESS] BUILD MARKET BASELINE: ", baseline.log, ""]

        macro = MacroBaseline()
        macroData = macro.data
        macroData.to_parquet(FILE.MACRO_BASELINE, engine='pyarrow')
        context += [f"- [SUCCESS] BUILD MACRO BASELINE: ", macro.log, ""]


    # ---------------------------------------------------------------------------------------
    # DEPLOY MARKET MAP
    # ---------------------------------------------------------------------------------------
    marketMap = MarketMap(marketData)
    try:
        with open(file=os.path.join(PATH.DOCS, 'index.html'), mode='w', encoding='utf-8') as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.TEMPLATES)) \
                    .get_template('marketmap-1.0.0.html') \
                    .render({
                    "service": "marketmap",
                    "local": ENV == "local",
                    "title": "404" if ENV == "local" else "LAB￦ONS: \uc2dc\uc7a5\uc9c0\ub3c4",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900',
                    "statusValue": marketMap.stat.to_dict(),
                    "srcTicker": marketMap.data.to_json(orient='index'),
                    "srcIndicatorOpt": dumps(marketMap.meta),
                })
            )
        context += [f'- [SUCCESS] DEPLOY MARKET MAP', marketMap.log, '']
    except Exception as error:
        context += [f'- [FAILED] DEPLOY MARKET MAP', f'  : {error}', '']

    # ---------------------------------------------------------------------------------------
    # DEPLOY BUBBLE
    # ---------------------------------------------------------------------------------------
    marketBubble = MarketBubble(marketData)
    try:
        with open(file=os.path.join(PATH.DOCS, r'bubble/index.html'), mode='w', encoding='utf-8') as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.TEMPLATES)) \
                    .get_template('bubble-1.0.0.html') \
                    .render({
                    "service": "bubble",
                    "local": ENV == "local",
                    "title": "404" if ENV == "local" else "LAB￦ONS: \uc885\ubaa9\ubd84\ud3ec",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900',
                    "srcTickers": marketBubble.data.to_json(orient='index'),
                    "srcSectors": marketBubble.sectors.to_json(orient='index'),
                    "srcIndicatorOpt": dumps(marketBubble.meta),
                })
            )

        context += [f'- [SUCCESS] DEPLOY BUBBLES', marketBubble.log, '']
    except Exception as error:
        context += [f'- [FAILED] DEPLOY BUBBLES', f'  : {error}', '']

    # ---------------------------------------------------------------------------------------
    # UPDATE STOCK PRICE
    # ---------------------------------------------------------------------------------------
    stocks = Stocks()
    if (not DOMAIN == "HKEFICO") and GITHUB.CONFIG.STOCKPRICE:
        tickersMap = marketMap.stat.loc[["minTicker", "maxTicker"]].values.flatten().tolist()
        tickers = tickersMap

        stocks.update(*tickers)
        stocks.price.to_parquet(FILE.PRICE, engine='pyarrow')

        context += [f'- [{"FAILED" if "Failed" in stocks.log else "SUCCESS"}] UPDATE STOCK PRICE ', stocks.log, '']
    else:
        context += [f"- [PASSED] UPDATE STOCK PRICE: ", ""]

    # ---------------------------------------------------------------------------------------
    # DEPLOY STOCKS
    # ---------------------------------------------------------------------------------------
    PATH.STOCKS = os.path.join(PATH.DOCS, r'stocks')
    os.makedirs(PATH.STOCKS, exist_ok=True)
    clearPath(PATH.STOCKS)

    for ticker, stock in stocks:
        os.makedirs(os.path.join(PATH.STOCKS, rf'{ticker}'), exist_ok=True)
        with open(file=os.path.join(PATH.STOCKS, rf'{ticker}/index.html'), mode='w', encoding='utf-8') as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.TEMPLATES)) \
                    .get_template('stock-1.0.0.html') \
                    .render({
                    "service": "stock",
                    "local": ENV == "local",
                    "title": "404" if ENV == "local" else f"LAB￦ONS: {stock.name}",
                    "nav": SYSTEM_NAV,
                    "ticker": ticker,
                    "name": stock.name,
                    "xrange": stock.xrange,
                    "date": stock.date,
                    "ohlcv": stock.ohlcv,
                    "sma": stock.sma,
                    "bollinger": stock.bollinger,
                    "sales_y": stock.sales_y,
                    "sales_q": stock.sales_q,
                    "asset": stock.asset
                })
            )
    context += [f'- [SUCCESS] DEPLOY INDIVIDUAL STOCK ', stocks.log, '']

    # ---------------------------------------------------------------------------------------
    # DEPLOY MACRO
    # ---------------------------------------------------------------------------------------
    macro = Macro(macroData)
    try:
        with open(file=os.path.join(PATH.DOCS, r'macro/index.html'), mode='w', encoding='utf-8') as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.TEMPLATES)) \
                    .get_template('macro-1.0.0.html') \
                    .render({
                    "service": "macro",
                    "local": ENV == "local",
                    "title": "404" if ENV == "local" else "LAB￦ONS: \uacbd\uc81c\u0020\uc9c0\ud45c",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE} (또는 최근 발표일) 기준',
                    "srcIndicator": dumps(macro.serialize()),
                    "srcIndicatorOpt": dumps(macro.meta),
                    "srcStatus": macro.status,
                })
            )
        context += [f'- [SUCCESS] DEPLOY MACRO', macro.log, '']
    except Exception as error:
        context += [f'- [FAILED] DEPLOY MACRO', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # DEPLOY RESOURCES
    # ---------------------------------------------------------------------------------------
    if not ENV == "local":
        try:
            minify(DOCS)
            context += [f'- [SUCCESS] MINIFY RESOURCES ', '']
        except Exception as error:
            context += [f'- [FAILED] MINIFY RESOURCES ', f'  : {error}', '']

        try:
            rss(DOCS, "https://labwons.com", os.path.join(DOCS, "feed.xml"))
            sitemap(DOCS, "https://labwons.com", os.path.join(DOCS, "sitemap.xml"))
            context += [f'- [SUCCESS] DEPLOY Sitemap and RSS', '']
        except Exception as error:
            context += [f'- [FAILED] DEPLOY Sitemap and RSS', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # REPORT BUILD RESULT
    # ---------------------------------------------------------------------------------------
    mail = eMail()
    mail.context = "\n".join([f"TRADING DATE: {TRADING_DATE}"] + context)
    mail.subject = (f'[{"FAILED" if "FAILED" in mail.context else "SUCCESS"}] '
                    f'BUILD BASELINE on {CLOCK().strftime("%Y/%m/%d %H:%M")}')

    print(f'{mail.subject}\n{mail.context}\n')

    if GITHUB.EVENT == "schedule" or GITHUB.EVENT == "push":
        mail.send()

