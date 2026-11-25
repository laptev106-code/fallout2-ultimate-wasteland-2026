import os
import struct

p = r"E:\Games\Fallout 2 (Expansion Version)\mods\KeysHelp.dat\scripts\gl_keyshelp.int"
with open(p, "rb") as f:
    data = f.read()

# Fallout 2 INT format string table:
# Header:
# 0x00: 0x8002 (signature)
# 0x08: count of identifiers / procedures
# Let's inspect how push_string works:
# Opcode 0x801A: push string
# Operand: offset from start of string table or index!
# Let's see the instructions pushing strings in create:
i = 0x03B4
while i < len(data) - 4:
    if data[i] == 0x80 and data[i+1] == 0x1A:
        str_offset = struct.unpack(">I", data[i+2:i+6])[0]
        # Let's find what is at str_offset or how string is located
        print(f"0x{i:04X}: PUSH_STR offset=0x{str_offset:04X} ({str_offset})")
        # In FO2 int, string table starts at some offset. Let's see if str_offset points directly to the string!
        if str_offset < len(data):
            # check string at str_offset
            s = data[str_offset:str_offset+30]
            print(f"       -> at offset 0x{str_offset:04X}: {s}")
        i += 6
        continue
    i += 1
