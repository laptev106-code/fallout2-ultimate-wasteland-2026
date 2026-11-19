import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/search/repositories?q=fallout2+talking+heads"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Talking heads repos:")
        for r in data.get('items', [])[:10]:
            print(" ", r.get('full_name'), "->", r.get('html_url'), f"({r.get('stargazers_count')} stars)")
except Exception as e:
    print("Error:", e)
