# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat\text\russian\dialog\kcdunton.msg", "r", encoding="cp1251", errors="replace") as f:
    text = f.read()

import re
entries = re.findall(r"\{(\d+)\}\{.*\}\{(.*)\}", text)
print(f"Total entries: {len(entries)}")
# Print first 30 entries
for num, val in entries[:35]:
    print(f"{{{num}}} {val}")
