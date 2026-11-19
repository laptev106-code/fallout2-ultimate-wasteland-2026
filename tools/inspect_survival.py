import configparser
import os

gameplay_mods = "E:/Fallout2_Ultimate/Fallout2_Gameplay/mods"
for f in ["fo2tweaks.ini", "F2MechanicsMiniRework.ini", "sfall-mods.ini", "rpu.ini"]:
    p = os.path.join(gameplay_mods, f)
    if os.path.exists(p):
        print(f"\n=== {f} ===")
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            for l in fp:
                l = l.strip()
                if l.startswith('[') or any(k in l.lower() for k in ['survival', 'hunger', 'thirst', 'sleep', 'fatigue', 'craft', 'cook', 'skin', 'meat', 'ration']):
                    print(" ", l)
