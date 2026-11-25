# -*- coding: utf-8 -*-
import os, sys, struct, zlib

class FastDat:
    def __init__(self, dat_path):
        self.f = open(dat_path, 'rb')
        self.f.seek(-8, os.SEEK_END)
        file_size = self.f.tell() + 8
        dir_size, data_size = struct.unpack('<II', self.f.read(8))
        dir_offset = file_size - dir_size - 8
        self.f.seek(dir_offset)
        num_files = struct.unpack('<I', self.f.read(4))[0]
        self.files = {}
        for _ in range(num_files):
            name_len = struct.unpack('<I', self.f.read(4))[0]
            fname = self.f.read(name_len).decode('ascii', errors='ignore').replace('/', '\\').lower()
            is_comp, uncomp_sz, comp_sz, offset = struct.unpack('<BIII', self.f.read(13))
            self.files[fname] = (is_comp, uncomp_sz, comp_sz, offset)

    def read_file(self, fname):
        fname = fname.lower()
        if fname not in self.files: return None
        is_comp, uncomp_sz, comp_sz, offset = self.files[fname]
        self.f.seek(offset)
        raw = self.f.read(comp_sz if is_comp else uncomp_sz)
        return zlib.decompress(raw) if is_comp else raw

    def close(self):
        self.f.close()

def main():
    sys.path.append('tools')
    from diff_engine import get_our_file

    foxx = FastDat(r'E:\Games\Fallout 2 (Expansion Version)\master.dat')
    print(f"Indexed {len(foxx.files)} files in Foxx master.dat")

    scripts = [f for f in foxx.files if f.startswith('scripts\\') and f.endswith('.int')]
    print(f"Total scripts: {len(scripts)}")

    diffs = []
    for s in sorted(scripts):
        f_raw = foxx.read_file(s)
        o_raw, o_src = get_our_file(s)
        if not o_raw or f_raw != o_raw:
            diffs.append((s, len(f_raw), len(o_raw) if o_raw else 0, o_src))

    print(f"Total differing scripts: {len(diffs)}")
    for d in diffs:
        print(f"  {d[0]}: Foxx={d[1]}b vs Ours={d[2]}b ({d[3]})")

    foxx.close()

if __name__ == '__main__':
    main()
