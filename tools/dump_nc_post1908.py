import urllib.request
import re

url = 'https://www.nuclear-city.com/topic/1908-fallout-2-expansion-version-rebuild-by-foxx/'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Page 1908 length:", len(html))
        
        # Find first post content
        match = re.search(r'<div data-role=[\'"]commentContent[\'"][^>]*>(.*?)</div>\s*<div class=[\'"]ipsItemControls', html, re.DOTALL)
        if match:
            content = match.group(1)
            clean = re.sub(r'<br\s*/?>', '\n', content)
            clean = re.sub(r'</p>', '\n', clean)
            clean = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', clean)
            clean = re.sub(r'<[^>]+>', '', clean)
            print("Post 1908 text:")
            print(clean[:3000])
except Exception as e:
    print("Error:", e)
