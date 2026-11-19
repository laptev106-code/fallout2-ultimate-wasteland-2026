import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}
for q in ["talking-heads fallout", "armored talking heads", "gl_footsteps", "MapBlurFX"]:
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Query: '{q}' -> {len(data.get('items', []))} results")
            for r in data.get('items', [])[:3]:
                print(" ", r.get('full_name'), "->", r.get('html_url'))
    except Exception as e:
        print("Error for", q, ":", e)
