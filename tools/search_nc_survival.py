import urllib.request
import re

url = 'https://www.nuclear-city.com/topic/560-fallout-2-rp-fixed-edition/'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Search for comments mentioning выживан or survival or внешний вид
matches = re.findall(r'([^.\n]{0,80}(?:выживан|survival|внешност|голод|жажд|харкор|hardcore)[^.\n]{0,80})', html, re.IGNORECASE)
print(f"Matches count: {len(matches)}")
for m in set(matches)[:20]:
    print(" -", m.strip())
