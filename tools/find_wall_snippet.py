import urllib.request
import re

url = 'https://vk.com/wall-174451664_10479'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    raw = resp.read()
    html = raw.decode('windows-1251', errors='ignore')

idx = html.find('Сборка Fallout 2')
if idx != -1:
    print(html[idx:idx+3000])
else:
    print("Not found by exact string, searching with lower:")
    idx = html.lower().find('fallout 2 (expansion version)')
    if idx != -1:
        print(html[idx-100:idx+2500])
