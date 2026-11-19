import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/users/BGforgeNet/repos?per_page=100"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
        print(f"BGforgeNet repos ({len(repos)}):")
        for r in repos:
            name = r.get('name')
            if any(k in name.lower() for k in ['fallout', 'rpu', 'upu', 'head', 'mod', 'tweak', 'sound', 'talking']):
                print(f"  {name} -> {r.get('html_url')} (stars: {r.get('stargazers_count')})")
except Exception as e:
    print("Error:", e)
