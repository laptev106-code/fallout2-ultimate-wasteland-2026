from audit_maps_quests import extract_file, base
import os

for d in ["rpu_russian_uncensored.dat", "talking_heads_that_rpu_map_update_patch.dat", "talking_heads.dat", "rpu.dat"]:
    p = os.path.join(base, d)
    if os.path.isfile(p):
        data = extract_file(p, "scripts/kctorr.int")
        if data:
            print(f"Found scripts/kctorr.int in {d}: {len(data)} bytes")
    elif os.path.isdir(p):
        f = os.path.join(p, "scripts", "kctorr.int")
        if os.path.isfile(f):
            print(f"Found scripts/kctorr.int in folder {d}: {os.path.getsize(f)} bytes")
