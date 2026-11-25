#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file, build_profile_vfs

foxx_dat = read_dat2_directory(r"E:\Games\Fallout 2 (Expansion Version)\master.dat")

# 1. Inspect blkrom.int
if 'scripts\\blkrom.int' in foxx_dat:
    raw = extract_dat2_file(foxx_dat['scripts\\blkrom.int'])
    print(f"=== blkrom.int ({len(raw)} bytes) ===")
    # Extract readable strings
    strings = [s.decode('latin-1', errors='replace') for s in raw.split(b'\x00') if len(s) > 3]
    print("Strings in blkrom.int:", strings[:10])

# 2. Inspect vcconnar.int
if 'scripts\\vcconnar.int' in foxx_dat:
    raw_foxx = extract_dat2_file(foxx_dat['scripts\\vcconnar.int'])
    strings_foxx = [s.decode('latin-1', errors='replace') for s in raw_foxx.split(b'\x00') if len(s) > 4]
    print("\n=== vcconnar.int strings (Foxx sample) ===")
    print(strings_foxx[:15])

# 3. Inspect dcanna.int
if 'scripts\\dcanna.int' in foxx_dat:
    raw_foxx = extract_dat2_file(foxx_dat['scripts\\dcanna.int'])
    strings_foxx = [s.decode('latin-1', errors='replace') for s in raw_foxx.split(b'\x00') if len(s) > 4]
    print("\n=== dcanna.int strings (Foxx sample) ===")
    print(strings_foxx[:15])

# 4. Inspect gcskeetr.int
if 'scripts\\gcskeetr.int' in foxx_dat:
    raw_foxx = extract_dat2_file(foxx_dat['scripts\\gcskeetr.int'])
    strings_foxx = [s.decode('latin-1', errors='replace') for s in raw_foxx.split(b'\x00') if len(s) > 4]
    print("\n=== gcskeetr.int strings (Foxx sample) ===")
    print(strings_foxx[:15])
