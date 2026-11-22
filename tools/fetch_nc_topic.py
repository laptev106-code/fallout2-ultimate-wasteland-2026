import urllib.request
import re

url = "https://nuclear-city.com/index.php?showtopic=1795"
req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('windows-1251', errors='ignore')
        # Find all external links
        links = re.findall(r'href=[\'"](https?://[^\'"]+)[\'"]', html)
        print("Page fetched! Found links:")
        for l in links:
            if any(k in l.lower() for k in ["yadi", "yandex", "drive", "mega", "mediafire", "github"]):
                print(" ", l)
except Exception as e:
    print("Error:", e)
