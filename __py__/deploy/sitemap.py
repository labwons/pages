from datetime import datetime
from pytz import timezone
import os


def updateSitemap():
    timestamp = datetime.now(timezone('Asia/Seoul'))
    timestamp = timestamp.replace(microsecond=0)
    with open(os.path.join(os.path.dirname(__file__), r"../sitemap.xml"), mode="w") as file:
        file.write(f"""---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://labwons.com</loc>
    <lastmod>{timestamp.isoformat()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://labwons.com/sectors</loc>
    <lastmod>{timestamp.isoformat()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>""")
    return
  

def updateRSS():
    timestamp = datetime.now(timezone('Asia/Seoul'))
    timestamp = timestamp.replace(microsecond=0)
    