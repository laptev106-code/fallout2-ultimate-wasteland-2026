import os, re, sys
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import read_vfs_text, read_dat2_directory

def parse_msg_lines(text):
    # returns list of (line_num, tag, text, raw_match)
    pattern = r'\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}'
    return list(re.finditer(pattern, text, re.DOTALL))

gp = r'E:\Fallout2_Ultimate\Fallout2_Gameplay'
patch_dat = os.path.join(gp, 'mods', 'talking_heads_that_rpu_map_update_patch.dat')
entries = read_dat2_directory(patch_dat)

for fname, tag_prefix in [('vcdrtroy.msg', 'TROY'), ('mcmiria.msg', 'MIRIA')]:
    p_rel = f'text\\russian\\dialog\\{fname}'
    patch_text, _ = read_vfs_text(entries[p_rel])
    patch_matches = parse_msg_lines(patch_text)
    tags_map = {}
    for m in patch_matches:
        num = int(m.group(1))
        tag = m.group(2).strip()
        if tag.upper().startswith(tag_prefix.upper()):
            tags_map[num] = tag
            
    print(f'{fname}: extracted {len(tags_map)} tags from patch DAT.')
    
    # Check against both Gameplay and HD
    for base in [r'E:\Fallout2_Ultimate\Fallout2_Gameplay', r'E:\Fallout2_Ultimate\Fallout2_HD']:
        target_path = os.path.join(base, 'mods', 'rpu_russian_uncensored.dat', p_rel)
        if not os.path.exists(target_path):
            print(f'Missing: {target_path}')
            continue
        with open(target_path, 'r', encoding='cp1251') as f:
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
        
        # Verify tag count
        new_tags = [t for n, t in re.findall(r'\{(\d+)\}\{([A-Za-z0-9_]+)\}', new_content) if t.upper().startswith(tag_prefix.upper())]
        print(f'{base[-16:]} {fname}: injected {len(new_tags)} tags. Total size: {len(new_content)}')
        
        with open(target_path, 'w', encoding='cp1251', newline='\r\n') as f:
            f.write(new_content)
        print(f'Successfully updated {target_path}')
