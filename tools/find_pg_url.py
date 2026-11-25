import urllib.request
import re

url = "https://www.playground.ru/fallout_2/file/fallout_2_russkij_perevod_moda_restoration_project_companion_expansion-1772439"
# Let's search Playground for the exact file ID
req = urllib.request.Request(
    "https://www.playground.ru/fallout_2/file?q=Companion+Expansion",
    headers={"User-Agent": "Mozilla/5.0"}
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'href="(/fallout_2/file/[^"]+)"[^>]*>([^<]+)<', html)
        print("Matches found on Playground:")
        for m in matches:
            print(" ", m)
except Exception as e:
    print("Error:", e)
