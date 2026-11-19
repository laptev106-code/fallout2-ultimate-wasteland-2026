import urllib.request
import json

url = 'https://api.github.com/repos/sfall-team/sfall/releases/latest'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    rel = json.loads(r.read())
    print('Tag:', rel['tag_name'])
    for a in rel.get('assets', []):
        print(f"{a['name']}: {a['size']} bytes -> {a['browser_download_url']}")
