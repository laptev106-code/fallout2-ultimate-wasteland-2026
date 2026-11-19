import urllib.request
import re

url = 'https://vk.com/wall-174451664_10479'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
        html = raw.decode('windows-1251', errors='ignore')
        print("Wall post length:", len(html))
        
        # Search for all links in wall post
        links = re.findall(r'href="([^"]+)"', html)
        for l in set(links):
            if any(k in l.lower() for k in ['txt', 'pastebin', 'drive', 'yadi', 'cloud', 'nuclear', 'topic', 'board']):
                print("Wall link:", l)
                
        # Find post text
        lines = html.splitlines()
        for line in lines:
            if any(k in line.lower() for k in ['expansion', 'fixed edition', 'fallout', 'обновлен', 'скачать', 'ссылка']):
                clean = re.sub(r'<[^>]+>', ' ', line).strip()
                if len(clean) > 20 and len(clean) < 300:
                    print("Text:", clean)
except Exception as e:
    print("Error:", e)
