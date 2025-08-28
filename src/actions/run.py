#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ON GOOGLE COLAB, THIS SECTION MUST BE INITIALIZED. IT TAKES ABOUT 2MINUTES.
# AFTER RUNNING THIS SECTION, RUNTIME(SESSION) MUST BE RESTARTED, IN ORDER TO
# USE labwons/ PACKAGE. SESSION RESTART HOTKEY IS CTRL + M.
import os
if any("COLAB" in e for e in os.environ):
    get_ipython().system('git clone https://github.com/labwons/labwons.git')
    get_ipython().run_line_magic('cd', 'labwons')
    get_ipython().system('pip install -r requirements.txt -e .')


# In[ ]:


JOBS   = [
    "BUILD.MARKET-BASELINE",

    # "FETCH.SECTOR-COMPOSITION",
    "FETCH.DAILY-MARKET",    
    # "FETCH.FINANCIAL-STATEMENT",
    # "FETCH.STOCK-DATA",  
]


# In[ ]:


from labwons.util import DATETIME
import os

ACTION = os.environ.get("GITHUB_EVENT_NAME", "LOCALHOST").upper()
HOSTID = os.environ.get("USERDOMAIN", "COLAB") if ACTION == "LOCALHOST" else "GITHUB"

if HOSTID == "GITHUB":
    os.chdir(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))

if HOSTID == "GITHUB" and ACTION == "SCHEDULE":
    # SYSTEM EXITS WHEN THE LATEST TRADING DATE AND BUILD DATE IS DIFFERENT.
    # THIS CODE IS IMPLEMENTED IN ORDER TO AVOID RUNNING ON WEEKDAY OR HOLIDAY
    # OF THE MARKET.
    if DATETIME.TRADING != DATETIME.TODAY:
        raise SystemExit

    # IF THE TASK IS TRIGGERED BEFORE THE MARKET CLOSES, WHICH HARDLY HAPPENS,
    # SYSTEM PAUSES UNTIL THE MARKET CLOSES
    while (DATETIME.TIME().hour == 15) and (15 <= DATETIME.TIME().minute < 31):
        DATETIME.pause(30)

    if DATETIME.TIME().hour >= 22:
        JOBS = ["FETCH.FINANCIAL-STATEMENT"]
    else:
        JOBS = ["FETCH.DAILY-MARKET"]
    JOBS += ["BUILD.MARKET-BASELINE", "DEPLOY.ALL"]


# In[ ]:


from labwons.path import ARCHIVE
from labwons.fetch import MarketDaily, MarketSectors, FinancialStatement

if HOSTID != "HKEFICO":
    # NEW = ARCHIVE.new(DATETIME.TRADING)
    NEW = ARCHIVE.new('20250827')

    if "FETCH.SECTOR-COMPOSITION" in JOBS:
        MarketSectors.saveAs(ARCHIVE.write(DATETIME.WISE).MARKET_SECTORS)

    if "FETCH.DAILY-MARKET" in JOBS:
        MarketDaily.saveAs(NEW.MARKET_DAILY)

    if "FETCH.FINANCIAL-STATEMENT" in JOBS:
        from pandas import read_parquet
        tickers = read_parquet(ARCHIVE.MARKET_BASELINE, engine='pyarrow').index
        financialStatement = FinancialStatement(*tickers)
        financialStatement.fetchOverview(NEW.MARKET_OVERVIEW)
        financialStatement.fetchAnnualStatement(NEW.STATEMENT_A)
        financialStatement.fetchQuarterStatement(NEW.STATEMENT_Q)

    if "FETCH.STOCK-DATA" in JOBS:
        # TODO
        # 로컬(HKEFICO)에서 개발할 때 사용하는 Cache
        # 실제로는 즉시 Fetch -> Deploy 로 사용
        pass


# In[ ]:


from labwons.path import ARCHIVE
from labwons.build import MarketBaseline

# NEW = ARCHIVE.write(DATETIME.TRADING)

if "BUILD.MARKET-BASELINE" in JOBS:
    MarketBaseline.build()

BASELINE_DATE = MarketBaseline.BASELINE_DATE
if not BASELINE_DATE:
    BASELINE_DATE = ARCHIVE.LATEST.DATE


# In[ ]:


if HOSTID == "COLAB":
    from google.colab import drive
    from json import load
    drive.mount('/content/drive')

    with open(r"/content/drive/MyDrive/secrets.json") as secrets:
        os.environ.update(load(secrets))

    if not os.getcwd().endswith('labwons'):
        get_ipython().run_line_magic('cd', 'labwons')

    get_ipython().system('git config --global user.name "$GITHUB_USER"')
    get_ipython().system('git config --global user.email "$GUTHUB_EMAIL"')
    get_ipython().system('git remote set-url origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"')
    get_ipython().system('git add .')
    get_ipython().system('git commit -m "COMMIT AND PUSH FROM COLAB"')
    get_ipython().system('git push origin main')


# In[ ]:


if HOSTID == "GITHUB":
    from labwons.util import Mail
    from labwons.logs import read_log

    report = Mail()
    report.content = content = read_log()
    report.subject = f'[{"FAILED" if "FAILED" in content else "SUCCESS"}] BUILD LABWONS : {DATETIME.CLOCK().strftime("%Y/%m/%d %H:%M")}'
    report.send()

