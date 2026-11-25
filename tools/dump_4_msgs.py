import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"

def main():
    foxx_files = read_dat2_directory(FOXX_MASTER)
    for name in ["dcliljny.msg", "dcljfthr.msg", "wstrpwr.msg", "zclvillrat.msg"]:
        key = f"text\\english\\dialog\\{name}"
        data = extract_dat2_file(foxx_files[key]).decode("cp1251", errors="replace")
        print(f"==================== {name} ====================")
        print(data)

if __name__ == "__main__":
    main()
