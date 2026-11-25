# -*- coding: utf-8 -*-
with open(r"E:\FALLOUT Ult pjt\tools\kcyellow.int", "rb") as f:
    data = f.read()

chunk = data[0x1a70:0x1b50]
print("Hexdump of 0x1a70 to 0x1b50:")
for i in range(0, len(chunk), 16):
    line = chunk[i:i+16]
    hex_str = " ".join(f"{b:02x}" for b in line)
    print(f"{0x1a70+i:04x}: {hex_str}")
