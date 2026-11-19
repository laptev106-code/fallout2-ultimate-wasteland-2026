import urllib.request
import re

url = "https://app.mediafire.com/5iciiinoqizc9"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Mediafire length:", len(html))
        # Search for files
        files = re.findall(r'href="([^"]+mediafire\.com/file/[^"]+)"', html)
        print("Files found:", set(files))
        # Search for filenames
        names = re.findall(r'class="filename"[^>]*>([^<]+)<', html)
        print("Names found:", names)
except Exception as e:
    print("Error:", e)
