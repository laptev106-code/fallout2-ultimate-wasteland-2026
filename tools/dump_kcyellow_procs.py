# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# Let's inspect the procedure offsets in the int file
# Fallout INT format header:
# 4 bytes: header size or magic
# Let's read procedure table:
# Count of procedures is at 0x26 or so.
# Let's write a script to inspect the export table.
num_identifiers = struct_val = struct_unpack = None
import struct
num_identifiers = struct.unpack('>I', data[4:8])[0]
print(f"Num identifiers: {num_identifiers}")
