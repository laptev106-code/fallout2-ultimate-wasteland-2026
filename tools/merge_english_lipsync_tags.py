import os, re, sys
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import read_vfs_text, read_dat2_directory

def parse_msg_lines(text):
    pattern = r'\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}'
    return list(re.finditer(pattern, text, re.DOTALL))

gp = r'E:\Fallout2_Ultimate\Fallout2_Gameplay'
patch_dat = os.path.join(gp, 'mods', 'talking_heads_that_rpu_map_update_patch.dat')
entries = read_dat2_directory(patch_dat)

for fname, tag_prefix in [('vcdrtroy.msg', 'TROY'), ('mcmiria.msg', 'MIRIA')]:
    p_rel = f'text\\english\\dialog\\{fname}'
    if p_rel not in entries:
        print(f'{p_rel} not in patch DAT')
        continue
    patch_text, _ = read_vfs_text(entries[p_rel])
    patch_matches = parse_msg_lines(patch_text)
    tags_map = {}
    for m in patch_matches:
        num = int(m.group(1))
        tag = m.group(2).strip()
        if tag.upper().startswith(tag_prefix.upper()):
            tags_map[num] = tag
            
    print(f'{fname}: extracted {len(tags_map)} english tags from patch DAT.')
    
    for base in [r'E:\Fallout2_Ultimate\Fallout2_Gameplay', r'E:\Fallout2_Ultimate\Fallout2_HD']:
        target_path = os.path.join(base, 'mods', 'rpu_russian_uncensored.dat', p_rel)
        if not os.path.exists(target_path):
            continue
        with open(target_path, 'r', encoding='latin1') as f:
            target_content = f.read()
            
        def replacer(match):
            num = int(match.group(1))
            cur_tag = match.group(2).strip()
            content = match.group(3)
            if num in tags_map:
                new_tag = tags_map[num]
                return f'{{{num}}}{{{new_tag}}}{{{content}}}'
            return match.group(0)
            
        new_content = re.sub(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}', replacer, target_content, flags=re.DOTALL)
        
        with open(target_path, 'w', encoding='latin1', newline='\r\n') as f:
            f.write(new_content)
        print(f'Successfully updated English {target_path}')
