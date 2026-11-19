import os

base_game = "E:/Fallout2_Ultimate/Fallout2_Gameplay"
mods_dir = os.path.join(base_game, "mods")

print("Checking mods directory:")
if os.path.exists(mods_dir):
    for f in os.listdir(mods_dir):
        print(" ", f)

# Check if Glasses mod or AleSiS fixes exist in rpu.dat
print("\nChecking key ini configs:")
for ini_name in ["sfall-mods.ini", "rpu.ini", "upu.ini", "ddraw.ini"]:
    p = os.path.join(base_game, ini_name)
    if not os.path.exists(p):
        p = os.path.join(mods_dir, ini_name)
    if os.path.exists(p):
        print(f"Found {ini_name} at {p}")
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [l.strip() for l in f if any(k in l.lower() for k in ['glasses', 'inventory', 'blur', 'timelimit', 'year', 'torr'])]
            for l in lines[:10]:
                print(f"  {l}")
