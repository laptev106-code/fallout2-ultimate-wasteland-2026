import os
import struct
import zlib
import shutil

def pack_to_dat2(source_dir, output_dat_path):
    files_to_pack = []
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, source_dir).replace('/', '\\')
            files_to_pack.append((rel_path, full_path))

    os.makedirs(os.path.dirname(output_dat_path), exist_ok=True)
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

def build_master_patch():
    staging_dir = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\staging_master_patch"
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    # 1. Base files from extracted_rpu (dialogs & texts)
    src_extracted = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\extracted_rpu"
    if os.path.exists(src_extracted):
        for root, dirs, files in os.walk(src_extracted):
            for f in files:
                full_src = os.path.join(root, f)
                rel = os.path.relpath(full_src, src_extracted)
                dst = os.path.join(staging_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(full_src, dst)

    # 2. Add custom compiled scripts
    scripts_map = {
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\AIBKDOR.INT": "scripts/AIBKDOR.INT",
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_temple_hints.int": "scripts/gl_temple_hints.int",
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_highlighting.int": "scripts/gl_highlighting.int",
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_glasses.int": "scripts/gl_glasses.int",
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_pariah_fix.int": "scripts/gl_pariah_fix.int"
    }

    for src_int, rel_target in scripts_map.items():
        if os.path.exists(src_int):
            dst = os.path.join(staging_dir, rel_target.replace('/', '\\'))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src_int, dst)
            print(f"Staged {rel_target}")

    # 3. Pack into target locations
    targets = [
        r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat",
        r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat",
        r"D:\AG games mods\fallout2-ultimate-wasteland-2026\mods\rpu_russian_uncensored.dat"
    ]

    for t in targets:
        pack_to_dat2(staging_dir, t)

    # Cleanup staging
    shutil.rmtree(staging_dir)
    print("Master patch build completed successfully!")

if __name__ == '__main__':
    build_master_patch()
