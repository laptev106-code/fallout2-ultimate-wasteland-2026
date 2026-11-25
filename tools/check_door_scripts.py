import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
OUR_RPU = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"

def main():
    foxx_files = read_dat2_directory(FOXX_MASTER)
    rpu_files = read_dat2_directory(OUR_RPU)

    for name in ["scripts\\ziwoddor.int", "scripts\\zimtldor.int", "scripts\\zilckdor.int",
                 "text\\english\\dialog\\ziwoddor.msg", "text\\english\\dialog\\zimtldor.msg"]:
        key = name.lower()
        if key in foxx_files and key in rpu_files:
            f_data = extract_dat2_file(foxx_files[key])
            r_data = extract_dat2_file(rpu_files[key])
            if f_data == r_data:
                print(f"[=] {name}: Identical ({len(f_data)} bytes)")
            else:
                print(f"[!] {name}: DIFFERENT! Foxx={len(f_data)} vs RPU={len(r_data)}")
        else:
            print(f"[-] {name}: not in both")

if __name__ == "__main__":
    main()
