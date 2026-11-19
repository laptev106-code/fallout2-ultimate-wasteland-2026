import urllib.request
import re

url = 'https://vk.com/wall-174451664_10479'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    raw = resp.read()
    html = raw.decode('windows-1251', errors='ignore')

# Extract wall post text
post = re.search(r'class="wall_post_text"[^>]*>(.*?)</div>', html, re.DOTALL)
if post:
    content = post.group(1)
    clean = re.sub(r'<br\s*/?>', '\n', content)
    clean = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', clean)
    clean = re.sub(r'<[^>]+>', '', clean)
    print("Post text:")
    print(clean)
else:
    print("No wall_post_text found, searching other tags...")
    matches = re.findall(r'<div class="[^"]*post_text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    for m in matches:
        clean = re.sub(r'<br\s*/?>', '\n', m)
        print("Match:\n", clean[:500])
