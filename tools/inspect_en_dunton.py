# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\text\english\dialog\kcdunton.msg", "r", encoding="latin1", errors="replace") as f:
    en_lines = f.readlines()

for l in en_lines:
    if any(k in l for k in ["{85", "{86", "{87", "{88"]):
        print(l.strip())
