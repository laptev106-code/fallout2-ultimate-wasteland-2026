import sys, os, re
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
ru_dialogs = [k for k in vfs if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]

print(f"Auditing ALL {len(ru_dialogs)} Russian dialog files in VFS...")

corrupted_encoding = []
syntax_errors = []
total_entries = 0

entry_pattern = re.compile(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}')

for d in ru_dialogs:
    info = vfs[d]
    if info.get('is_disk'):
        with open(info['disk_path'], 'rb') as f:
            raw = f.read()
    else:
        raw = efa.extract_dat2_file(info)
    if not raw:
        syntax_errors.append((d, 'Empty file or unreadable'))
        continue

    # Try CP1251
    try:
        decoded = raw.decode('cp1251')
    except UnicodeDecodeError as e:
        corrupted_encoding.append((d, str(e)))
        decoded = raw.decode('cp1251', errors='ignore')

    matches = list(entry_pattern.finditer(decoded))
    total_entries += len(matches)
    
    # Check braces count
    c_open = decoded.count('{')
    c_close = decoded.count('}')
    if c_open != c_close:
        syntax_errors.append((d, f"Mismatched braces: {c_open} open vs {c_close} close"))

print(f"Audit completed: {len(ru_dialogs)} files, {total_entries} total dialogue entries.")
print(f"Files with encoding corruption: {len(corrupted_encoding)}")
for d, err in corrupted_encoding:
    print(f"  {d}: {err}")

print(f"Files with syntax errors (mismatched braces): {len(syntax_errors)}")
for d, err in syntax_errors[:15]:
    print(f"  {d}: {err}")
