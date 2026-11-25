# -*- coding: utf-8 -*-
import struct

with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# In Fallout INT, opcodes:
# PUSH_INT: 0x8000..0x803F or 0xC001 (push long) etc.
# In big-endian 4-byte or 2-byte:
for msg_id in [110, 111, 112, 113, 114, 120, 130, 140]:
    b2 = struct.pack('>H', msg_id)
    b4 = struct.pack('>I', msg_id)
    pos = 0
    found = []
    while True:
        p = data.find(b2, pos)
        if p == -1: break
        found.append(f"0x{p:x}")
        pos = p + 1
    print(f"Msg {msg_id}: found at {found[:5]}")
