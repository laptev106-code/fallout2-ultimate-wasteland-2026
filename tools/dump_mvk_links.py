import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
}

req = urllib.request.Request('https://m.vk.com/board174451664', headers=headers)
with urllib.request.urlopen(req, timeout=10) as r:
    raw = r.read().decode('windows-1251', errors='ignore')

with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/mvk_board.html', 'w', encoding='utf-8') as f:
    f.write(raw)

print("Saved mvk_board.html")
# Print all links
links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', raw, re.DOTALL)
print(f"Total links: {len(links)}")
for href, text in links:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if clean_text or 'topic' in href:
        print(f"  {href} -> {clean_text[:60]}")
