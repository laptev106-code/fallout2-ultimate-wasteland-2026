import urllib.request
import re

url = 'https://m.vk.com/rebuild_by_foxx'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/m_vk_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    links = set(re.findall(r'https?://[^\s\"\'<>]+', html))
    print(f"Total links found: {len(links)}")
    for l in sorted(links):
        if any(k in l.lower() for k in ['drive', 'yadi', 'mail.ru', 'rutracker', 'topic', 'wall', 'doc', 'mediafire']):
            print("FOUND LINK:", l)
except Exception as e:
    print("Error:", e)

