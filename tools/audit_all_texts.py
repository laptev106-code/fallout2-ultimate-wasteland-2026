import os
import struct
import zlib

def read_dat(dat_path):
    try:
        with open(dat_path, 'rb') as f:
            f.seek(-8, os.SEEK_END)
            dir_size, total_size = struct.unpack('<II', f.read(8))
            f.seek(- (dir_size + 8), os.SEEK_END)
            file_count = struct.unpack('<I', f.read(4))[0]
            files = []
            for _ in range(file_count):
                name_len = struct.unpack('<I', f.read(4))[0]
                name = f.read(name_len).decode('ascii', errors='ignore')
                packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
                files.append(name)
            return files
    except Exception as e:
        return []

base_dir = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
mods_dir = os.path.join(base_dir, "mods")

print("=== AUDITING TEXT DIRECTORIES IN MODS & BASE ===")
# 1. Loose directories
for root, dirs, files in os.walk(base_dir):
    rel = os.path.relpath(root, base_dir)
    if "text" in rel.lower():
        text_files = [f for f in files if f.endswith(".msg") or f.endswith(".txt")]
        if text_files:
            print(f"Loose Folder: {rel} ({len(text_files)} msg/txt files)")

# 2. DAT files in mods/ and root
dat_candidates = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.lower().endswith(".dat") and os.path.isfile(os.path.join(root, f)):
            dat_candidates.append(os.path.join(root, f))

for dp in sorted(dat_candidates):
    files = read_dat(dp)
    if not files:
        continue
    eng_texts = [f for f in files if "text/english" in f.lower().replace("\\", "/")]
    rus_texts = [f for f in files if "text/russian" in f.lower().replace("\\", "/")]
    other_texts = [f for f in files if "text/" in f.lower().replace("\\", "/") and f not in eng_texts and f not in rus_texts]
    if eng_texts or rus_texts or other_texts:
        print(f"\nDAT Archive: {os.path.relpath(dp, base_dir)}")
        print(f"  English texts: {len(eng_texts)}")
        print(f"  Russian texts: {len(rus_texts)}")
        if other_texts:
            print(f"  Other texts: {len(other_texts)}")
