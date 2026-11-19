import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def check_contents(repo, path=''):
    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            items = json.loads(r.read())
            print(f'=== {repo}/{path} ===')
            for it in items:
                print(f"  [{it.get('type')}] {it.get('name')} ({it.get('size')} bytes)")
    except Exception as e:
        print(f"Error {repo}/{path}: {e}")

if __name__ == '__main__':
    check_contents('rotators/fallout-mods')
    check_contents('rotators/fallout-animations')
    check_contents('BGforgeNet/f2rp-walkthrough')
