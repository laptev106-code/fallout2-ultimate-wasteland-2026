import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/repos/sfall-team/sfall/releases"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        releases = json.loads(resp.read().decode('utf-8'))
        print(f"Total releases: {len(releases)}")
        for r in releases[:5]:
            print("--- Release:", r.get('tag_name'), r.get('name'))
            for a in r.get('assets', []):
                print(f"    Asset: {a.get('name')} ({a.get('size')} bytes) -> {a.get('browser_download_url')}")
except Exception as e:
    print("Error:", e)
