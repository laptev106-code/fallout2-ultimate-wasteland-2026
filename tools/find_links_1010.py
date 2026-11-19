import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'https://nuclear-city.com/index.php/topic/1010-fallout-2-rp-fixed-edition/'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Extract links inside post
links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>(.*?)</a>', html, re.I)
for href, text in links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if any(k in href.lower() or k in clean_text.lower() for k in ['изменен', 'changelog', 'история', 'яндекс', 'drive', 'mediafire', 'мод', 'выжив', 'txt']):
        print(f"Text: '{clean_text}' -> URL: {href}")
