import urllib.request
import re

url = 'https://www.nuclear-city.com/topic/560-fallout-2-rp-fixed-edition/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Page length:", len(html))
        
        # Search for .txt links or pastebin links or yandex disk
        txts = re.findall(r'https?://[^\s"\'<>]+\.(?:txt|log)[^\s"\'<>]*', html)
        print("TXT/LOG links:", txts)
        
        # Search for links
        links = re.findall(r'href="(https?://[^"]+)"', html)
        interesting = [l for l in links if any(k in l.lower() for k in ['vk.com', 'pastebin', 'yadi.sk', 'drive.google', 'cloud.mail', 'dropbox', 'github', 'txt', 'mediafire'])]
        print("Interesting links:", set(interesting))
        
        # Find spoilers / changelog in first post
        spoilers = re.findall(r'<div class=[\'"]ipsSpoiler_contents[\'"][^>]*>(.*?)</div>', html, re.DOTALL)
        print(f"Spoilers found: {len(spoilers)}")
        for i, s in enumerate(spoilers[:5]):
            clean = re.sub(r'<[^>]+>', ' ', s)
            clean = re.sub(r'\s+', ' ', clean).strip()
            print(f"--- Spoiler {i} (len {len(clean)}):")
            print(clean[:400])
except Exception as e:
    print("Error:", e)
