# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# Let's decode bytes from 0x1ac0 to 0x1b20
chunk = data[0x1ac0:0x1b20]
for idx, b in enumerate(chunk):
    print(f"0x{0x1ac0+idx:x}: 0x{b:02x} ({b})")
