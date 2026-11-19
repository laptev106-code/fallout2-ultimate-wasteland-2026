import json
import re

with open(r'd:\AG games mods\nexus_tab_files.json', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Try json or regex
try:
    data = json.loads(text)
    obs_text = data.get('text', '')
    print("Obs length:", len(obs_text))
    for line in obs_text.splitlines():
        if any(k in line.lower() for k in ['manual', 'download', 'rpu', 'talking heads', 'file', 'version']):
            print(line)
except Exception as e:
    print("Error parsing json:", e)
    for line in text.splitlines():
        if any(k in line.lower() for k in ['manual', 'download', 'rpu', 'talking heads', 'file', 'version']):
            print(line[:120])
