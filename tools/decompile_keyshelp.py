import os
import sys

# Let's inspect the exact instructions in gl_keyshelp.int
# FO2 INT instruction format:
# 2-byte opcodes or 1-byte opcodes.
# Common sfall / fallout opcodes:
# 0x8004: push int
# 0x801A: push string
# 0x802A: call procedure
# 0x802F: fetch variable
# 0x8033: pop to variable
# 0x803A: add
# 0x803C: sub
# 0x803E: mul
# 0x8040: div
# 0x8042: mod
# 0x8044: and
# 0x8046: or
# 0x8048: not
# 0x804A: neg
# 0x804C: eq
# 0x804E: neq
# 0x8050: lt
# 0x8052: gt
# 0x8054: lte
# 0x8056: gte

p = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\KeysHelp.dat\scripts\gl_keyshelp.int"
with open(p, "rb") as f:
    data = f.read()

print("File size:", len(data))

# Let's dump all push string operands and their surrounding bytes
i = 0x03B4
while i < len(data) - 4:
    # 0x80 0x1A or 0x90 0x01
    if data[i] == 0x80 and data[i+1] == 0x1A:
        # push string
        pass
    i += 1

# Let's print the raw text blocks and strings referenced
strings_p = r"E:\Games\Fallout 2 (Expansion Version)\mods\KeysHelp.dat\scripts\gl_keyshelp.int"
with open(strings_p, "rb") as f:
    raw = f.read()

import re
matches = re.finditer(b'[\x20-\x7E\xC0-\xFF]{2,}', raw)
for m in matches:
    try:
        s = m.group().decode('cp1251')
        print(f"0x{m.start():04X}: {s}")
    except:
        pass
