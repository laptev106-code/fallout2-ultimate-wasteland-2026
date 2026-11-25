import struct
import zlib
import os

fores_path = r'D:\AG games mods\downloads\fores.dat'
out_dir = r'D:\AG games mods\downloads\resurrection_interface'

with open(fores_path, 'rb') as f:
    f.seek(-8, os.SEEK_END)
    file_size = f.tell() + 8
    dir_size, _ = struct.unpack('<II', f.read(8))
    dir_offset = file_size - dir_size - 8
    f.seek(dir_offset)
    num_files = struct.unpack('<I', f.read(4))[0]
    
    files_to_extract = []
    for _ in range(num_files):
        name_len = struct.unpack('<I', f.read(4))[0]
        fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
        is_compressed, uncomp_size, comp_size, offset = struct.unpack('<BIII', f.read(13))
        
        # We want the intrface art from Resurrection
        if fname.lower().startswith('art/intrface/'):
            # Pick all interface components: inv, barter, trade, dialog, charwin, buttons
            basename = os.path.basename(fname).lower()
            if any(k in basename for k in [
                'barter', 'trade', 'charwin', 'inv', 'dialog', 'automap', 'donebox',
                'agebox', 'attrib', 'skill', 'warnbox', 'hr_menu', 'helpscrn'
            ]):
                files_to_extract.append((fname, is_compressed, uncomp_size, comp_size, offset))

    print(f"Extracting {len(files_to_extract)} interface files to {out_dir}...")
    for fname, is_c, usize, csize, offset in files_to_extract:
        f.seek(offset)
        raw = f.read(csize)
        if is_c:
            data = zlib.decompress(raw)
        else:
            data = raw
            
        dest_path = os.path.join(out_dir, fname)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'wb') as out_f:
            out_f.write(data)

print("Extraction completed successfully!")
