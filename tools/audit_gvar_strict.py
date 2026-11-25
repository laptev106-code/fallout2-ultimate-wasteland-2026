import sys, os, struct
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
scripts = [k for k in vfs if k.startswith('scripts\\') and k.endswith('.int')]

v13_info = vfs.get('data\\vault13.gam')
txt, _ = efa.read_vfs_text(v13_info)
gvar_count = len([l for l in txt.splitlines() if ':=' in l])
print(f"Total GVARs in vault13.gam: {gvar_count}")

real_oob_gvars = []

for s in scripts:
    info = vfs[s]
    if info.get('is_disk'):
        with open(info['disk_path'], 'rb') as f:
            data = f.read()
    else:
        data = efa.extract_dat2_file(info)
    if not data:
        continue

    # 1. global_var(gvar) -> [C0 01 gvar] 80 C5
    for i in range(len(data) - 1):
        if data[i] == 0x80 and data[i+1] == 0xC5:
            # Check if immediately preceded by C0 01 [4 bytes]
            if i >= 6 and data[i-6] == 0xC0 and data[i-5] == 0x01:
                gvar_id = struct.unpack('>i', data[i-4:i])[0]
                if gvar_id < 0 or gvar_id >= gvar_count:
                    real_oob_gvars.append((s, hex(i), 'global_var', gvar_id))

        # 2. set_global_var(gvar, val) -> [C0 01 gvar] [value expr] 80 C6
        if data[i] == 0x80 and data[i+1] == 0xC6:
            # Check if preceded by [C0 01 gvar] [C0 01 val]
            if i >= 12 and data[i-12] == 0xC0 and data[i-11] == 0x01 and data[i-6] == 0xC0 and data[i-5] == 0x01:
                gvar_id = struct.unpack('>i', data[i-10:i-6])[0]
                if gvar_id < 0 or gvar_id >= gvar_count:
                    real_oob_gvars.append((s, hex(i), 'set_global_var', gvar_id))

print(f"Audited {len(scripts)} scripts with strict opcode layout.")
print(f"Verified Out-Of-Bounds GVAR accesses: {len(real_oob_gvars)}")
for s, off, op, val in real_oob_gvars[:20]:
    print(f"  {s} at {off}: {op} with GVAR index {val} (>= {gvar_count})!")
