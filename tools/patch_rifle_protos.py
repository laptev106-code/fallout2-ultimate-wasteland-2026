from audit_weapon_anim_collision import extract_file, base
import os

target_pids = [
    ("proto/items/00000011.pro", "Hunting Rifle"),
    ("proto/items/00000351.pro", "Red Ryder LE"),
    ("proto/items/00000500.pro", "Scoped Hunting Rifle"),
]

for pro_rel, name in target_pids:
    ecco_bytes = bytearray(extract_file(os.path.join(base, "rpu_y_ecco.dat"), pro_rel))
    print(f"Patching {name} ({pro_rel}): old anim byte = {hex(ecco_bytes[0x3c])}")
    # Set anim code to 0x0D (RPU rifle custom anim)
    ecco_bytes[0x3c] = 0x0D
    print(f"  New anim byte = {hex(ecco_bytes[0x3c])}")
    
    # Save to both profiles
    for prof in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD"]:
        out_f = os.path.join(prof, "mods", "rpu_russian_uncensored.dat", pro_rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(out_f), exist_ok=True)
        with open(out_f, "wb") as f:
            f.write(ecco_bytes)
        print(f"  Saved to {out_f}")
        
    # Save to workspace
    ws_f = os.path.join(r"E:\FALLOUT Ult pjt", pro_rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(ws_f), exist_ok=True)
    with open(ws_f, "wb") as f:
        f.write(ecco_bytes)
    print(f"  Saved to workspace: {ws_f}")

print("All 3 rifle prototypes merged and patched successfully!")
