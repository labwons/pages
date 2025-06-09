"""
TITLE   : BUILD LABWONS
AUTHOR  : SNOB
CONTACT : snob.labwons@gmail.com
ROUTINE : 15:40+09:00UTC on weekday
"""
if __name__ == "__main__":
    try:
        from ..common import env
        from ..common.path import PATH
        from ..common.email import eMail
        from ..fetch.market.spec import MarketSpec
        from ..fetch.market.fstat import FinancialStatement
        from ..render.navigate import navigate, minify
        from .service.baseline import MarketBaseline
        from .service.bubble import MarketBubble
        from .service.macro import Macro
        from .service.marketmap import MarketMap
        # from .service.portfolio import StockPortfolio
        from .resource.scope import rss, sitemap
    except ImportError:
        from src.common import env
        from src.common.path import PATH
        from src.common.email import eMail
        from src.fetch.market.spec import MarketSpec
        from src.fetch.market.fstat import FinancialStatement
        from src.render.navigate import navigate, minify
        from src.build.service.baseline import MarketBaseline
        from src.build.service.bubble import MarketBubble
        from src.build.service.macro import Macro
        from src.build.service.marketmap import MarketMap
        # from src.build.service.portfolio import StockPortfolio
        from src.build.resource.scope import rss, sitemap

    from jinja2 import Environment, FileSystemLoader
    from json import dumps
    from pykrx.stock import get_nearest_business_day_in_a_week
    from numpy import datetime_as_string
    from time import sleep
    import os

    # ---------------------------------------------------------------------------------------
    # ENVIRONMENT SETTINGS
    # ---------------------------------------------------------------------------------------
    SYSTEM_NAV      = navigate()
    CONFIG_BASELINE = True
    CONFIG_MACRO    = False
    CONFIG_STATE    = False



    if env.ENV == "local":
        # FOR LOCAL HOST TESTING, EXTERNAL DIRECTORY IS RECOMMENDED AND USED. USING THE SAME
        # LOCAL HOSTING DIRECTORY WITH DEPLOYMENT DIRECTORY, DEPLOYMENT MIGHT BE CORRUPTED.
        # IF YOU WANT TO USE DIFFERENT PATH FOR LOCAL HOST TESTING, BELOW {ROOT} VARIABLE ARE
        # TO BE CHANGED.
        _docs = os.path.join(PATH.DOWNLOADS, 'labwons')
        env.copytree(env.DOCS, _docs)
        env.DOCS = _docs

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

        if now.hour >= 20:
            CONFIG_BASELINE = False
            CONFIG_MACRO = True
            CONFIG_STATE = True

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "workflow_dispatch":
        # SELECTIVE FOR TESTING. CHANGE BEFORE COMMIT & PUSH, IF NEEDED.
        CONFIG_BASELINE = False
        CONFIG_MACRO = False
        CONFIG_STATE = False

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "push":
        pass


    context = ["DETAILS"]
    # ---------------------------------------------------------------------------------------
    # UPDATE BASELINE
    # ---------------------------------------------------------------------------------------
    # try:
    #     group = MarketGroup(update=CACHE)
    #     if CACHE andnot PATH.GROUP.startswith('http'):
    #         with open(PATH.GROUP, 'w') as f:
    #             f.write(group.to_json(orient='index').replace("nan", ""))
    #     context += [f"- [SUCCESS] MARKET GROUP: ", group.log, ""]
    # except Exception as report:
    #     context += [f"- [FAILED] MARKET GROUP: ", f'{report}', ""]

    # try:
    #     spec = MarketSpec(CONFIG_STATE)
    #     if CONFIG_STATE and not PATH.SPEC.startswith('http'):
    #         with open(PATH.SPEC, 'w') as f:
    #             f.write(spec.to_json(orient='index').replace("nan", ""))
    #     prefix = "PARTIALLY FAILED" if "FAIL" in spec.log else "SUCCESS"
    #     context += [f"- [{prefix}] MARKET NUMBERS: ", spec.log, ""]
    # except Exception as report:
    #     context += [f"- [FAILED] MARKET NUMBERS: ", f'{report}', ""]

    try:
        financialStatement = FinancialStatement(update=CONFIG_STATE)
        if env.ENV == "github_action":
            financialStatement.overview.to_parquet(path=env.FILE.STATEMENT_OVERVIEW, engine='pyarrow')
            financialStatement.annual.to_parquet(path=env.FILE.ANNUAL_STATEMENT, engine='pyarrow')
            financialStatement.quarter.to_parquet(path=env.FILE.QUARTER_STATEMENT, engine='pyarrow')
        prefix = "PARTIALLY FAILED" if "FAIL" in financialStatement.log else "SUCCESS"
        context += [f"- [{prefix}] MARKET NUMBERS: ", financialStatement.log, ""]
    except Exception as report:
        context += [f"- [FAILED] MARKET NUMBERS: ", f'{report}', ""]

    try:
        baseline = MarketBaseline(update=CONFIG_BASELINE)
        if not PATH.BASE.startswith('http'):
            with open(PATH.BASE, 'w') as f:
                f.write(baseline.to_json(orient='index').replace("nan", "null"))
        context += [f'- [SUCCESS] BUILD Baseline', baseline.log, '']
    except Exception as error:
        baseline = MarketBaseline(update=False)
        context += [f'- [FAILED] BUILD Baseline', f'  : {error}', '* Using latest baseline', '']

    TRADING_DATE = baseline['date'].values[0]
    if not isinstance(TRADING_DATE, str):
        TRADING_DATE = f"{datetime_as_string(TRADING_DATE, unit='D').replace('-', '/')}"

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
    # BUILD MARKET MAP
    # ---------------------------------------------------------------------------------------
    marketMap = MarketMap(baseline)

    try:
        with open(
            file=os.path.join(env.DOCS, 'index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                .get_template('marketmap-1.0.0.html') \
                .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: 시장지도",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900',
                    "historySection": False,
                    "statusValue": marketMap.peakPoint.to_dict(),
                    "srcTicker": marketMap.to_json(orient='index'),
                    "srcColors": marketMap.colors.to_json(orient='index'),
                    "srcIndicatorOpt": dumps(marketMap.meta),
                    "faq": marketMap.faqs
                })
            )

        context += [f'- [SUCCESS] Deploy Market-Map', marketMap.log, '']
    except Exception as error:
        context += [f'- [FAILED] Deploy Market-Map', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # BUILD BUBBLE
    # ---------------------------------------------------------------------------------------
    marketBubble = MarketBubble(baseline)
    try:
        with open(
            file=os.path.join(env.DOCS, r'bubble/index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                .get_template('bubble-1.0.0.html') \
                .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: 종목분포",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900',
                    "historySection": False,
                    "srcTickers": marketBubble.to_json(orient='index'),
                    "srcSectors": dumps(marketBubble.sector),
                    "srcIndicatorOpt": dumps(marketBubble.meta),
                    "faq": marketBubble.faqs
                })
            )

        context += [f'- [SUCCESS] Deploy Market-Bubble', marketBubble.log, '']
    except Exception as error:
        context += [f'- [FAILED] Deploy Market-Bubble', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # BUILD MACRO
    # ---------------------------------------------------------------------------------------
    macro = Macro(CONFIG_MACRO)

    try:
        if CONFIG_MACRO and not PATH.MACRO.startswith('http'):
            with open(PATH.MACRO, 'w') as f:
                f.write(macro.to_json(orient='index').replace('nan', ''))

        with open(
            file=os.path.join(env.DOCS, r'macro/index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                    .get_template('macro-1.0.0.html') \
                    .render({
                    "local": env.ENV == "local",
                    "title": "LAB￦ONS: 거시경제",
                    "nav": SYSTEM_NAV,
                    "tradingDate": f'{TRADING_DATE} (또는 최근 발표일) 기준',
                    "historySection": False,
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
    # BUILD RESOURCES
    # ---------------------------------------------------------------------------------------
    try:
        if not env.ENV == "local":
            minify()
        context += [f'- [SUCCESS] Minify Resources', '']
    except Exception as error:
        context += [f'- [FAILED] Minify Resources', f'  : {error}', '']

    try:
        rss(env.DOCS, "https://labwons.com", os.path.join(env.DOCS, "feed.xml"))
        sitemap(env.DOCS, "https://labwons.com", os.path.join(env.DOCS, "sitemap.xml"))
        context += [f'- [SUCCESS] Build RSS and Sitemap', '']
    except Exception as error:
        context += [f'- [FAILED] Build RSS and Sitemap', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # REPORT
    # ---------------------------------------------------------------------------------------
    mail = eMail()
    mail.context = "\n".join([f"TRADING DATE: {TRADING_DATE}"] + context)
    prefix = "SUCCESS"
    if "FAILED" in mail.context:
        prefix = "FAILED"
    mail.subject = f'[{prefix}] BUILD BASELINE on {env.CLOCK().strftime("%Y/%m/%d %H:%M")}'

    print(f'{mail.subject}\n{mail.context}\n')

    if env.ENV == 'github_action' and env.GITHUB_ACTION_EVENT == "schedule":
        mail.send()

