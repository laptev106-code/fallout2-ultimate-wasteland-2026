import sys, os, struct
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
critters_info = vfs.get('art\\critters\\critters.lst')
txt, _ = efa.read_vfs_text(critters_info)
critter_lst_lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith(';')]
critter_lst_len = len(critter_lst_lines)
print(f"Total lines in critters.lst: {critter_lst_len}")

critter_protos = [k for k in vfs if k.startswith('proto\\critters\\') and k.endswith('.pro')]
print(f"Total critter proto files: {len(critter_protos)}")

oob_critter_fids = []

for cp in critter_protos:
    info = vfs[cp]
    if info.get('is_disk'):
        with open(info['disk_path'], 'rb') as f:
            data = f.read()
    else:
        data = efa.extract_dat2_file(info)
    if not data or len(data) < 12:
        continue

    # In Fallout 2 critter proto:
    # 0x00: PID (4 bytes)
    # 0x04: text_id (4 bytes)
    # 0x08: FID (4 bytes)
    fid = struct.unpack('>I', data[8:12])[0]
    art_type = (fid >> 24) & 0xFF
    art_id = fid & 0x0000FFFF
    
    # art_type 1 is critter
    if art_type == 1:
        if art_id >= critter_lst_len:
            oob_critter_fids.append((cp, hex(fid), art_id))

print(f"Critter protos with Out-Of-Bounds FID: {len(oob_critter_fids)}")
for cp, fid_hex, art_id in oob_critter_fids:
    print(f"  {cp}: FID={fid_hex} (art_id={art_id} >= {critter_lst_len})!")
