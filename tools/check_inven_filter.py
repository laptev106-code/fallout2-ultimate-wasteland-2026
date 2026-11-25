import os

path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\InventoryFilter.dat\InvenFilter.ini"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
else:
    print("InvenFilter.ini not found")
