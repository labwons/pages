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


# In[1]:


JOBS   = [
    # "FETCH.DAILY-MARKET",
    "FETCH.SECTOR-COMPOSITION",
    # "FETCH.FINANCIAL-STATEMENT",
    # "FETCH.STOCK-DATA"
]


# In[ ]:


from labwons.util import DATETIME
import os

os.chdir(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))
ACTION = os.environ.get("GITHUB_EVENT_NAME", "LOCALHOST").upper()
HOSTID = os.environ.get("USERDOMAIN", "COLAB") if ACTION == "LOCALHOST" else "GITHUB"

# GITHUB ACTION
if ACTION == "SCHEDULE":

    # SYSTEM EXITS WHEN THE LATEST TRADING DATE AND BUILD DATE IS DIFFERENT.
    # THIS CODE IS IMPLEMENTED IN ORDER TO AVOID RUNNING ON WEEKDAY OR HOLIDAY
    # OF THE MARKET.
    if DATETIME.TRADING != DATETIME.TODAY:
        raise SystemExit

    # IF THE TASK IS TRIGGERED BEFORE THE MARKET CLOSES, WHICH HARDLY HAPPENS,
    # SYSTEM PAUSES UNTIL THE MARKET CLOSES
    while (DATETIME.TIME().hour == 15) and (15 <= DATETIME.TIME().minute < 31):
        DATETIME.pause(30)

    if DATETIME.TIME().hour >= 20:
        JOBS = ["FETCH.ECOS", "FETCH.FRED", "FETCH.FINANCIAL-STATEMENT"]
    else:
        JOBS = ["FETCH.DAILY-MARKET", "FETCH.STOCKS"]
    JOBS += ["BUILD.MARKET-BASELINE", "BUILD.MACRO-BASELINE", "DEPLOY.ALL"]

# if ACTION == "LOCALHOST" and HOSTID == "HKEFICO":
#     JOBS = [job for job in JOBS if not job.startswith("FETCH")]


# In[ ]:


from labwons.path import ARCHIVE, GITHUB_REMOTE
from labwons.fetch import (
    MarketDaily, MarketSectors, FinancialStatement
)

ARCHIVE.create(DATETIME.TODAY)
if "FETCH.DAILY-MARKET" in JOBS:
    MarketDaily.fetch(ARCHIVE.MARKET_DAILY)

if "FETCH.SECTOR-COMPOSITION" in JOBS:
    MarketSectors.fetch(ARCHIVE.MARKET_SECTORS)

if "FETCH.FINANCIAL-STATEMENT" in JOBS:
    from pandas import read_parquet
    tickers = read_parquet(ARCHIVE.recentBaseline, engine='pyarrow').index
    financialStatement = FinancialStatement(*tickers)
    financialStatement.fetchOverview(ARCHIVE.MARKET_OVERVIEW)
    financialStatement.fetchAnnualStatement(ARCHIVE.STATEMENT_A)
    financialStatement.fetchQuarterStatement(ARCHIVE.STATEMENT_Q)

if "FETCH.STOCK-DATA" in JOBS:
    # TODO
    # 로컬(HKEFICO)에서 개발할 때 사용하는 Cache
    # 실제로는 즉시 Fetch -> Deploy 로 사용
    pass

if HOSTID == "COLAB" and "FETCH.SECTOR-COMPOSITION" in JOBS:
    get_ipython().run_line_magic('cd', 'labwons')
    get_ipython().system('git config --global user.name "SNOB ACTIONS"')
    get_ipython().system('git config --global user.email "snob.labwons@gmail.com"')
    get_ipython().system('git remote set-url origin {GITHUB_REMOTE}')
    get_ipython().system('git add {ARCHIVE.MARKET_SECTORS}')
    get_ipython().system('git commit -m "Update MARKET SECTOR COMPOSITION"')
    get_ipython().system('git push origin main')

# TODO
# 일정 기간이 지난 날짜의 아카이브 폴더는 드라이브로 백업하는 코드 작성: Clean-UP


# In[ ]:


if HOSTID == "GITHUB":
    from labwons.util import Mail
    from labwons.logs import read_log

    report = Mail()
    report.content = content = read_log("fetch", "build")
    report.subject = f'[{"FAILED" if "FAILED" in content else "SUCCESS"}] BUILD LABWONS : {DATETIME.CLOCK().strftime("%Y/%m/%d %H:%M")}'
    report.send()
    # print(content) # TODO 만약 로그가 GITHUB 콘솔에 찍히면 삭제하세요.

