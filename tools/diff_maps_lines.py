from audit_maps_quests import extract_file, base
import os

rpu_maps = extract_file(os.path.join(base, "rpu.dat"), "data/maps.txt").decode('ascii', errors='replace').splitlines()
ecco_maps = extract_file(os.path.join(base, "rpu_y_ecco.dat"), "data/maps.txt").decode('ascii', errors='replace').splitlines()

diffs = []
for i in range(min(len(rpu_maps), len(ecco_maps))):
    if rpu_maps[i] != ecco_maps[i]:
        diffs.append((i+1, rpu_maps[i], ecco_maps[i]))

print(f"Total line differences in maps.txt: {len(diffs)}")
for d in diffs[:10]:
    print(f"Line {d[0]}:")
    print(f"  RPU:  {d[1]}")
    print(f"  EcCo: {d[2]}")
