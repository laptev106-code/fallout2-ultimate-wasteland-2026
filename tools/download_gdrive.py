import urllib.request
import re

file_id = '1d0EmOcBwH7zEgnPgzEhdpYXC3DiL67QE'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read()
        print("Downloaded bytes:", len(content))
        # Try decoding
        for enc in ['utf-8', 'windows-1251', 'cp866']:
            try:
                text = content.decode(enc)
                print(f"Decoded with {enc}, first 500 chars:")
                print(text[:500])
                with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/foxx_changelog.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                print("Saved to tools/foxx_changelog.txt successfully!")
                break
            except UnicodeDecodeError:
                pass
except Exception as e:
    print("Download error:", e)
