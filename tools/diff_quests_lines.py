from audit_maps_quests import extract_file, base
import os

rpu_q = extract_file(os.path.join(base, "rpu.dat"), "data/quests.txt").decode('ascii', errors='replace').splitlines()
ecco_q = extract_file(os.path.join(base, "rpu_y_ecco.dat"), "data/quests.txt").decode('ascii', errors='replace').splitlines()

rpu_entries = [l.strip() for l in rpu_q if l.strip() and not l.strip().startswith("#")]
ecco_entries = [l.strip() for l in ecco_q if l.strip() and not l.strip().startswith("#")]

print(f"Active quest lines: RPU={len(rpu_entries)} | EcCo={len(ecco_entries)}")

diff_ecco = [l for l in ecco_entries if l not in rpu_entries]
print(f"Added in EcCo: {len(diff_ecco)}")
for d in diff_ecco:
    print("  +", d)

diff_rpu = [l for l in rpu_entries if l not in ecco_entries]
print(f"Missing in EcCo from RPU: {len(diff_rpu)}")
for d in diff_rpu:
    print("  -", d)
