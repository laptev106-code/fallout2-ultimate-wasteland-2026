import urllib.request
import zipfile
import os

url = "https://github.com/BGforgeNet/FO2tweaks/releases/download/v15.0/fo2tweaks_v15.0.zip"
out_zip = "d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/fo2tweaks_v15.0.zip"
out_dir = "d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/fo2tweaks_v15"

headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()
    with open(out_zip, 'wb') as f:
        f.write(data)
    print("Downloaded bytes:", len(data))

with zipfile.ZipFile(out_zip, 'r') as z:
    z.extractall(out_dir)
    print("Extracted files:")
    for n in z.namelist():
        print(" ", n)

ini_path = os.path.join(out_dir, "mods", "fo2tweaks.ini")
if os.path.exists(ini_path):
    with open(ini_path, 'r', encoding='utf-8', errors='ignore') as f:
        print("\nSections in v15.0 fo2tweaks.ini:")
        for l in f:
            if l.startswith('['):
                print(" ", l.strip())
