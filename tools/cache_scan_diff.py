# -*- coding: utf-8 -*-
import os, sys, struct, zlib

class FastDat:
    def __init__(self, dat_path):
        self.dat_path = dat_path
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
    foxx_dat = FastDat(r'E:\Games\Fallout 2 (Expansion Version)\master.dat')
    print(f"Indexed {len(foxx_dat.files)} files in Foxx master.dat")

    our_root = r'E:\Fallout2_Ultimate\Fallout2_Gameplay'
    dats_to_check = [
        os.path.join(our_root, 'mods', 'rpu_russian_uncensored.dat'),
        os.path.join(our_root, 'mods', 'foxx_rebuild_tribute.dat'),
        os.path.join(our_root, 'mods', 'talking_heads_that_rpu_map_update_patch.dat'),
        os.path.join(our_root, 'mods', 'rpu_russian.dat'),
        os.path.join(our_root, 'mods', 'rpu_y_ecco.dat'),
        os.path.join(our_root, 'mods', 'talking_heads.dat'),
        os.path.join(our_root, 'mods', 'rpu.dat'),
        os.path.join(our_root, 'master.dat')
    ]

    loaded_dats = []
    for d in dats_to_check:
        if os.path.exists(d) and not os.path.isdir(d):
            loaded_dats.append((os.path.basename(d), FastDat(d)))

    def get_our(fname):
        fname_low = fname.lower()
        # check loose dir first
        loose = os.path.join(our_root, 'mods', 'rpu_russian_uncensored.dat', fname)
        if os.path.exists(loose):
            with open(loose, 'rb') as f:
                return f.read(), 'loose'
        for name, d in loaded_dats:
            res = d.read_file(fname_low)
            if res is not None:
                return res, name
        return None, 'none'

    scripts = [f for f in foxx_dat.files if f.startswith('scripts\\') and f.endswith('.int')]
    print(f"Comparing {len(scripts)} scripts...")

    diffs = []
    for s in sorted(scripts):
        f_raw = foxx_dat.read_file(s)
        o_raw, src = get_our(s)
        if not o_raw or f_raw != o_raw:
            diffs.append((s, len(f_raw), len(o_raw) if o_raw else 0, src))

    print(f"\nDone! Differing scripts count: {len(diffs)}")
    for d in diffs:
        print(f"  {d[0]}: Foxx={d[1]}b vs Ours={d[2]}b (source: {d[3]})")

    foxx_dat.close()
    for _, d in loaded_dats:
        d.close()

if __name__ == '__main__':
    main()
