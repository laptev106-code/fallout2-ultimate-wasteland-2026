import urllib.request
import re

url = 'https://www.nexusmods.com/fallout2/mods/45?tab=files'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8', errors='ignore')
        fids = re.findall(r'file_id=(\d+)', html)
        print('Found file_ids:', set(fids))
        for m in re.finditer(r'href="([^"]*file_id=\d+[^"]*)"', html):
            print('Link:', m.group(1))
except Exception as e:
    print('Error:', e)
