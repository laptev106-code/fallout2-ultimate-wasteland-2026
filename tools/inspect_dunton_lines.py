# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\text\russian\dialog\kcdunton.msg", "r", encoding="cp1251", errors="replace") as f:
    ru_lines = f.readlines()

print(f"Total lines in ru kcdunton.msg: {len(ru_lines)}")
for l in ru_lines:
    if any(k in l for k in ["{85", "{86", "{87", "{88", "{89", "{90", "{91", "{92"]):
        print(l.strip())
