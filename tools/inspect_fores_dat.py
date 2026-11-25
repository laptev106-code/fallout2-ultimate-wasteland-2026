import zipfile
import struct
import zlib
import os

zip_path = r'D:\AG games mods\downloads\FoRes_EN_1_5.zip'
print("Opening zip...")
zf = zipfile.ZipFile(zip_path)

# Extract only fores.dat
info = zf.getinfo('Resurrection/fores.dat')
print(f"fores.dat compressed size: {info.compress_size / 1024 / 1024:.2f} MB, uncompressed: {info.file_size / 1024 / 1024:.2f} MB")

out_fores = r'D:\AG games mods\downloads\fores.dat'
if not os.path.exists(out_fores):
    print("Extracting fores.dat...")
    with zf.open('Resurrection/fores.dat') as src, open(out_fores, 'wb') as dst:
        while True:
            chunk = src.read(4*1024*1024)
            if not chunk:
                break
            dst.write(chunk)
    print("Extracted fores.dat successfully!")

# Now inspect Fallout DAT2 format of fores.dat
# Fallout DAT2 format:
# Last 8 bytes: [dir_size (uint32)][archive_size (uint32)]
# Directory is located at archive_size - dir_size - 8 (or similar depending on spec)
with open(out_fores, 'rb') as f:
    f.seek(-8, os.SEEK_END)
    file_size = f.tell() + 8
    dir_size, data_size = struct.unpack('<II', f.read(8))
    print(f"File size: {file_size}, Dir size: {dir_size}, Data size: {data_size}")

    # The directory starts at file_size - dir_size - 8
    dir_offset = file_size - dir_size - 8
    f.seek(dir_offset)
    num_files = struct.unpack('<I', f.read(4))[0]
    print(f"Total files in fores.dat: {num_files}")

    matching_files = []
    for _ in range(num_files):
        name_len = struct.unpack('<I', f.read(4))[0]
        fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
        is_compressed, uncomp_size, comp_size, offset = struct.unpack('<BIII', f.read(13))
        
        if any(k in fname.lower() for k in ['intrface', 'inventry', 'barter', 'trade']):
            matching_files.append((fname, is_compressed, uncomp_size, comp_size, offset))

    print(f"Found {len(matching_files)} matching interface files in fores.dat:")
    for m in matching_files[:40]:
        print(f"  {m[0]} (comp={m[1]}, size={m[2]})")
