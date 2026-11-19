import urllib.request
import re

url = 'https://drive.google.com/file/d/1d0EmOcBwH7zEgnPgzEhdpYXC3DiL67QE/view?usp=sharing'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print("GDrive HTML length:", len(content))
        with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/gdrive_page.html', 'w', encoding='utf-8') as f:
            f.write(content)
        # Check title
        title = re.search(r'<title>(.*?)</title>', content)
        if title:
            print("Title:", title.group(1))
except Exception as e:
    print("Error:", e)
