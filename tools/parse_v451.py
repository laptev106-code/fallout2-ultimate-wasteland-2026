import urllib.request
import re

url = 'https://github.com/sfall-team/sfall/releases/tag/v4.5.1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

assets = re.findall(r'href="(/sfall-team/sfall/releases/download/[^"]+)"', html)
for a in set(assets):
    print("Asset:", "https://github.com" + a)
