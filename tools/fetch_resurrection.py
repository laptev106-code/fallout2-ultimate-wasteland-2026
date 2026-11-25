import urllib.request
import re

url = 'https://resurrection.cz/en/download/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
    links = re.findall(r'href=[\"\']([^\"\']+)[\"\']', html)
    print("Found links on resurrection.cz:")
    for l in links:
        if any(ext in l.lower() for ext in ['.exe', '.zip', '.rar', '.7z', '.dat', 'patch']):
            print(" ->", l)
except Exception as e:
    print("Error:", e)
