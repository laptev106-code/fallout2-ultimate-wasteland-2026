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

res = search_ddg('"MapBlurFX" site:nuclear-city.com')
print("MapBlurFX Nuclear City:", len(res))
for l, t, s in res[:5]:
    clean_t = re.sub(r'<[^>]+>', '', t).strip()
    clean_s = re.sub(r'<[^>]+>', '', s).strip()
    print(" ", clean_t, "->", l)
    print("   ", clean_s[:150])

res2 = search_ddg('"Glasses Mod" site:nuclear-city.com')
print("\nGlasses Mod Nuclear City:", len(res2))
for l, t, s in res2[:5]:
    clean_t = re.sub(r'<[^>]+>', '', t).strip()
    clean_s = re.sub(r'<[^>]+>', '', s).strip()
    print(" ", clean_t, "->", l)
    print("   ", clean_s[:150])
