import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"

def main():
    foxx_files = read_dat2_directory(FOXX_MASTER)
    
    # Check all scripts containing 0x0014 (PID 20 = Crowbar) or string related to crowbar
    matches = []
    for k, info in foxx_files.items():
        if k.startswith("scripts\\") and k.endswith(".int"):
            data = extract_dat2_file(info)
            # Check for PID 20 in bytecode
            # In SSL/sfall bytecode: push int 20 or similar, or string
            if b"crowbar" in data.lower() or b"alesis" in data.lower():
                matches.append((k, "string match"))
            # Check if any text/msg mentions crowbar
        elif k.startswith("text\\") and k.endswith(".msg"):
            data = extract_dat2_file(info)
            if b"alesis" in data.lower():
                matches.append((k, "alesis in msg"))

    print(f"Total matches: {len(matches)}")
    for m in matches:
        print(" ", m)

if __name__ == "__main__":
    main()
