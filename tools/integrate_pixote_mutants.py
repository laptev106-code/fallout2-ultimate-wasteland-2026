import os
import sys
import shutil

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file
from tools.build_foxx_tribute_pack import pack_to_dat2

FOXX_CRITTER = r"E:\Games\Fallout 2 (Expansion Version)\critter.dat"
OUR_CRITTER = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\critter.dat"
TRIBUTE_DATA_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data"
TRIBUTE_DAT_PATH = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\foxx_rebuild_tribute.dat"

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def main():
    print("=" * 70)
    print("  INTEGRATING PIXOTE MUTANT DEATH ANIMATIONS & GL_GLASSES")
    print("=" * 70)

    # 1. Add gl_glasses.int
    src_glasses = r"E:\FALLOUT Ult pjt\tools\gl_glasses.int"
    dest_glasses = os.path.join(TRIBUTE_DATA_DIR, "scripts", "gl_glasses.int")
    os.makedirs(os.path.dirname(dest_glasses), exist_ok=True)
    shutil.copy2(src_glasses, dest_glasses)
    print(f"[+] Added gl_glasses.int ({os.path.getsize(dest_glasses)} bytes)")

    # 2. Extract Pixote mutant files
    foxx_c = read_dat2_directory(FOXX_CRITTER)
    our_c = read_dat2_directory(OUR_CRITTER)

    foxx_mutants = {k: v for k, v in foxx_c.items() if k.startswith("art\\critters\\ma") or k.startswith("art\\critters\\mb")}
    our_mutants = {k: v for k, v in our_c.items() if k.startswith("art\\critters\\ma") or k.startswith("art\\critters\\mb")}

    targets = {}
    for k, v in foxx_mutants.items():
        if k not in our_mutants or v["real_size"] != our_mutants[k]["real_size"]:
            targets[k] = v

    print(f"[*] Extracting {len(targets)} Pixote mutant animation files...")
    critters_out_dir = os.path.join(TRIBUTE_DATA_DIR, "art", "critters")
    os.makedirs(critters_out_dir, exist_ok=True)

    extracted_count = 0
    extracted_bytes = 0
    for k, v in targets.items():
        filename = os.path.basename(k)
        dest_file = os.path.join(critters_out_dir, filename)
        data = extract_dat2_file(v)
        if data:
            with open(dest_file, "wb") as f:
                f.write(data)
            extracted_count += 1
            extracted_bytes += len(data)

    print(f"[✔] Extracted {extracted_count} files ({extracted_bytes:,} bytes)")

    # 3. Repack foxx_rebuild_tribute.dat
    print("[*] Repacking foxx_rebuild_tribute.dat...")
    pack_to_dat2(TRIBUTE_DATA_DIR, TRIBUTE_DAT_PATH)
    dat_size = os.path.getsize(TRIBUTE_DAT_PATH)
    print(f"[✔] Built DAT2: {TRIBUTE_DAT_PATH} ({dat_size:,} bytes)")

    # 4. Deploy to profiles
    for prof in PROFILES:
        target_dir = os.path.join(prof, "mods")
        if os.path.exists(target_dir):
            target_dat = os.path.join(target_dir, "foxx_rebuild_tribute.dat")
            shutil.copy2(TRIBUTE_DAT_PATH, target_dat)
            print(f"  [+] Deployed to {target_dat}")

if __name__ == "__main__":
    main()
