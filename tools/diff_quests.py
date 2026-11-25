from audit_maps_quests import extract_file, base
import os

rpu_q = extract_file(os.path.join(base, "rpu.dat"), "data/quests.txt").decode('ascii', errors='replace').splitlines()
ecco_q = extract_file(os.path.join(base, "rpu_y_ecco.dat"), "data/quests.txt").decode('ascii', errors='replace').splitlines()

def get_quest_sections(lines):
    secs = set()
    for l in lines:
        l = l.strip()
        if l.startswith("[") and l.endswith("]"):
            secs.add(l)
    return secs

sq_rpu = get_quest_sections(rpu_q)
sq_ecco = get_quest_sections(ecco_q)

print(f"Quests in RPU: {len(sq_rpu)} | Quests in EcCo: {len(sq_ecco)}")
missing = sq_rpu - sq_ecco
print(f"Missing in EcCo: {len(missing)}")
added = sq_ecco - sq_rpu
print(f"Added in EcCo: {len(added)}")
for a in added:
    print("  Added:", a)
