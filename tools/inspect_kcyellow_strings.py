# -*- coding: utf-8 -*-
import struct

with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

# INT file format:
# header: 42 bytes or so
# Let's inspect text strings or disassemble
import re
strings = re.findall(b"[\x20-\x7e]{3,}", data)
for s in strings[:40]:
    print("STR:", s.decode('ascii'))
