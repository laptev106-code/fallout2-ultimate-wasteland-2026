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

miria_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\DB_Enchanced_Miria.dat", "data/ai.txt").decode('ascii', errors='replace')
ecco_ai = extract_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat", "data/ai.txt").decode('ascii', errors='replace')

# Parse sections
def get_sections(text):
    sections = {}
    cur = None
    cur_lines = []
    for line in text.splitlines():
        line_s = line.strip()
        if line_s.startswith('[') and line_s.endswith(']'):
            if cur:
                sections[cur] = cur_lines
            cur = line_s
            cur_lines = []
        elif cur:
            cur_lines.append(line)
    if cur:
        sections[cur] = cur_lines
    return sections

sec_m = get_sections(miria_ai)
sec_e = get_sections(ecco_ai)

print(f"Total sections in Miria ai.txt: {len(sec_m)}")
print(f"Total sections in EcCo ai.txt: {len(sec_e)}")

miria_only = [s for s in sec_m if s not in sec_e]
print(f"Sections present in Miria ai.txt but MISSING in EcCo ai.txt: {len(miria_only)}")
for s in miria_only:
    print("  Missing section:", s)

# Also check if any common sections have different values for Miria
for s, lines in sec_m.items():
    if any("miria" in l.lower() for l in lines):
        print("Section with Miria:", s, "in EcCo?", s in sec_e)
        if s in sec_e:
            has_in_ecco = any("miria" in l.lower() for l in sec_e[s])
            print("  Does EcCo have Miria lines in it?", has_in_ecco)
