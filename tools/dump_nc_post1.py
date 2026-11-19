import urllib.request
import re

url = 'https://www.nuclear-city.com/topic/560-fallout-2-rp-fixed-edition/'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Find first post content
match = re.search(r'<div data-role=[\'"]commentContent[\'"][^>]*>(.*?)</div>\s*<div class=[\'"]ipsItemControls', html, re.DOTALL)
if match:
    content = match.group(1)
    # clean tags but keep links and text
    clean = re.sub(r'<br\s*/?>', '\n', content)
    clean = re.sub(r'</p>', '\n', clean)
    clean = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', clean)
    clean = re.sub(r'<[^>]+>', '', clean)
    print("Post 1 text:")
    print(clean[:3000])
