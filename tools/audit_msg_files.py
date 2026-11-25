import os
import re

dialog_dir = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog"

def audit_msg(filepath):
    errors = []
    line_re = re.compile(r'^\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*)\}')
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Check encoding
    try:
        text = raw.decode('windows-1251')
    except UnicodeDecodeError as e:
        errors.append(f"CP1251 Decode Error: {e}")
        return errors
        
    lines = text.splitlines()
    msg_ids = set()
    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = line_re.match(line)
        if not m:
            # Check if it's a broken msg line
            if line.startswith('{'):
                errors.append(f"Line {idx}: Malformed format: {line[:50]}")
            continue
        num, sound, content = int(m.group(1)), m.group(2), m.group(3)
        if num in msg_ids:
            errors.append(f"Line {idx}: Duplicate ID {{{num}}}")
        msg_ids.add(num)
        
        # Check unclosed braces
        if content.count('{') != content.count('}'):
            errors.append(f"Line {idx}: Unbalanced braces in content: {line[:60]}")
            
    return errors

for fname in os.listdir(dialog_dir):
    if fname.lower().endswith('.msg'):
        full = os.path.join(dialog_dir, fname)
        errs = audit_msg(full)
        if errs:
            print(f"FAILED: {fname} ({len(errs)} issues):")
            for e in errs[:5]:
                print(f"  {e}")
        else:
            print(f"OK: {fname}")
