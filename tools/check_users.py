import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def list_user_repos(user):
    url = f'https://api.github.com/users/{user}/repos?per_page=100'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            repos = json.loads(r.read())
            print(f'=== Repos for {user} ({len(repos)}) ===')
            for repo in repos:
                name = repo.get('name')
                desc = repo.get('description') or ''
                stars = repo.get('stargazers_count', 0)
                if any(k in name.lower() or k in desc.lower() for k in ['fallout', 'sfall', 'mod', 'head', 'tweak', 'rpu', 'f2']):
                    print(f"  {name}: {desc} (stars: {stars})")
    except Exception as e:
        print(f"Error {user}: {e}")

if __name__ == '__main__':
    users = ['BGforgeNet', 'rotators', 'phobos2077', 'sfall-team', 'Fakels']
    for u in users:
        list_user_repos(u)
