import sys, os, struct
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')

# Read items.lst and inven.lst
items_lst_info = vfs.get('art\\items\\items.lst')
inven_lst_info = vfs.get('art\\inven\\inven.lst')

items_len = len([l for l in efa.read_vfs_text(items_lst_info)[0].splitlines() if l.strip()]) if items_lst_info else 0
inven_len = len([l for l in efa.read_vfs_text(inven_lst_info)[0].splitlines() if l.strip()]) if inven_lst_info else 0

print(f"items.lst total lines: {items_len}")
print(f"inven.lst total lines: {inven_len}")

item_protos = [k for k in vfs if k.startswith('proto\\items\\') and k.endswith('.pro')]
print(f"Total item proto files: {len(item_protos)}")

oob_ground = []
oob_inven = []

for ip in item_protos:
    info = vfs[ip]
    if info.get('is_disk'):
        with open(info['disk_path'], 'rb') as f:
            data = f.read()
    else:
        data = efa.extract_dat2_file(info)
    if not data or len(data) < 60:
        continue

    # Ground FID at 0x08
    ground_fid = struct.unpack('>I', data[8:12])[0]
    g_type = (ground_fid >> 24) & 0xFF
    g_id = ground_fid & 0x0000FFFF
    
    # Inven FID at 0x34
    inven_fid = struct.unpack('>I', data[0x34:0x38])[0]
    i_type = (inven_fid >> 24) & 0xFF
    i_id = inven_fid & 0x0000FFFF

    if g_type == 2 and items_len > 0:
        if g_id >= items_len:
            oob_ground.append((ip, hex(ground_fid), g_id))

    if i_type == 7 and inven_len > 0:
        if i_id >= inven_len:
            oob_inven.append((ip, hex(inven_fid), i_id))

print(f"Item protos with Out-Of-Bounds Ground FID: {len(oob_ground)}")
for ip, f_hex, gid in oob_ground[:10]:
    print(f"  {ip}: ground FID={f_hex} (id={gid} >= {items_len})!")

print(f"Item protos with Out-Of-Bounds Inven FID: {len(oob_inven)}")
for ip, f_hex, iid in oob_inven[:10]:
    print(f"  {ip}: inven FID={f_hex} (id={iid} >= {inven_len})!")
