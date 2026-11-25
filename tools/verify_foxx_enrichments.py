import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
FOXX_CASSIDY = r"E:\Games\Fallout 2 (Expansion Version)\mods\DB_Cassidy_Voice.dat"

def main():
    fm = read_dat2_directory(FOXX_MASTER)
    fc = read_dat2_directory(FOXX_CASSIDY)

    # Heads:
    heads = [k for k in fm if k.startswith("art\\heads\\cas") and k.endswith(".frm")]
    print(f"Cassidy armored heads in master.dat: {len(heads)} files")

    # Cursors:
    cursors = [k for k in fm if k.startswith("art\\intrface\\curs") and k.endswith(".frm")]
    print(f"Skill cursors in master.dat: {len(cursors)} files")

    # Sulik speech:
    sul_speech = [k for k in fm if any(k.startswith(f"sound\\speech\\{x}\\") for x in ['sulap', 'sulca', 'sulla', 'sullj', 'sulma', 'sulpa', 'sulro'])]
    print(f"Sulik armored speech in master.dat: {len(sul_speech)} files")

    # Myron speech:
    myr_speech = [k for k in fm if any(k.startswith(f"sound\\speech\\{x}\\") for x in ['myrap', 'myrca', 'myrpa', 'myrro'])]
    print(f"Myron armored speech in master.dat: {len(myr_speech)} files")

    # Cassidy speech:
    cas_speech = [k for k in fc if any(k.startswith(f"sound\\speech\\{x}\\") for x in ['casap', 'casca', 'caslj', 'casma', 'caspa', 'casro'])]
    print(f"Cassidy armored speech in DB_Cassidy_Voice.dat: {len(cas_speech)} files")

if __name__ == "__main__":
    main()
