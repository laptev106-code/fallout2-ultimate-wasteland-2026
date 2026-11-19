import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/repos/sfall-team/sfall/releases/tags/v4.5.1"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        r = json.loads(resp.read().decode('utf-8'))
        print("Release 4.5.1 assets:")
        for a in r.get('assets', []):
            print(f" {a.get('name')} ({a.get('size')} bytes) -> {a.get('browser_download_url')}")
except Exception as e:
    print("Error:", e)
