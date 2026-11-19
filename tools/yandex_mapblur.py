import urllib.request
import urllib.parse
import re

url = "https://ya.ru/search/?text=MapBlurFX+Fallout+2"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        # Find links
        links = re.findall(r'href="([^"]+)"', html)
        interesting = [l for l in links if any(k in l.lower() for k in ['nuclear-city', 'rutracker', 'github', 'mediafire', 'drive.google', 'yadi.sk'])]
        print("Yandex interesting links:", set(interesting[:10]))
        # Snippets
        lines = html.splitlines()
        for line in lines:
            if 'mapblur' in line.lower() or 'foxx' in line.lower():
                clean = re.sub(r'<[^>]+>', ' ', line).strip()
                if len(clean) > 20 and len(clean) < 250:
                    print("Line:", clean)
except Exception as e:
    print("Error:", e)
