import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory

FOXX_DIR = r"E:\Games\Fallout 2 (Expansion Version)"

def check_docs():
    docs_dir = os.path.join(FOXX_DIR, "!docs")
    if os.path.exists(docs_dir):
        print("\n=== !DOCS IN FOXX ===")
        for f in os.listdir(docs_dir):
            p = os.path.join(docs_dir, f)
            print(f"  {f} ({os.path.getsize(p):,} bytes)")

def check_shaders():
    print("\n=== SHADERS IN FOXX ===")
    for root, dirs, files in os.walk(FOXX_DIR):
        for f in files:
            if f.endswith(".fx"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, FOXX_DIR)
                print(f"  {rel} ({os.path.getsize(p):,} bytes)")

def check_mods_dats():
    print("\n=== MODS DATS IN FOXX ===")
    mods_dir = os.path.join(FOXX_DIR, "mods")
    for f in os.listdir(mods_dir):
        p = os.path.join(mods_dir, f)
        if os.path.isfile(p) and f.endswith(".dat"):
            d = read_dat2_directory(p)
            print(f"  {f}: {os.path.getsize(p):,} bytes, {len(d)} files")
            for k in list(d.keys())[:5]:
                print(f"    - {k}")

def check_sfall_scripts():
    print("\n=== SFALL SCRIPTS IN FOXX ===")
    sfall_dir = os.path.join(FOXX_DIR, "sFall", "scripts")
    if os.path.exists(sfall_dir):
        for f in os.listdir(sfall_dir):
            p = os.path.join(sfall_dir, f)
            print(f"  {f} ({os.path.getsize(p):,} bytes)")

def check_worldmap_dat():
    p = os.path.join(FOXX_DIR, "data", "worldmap.dat")
    if os.path.exists(p):
        print(f"\n=== data/worldmap.dat ({os.path.getsize(p):,} bytes) ===")
        d = read_dat2_directory(p)
        print(f"  Contains {len(d)} files:")
        for k in d.keys():
            print(f"    - {k}")

def main():
    check_docs()
    check_shaders()
    check_mods_dats()
    check_sfall_scripts()
    check_worldmap_dat()

if __name__ == "__main__":
    main()
