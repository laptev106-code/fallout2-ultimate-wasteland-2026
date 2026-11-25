from audit_weapon_anim_collision import extract_file, base
import os

for fname in ["data/aibdymsg.txt", "data/aigenmsg.txt"]:
    data = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), fname)
    for prof in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD"]:
        out = os.path.join(prof, "mods", "rpu_russian_uncensored.dat", fname.replace('/', os.sep))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as f:
            f.write(data)
        print(f"Saved: {out}")
    ws_out = os.path.join(r"E:\FALLOUT Ult pjt", fname.replace('/', os.sep))
    os.makedirs(os.path.dirname(ws_out), exist_ok=True)
    with open(ws_out, "wb") as f:
        f.write(data)
    print(f"Saved to workspace: {ws_out}")
