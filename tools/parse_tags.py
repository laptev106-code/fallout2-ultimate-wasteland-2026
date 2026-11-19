import urllib.request
import re

url = 'https://github.com/sfall-team/sfall/releases'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

tags = re.findall(r'href="(/sfall-team/sfall/releases/tag/[^"]+)"', html)
for t in set(tags):
    print("Tag:", t)
