import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
OUR_REPO = r"E:\FALLOUT Ult pjt"
OUR_RPU = r"E:\FALLOUT Ult pjt\mods\rpu.dat"

def get_file_from_vfs(rel_path):
    # Check loose files first
    loose = os.path.join(OUR_REPO, rel_path)
    if os.path.exists(loose):
        with open(loose, "rb") as f:
            return f.read(), f"loose: {loose}"
    
    # Check rpu.dat
    if os.path.exists(OUR_RPU):
        rpu_files = read_dat2_directory(OUR_RPU)
        key = rel_path.lower().replace("/", "\\")
        if key in rpu_files:
            return extract_dat2_file(rpu_files[key]), f"rpu.dat: {key}"
    return None, "not found"

def main():
    print("=" * 70)
    print("  COMPARING FOXX CHANGELOG FIXES AGAINST OUR REPOSITORY")
    print("=" * 70)

    foxx_files = read_dat2_directory(FOXX_MASTER)

    candidates = [
        "scripts\\ecpariah.int",
        "scripts\\scduppo.int",
        "scripts\\epai43.int",
        "scripts\\tribec1.int",
        "scripts\\tribec9.int",
        "maps\\tribe02.map",
        "maps\\raiders1.map",
        "maps\\raiders2.map",
        "text\\english\\dialog\\vilrat.msg",
        "text\\english\\dialog\\ectravlr.msg"
    ]

    for rel in candidates:
        key = rel.lower()
        if key in foxx_files:
            foxx_data = extract_dat2_file(foxx_files[key])
            our_data, source = get_file_from_vfs(rel)
            if our_data is None:
                print(f"[-] {rel}: In Foxx ({len(foxx_data)} bytes), but NOT found in our VFS ({source})")
            elif foxx_data == our_data:
                print(f"[=] {rel}: IDENTICAL ({len(foxx_data)} bytes) with {source}")
            else:
                print(f"[!] {rel}: DIFFERENT! Foxx={len(foxx_data)} bytes vs Ours={len(our_data)} bytes ({source})")
        else:
            print(f"[?] {rel}: Not in Foxx master.dat")

if __name__ == "__main__":
    main()
