#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

foxx_dat_path = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
foxx_d = read_dat2_directory(foxx_dat_path)
print(f"Total files in Foxx master.dat: {len(foxx_d)}")

patterns = ['skeet', 'anna', 'slave', 'lenny', 'myron', 'vilrat', 'travlr', 'jules', 'duppo', 'connar', 'robot', 'skynet', 'tribem', 'tribec', 'raider', 'marley', 'krom']

for p in patterns:
    matches = [k for k in foxx_d if p in k.lower()]
    print(f"[{p}] -> {len(matches)} files: {matches[:4]}")
