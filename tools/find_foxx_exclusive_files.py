import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory
from tools.exhaustive_foxx_diff import build_vfs_map

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
GAMEPLAY_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"

def main():
    print("=" * 70)
    print("  FILES IN FOXX MASTER.DAT BUT MISSING FROM GAMEPLAY VFS")
    print("=" * 70)

    foxx_files = read_dat2_directory(FOXX_MASTER)
    vfs = build_vfs_map(GAMEPLAY_DIR)

    missing = {}
    for k, info in foxx_files.items():
        if k not in vfs:
            folder = k.split("\\")[0] if "\\" in k else "root"
            missing.setdefault(folder, []).append((k, info["real_size"]))

    print(f"Total files in Foxx master.dat: {len(foxx_files)}")
    print(f"Total missing from Gameplay VFS: {sum(len(v) for v in missing.values())}")

    for folder, items in sorted(missing.items()):
        print(f"\n--- Folder: {folder} ({len(items)} files) ---")
        for k, sz in sorted(items)[:20]:
            print(f"  {k} ({sz:,} bytes)")
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")

if __name__ == "__main__":
    main()
