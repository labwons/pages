"""
TITLE   : BUILD MARKET BASELINE
AUTHOR  : SNOB
CONTACT : snob.labwons@gmail.com
ROUTINE : 15:40+09:00UTC on weekday
"""
if __name__ == "__main__":
    try:
        from ..common.path import PATH
        from ..common.report import eMail
        from ..render.navigate import navigate, minify
        from .service.baseline import MarketBaseline
        from .service.bubble import MarketBubble
        from .service.macro import Macro
        from .service.marketmap import MarketMap
        from .service.portfolio import StockPortfolio
        from .resource.scope import rss, sitemap
    except ImportError:
        from src.common.path import PATH
        from src.common.report import eMail
        from src.render.navigate import navigate, minify
        from src.build.service.baseline import MarketBaseline
        from src.build.service.bubble import MarketBubble
        from src.build.service.macro import Macro
        from src.build.service.marketmap import MarketMap
        from src.build.service.portfolio import StockPortfolio
        from src.build.resource.scope import rss, sitemap
    from datetime import datetime, timezone, timedelta
    from jinja2 import Environment, FileSystemLoader
    from json import dumps
    from pandas import set_option as PRINT_DATA
    from pykrx.stock import get_nearest_business_day_in_a_week
    from numpy import datetime_as_string
    from time import sleep
    import os

    # ---------------------------------------------------------------------------------------
    # ENVIRONMENT SETTINGS
    # ---------------------------------------------------------------------------------------
    PRINT_DATA('display.expand_frame_repr', False)

    BASE_DIR   = PATH.DOCS
    BASELINE   = True
    CLOCK      = lambda zone: datetime.now(zone)
    LOCAL_HOST = os.getenv('LOCAL_HOST') is None
    LOCAL_ZONE = timezone(timedelta(hours=9))
    ROUTER     = ''
    NAVIGATION = navigate()

    if LOCAL_HOST:
        # FOR LOCAL HOST TESTING, EXTERNAL DIRECTORY IS RECOMMENDED AND USED. USING THE SAME
        # LOCAL HOSTING DIRECTORY WITH DEPLOYMENT DIRECTORY, DEPLOYMENT MIGHT BE CORRUPTED.
        # IF YOU WANT TO USE DIFFERENT PATH FOR LOCAL HOST TESTING, BELOW {ROOT} VARIABLE ARE
        # TO BE CHANGED.
        BASE_DIR = os.path.join(PATH.DOWNLOADS, 'labwons')
        PATH.copytree(PATH.DOCS, BASE_DIR)

    if not LOCAL_HOST:
        # ON GITHUB ACTIONS, SYSTEM EXITS WHEN THE LATEST TRADING DATE AND CURRENT DATETIME
        # IS NOT MATCHED. THIS CODE IS IMPLEMENTED IN ORDER TO AVOID RUNNING ON WEEKDAY WHILE
        # HOLIDAYS OF THE MARKET.
        if get_nearest_business_day_in_a_week() != datetime.today().strftime("%Y%m%d"):
            raise SystemExit

        # ON GITHUB ACTIONS, IF SCHEDULED CRON TIME IS ACTIVATED BEFORE THE MARKET IS CLOSED,
        # WHICH ALMOST NEVER HAPPENS, BUILD AND DEPLOY WILL HOLD UNTIL THE MARKET IS CLOSED.
        now = CLOCK(LOCAL_ZONE)
        while now.hour == 15 and now.minute < 31:
            sleep(30)
            now = CLOCK(LOCAL_ZONE)

        if now.hour < 15:
            BASELINE = False

    # ---------------------------------------------------------------------------------------
    # UPDATE BASELINE
    # ---------------------------------------------------------------------------------------
    context = ["DETAILS"]

    try:
        baseline = MarketBaseline(update=BASELINE)
        if not PATH.BASE.startswith('http'):
            with open(PATH.BASE, 'w') as f:
                f.write(baseline.to_json(orient='index').replace("nan", "null"))
        prefix_baseline = "PARTIALLY FAILED" if baseline.log.count("FAIL") else "SUCCESS"
        context += [f'- [{prefix_baseline}] BUILD Baseline', baseline.log, '']
    except Exception as error:
        baseline = MarketBaseline(update=False)
        prefix_baseline = "FAILED"
        context += [f'- [{prefix_baseline}] BUILD Baseline', f'  : {error}', '* Using latest baseline', '']

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
    #     portfolio.javascript(**portfolioJsKeys).save(os.path.join(BASE_DIR, r'src/js/'))
    #     portfolioKeys = config.templateKeys()
    #     portfolioKeys.merge(**portfolio.defaultPortfolioAttribute)
    #     portfolioKeys["trading_date"] = f'{TRADING_DATE}\u0020\uc885\uac00\u0020\uae30\uc900'
    #     portfolioKeys["track_record"] = portfolioData.history()
    #     if LOCAL_HOST:
    #         portfolioKeys.fulltext()
    #     if not LOCAL_HOST:
    #         portfolioKeys.route(ROUTER)
    #     portfolio.html(**portfolioKeys).save(os.path.join(BASE_DIR, 'portfolio'))
    #     context += [f'- [SUCCESS] Deploy Portfolio', portfolioData.log, '']
    # except Exception as error:
    #     context += [f'- [FAILED] Deploy Portfolio',f'  : {error}', '']

    # ---------------------------------------------------------------------------------------
    # BUILD MARKET MAP
    # ---------------------------------------------------------------------------------------
    marketMap = MarketMap(baseline)

    try:
        with open(
            file=os.path.join(BASE_DIR, 'index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                .get_template('marketmap-1.0.0.html') \
                .render({
                    "local": LOCAL_HOST,
                    "title": "LAB￦ONS: 시장지도",
                    "nav": NAVIGATION,
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
            file=os.path.join(BASE_DIR, r'bubble/index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                .get_template('bubble-1.0.0.html') \
                .render({
                    "local": LOCAL_HOST,
                    "title": "LAB￦ONS: 종목분포",
                    "nav": NAVIGATION,
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
    macro = Macro(not LOCAL_HOST)
    try:
        with open(
            file=os.path.join(BASE_DIR, r'macro/index.html'),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write(
                Environment(loader=FileSystemLoader(PATH.HTML.TEMPLATES)) \
                    .get_template('macro-1.0.0.html') \
                    .render({
                    "local": LOCAL_HOST,
                    "title": "LAB￦ONS: 거시경제",
                    "nav": NAVIGATION,
                    "tradingDate": f'{TRADING_DATE} 기준 / 일부 지연',
                    "historySection": False,
                    "srcIndicator": dumps(macro.serialize()).replace(" ", ""),
                    "srcIndicatorOpt": dumps(macro.meta).replace(" ", ""),
                    "srcStatus": macro.status,
                    "faq": marketBubble.faqs
                })
            )

        context += [f'- [SUCCESS] Deploy Macro', marketBubble.log, '']
    except Exception as error:
        context += [f'- [FAILED] Deploy Macro', f'  : {error}', '']


    # ---------------------------------------------------------------------------------------
    # BUILD RESOURCES
    # ---------------------------------------------------------------------------------------
    try:
        if not LOCAL_HOST:
            minify()
        context += [f'- [SUCCESS] Minify Resources', '']
    except Exception as error:
        context += [f'- [FAILED] Minify Resources', f'  : {error}', '']

    try:
        rss(BASE_DIR, "https://labwons.com", os.path.join(BASE_DIR, "feed.xml"))
        sitemap(BASE_DIR, "https://labwons.com", os.path.join(BASE_DIR, "sitemap.xml"))
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
    mail.subject = f'[{prefix}] BUILD BASELINE on {datetime.now(LOCAL_ZONE).strftime("%Y/%m/%d %H:%M")}'

    if LOCAL_HOST:
        print(f'{mail.subject}\n{mail.context}\n')
        # print(f'{baseline}\n{"-" * 50}\n{marketMap}')
    else:
        mail.send()

