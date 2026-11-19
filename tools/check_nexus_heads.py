import urllib.request
import urllib.parse
import re

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote('site:nexusmods.com/fallout2 "Talking Heads"')
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        titles = re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL)
        links = re.findall(r'class="result__url"[^>]*href="([^"]+)"', html)
        for t, l in zip(titles, links):
            clean_t = re.sub(r'<[^>]+>', '', t).strip()
            print("Title:", clean_t)
            print("URL:", l)
except Exception as e:
    print("Error:", e)
