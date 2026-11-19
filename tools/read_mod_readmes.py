import urllib.request
import base64
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def get_file(repo, path):
    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            print(f'=== {repo}/{path} ===')
            print(content)
    except Exception as e:
        print(f"Error {path}: {e}")

if __name__ == '__main__':
    get_file('rotators/fallout-mods', 'fo2_footprints/Readme.md')
    get_file('rotators/fallout-mods', 'fo2_interface_upscaled.dat/README.md')
    get_file('rotators/fallout-mods', 'fo2_pip_timers.dat/Readme.md')
