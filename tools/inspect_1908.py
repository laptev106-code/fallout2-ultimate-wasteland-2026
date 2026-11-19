import urllib.request
import re

url = 'https://www.nuclear-city.com/topic/1908-fallout-2-expansion-version-rebuild-by-foxx/'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Search for any links in the page
links = re.findall(r'href="(https?://[^"]+)"', html)
for l in links:
    if any(k in l.lower() for k in ['txt', 'pastebin', 'drive', 'yadi.sk', 'cloud.mail', 'rebuild', 'vk.com']):
        print("Link:", l)

# Print some text
lines = html.splitlines()
for line in lines:
    if any(k in line.lower() for k in ['изменения', 'changelog', 'история', 'версия', 'скачать']):
        clean = re.sub(r'<[^>]+>', ' ', line).strip()
        if len(clean) > 20 and len(clean) < 300:
            print("Line:", clean)
