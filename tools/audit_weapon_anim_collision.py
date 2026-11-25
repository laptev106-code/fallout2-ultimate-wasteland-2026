import struct, zlib, os

def extract_file(dat_path, inner_name):
    with open(dat_path, "rb") as f:
        f.seek(-8, os.SEEK_END)
        file_size = f.tell() + 8
        dir_size, data_size = struct.unpack('<II', f.read(8))
        dir_offset = file_size - dir_size - 8
        f.seek(dir_offset)
        num_files = struct.unpack('<I', f.read(4))[0]
        for _ in range(num_files):
            name_len = struct.unpack('<I', f.read(4))[0]
            fname = f.read(name_len).decode('ascii', errors='ignore').replace('\\', '/')
            is_compressed, uncomp_size, comp_size, offset = struct.unpack('<BIII', f.read(13))
            if fname.lower() == inner_name.lower():
                f.seek(offset)
                data = f.read(comp_size if is_compressed else uncomp_size)
                return zlib.decompress(data) if is_compressed else data
    return None

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
pids = [
    ("proto/items/00000011.pro", "Hunting Rifle"),
    ("proto/items/00000143.pro", "Sniper Rifle"),
    ("proto/items/00000287.pro", "Pipe Rifle"),
    ("proto/items/00000351.pro", "Red Ryder LE"),
    ("proto/items/00000403.pro", "Gauss Rifle"),
    ("proto/items/00000500.pro", "Scoped Hunting Rifle"),
    ("proto/items/00000522.pro", "Wakizashi Blade"),
]

for pro_path, name in pids:
    anim_dat = "rpu_wakizashi_animations.dat" if "522" in pro_path else "rpu_rifle_animations.dat"
    pro_anim = extract_file(os.path.join(base, anim_dat), pro_path)
    pro_ecco = extract_file(os.path.join(base, "rpu_y_ecco.dat"), pro_path)
    pro_orig = extract_file(os.path.join(base, "rpu.dat"), pro_path)
    
    # Weapon anim code in proto format:
    # Header: PID (4), TextID (4), FID (4), LightRadius (4), LightInt (4), Flags (4), FlagsExt (4), SID (4), Subtype (4), Material (4), Size (4), Weight (4), Cost (4), InvFID (4), SoundCode (1)
    # Weapon sub-proto starts at offset 0x39: anim_code is at 0x39 (or 0x38-0x3C depending on sub-type offset)
    print(f"=== {name} ({pro_path}) ===")
    print(f"  Anim mod size: {len(pro_anim) if pro_anim else 'None'}")
    print(f"  EcCo mod size: {len(pro_ecco) if pro_ecco else 'None'}")
    print(f"  RPU orig size: {len(pro_orig) if pro_orig else 'None'}")
    
    # Let's inspect differences between anim mod and ecco
    diffs = []
    if pro_anim and pro_ecco:
        min_len = min(len(pro_anim), len(pro_ecco))
        for i in range(min_len):
            if pro_anim[i] != pro_ecco[i]:
                diffs.append((hex(i), hex(pro_orig[i]) if pro_orig and i < len(pro_orig) else '?', hex(pro_anim[i]), hex(pro_ecco[i])))
        print(f"  Total byte differences: {len(diffs)}")
        for d in diffs[:8]:
            print(f"    Offset {d[0]}: Orig={d[1]} -> AnimMod={d[2]} vs EcCo={d[3]}")
