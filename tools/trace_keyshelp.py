import os
import struct

p = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\KeysHelp.dat\scripts\gl_keyshelp.int"
with open(p, "rb") as f:
    data = f.read()

i = 0x03B4
while i < len(data) - 4:
    if data[i] == 0x90 and data[i+1] == 0x01:
        val = struct.unpack(">I", data[i+2:i+6])[0]
        print(f"0x{i:04X}: sfall_func / metarule (val={val})")
        i += 6
        continue
    elif data[i] == 0x80 and data[i+1] == 0x1A:
        str_idx = struct.unpack(">I", data[i+2:i+6])[0]
        print(f"0x{i:04X}: PUSH_STR idx={str_idx}")
        i += 6
        continue
    elif data[i] == 0xC0 and data[i+1] == 0x01:
        val = struct.unpack(">i", data[i+2:i+6])[0]
        print(f"0x{i:04X}: PUSH_INT {val}")
        i += 6
        continue
    i += 1
