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

def get_sections(text):
    sections = {}
    cur = None
    cur_lines = []
    order = []
    for line in text.splitlines():
        line_s = line.strip()
        if line_s.startswith('[') and line_s.endswith(']'):
            if cur:
                sections[cur] = cur_lines
            cur = line_s
            order.append(cur)
            cur_lines = []
        elif cur:
            cur_lines.append(line)
    if cur:
        sections[cur] = cur_lines
    return sections, order

sec_m, _ = get_sections(miria_ai)
sec_e, order_e = get_sections(ecco_ai)

# Replace the 5 Maria sections in EcCo with the ones from Miria
maria_sections = ["[PARTY MARIA AGGRESSIVE]", "[PARTY MARIA BERSERK]", "[PARTY MARIA COWARD]", "[PARTY MARIA CUSTOM]", "[PARTY MARIA DEFENSIVE]"]
merged_output = []
for s in order_e:
    merged_output.append(s)
    if s in maria_sections:
        merged_output.extend(sec_m[s])
    else:
        merged_output.extend(sec_e[s])

merged_text = "\r\n".join(merged_output) + "\r\n"

# Verify that merged_text contains both EcCo features and Miria features
print(f"Merged ai.txt length: {len(merged_text)} characters, {len(order_e)} sections")
assert "body_type=Miria" in merged_text
assert "[PARTY SULIK BERSERK]" in merged_text

# Save to both profiles in rpu_russian_uncensored.dat/data/ai.txt
for p in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD"]:
    out_dir = os.path.join(p, "mods", "rpu_russian_uncensored.dat", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "ai.txt")
    with open(out_file, "wb") as f:
        f.write(merged_text.encode('ascii'))
    print(f"Saved: {out_file} ({os.path.getsize(out_file)} bytes)")

# Also save to workspace tools/
os.makedirs("data", exist_ok=True)
with open("data/ai.txt", "wb") as f:
    f.write(merged_text.encode('ascii'))
print("Saved data/ai.txt to workspace successfully.")
