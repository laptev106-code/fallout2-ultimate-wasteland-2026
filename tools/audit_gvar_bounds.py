import sys, os, struct
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
scripts = [k for k in vfs if k.startswith('scripts\\') and k.endswith('.int')]

# Total GVARs in vault13.gam
v13_info = vfs.get('data\\vault13.gam')
txt, _ = efa.read_vfs_text(v13_info)
gvar_count = len([l for l in txt.splitlines() if ':=' in l])
print(f"Total GVARs in vault13.gam: {gvar_count} (valid range: 0..{gvar_count-1})")

# In Fallout INT opcode set:
# opcode 0x80C6 = set_global_var(gvar, val)
# opcode 0x80C5 = global_var(gvar)

oob_gvars = []

for s in scripts:
    info = vfs[s]
    if info.get('is_disk'):
        with open(info['disk_path'], 'rb') as f:
            data = f.read()
    else:
        data = efa.extract_dat2_file(info)
    if not data:
        continue

    # Search for opcodes 0x80C6 and 0x80C5
    for i in range(len(data) - 1):
        op = (data[i] << 8) | data[i+1]
        if op in [0x80C5, 0x80C6]:
            # Look backwards for pushed constant (0xC001)
            # In SSLC, for set_global_var(gvar, val):
            # args are pushed: gvar, then val, then 0x80C6 (or val then gvar)
            window = data[max(0, i-25):i]
            for j in range(len(window)-5):
                if window[j] == 0xC0 and window[j+1] == 0x01:
                    val = struct.unpack('>i', window[j+2:j+6])[0]
                    if val >= gvar_count and val < 50000:
                        dist = len(window) - j
                        if dist <= 14:
                            oob_gvars.append((s, hex(i), op, val))

print(f"Audited {len(scripts)} scripts for out-of-bounds GVAR accesses.")
print(f"Potential OOB GVAR accesses: {len(oob_gvars)}")
for s, off, op, val in oob_gvars[:20]:
    op_name = 'set_global_var' if op == 0x80C6 else 'global_var'
    print(f"  {s} at {off}: {op_name} with GVAR index {val} (>= {gvar_count})!")
