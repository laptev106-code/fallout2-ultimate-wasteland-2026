from audit_weapon_anim_collision import extract_file, base
import os

w_anim = extract_file(os.path.join(base, "rpu_wakizashi_animations.dat"), "proto/items/00000522.pro")
w_ecco = extract_file(os.path.join(base, "rpu_y_ecco.dat"), "proto/items/00000522.pro")

print("Wakizashi Anim Mod:", [hex(b) for b in w_anim[0x30:0x48]])
print("Wakizashi EcCo Mod:", [hex(b) for b in w_ecco[0x30:0x48]])
