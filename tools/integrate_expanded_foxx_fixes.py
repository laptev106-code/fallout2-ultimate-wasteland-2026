#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPANDED FOXX REBUILD TRIBUTE PACK BUILDER & FIXER (2026)
Incorporates newly uncovered critical engine & prototype fixes from Foxx:
1. proto/critters/00000522.pro: Cat Jules level 5 internal ID fix (was 42, fixed to 522).
2. proto/critters/00000542.pro: Krom tribal warrior HP & stat balance (was 400+ HP bugged).
3. proto/critters/00000489..493.pro: Kaga 1..5 encounter balance.
4. proto/items/00000278.pro & 00000329.pro: Flint & Serum 0xCCCCCCCC corrupt charges fix.
5. scripts/vcconnar.int: Vault City Village softlock fix (21,566 bytes updated).
"""

import os
import sys
import shutil

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
MOD_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute"
DATA_DIR = os.path.join(MOD_DIR, "data")

def extract_expanded_foxx_fixes():
    print("[*] Extracting expanded fixes from Foxx master.dat...")
    foxx_dat = read_dat2_directory(FOXX_MASTER)

    # 1. Critters
    crit_dir = os.path.join(DATA_DIR, "proto", "critters")
    os.makedirs(crit_dir, exist_ok=True)
    crit_targets = [522, 542, 489, 490, 491, 492, 493]
    for pid in crit_targets:
        k = f"proto\\critters\\{pid:08d}.pro"
        if k in foxx_dat:
            raw = extract_dat2_file(foxx_dat[k])
            dst = os.path.join(crit_dir, f"{pid:08d}.pro")
            with open(dst, "wb") as f:
                f.write(raw)
            print(f"  [+] Critter Proto: {pid:08d}.pro ({len(raw)} bytes)")

    # 2. Items
    item_dir = os.path.join(DATA_DIR, "proto", "items")
    os.makedirs(item_dir, exist_ok=True)
    item_targets = [278, 329]
    for pid in item_targets:
        k = f"proto\\items\\{pid:08d}.pro"
        if k in foxx_dat:
            raw = extract_dat2_file(foxx_dat[k])
            dst = os.path.join(item_dir, f"{pid:08d}.pro")
            with open(dst, "wb") as f:
                f.write(raw)
            print(f"  [+] Item Proto: {pid:08d}.pro ({len(raw)} bytes)")

    # 3. vcconnar.int (21,566 bytes)
    script_dir = os.path.join(DATA_DIR, "scripts")
    os.makedirs(script_dir, exist_ok=True)
    if "scripts\\vcconnar.int" in foxx_dat:
        raw = extract_dat2_file(foxx_dat["scripts\\vcconnar.int"])
        dst = os.path.join(script_dir, "vcconnar.int")
        with open(dst, "wb") as f:
            f.write(raw)
        print(f"  [+] Script: vcconnar.int ({len(raw)} bytes)")

        # Also update in rpu_russian_uncensored.dat across profiles to eliminate the outdated 18,892 byte file!
        for prof in [
            r"E:\FALLOUT Ult pjt\scripts\vcconnar.int",
            r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\scripts\vcconnar.int",
            r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\scripts\vcconnar.int",
            r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat\scripts\vcconnar.int"
        ]:
            if os.path.exists(os.path.dirname(prof)):
                with open(prof, "wb") as f:
                    f.write(raw)
                print(f"  [+] Synced clean vcconnar.int to {prof}")

def main():
    print("=" * 70)
    print("  INTEGRATING EXPANDED FOXX FIXES INTO TRIBUTE PACK (2026)")
    print("=" * 70)

    extract_expanded_foxx_fixes()

    # Re-pack and re-deploy
    from tools.build_foxx_tribute_pack import build_dat, deploy_and_register
    dat_size = build_dat()
    deploy_and_register()

    print("\n" + "=" * 70)
    print(f"  EXPANDED FOXX TRIBUTE PACK DEPLOYED! ({dat_size:,} bytes)")
    print("=" * 70)

if __name__ == "__main__":
    main()
