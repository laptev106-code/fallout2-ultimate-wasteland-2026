import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def search_gh_repos(q):
    url = f'https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=updated'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            print(f'=== Search: {q} ({data.get("total_count")} results) ===')
            for item in data.get('items', [])[:8]:
                print(f"Repo: {item.get('full_name')} - {item.get('description')}")
                print(f"  URL: {item.get('html_url')}")
    except Exception as e:
        print(f"Error searching {q}: {e}")

if __name__ == '__main__':
    search_gh_repos('fallout 2 talking heads')
    search_gh_repos('fallout2 sfall mods')
    search_gh_repos('fallout 2 "gl_"')
    search_gh_repos('fallout 2 mapblur')
    search_gh_repos('fallout 2 glasses')
