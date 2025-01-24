try:
    from .deploy.report import Report
    from ..common.path import PATH
except ImportError:
    from dev.portfolio.deploy.report import Report
    from dev.common.path import PATH
import pandas as pd
import os


TRACK = [
    {
        "ticker": "003230",
        "name": "",
        "path": "",
        "period": 10,
        "StartDate": "2024-12-18"
    },
    {
        "ticker": "214450",
        "name": "",
        "path": "",
        "period": 10,
        "StartDate": "2024-12-18"
    },
    {
        "ticker":"018290",
        "name": "",
        "path": "",
        "period": 10,
        "StartDate": "2024-12-18"
    }
]



def individualReport():
    sector = pd.read_json(PATH.GROUP).T
    sector.index = sector.index.astype(str).str.zfill(6)
    for n, meta in enumerate(TRACK):
        if not meta["ticker"] in TRACK:
            raise KeyError(f"Ticker: {meta['ticker']} 정보를 찾을 수 없습니다.")
        meta['name'] = sector.loc[meta['ticker'], 'name']

        path = os.path.join(PATH.ROOT, rf"portfolio/{str(n + 1).zfill(2)}")
        os.makedirs(path, exist_ok=True)
        meta['path'] = os.path.join(path, "index.html")
        docs = Report(**meta)
        docs.write(meta["path"])
    return



if __name__ == "__main__":
    individualReport()

