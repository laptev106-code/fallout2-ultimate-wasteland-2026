import sys
sys.path.insert(0, '.')
import tools.engine_full_audit as efa
import os, re

def parse_msg_full(text):
    entries = {}
    order = []
    # Match {number}{sound/tag}{text}
    pattern = re.compile(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}')
    for m in pattern.finditer(text):
        num = int(m.group(1))
        sound = m.group(2)
        val = m.group(3)
        entries[num] = (sound, val)
        order.append(num)
    return entries, order

ecco_files = efa.read_dat2_directory(r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat')
vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')

ru_dialogs = [k for k in ecco_files if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]

print(f"Auditing {len(ru_dialogs)} EcCo Russian dialog files against VFS...")

results = {}
for k in sorted(ru_dialogs):
    e_data = efa.extract_dat2_file(ecco_files[k]).decode('cp1251', errors='ignore')
    e_entries, e_order = parse_msg_full(e_data)
    
    v_info = vfs.get(k)
    if not v_info:
        results[k] = {'status': 'MISSING_IN_VFS', 'missing_keys': list(e_entries.keys()), 'format_keys': []}
        continue
    v_data, enc = efa.read_vfs_text(v_info)
    v_entries, v_order = parse_msg_full(v_data) if v_data else ({}, [])
    
    missing_keys = [num for num in e_order if num not in v_entries]
    
    # Check format specifier differences: e.g. %d in ecco vs hardcoded number in vfs
    format_diffs = []
    for num in e_entries:
        if num in v_entries:
            e_snd, e_txt = e_entries[num]
            v_snd, v_txt = v_entries[num]
            if '%d' in e_txt and '%d' not in v_txt:
                format_diffs.append((num, v_txt, e_txt))
            elif e_txt.strip() != v_txt.strip() and num < 7000:
                # Other text difference in quest/mechanic lines
                pass

    if missing_keys or format_diffs:
        results[k] = {
            'status': 'NEEDS_UPDATE',
            'missing_count': len(missing_keys),
            'missing_keys': missing_keys,
            'format_diffs': format_diffs,
            'source': os.path.basename(v_info['source'])
        }

print(f"\nFiles requiring updates: {len(results)}")
for k, data in results.items():
    print(f"\n=== {k} (source: {data['source']}) ===")
    print(f"  Missing lines from EcCo: {data['missing_count']} lines: {data['missing_keys'][:10]} ...")
    if data['format_diffs']:
        print(f"  Dynamic format specifier lines (%d): {len(data['format_diffs'])}")
        for num, v_txt, e_txt in data['format_diffs']:
            print(f"    [{num}] VFS: {v_txt} -> EcCo: {e_txt}")
