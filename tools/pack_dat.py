import os
import struct
import zlib

def pack_to_dat2(source_dir, output_dat_path):
    files_to_pack = []
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, source_dir).replace('/', '\\')
            files_to_pack.append((rel_path, full_path))

    print(f"Packing {len(files_to_pack)} files to {output_dat_path}...")
    
    file_records = []
    with open(output_dat_path, 'wb') as out_f:
        for rel_path, full_path in files_to_pack:
            with open(full_path, 'rb') as src_f:
                raw_data = src_f.read()
            uncomp_size = len(raw_data)
            comp_data = zlib.compress(raw_data)
            comp_size = len(comp_data)
            offset = out_f.tell()
            out_f.write(comp_data)
            file_records.append((rel_path, uncomp_size, comp_size, offset))

        # Write directory
        dir_start_offset = out_f.tell()
        out_f.write(struct.pack('<I', len(file_records)))
        
        for rel_path, uncomp_size, comp_size, offset in file_records:
            name_bytes = rel_path.encode('ascii')
            out_f.write(struct.pack('<I', len(name_bytes)))
            out_f.write(name_bytes)
            out_f.write(struct.pack('<BIII', 1, uncomp_size, comp_size, offset))

        dir_end_offset = out_f.tell()
        dir_size = dir_end_offset - dir_start_offset
        total_file_size = dir_end_offset + 8
        out_f.write(struct.pack('<II', dir_size, total_file_size))

    print(f"Packed successfully! Total DAT size: {os.path.getsize(output_dat_path)} bytes")

if __name__ == '__main__':
    src = r'D:\AG games mods\downloads\resurrection_interface'
    dsts = [
        r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\resurrection_interface.dat',
        r'E:\Fallout2_Ultimate\Fallout2_HD\mods\resurrection_interface.dat'
    ]
    for dst in dsts:
        pack_to_dat2(src, dst)
