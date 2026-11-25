import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"

def main():
    foxx_files = read_dat2_directory(FOXX_MASTER)
    speech_folders = set()
    for k in foxx_files:
        if k.startswith("sound\\speech\\"):
            parts = k.split("\\")
            if len(parts) >= 3:
                speech_folders.add(parts[2])

    print("=== VOICED TALKING HEAD FOLDERS IN FOXX ===")
    for sf in sorted(speech_folders):
        count = sum(1 for k in foxx_files if k.startswith(f"sound\\speech\\{sf}\\"))
        print(f"  {sf}: {count} files")

if __name__ == "__main__":
    main()
