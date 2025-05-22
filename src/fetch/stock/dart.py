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