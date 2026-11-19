import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/repos/BGforgeNet/Fallout2_Restoration_Project/contents/tools"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        items = json.loads(resp.read().decode('utf-8'))
        print("Tools in RPU repo:")
        for it in items:
            print(" ", it.get('name'), "->", it.get('download_url'))
except Exception as e:
    print("Error:", e)
