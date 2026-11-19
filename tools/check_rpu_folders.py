import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
for folder in ["components", "docs", "extra"]:
    url = f"https://api.github.com/repos/BGforgeNet/Fallout2_Restoration_Project/contents/{folder}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode('utf-8'))
            print(f"=== {folder} ({len(items)}) ===")
            for it in items:
                print(" ", it.get('name'))
    except Exception as e:
        print(f"Error for {folder}: {e}")
