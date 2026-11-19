import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def check_repo_releases_and_contents(repo):
    # Releases
    url_rel = f'https://api.github.com/repos/{repo}/releases'
    try:
        req = urllib.request.Request(url_rel, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            rels = json.loads(r.read())
            print(f'=== Releases for {repo} ({len(rels)}) ===')
            for rel in rels[:5]:
                print(f"Tag: {rel.get('tag_name')}, Name: {rel.get('name')}")
                for a in rel.get('assets', []):
                    print(f"  Asset: {a.get('name')} ({a.get('size')} bytes) -> {a.get('browser_download_url')}")
    except Exception as e:
        print(f"Error releases {repo}: {e}")

    # Root contents
    url_cnt = f'https://api.github.com/repos/{repo}/contents'
    try:
        req = urllib.request.Request(url_cnt, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            cnt = json.loads(r.read())
            print(f'=== Root contents of {repo} ===')
            for c in cnt:
                print(f"  [{c.get('type')}] {c.get('name')} ({c.get('size')} bytes)")
    except Exception as e:
        print(f"Error contents {repo}: {e}")

if __name__ == '__main__':
    check_repo_releases_and_contents('GoatBoy-11/Fallout2_Restoration_Project_Talking_Heads_Addon')
