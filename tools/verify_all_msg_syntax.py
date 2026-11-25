import sys, os, re
sys.path.insert(0, '.')
import tools.engine_full_audit as efa

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
all_msgs = [k for k in vfs if k.startswith('text\\russian\\') and k.endswith('.msg')]

print(f"Verifying syntax across ALL {len(all_msgs)} Russian message files...")

errors = []

for m_path in all_msgs:
    info = vfs[m_path]
    txt, _ = efa.read_vfs_text(info)
    if not txt:
        errors.append((m_path, 0, "Empty or unreadable file"))
        continue

    lines = txt.splitlines()
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean or line_clean.startswith(';') or line_clean.startswith('#'):
            continue
        
        # Check braces
        o_brace = line_clean.count('{')
        c_brace = line_clean.count('}')
        if o_brace != c_brace:
            errors.append((m_path, i + 1, f"Mismatched braces ({o_brace} vs {c_brace}): {line_clean[:60]}"))
        elif o_brace < 3 and not line_clean.startswith('//'):
            # Fallout msg format is {num}{sound}{text}
            # Some multi-line entries exist, check if it's part of a multi-line entry
            pass

print(f"Total syntax issues found: {len(errors)}")
for p, l_num, err in errors:
    print(f"  {p}:{l_num} -> {err}")
