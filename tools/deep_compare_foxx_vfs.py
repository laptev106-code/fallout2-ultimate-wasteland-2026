import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
GAMEPLAY_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"

def build_vfs_map(profile_dir):
    mods_order_file = os.path.join(profile_dir, "mods", "mods_order.txt")
    vfs_layers = []
    
    # 1. Base master.dat and critter.dat
    for base in ["master.dat", "critter.dat"]:
        p = os.path.join(profile_dir, base)
        if os.path.exists(p):
            vfs_layers.append(p)
            
    # 2. mods_order.txt layers
    if os.path.exists(mods_order_file):
        with open(mods_order_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(";"):
                    dat_path = os.path.join(profile_dir, "mods", line)
                    if os.path.exists(dat_path):
                        vfs_layers.append(dat_path)
                    folder_path = os.path.join(profile_dir, "mods", line)
                    # might be directory

    # Index all layers from bottom to top
    vfs_index = {}
    for layer in vfs_layers:
        if os.path.isfile(layer) and layer.lower().endswith(".dat"):
            files = read_dat2_directory(layer)
            for k, info in files.items():
                vfs_index[k] = info
    return vfs_index

def main():
    print("=" * 70)
    print("  DEEP VFS COMPARISON: FOXX FIXES VS ULTIMATE WASTELAND GAMEPLAY")
    print("=" * 70)

    foxx_files = read_dat2_directory(FOXX_MASTER)
    vfs = build_vfs_map(GAMEPLAY_DIR)

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
        "text\\english\\dialog\\ectravlr.msg",
        "scripts\\gl_k_dogmeat_fix.int",
        "proto\\critters\\00000543.pro",
        "proto\\critters\\00000544.pro"
    ]

    for rel in candidates:
        key = rel.lower()
        if key in foxx_files:
            foxx_info = foxx_files[key]
            foxx_data = extract_dat2_file(foxx_info)
            if key in vfs:
                our_info = vfs[key]
                our_data = extract_dat2_file(our_info)
                our_src = os.path.basename(our_info['archive'])
                if foxx_data == our_data:
                    print(f"[=] {rel}: IDENTICAL ({len(foxx_data)} bytes) with {our_src}")
                else:
                    print(f"[!] {rel}: DIFFERENT! Foxx={len(foxx_data)} bytes vs Ours={len(our_data)} bytes ({our_src})")
            else:
                print(f"[-] {rel}: In Foxx ({len(foxx_data)} bytes), but MISSING from our VFS!")
        else:
            print(f"[?] {rel}: Not in Foxx master.dat")

if __name__ == "__main__":
    main()
