"""
TITLE   : BUILD LABWONS
AUTHOR  : SNOB
CONTACT : snob.labwons@gmail.com
ROUTINE : 15:30+09:00UTC on weekday
"""
if __name__ == "__main__":
    try:
        from ..common import env
        from ..common.email import eMail
        from ..fetch.market.aftermarket import AfterMarket
        from ..fetch.market.finances import FinancialStatement
        from ..fetch.market.sector import SectorComposition
        from ..render.navigate import navigate, minify
        from .baseline.baseline import Baseline
        from .apps.marketmap import MarketMap
        from .apps.bubble import MarketBubble
        from .apps.sitemap import rss, sitemap
        from .service.baseline import MarketBaseline
        # from .service.bubble import MarketBubble
        from .service.macro import Macro
        from .action import ACTION
    except ImportError:
        from src.common import env
        from src.common.email import eMail
        from src.fetch.market.aftermarket import AfterMarket
        from src.fetch.market.finances import FinancialStatement
        from src.fetch.market.sector import SectorComposition
        from src.render.navigate import navigate, minify
        from src.build.baseline.baseline import Baseline
        from src.build.apps.marketmap import MarketMap
        from src.build.apps.bubble import MarketBubble
        from src.build.apps.sitemap import rss, sitemap
        from src.build.service.baseline import MarketBaseline
        # from src.build.service.bubble import MarketBubble
        from src.build.service.macro import Macro
        from src.build.action import ACTION

    from jinja2 import Environment, FileSystemLoader
    from json import dumps
    from pykrx.stock import get_nearest_business_day_in_a_week
    from numpy import datetime_as_string
    from time import sleep
    import os

    # ---------------------------------------------------------------------------------------
    # ENVIRONMENT SETTINGS
    # ---------------------------------------------------------------------------------------
    SYSTEM_NAV = navigate()

    DUPLICATED_CONFIG = False

    if env.ENV == "local":
        # FOR LOCAL HOST TESTING, EXTERNAL DIRECTORY IS RECOMMENDED AND USED. USING THE SAME
        # LOCAL HOSTING DIRECTORY WITH DEPLOYMENT DIRECTORY, DEPLOYMENT MIGHT BE CORRUPTED.
        # IF YOU WANT TO USE DIFFERENT PATH FOR LOCAL HOST TESTING, BELOW {ROOT} VARIABLE ARE
        # TO BE CHANGED.
        _docs = os.path.join(env.DOWNLOADS, 'labwons')
        env.copytree(env.DOCS, _docs)
        env.DOCS = _docs
        ACTION.reset()

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "schedule":
        # ON GITHUB ACTIONS, SYSTEM EXITS WHEN THE LATEST TRADING DATE AND CURRENT DATETIME
        # IS NOT MATCHED. THIS CODE IS IMPLEMENTED IN ORDER TO AVOID RUNNING ON WEEKDAY WHILE
        # HOLIDAYS OF THE MARKET.
        if get_nearest_business_day_in_a_week() != env.CLOCK().strftime("%Y%m%d"):
            raise SystemExit

        # ON GITHUB ACTIONS, IF SCHEDULED TIME IS ACTIVATED BEFORE THE MARKET IS CLOSED,
        # WHICH HARDLY HAPPENS, BUILD AND DEPLOY WILL HOLD UNTIL THE MARKET IS CLOSED.
        now = env.CLOCK()
        while (now.hour == 15) and (15 <= now.minute < 31):
            sleep(30)
            now = env.CLOCK()

        ACTION.reset()
        if now.hour >= 20:
            ACTION.MACRO = ACTION.STATEMENT = True
        else:
            DUPLICATED_CONFIG = True
            ACTION.AFTERMARKET = True

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "workflow_dispatch":
        # USE LATEST CACHING RESOURCES TO DEPLOY AND BUILD.
        ACTION.reset()

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "push":
        # EXTERNAL CONFIGURATION FOR BUILD CACHING. CONFIGURATION SCRIPT AT //src/build/action.py
        # IF CONFIGURED AND PUSHED, GITHUB ACTION AUTOMATICALLY RUNS AND DEPLOY.
        pass


    context = ["DETAILS"]
    # ---------------------------------------------------------------------------------------
    # UPDATE SECTOR COMPOSITION
    # ---------------------------------------------------------------------------------------
    if ACTION.SECTOR:
        try:
            sector = SectorComposition()
            if sector.state == "SUCCESS":
                sector.data.to_parquet(path=env.FILE.SECTOR_COMPOSITION, engine='pyarrow')
            context += [f"- [{sector.state}] UPDATE SECTOR COMPOSITION: ", sector.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE SECTOR COMPOSITION: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE SECTOR COMPOSITION: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE FINANCIAL STATEMENT
    # ---------------------------------------------------------------------------------------
    if ACTION.STATEMENT:
        tickers = FinancialStatement.checkTickers(env.FILE.BASELINE)
        try:
            financialStatement = FinancialStatement(*tickers)
            if not financialStatement.state == "PASSED":
                financialStatement.overview.to_parquet(path=env.FILE.STATEMENT_OVERVIEW, engine='pyarrow')
                financialStatement.annual.to_parquet(path=env.FILE.ANNUAL_STATEMENT, engine='pyarrow')
                financialStatement.quarter.to_parquet(path=env.FILE.QUARTER_STATEMENT, engine='pyarrow')
            context += [f"- [{financialStatement.state}] UPDATE FINANCIAL STATEMENT: ", financialStatement.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE FINANCIAL STATEMENT: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE FINANCIAL STATEMENT: ", ""]

    # ---------------------------------------------------------------------------------------
    # UPDATE AFTER MARKET DATA
    # ---------------------------------------------------------------------------------------
    if ACTION.AFTERMARKET:
        try:
            afterMarket = AfterMarket()
            afterMarket.data.to_parquet(env.FILE.AFTER_MARKET, engine='pyarrow')
            context += [f"- [{afterMarket.state}] UPDATE AFTER MARKET: ", afterMarket.log, ""]
        except Exception as report:
            context += [f"- [FAILED] UPDATE AFTER MARKET: ", f'{report}', ""]
    else:
        context += [f"- [PASSED] UPDATE AFTER MARKET: ", ""]

    # ---------------------------------------------------------------------------------------
    # BUILD BASELINE
    # ---------------------------------------------------------------------------------------
    # NO FAIL-SAFE ACTION FOR BASELINE. THIS PROCESS IS MANDATORY.
    if env.ENV == "local":
        from pandas import read_parquet
        resource = read_parquet(env.FILE.BASELINE, engine='pyarrow')
        TRADING_DATE = "LOCAL"
        context += [f"- [PASSED] UPDATE BASELINE: READ ON LOCAL ENV.", ""]
    else:
        baseline = Baseline()
        baseline.data.to_parquet(env.FILE.BASELINE, engine='pyarrow')
        resource = baseline.data
        TRADING_DATE = baseline.tradingDate
        context += [f"- [SUCCESS] UPDATE BASELINE: ", baseline.log, ""]

    # ---------------------------------------------------------------------------------------
    # DEPLOY MARKET MAP
    # ---------------------------------------------------------------------------------------
    marketMap = MarketMap(resource)
    try:
        with open(
                file=os.path.join(env.DOCS, 'index.html'),
                mode='w',
                encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(env.HTML.TEMPLATES)) \
                    .get_template('marketmap-1.0.0.html') \
                    .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: \uc2dc\uc7a5\uc9c0\ub3c4",
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
    marketBubble = MarketBubble(resource)
    try:
        with open(
                file=os.path.join(env.DOCS, r'bubble/index.html'),
                mode='w',
                encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(env.HTML.TEMPLATES)) \
                    .get_template('bubble-1.0.0.html') \
                    .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: \uc885\ubaa9\ubd84\ud3ec",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900',
                    "srcTickers": marketBubble.data.to_json(orient='index'),
                    "srcSectors": marketBubble.sectors.to_json(orient='index'),
                    "srcIndicatorOpt": dumps(marketBubble.meta),
                })
            )

        context += [f'- [SUCCESS] DEPLOY BUBBLES', marketBubble.log, '']
    except Exception as error:
        context += [f'- [FAILED] Deploy Market-Bubble', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # BUILD BASELINE
    # ---------------------------------------------------------------------------------------
    # try:
    #     baseline = MarketBaseline(update=DUPLICATED_CONFIG)
    #     with open(env.FILE.BASELINE_DUPLICATED, 'w') as f:
    #         f.write(baseline.to_json(orient='index').replace("nan", "null"))
    #     context += [f'- [SUCCESS] BUILD Baseline', baseline.log, '']
    # except Exception as error:
    #     baseline = MarketBaseline(update=False)
    #     context += [f'- [FAILED] BUILD Baseline', f'  : {error}', '  * Using latest baseline', '']
    #
    # TRADING_DATE = baseline['date'].values[0]
    # if not isinstance(TRADING_DATE, str):
    #     TRADING_DATE = f"{datetime_as_string(TRADING_DATE, unit='D').replace('-', '/')}"

    # ---------------------------------------------------------------------------------------
    # UPDATE PORTFOLIO
    # ---------------------------------------------------------------------------------------
    # try:
    #     portfolioData = StockPortfolio(baseline)
    #
    #     portfolioJsKeys = {
    #         "srcTickers": portfolioData.status().to_json(orient='index')
    #     }
    #     portfolio.javascript(**portfolioJsKeys).save(os.path.join(env.DOCS, r'src/js/'))
    #     portfolioKeys = config.templateKeys()
    #     portfolioKeys.merge(**portfolio.defaultPortfolioAttribute)
    #     portfolioKeys["trading_date"] = f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900'
    #     portfolioKeys["track_record"] = portfolioData.history()
    #     if LOCAL_HOST:
    #         portfolioKeys.fulltext()
    #     portfolio.html(**portfolioKeys).save(os.path.join(env.DOCS, 'portfolio'))
    #     context += [f'- [SUCCESS] Deploy Portfolio', portfolioData.log, '']
    # except Exception as error:
    #     context += [f'- [FAILED] Deploy Portfolio',f'  : {error}', '']





    # ---------------------------------------------------------------------------------------
    # DEPLOY MACRO
    # ---------------------------------------------------------------------------------------
    try:
        macro = Macro(update=ACTION.MACRO)
        if ACTION.MACRO:
            with open(env.FILE.MACRO, 'w') as f:
                f.write(macro.to_json(orient='index').replace('nan', ''))

        with open(
            file=os.path.join(env.DOCS, r'macro/index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(env.HTML.TEMPLATES)) \
                    .get_template('macro-1.0.0.html') \
                    .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: 거시경제",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE} (또는 최근 발표일) 기준',
                    "srcIndicator": dumps(macro.serialize()).replace(" ", ""),
                    "srcIndicatorOpt": dumps(macro.meta).replace(" ", ""),
                    "srcStatus": macro.status,
                    "faq": macro.faqs
                })
            )

        context += [f'- [SUCCESS] Deploy Macro', macro.log, '']
    except Exception as error:
        context += [f'- [FAILED] Deploy Macro', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # DEPLOY RESOURCES
    # ---------------------------------------------------------------------------------------
    try:
        if not env.ENV == "local":
            minify()
        context += [f'- [SUCCESS] DEPLOY RESOURCES (MINIFY)', '']
    except Exception as error:
        context += [f'- [FAILED] DEPLOY RESOURCES (MINIFY)', f'  : {error}', '']

    try:
        rss(env.DOCS, "https://labwons.com", os.path.join(env.DOCS, "feed.xml"))
        sitemap(env.DOCS, "https://labwons.com", os.path.join(env.DOCS, "sitemap.xml"))
        context += [f'- [SUCCESS] DEPLOY Sitemap and RSS', '']
    except Exception as error:
        context += [f'- [FAILED] DEPLOY Sitemap and RSS', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # REPORT BUILD RESULT
    # ---------------------------------------------------------------------------------------
    mail = eMail()
    mail.context = "\n".join([f"TRADING DATE: {TRADING_DATE}"] + context)
    mail.subject = (f'[{"FAILED" if "FAILED" in mail.context else "SUCCESS"}] '
                    f'BUILD BASELINE on {env.CLOCK().strftime("%Y/%m/%d %H:%M")}')

    print(f'{mail.subject}\n{mail.context}\n')

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "schedule":
        mail.send()

