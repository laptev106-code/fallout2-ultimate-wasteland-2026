import urllib.request
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://vk.com/rebuild_by_foxx', headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    raw = resp.read()
    html = raw.decode('windows-1251', errors='ignore')

out_path = os.path.join(os.path.dirname(__file__), 'vk_page.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved", out_path, "size:", len(html))

for line in html.splitlines():
    if '<title>' in line or 'og:' in line:
        print(line[:120])
