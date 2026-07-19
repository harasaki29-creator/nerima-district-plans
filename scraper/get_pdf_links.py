#!/usr/bin/env python3
"""
scraper/get_pdf_links.py

スクレイパー：指定の練馬区「地区計画一覧」ページからPDFリンクを抽出してdata/pdfsにダウンロードします。
"""
import os
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_PAGE = "https://www.city.nerima.tokyo.jp/kusei/machi/chikukeikaku/chiku_ichiran.html"
OUT_DIR = "data/pdfs"
HEADERS = {"User-Agent": "nerima-district-plans-scraper/1.0 (+https://github.com/harasaki29-creator/nerima-district-plans)"}

os.makedirs(OUT_DIR, exist_ok=True)

def get_pdf_links(page_url):
    r = requests.get(page_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith('.pdf'):
            full = urljoin(page_url, href)
            links.append((a.get_text(strip=True), full))
    # remove duplicates while preserving order
    seen = set()
    out = []
    for text, url in links:
        if url in seen:
            continue
        seen.add(url)
        out.append((text, url))
    return out

def download_pdf(url, out_dir=OUT_DIR, delay=0.5):
    local_name = url.split('/')[-1]
    local_path = os.path.join(out_dir, local_name)
    if os.path.exists(local_path):
        print(f"exists: {local_name}")
        return local_path
    with requests.get(url, stream=True, headers=HEADERS, timeout=60) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    time.sleep(delay)
    print(f"downloaded: {local_name}")
    return local_path

def main():
    print(f"fetching links from {BASE_PAGE}")
    links = get_pdf_links(BASE_PAGE)
    print(f"found {len(links)} pdf links")
    for text, url in links:
        try:
            download_pdf(url)
        except Exception as e:
            print(f"failed to download {url}: {e}")

if __name__ == '__main__':
    main()
