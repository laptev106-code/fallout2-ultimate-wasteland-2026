from audit_weapon_anim_collision import extract_file, base
import os

pids = [
    ("proto/items/00000011.pro", "Hunting Rifle"),
    ("proto/items/00000143.pro", "Sniper Rifle"),
    ("proto/items/00000287.pro", "Pipe Rifle"),
    ("proto/items/00000351.pro", "Red Ryder LE"),
    ("proto/items/00000403.pro", "Gauss Rifle"),
    ("proto/items/00000500.pro", "Scoped Hunting Rifle"),
]

for pro_path, name in pids:
    p_anim = extract_file(os.path.join(base, "rpu_rifle_animations.dat"), pro_path)
    p_ecco = extract_file(os.path.join(base, "rpu_y_ecco.dat"), pro_path)
    print(f"{name:20}: AnimMod[0x3c]={hex(p_anim[0x3c])} | EcCo[0x3c]={hex(p_ecco[0x3c])}")
