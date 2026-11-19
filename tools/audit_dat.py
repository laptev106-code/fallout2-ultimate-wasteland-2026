import struct
import zlib
import sys
import os

def read_dat2_directory(dat_path):
    with open(dat_path, 'rb') as f:
        f.seek(-8, os.SEEK_END)
        dir_size, total_size = struct.unpack('<II', f.read(8))
        
        # Seek to start of directory table
        f.seek(- (dir_size + 8), os.SEEK_END)
        file_count = struct.unpack('<I', f.read(4))[0]
        print(f"Archive: {dat_path}")
        print(f"Total files: {file_count}, Directory size: {dir_size} bytes")
        
        files = []
        for _ in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            name = f.read(name_len).decode('ascii', errors='ignore')
            packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
            files.append({
                'name': name,
                'packed': packed,
                'real_size': real_size,
                'pack_size': pack_size,
                'offset': offset
            })
        return files

if __name__ == '__main__':
    dat_file = sys.argv[1] if len(sys.argv) > 1 else r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads.dat"
    files = read_dat2_directory(dat_file)
    
    # Categorize files
    exts = {}
    dirs = {}
    for fl in files:
        n = fl['name'].lower()
        ext = os.path.splitext(n)[1]
        exts[ext] = exts.get(ext, 0) + 1
        d = n.split('\\')[0] if '\\' in n else (n.split('/')[0] if '/' in n else '')
        dirs[d] = dirs.get(d, 0) + 1
        
    print("\nFile types distribution:")
    for ext, count in sorted(exts.items(), key=lambda x: -x[1]):
        print(f"  {ext or '[no ext]'}: {count}")
        
    print("\nDirectory distribution:")
    for d, count in sorted(dirs.items(), key=lambda x: -x[1]):
        print(f"  {d}: {count}")
        
    # Check for scripts or text files
    scripts = [fl['name'] for fl in files if any(fl['name'].lower().endswith(x) for x in ['.int', '.ssl', '.msg', '.txt', '.lst', '.ini'])]
    print(f"\nScripts / Logic / Text files ({len(scripts)}):")
    for s in scripts[:50]:
        print(f"  {s}")
