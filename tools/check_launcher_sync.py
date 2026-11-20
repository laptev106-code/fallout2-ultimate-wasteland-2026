import os
import re

app_js = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\app.js"
mods_js = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\js\mods_data.js"
index_html = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\index.html"

with open(app_js, "r", encoding="utf-8") as f:
    c_app = f.read()

ids_app = re.findall(r'id:\s*"([^"]+)"', c_app)
print(f"app.js has {len(ids_app)} mods: {ids_app}")

if os.path.exists(mods_js):
    with open(mods_js, "r", encoding="utf-8") as f:
        c_mods = f.read()
    ids_mods = re.findall(r'id:\s*"([^"]+)"', c_mods)
    print(f"mods_data.js has {len(ids_mods)} mods: {ids_mods}")
else:
    print("mods_data.js not found")

with open(index_html, "r", encoding="utf-8") as f:
    c_html = f.read()

# Check hardcoded mod counts in index_html
print("Matches in index.html for mod counts:")
for m in re.finditer(r'(\d+)\s*(МОД|МОДУЛ)', c_html):
    print(f"  Line near: {c_html[max(0, m.start()-30):min(len(c_html), m.end()+30)]}")
