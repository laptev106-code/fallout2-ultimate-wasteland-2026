# -*- coding: utf-8 -*-
import struct

with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# Fallout INT format:
# 0x00: 4 bytes: signature?
# Let's inspect procedure names and offsets:
# In sfall/fallout INT, procedures are listed with name string and offset.
# Let's find "Node001" offset in the file
idx = data.find(b"Node001")
print("Node001 found at:", idx)
# Procedures table is usually near the start or end.
# Let's find all procedure definitions:
for proc in [b"talk_p_proc", b"Node001", b"Node002", b"Node003", b"Node004", b"Node005", b"Node910", b"Node920"]:
    pos = 0
    while True:
        p = data.find(proc, pos)
        if p == -1: break
        print(f"Proc {proc.decode()}: at offset 0x{p:x}")
        pos = p + len(proc)
