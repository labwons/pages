from io import BytesIO
from pandas import DataFrame
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import requests


API = 'fcf58ccf10928bd7898541204ce46824537cbd9f'

url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API}"
response = requests.get(url)

# zip 파일 안의 XML을 읽기
with ZipFile(BytesIO(response.content)) as zf:
    with zf.open(zf.namelist()[0]) as xml_file:
        xml_text = xml_file.read().decode("utf-8")


root = ET.fromstring(xml_text)
data = []
for corp in root.iter("list"):
    data.append({
        "corp_code": corp.findtext("corp_code"),
        "corp_name": corp.findtext("corp_name"),
        "stock_code": corp.findtext("stock_code"),
        "modify_date": corp.findtext("modify_date")
    })

df = DataFrame(data)
df = df[df["stock_code"] != " "]  # 상장사만 필터링

print(df)


# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# from pandas import set_option
#
# set_option('display.expand_frame_repr', False)
#
# def get_dart_filings(corp_code=None, start_date=None, end_date=None):
#     """
#     DART 공시 목록 조회
#     corp_code: 기업 고유 코드 (없으면 전체)
#     start_date, end_date: YYYYMMDD 형식
#     """
#     url = "https://opendart.fss.or.kr/api/list.json"
#     params = {
#         "crtfc_key": API,
#         "bgn_de": start_date,
#         "end_de": end_date,
#         "corp_code": corp_code or "",  # 특정 기업만 추적할 수도 있음
#         "page_no": 1,
#         "page_count": 100
#     }
#
#     resp = requests.get(url, params=params)
#     data = resp.json()
#
#     if data["status"] != "013":  # 013 = 조회된 데이터 없음
#         return pd.DataFrame(data["list"])
#     else:
#         return pd.DataFrame()
#
# # 오늘 날짜 기준으로 최근 7일간 공시 확인
# today = datetime.today()
# start = (today - timedelta(days=7)).strftime("%Y%m%d")
# end = today.strftime("%Y%m%d")
#
# df = get_dart_filings(start_date=start, end_date=end)
# print(df)
#
# # 정기보고서(사업, 분기, 반기)만 필터링
# reports = df[df["report_nm"].str.contains("사업보고서|분기보고서|반기보고서")]
#
# if not reports.empty:
#     print("최근 업데이트된 정기보고서:")
#     print(reports[["corp_name", "report_nm", "rcept_dt", "rcept_no"]])
#     # 여기서 FnGuide 크롤링 루틴 실행
# else:
#     print("최근 일주일간 정기보고서 공시 없음")
