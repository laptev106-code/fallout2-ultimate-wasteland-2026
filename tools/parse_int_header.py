# -*- coding: utf-8 -*-
import struct

with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# In Fallout INT:
# Offset 0x00: count of identifiers/procedures or header.
# Let's inspect bytes around 0x3a0 and 0x594
print("Around 0x3a0:", data[0x390:0x3e0])
print("Around 0x590:", data[0x580:0x5d0])
