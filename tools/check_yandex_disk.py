import urllib.request
import json
import urllib.parse

def check_yadi(url):
    api = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={urllib.parse.quote(url)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(api, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Name:", data.get('name'))
            print("Type:", data.get('type'))
            if data.get('type') == 'dir':
                items = data.get('_embedded', {}).get('items', [])
                print(f"Items in folder ({len(items)}):")
                for it in items:
                    print(f"  {it.get('name')} ({it.get('size')} bytes) -> {it.get('file')}")
            else:
                print("Direct file download url:", data.get('file'))
    except Exception as e:
        print(f"Error for {url}: {e}")

print("Checking Yandex Disk 1:")
check_yadi('https://yadi.sk/d/Qw3rwUc4wmYaK')
print("\nChecking Yandex Disk 2:")
check_yadi('https://yadi.sk/d/nqjcrgQFqfDgU')
