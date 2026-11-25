from audit_maps_quests import extract_file, base
import os

dats = ["rpu.dat", "rpu_russian.dat", "rpu_y_ecco.dat", "master.dat"]
for d in dats:
    full = os.path.join(base, d) if d != "master.dat" else r"E:\Fallout2_Ultimate\Fallout2_Gameplay\master.dat"
    for path in ["text/english/game/quests.msg", "text/russian/game/quests.msg"]:
        data = extract_file(full, path)
        if data:
            print(f"Found {path} in {d} ({len(data)} bytes)")
