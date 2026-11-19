import urllib.request
import urllib.parse
import re

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        links = re.findall(r'class="result__url"[^>]*href="([^"]+)"', html)
        titles = re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        return list(zip(links, titles, snippets))

res = search_ddg('site:github.com "Mr.Stalin" OR "sfall" "MapBlur"')
print("DDG MapBlur:", len(res))
for l, t, s in res[:4]:
    print(" ", l)

res2 = search_ddg('site:github.com/BGforgeNet "footsteps" OR "glasses"')
print("DDG BGforgeNet:", len(res2))
for l, t, s in res2[:4]:
    print(" ", l)
