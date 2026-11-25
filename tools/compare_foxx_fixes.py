#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file, build_profile_vfs

foxx_dat = read_dat2_directory(r"E:\Games\Fallout 2 (Expansion Version)\master.dat")
vfs, _, _, _ = build_profile_vfs(r"E:\Fallout2_Ultimate\Fallout2_Gameplay")

diff_targets = [
    'scripts\\gcskeetr.int',
    'scripts\\dcanna.int',
    'scripts\\gclenny.int',
    'scripts\\gl_k_lenny_look.int',
    'scripts\\vilrat.int',
    'scripts\\ectravlr.int',
    'scripts\\ncjules.int',
    'scripts\\scduppo.int',
    'scripts\\vcconnar.int',
    'scripts\\blkrom.int',
    'maps\\raiders1.map',
    'maps\\raiders2.map',
    'maps\\tribe02.map',
    'scripts\\tribem1.int',
    'scripts\\tribec1.int',
    'scripts\\scslvgrd.int'
]

print(f"{'Target File':<32} | {'In Foxx':<8} | {'Foxx Size':<10} | {'In Our VFS':<10} | {'Our Size':<10} | {'Identical?':<10}")
print("-" * 95)

for t in diff_targets:
    in_foxx = t in foxx_dat
    foxx_size = len(extract_dat2_file(foxx_dat[t])) if in_foxx else 0
    in_vfs = t in vfs
    vfs_size = len(vfs[t]['size']) if in_vfs and 'size' in vfs[t] else (os.path.getsize(vfs[t]['disk_path']) if in_vfs and vfs[t].get('is_disk') else 0)
    
    # Check byte identity if both exist
    identical = "N/A"
    if in_foxx and in_vfs:
        raw_foxx = extract_dat2_file(foxx_dat[t])
        # get our raw
        if vfs[t].get('is_disk'):
            with open(vfs[t]['disk_path'], 'rb') as f:
                raw_our = f.read()
        else:
            raw_our = extract_dat2_file(vfs[t])
        identical = "YES" if raw_foxx == raw_our else "DIFF"
        vfs_size = len(raw_our)

    print(f"{t:<32} | {str(in_foxx):<8} | {foxx_size:<10} | {str(in_vfs):<10} | {vfs_size:<10} | {identical:<10}")
