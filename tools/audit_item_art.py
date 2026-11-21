import os, sys, struct
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_dat2_directory, read_vfs_text, extract_dat2_file

print('=== AUDIT: ITEM ART & INVENTORY ICONS INTEGRITY ===')

def check_item_art(pname, pdir):
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    master_entries = read_dat2_directory(os.path.join(pdir, 'master.dat'))
    
    # Load items.lst (ground items) and inven.lst (inventory items)
    items_lst_info = vfs.get(r'art\items\items.lst') or master_entries.get(r'art\items\items.lst')
    inven_lst_info = vfs.get(r'art\inven\inven.lst') or master_entries.get(r'art\inven\inven.lst')
    
    txt_items, _ = read_vfs_text(items_lst_info)
    ground_frms = [l.strip().lower() for l in txt_items.splitlines() if l.strip() and not l.startswith(';')]
    
    txt_inven, _ = read_vfs_text(inven_lst_info)
    inven_frms = [l.strip().lower() for l in txt_inven.splitlines() if l.strip() and not l.startswith(';')]
    
    print(f'[{pname}] items.lst: {len(ground_frms)} frms, inven.lst: {len(inven_frms)} frms')
    
    item_pros = [k for k in vfs.keys() if k.startswith('proto\\items\\') and k.endswith('.pro')]
    print(f'[{pname}] Item prototypes: {len(item_pros)}')
    
    missing_ground = []
    missing_inven = []
    
    for ip in item_pros:
        info = vfs[ip]
        if info['is_disk']:
            with open(info['disk_path'], 'rb') as f:
                data = f.read()
        else:
            data = extract_dat2_file(info)
            
        if len(data) >= 0x24:
            # FID (ground) is offset 0x08
            ground_fid = struct.unpack('>I', data[0x08:0x0C])[0]
            # Inventory FID is offset 0x20 in item header
            inven_fid = struct.unpack('>I', data[0x20:0x24])[0]
            
            # Ground FID
            g_idx = ground_fid & 0x00FFFFFF
            if g_idx != 0x00FFFFFF and g_idx < len(ground_frms):
                frm_name = ground_frms[g_idx]
                key = f'art\\items\\{frm_name}'
                if key not in vfs and key not in master_entries:
                    missing_ground.append((ip, frm_name))
            elif g_idx != 0x00FFFFFF and g_idx >= len(ground_frms):
                missing_ground.append((ip, f'OOB index {g_idx}'))
                
            # Inven FID
            i_idx = inven_fid & 0x00FFFFFF
            if i_idx != 0x00FFFFFF and i_idx < len(inven_frms):
                frm_name = inven_frms[i_idx]
                key = f'art\\inven\\{frm_name}'
                if key not in vfs and key not in master_entries:
                    missing_inven.append((ip, frm_name))
            elif i_idx != 0x00FFFFFF and i_idx >= len(inven_frms):
                missing_inven.append((ip, f'OOB index {i_idx}'))
                
    print(f'[{pname}] Missing ground FRMs: {len(missing_ground)}')
    if missing_ground:
        print('  Sample ground:', missing_ground[:5])
    print(f'[{pname}] Missing inven FRMs: {len(missing_inven)}')
    if missing_inven:
        print('  Sample inven:', missing_inven[:5])

check_item_art('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
check_item_art('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')
