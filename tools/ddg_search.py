import urllib.request
import urllib.parse
import re

query = 'rebuild_by_foxx fallout 2 txt'
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        links = re.findall(r'class="result__url"[^>]*href="([^"]+)"', html)
        titles = re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        print(f"Found {len(links)} results:")
        for l, t, s in zip(links, titles, snippets):
            clean_t = re.sub(r'<[^>]+>', '', t).strip()
            clean_s = re.sub(r'<[^>]+>', '', s).strip()
            print("---")
            print("Title:", clean_t)
            print("URL:", l)
            print("Snippet:", clean_s[:150])
except Exception as e:
    print("Error:", e)
