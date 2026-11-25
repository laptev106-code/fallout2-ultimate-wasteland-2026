import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
GAMEPLAY_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"

def build_vfs_map(profile_dir):
    mods_order_file = os.path.join(profile_dir, "mods", "mods_order.txt")
    vfs_layers = []
    
    for base in ["master.dat", "critter.dat"]:
        p = os.path.join(profile_dir, base)
        if os.path.exists(p):
            vfs_layers.append(p)
            
    if os.path.exists(mods_order_file):
        with open(mods_order_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(";"):
                    dat_path = os.path.join(profile_dir, "mods", line)
                    if os.path.isfile(dat_path) and dat_path.lower().endswith(".dat"):
                        vfs_layers.append(dat_path)

    vfs_index = {}
    for layer in vfs_layers:
        files = read_dat2_directory(layer)
        for k, info in files.items():
            vfs_index[k] = info
    return vfs_index

def main():
    print("=" * 70)
    print("  EXHAUSTIVE DIFF: FOXX MASTER.DAT VS GAMEPLAY VFS STACK")
    print("=" * 70)

    foxx_files = read_dat2_directory(FOXX_MASTER)
    vfs = build_vfs_map(GAMEPLAY_DIR)

    categories = {
        "scripts": [],
        "proto": [],
        "maps": [],
        "dialog": [],
        "art": [],
        "other": []
    }

    for k, f_info in foxx_files.items():
        if k not in vfs:
            continue
        v_info = vfs[k]
        
        # Quick size check first
        if f_info["real_size"] != v_info["real_size"]:
            cat = "other"
            if k.startswith("scripts\\"): cat = "scripts"
            elif k.startswith("proto\\"): cat = "proto"
            elif k.startswith("maps\\"): cat = "maps"
            elif "\\dialog\\" in k or "\\dialog_female\\" in k: cat = "dialog"
            elif k.startswith("art\\"): cat = "art"
            categories[cat].append((k, f_info["real_size"], v_info["real_size"], os.path.basename(v_info["archive"])))

    print("\n--- DIFFERING SCRIPTS (Size Mismatch) ---")
    for k, f_sz, v_sz, arch in sorted(categories["scripts"]):
        print(f"  {k}: Foxx={f_sz} vs VFS={v_sz} ({arch})")

    print(f"\nTotal differing scripts: {len(categories['scripts'])}")

    print("\n--- DIFFERING PROTO FILES ---")
    for k, f_sz, v_sz, arch in sorted(categories["proto"]):
        print(f"  {k}: Foxx={f_sz} vs VFS={v_sz} ({arch})")

    print(f"\nTotal differing proto: {len(categories['proto'])}")

    print("\n--- DIFFERING MAPS ---")
    for k, f_sz, v_sz, arch in sorted(categories["maps"]):
        print(f"  {k}: Foxx={f_sz} vs VFS={v_sz} ({arch})")

    print(f"\nTotal differing maps: {len(categories['maps'])}")

    print(f"\nTotal differing dialog: {len(categories['dialog'])}")
    print(f"Total differing art: {len(categories['art'])}")

if __name__ == "__main__":
    main()
