import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
OUR_RPU = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"

def main():
    foxx_files = read_dat2_directory(FOXX_MASTER)
    rpu_files = read_dat2_directory(OUR_RPU)

    for msg in ["text\\english\\dialog\\vilrat.msg", "text\\english\\dialog\\ectravlr.msg"]:
        key = msg.lower()
        foxx_txt = extract_dat2_file(foxx_files[key]).decode("latin-1", errors="replace")
        our_txt = extract_dat2_file(rpu_files[key]).decode("latin-1", errors="replace")
        print(f"=== {msg} ===")
        print("--- Foxx ---")
        print(foxx_txt[:300])
        print("--- Our RPU ---")
        print(our_txt[:300])

        foxx_lines = set(foxx_txt.splitlines())
        our_lines = set(our_txt.splitlines())
        print(f"Foxx only lines: {foxx_lines - our_lines}")
        print(f"Our RPU only lines: {our_lines - foxx_lines}")

if __name__ == "__main__":
    main()
