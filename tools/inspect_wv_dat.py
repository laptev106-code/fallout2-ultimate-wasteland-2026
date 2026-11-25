# -*- coding: utf-8 -*-
import os
import struct
import zlib

def inspect_dat(dat_path):
    print("Inspecting:", dat_path)
    with open(dat_path, "rb") as f:
        f.seek(-8, os.SEEK_END)
        dir_size, file_size = struct.unpack("<II", f.read(8))
        f.seek(-8 - dir_size, os.SEEK_END)
        file_count = struct.unpack("<I", f.read(4))[0]
        print(f"File count: {file_count}, Total archive size: {file_size}")

        entries = []
        for _ in range(file_count):
            fn_len = struct.unpack("<I", f.read(4))[0]
            fn = f.read(fn_len).decode("ascii")
            is_comp, real_sz, comp_sz, offset = struct.unpack("<BIII", f.read(13))
            entries.append((fn, is_comp, real_sz, comp_sz, offset))

        for fn, is_comp, real_sz, comp_sz, offset in entries:
            print(f"  {fn} -> Real: {real_sz} bytes, Packed: {comp_sz} bytes, Offset: {offset}")

if __name__ == "__main__":
    inspect_dat("E:/FALLOUT Ult pjt/standalone_mods/wasteland_voices/dist/wasteland_voices.dat")
