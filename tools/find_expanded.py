import urllib.request
import re

url = 'https://github.com/sfall-team/sfall/releases/expanded_assets/v4.5.1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

links = re.findall(r'href="([^"]+)"', html)
for l in set(links):
    if any(ext in l.lower() for ext in ['.zip', '.7z', '.rar']):
        print("Asset link:", l)
