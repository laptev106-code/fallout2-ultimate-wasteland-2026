import os
import re

ai_path = r"mods\rpu_russian_uncensored.dat\data\ai.txt"
with open(ai_path, "r", encoding="latin-1") as f:
    text = f.read()

companion_sections = []
for m in re.finditer(r"\[(PARTY [^\]]+)\](.*?)(?=\n\[|\Z)", text, re.S):
    sec_name = m.group(1)
    body = m.group(2)
    burst = "not_set"
    best_wep = "not_set"
    run_away = "not_set"
    chem = "not_set"
    dist = "not_set"
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("area_attack_mode="):
            burst = line.split("=")[1]
        elif line.startswith("best_weapon="):
            best_wep = line.split("=")[1]
        elif line.startswith("run_away_mode="):
            run_away = line.split("=")[1]
        elif line.startswith("chem_use="):
            chem = line.split("=")[1]
        elif line.startswith("distance="):
            dist = line.split("=")[1]
    companion_sections.append((sec_name, burst, best_wep, run_away, chem, dist))

print(f"Total PARTY AI sections: {len(companion_sections)}")
for s, b, w, r, c, d in companion_sections:
    print(f"{s:<30} | burst: {b:<15} | wep: {w:<22} | dist: {d}")
