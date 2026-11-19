import urllib.request
import re

url = 'https://vk.com/wall-174451664_10479'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    print("Content-Type:", resp.headers.get('Content-Type'))
    raw = resp.read()

# Save raw bytes to file
with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/wall_10479.html', 'wb') as f:
    f.write(raw)

print("Saved raw bytes:", len(raw))

# Let's inspect decoding
for enc in ['windows-1251', 'utf-8']:
    try:
        txt = raw.decode(enc)
        print(f"Decoded {enc} successfully, length: {len(txt)}")
        # search for Fallout
        matches = [m.start() for m in re.finditer('Fallout 2', txt)]
        print(f"Matches for 'Fallout 2': {len(matches)}")
        if matches:
            for m in matches[:3]:
                snippet = txt[max(0, m-50):min(len(txt), m+300)]
                clean = re.sub(r'<[^>]+>', ' ', snippet)
                print(f"[{m}]:", re.sub(r'\s+', ' ', clean))
    except Exception as e:
        print(f"{enc} failed:", e)
