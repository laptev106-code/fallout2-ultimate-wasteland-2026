import os, sys, struct, re
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_vfs_text, extract_dat2_file

print('=== AUDIT: PROTOTYPE TEXT DESCRIPTIONS ===')

def audit_proto_texts(pname, pdir):
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    
    # Load pro_item.msg
    pro_item_info = vfs.get(r'text\russian\game\pro_item.msg')
    if not pro_item_info:
        print(f'[{pname}] CRITICAL: pro_item.msg not found in VFS!')
        return
    txt, _ = read_vfs_text(pro_item_info)
    
    # parse message lines
    item_msgs = {}
    for m in re.finditer(r'\{(\d+)\}\s*\{[^}]*\}\s*\{(.*?)\}', txt, re.DOTALL):
        item_msgs[int(m.group(1))] = m.group(2).strip()
        
    print(f'[{pname}] pro_item.msg has {len(item_msgs)} lines.')
    
    # Check all proto\items\*.pro
    item_pros = [k for k in vfs.keys() if k.startswith('proto\\items\\') and k.endswith('.pro')]
    print(f'[{pname}] Found {len(item_pros)} item prototype files.')
    
    missing_items = []
    for ip in item_pros:
        # Proto filename is like 00000001.pro or 00000624.pro
        base_name = os.path.basename(ip)
        try:
            pid = int(base_name.split('.')[0])
        except ValueError:
            continue
            
        name_line = pid * 100
        desc_line = pid * 100 + 1
        
        has_name = name_line in item_msgs and item_msgs[name_line]
        has_desc = desc_line in item_msgs and item_msgs[desc_line]
        
        if not has_name or not has_desc:
            missing_items.append((pid, base_name, has_name, has_desc))
            
    print(f'[{pname}] Items missing name or description: {len(missing_items)}')
    if missing_items:
        for itm in missing_items[:15]:
            print(f'  PID {itm[0]} ({itm[1]}): has_name={itm[2]}, has_desc={itm[3]}')

audit_proto_texts('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
audit_proto_texts('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')
