from audit_maps_quests import extract_file, base
import os

rpu_maps = extract_file(os.path.join(base, "rpu.dat"), "data/maps.txt").decode('ascii', errors='replace')
ecco_maps = extract_file(os.path.join(base, "rpu_y_ecco.dat"), "data/maps.txt").decode('ascii', errors='replace')

def get_map_sections(text):
    secs = set()
    for l in text.splitlines():
        l = l.strip()
        if l.startswith("[Map ") and l.endswith("]"):
            secs.add(l)
    return secs

s_rpu = get_map_sections(rpu_maps)
s_ecco = get_map_sections(ecco_maps)

print(f"Maps in RPU: {len(s_rpu)} | Maps in EcCo: {len(s_ecco)}")
missing_in_ecco = s_rpu - s_ecco
print(f"Maps present in RPU but missing in EcCo: {len(missing_in_ecco)}")
for m in missing_in_ecco:
    print("  Missing:", m)

added_in_ecco = s_ecco - s_rpu
print(f"Maps added by EcCo: {len(added_in_ecco)}")
for m in added_in_ecco:
    print("  Added:", m)
