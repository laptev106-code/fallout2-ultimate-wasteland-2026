import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory

def main():
    p = r"E:\Games\Fallout 2 (Expansion Version)\mods\DB_Cassidy_Voice.dat"
    d = read_dat2_directory(p)
    cas_folders = set()
    for k in d:
        parts = k.split("\\")
        if len(parts) >= 3:
            cas_folders.add(parts[2])
    print("Cassidy voice folders in DB_Cassidy_Voice.dat:")
    for f in sorted(cas_folders):
        count = sum(1 for k in d if k.startswith(f"sound\\speech\\{f}\\"))
        print(f"  {f}: {count} files")

if __name__ == "__main__":
    main()
