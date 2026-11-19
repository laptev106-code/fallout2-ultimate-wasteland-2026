import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://api.github.com/users/Mr-Stalin/repos"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        repos = json.loads(resp.read().decode('utf-8'))
        print("Mr-Stalin repos:")
        for r in repos:
            print(" ", r.get('name'), "->", r.get('html_url'))
except Exception as e:
    print("User Mr-Stalin error:", e)

# Also check sfall repository
url2 = "https://api.github.com/search/repositories?q=sfall"
try:
    req2 = urllib.request.Request(url2, headers=headers)
    with urllib.request.urlopen(req2, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("sfall repos:")
        for r in data.get('items', [])[:6]:
            print(" ", r.get('full_name'), "->", r.get('html_url'))
except Exception as e:
    print("sfall search error:", e)
