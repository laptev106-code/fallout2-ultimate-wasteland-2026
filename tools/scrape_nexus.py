import urllib.request
import re
import json

url = "https://www.nexusmods.com/fallout2/mods?RH_ModList=nav:true,home:false,type:0,user_id:0,game_id:156,advfilt:true,include_adult:1,page_size:100"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        # Find mod tiles
        # Usually <div class="tile-desc"> or href="/fallout2/mods/<id>"
        links = re.findall(r'href=["\'](/fallout2/mods/(\d+))["\'][^>]*>(.*?)</a>', html, re.DOTALL)
        seen = {}
        for link, mod_id, raw_name in links:
            name = re.sub(r'<[^>]+>', '', raw_name).strip()
            if name and len(name) > 2 and not name.startswith("http") and not name.lower().startswith("view"):
                if mod_id not in seen:
                    seen[mod_id] = {"id": mod_id, "url": f"https://www.nexusmods.com{link}", "name": name}
        
        print(f"Total unique mods parsed: {len(seen)}")
        for mid, data in sorted(seen.items(), key=lambda x: int(x[0])):
            print(f"#{data['id']}: {data['name']}")
except Exception as e:
    print(f"Fetch failed: {e}")
