import json

with open(r'd:\AG games mods\nexus_tab_files.json', 'r', encoding='utf-16', errors='ignore') as f:
    text = f.read()

data = json.loads(text)
obs = data['text']
lines = obs.splitlines()
for i, line in enumerate(lines):
    if any(k in line for k in ['RPU - Talking Heads Addon', 'RPU 2.4.34', 'Manual']):
        print(f"--- Hit at line {i}: {line} ---")
        for j in range(max(0, i-3), min(len(lines), i+8)):
            print(f"  [{j}] {lines[j]}")
