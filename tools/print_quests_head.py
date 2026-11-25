from audit_maps_quests import extract_file, base
import os

rpu_q = extract_file(os.path.join(base, "rpu.dat"), "data/quests.txt").decode('ascii', errors='replace').splitlines()
print("\n".join(rpu_q[:25]))
