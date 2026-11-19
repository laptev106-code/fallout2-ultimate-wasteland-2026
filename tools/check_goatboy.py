import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def list_user(u):
    url = f'https://api.github.com/users/{u}/repos'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            repos = json.loads(r.read())
            print(f'=== Repos for {u} ===')
            for r in repos:
                print(f"  {r.get('name')}: {r.get('description')} ({r.get('html_url')})")
    except Exception as e:
        print(f"Error {u}: {e}")

if __name__ == '__main__':
    list_user('GoatBoy-11')
    list_user('GoatBoy11')
