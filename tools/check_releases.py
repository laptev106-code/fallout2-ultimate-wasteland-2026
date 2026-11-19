import urllib.request
import json
import sys

headers = {'User-Agent': 'Mozilla/5.0'}

def check_gh(repo):
    url = f'https://api.github.com/repos/{repo}/releases'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            print(f'=== {repo} releases ===')
            for rel in data[:3]:
                print(f"Tag: {rel.get('tag_name')}, Name: {rel.get('name')}")
                for a in rel.get('assets', []):
                    print(f"  Asset: {a.get('name')} ({a.get('size')} bytes) -> {a.get('browser_download_url')}")
    except Exception as e:
        print(f'{repo}: {e}')

if __name__ == '__main__':
    repos = [
        'BGforgeNet/Fallout2_Restoration_Project',
        'BGforgeNet/fo2tweaks',
        'sfall-team/sfall',
        'phobos2077/fo2_tweaks',
        'Fakels/sfall-mods'
    ]
    for r in repos:
        check_gh(r)
