from datetime import datetime, timezone, timedelta
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom


KST = timezone(timedelta(hours=9))
def sitemap(root: str, domain: str, save:str="") -> str:
    """
    특정 루트 경로에서 index.html이 포함된 하위 디렉토리를 찾아 사이트맵(XML) 문자열로 반환.

    :param root: 파일 시스템 내 검색할 루트 디렉토리
    :param domain: 사이트의 기본 URL (예: "https://www.example.com")
    :param save: 저장 경로
    :return: XML 사이트맵 문자열
    """
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for dirpath, _, filenames in os.walk(root):
        if not "index.html" in filenames:
            continue
        index_path = os.path.join(dirpath, "index.html")
        last_modified_timestamp = os.path.getmtime(index_path)
        last_modified_dt = datetime.fromtimestamp(last_modified_timestamp, KST)
        last_modified_str = last_modified_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        last_modified_str = last_modified_str[:-2] + ":" + last_modified_str[-2:]  # +0900 → +09:00 변환

        relative_path = os.path.relpath(dirpath, root)
        path = f"{domain}/{relative_path.replace(os.sep, '/')}" if relative_path != '.' else domain

        url_element = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_element, "loc")
        loc.text = path
        lastmod = ET.SubElement(url_element, "lastmod")
        lastmod.text = last_modified_str
        freq = ET.SubElement(url_element, "changefreq")
        freq.text = "daily"
        priority = ET.SubElement(url_element, "priority")
        priority.text = "1.0" if path.count('/') < 3 else "0.9" if path.count("/") < 4 else "0.8"

    string = ET.tostring(urlset, encoding="utf-8", method="xml").decode("utf-8")
    if save:
        dom = xml.dom.minidom.parseString(string)
        with open(save, "w", encoding="utf-8") as file:
            file.write(f'''{dom.toprettyxml(indent="  ").replace(
'<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>'
)}''')
    return string


def rss(root: str, domain:str, save:str="") -> str:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "LAB￦ONS"
    ET.SubElement(channel, "link").text = domain
    ET.SubElement(channel, "description").text = "SNO￦BALL YOUR ASSET"
    ET.SubElement(channel, "pubDate").text = "Fri, 26 Jul 2024 12:00:00 +0900"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(KST).strftime("%a, %d %b %Y %H:%M:%S +0900")
    ET.SubElement(channel, "generator").text = "Custom Python Script 1.0"

    for dirpath, _, filenames in os.walk(root):
        if not "index.html" in filenames:
            continue
        file = os.path.join(dirpath, "index.html")
        date = datetime.fromtimestamp(os.stat(file).st_ctime, tz=KST) \
               .strftime("%a, %d %b %Y %H:%M:%S +0900")

        rel_path = os.path.relpath(dirpath, root).replace("\\", "/")
        url_page = f"{domain}/{rel_path}/index.html" if rel_path != "." else f"{domain}/index.html"
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = os.path.basename(dirpath)
        ET.SubElement(item, "author").text = "snob.labwons@gmail.com"
        ET.SubElement(item, "link").text = url_page
        ET.SubElement(item, "description").text = os.path.basename(dirpath)
        ET.SubElement(item, "pubDate").text = date

    string = ET.tostring(rss, encoding="utf-8", method="xml").decode("utf-8")
    if save:
        dom = xml.dom.minidom.parseString(string)
        with open(save, "w", encoding="utf-8") as file:
            file.write(f'''{dom.toprettyxml(indent="  ").replace(
'<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>'
)}''')
    return string


# 예제 실행
if __name__ == "__main__":
    from src.common.path import PATH

    domain = "https://www.labwons.com"
    print(sitemap(PATH.DOCS, domain))
    print(rss(PATH.DOCS, domain))