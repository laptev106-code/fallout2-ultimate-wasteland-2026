import os, re, sys
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import read_vfs_text, read_dat2_directory

gp = r'E:\Fallout2_Ultimate\Fallout2_Gameplay'
patch_dat = os.path.join(gp, 'mods', 'talking_heads_that_rpu_map_update_patch.dat')
th_dat = os.path.join(gp, 'mods', 'talking_heads.dat')
p_entries = read_dat2_directory(patch_dat)
th_entries = read_dat2_directory(th_dat)

test_files = ['door.msg', 'ecpariah.msg', 'kcdunton.msg', 'kctorr.msg', 'mccornel.msg', 'mcmiria.msg', 'vccasidy.msg', 'vcdrtroy.msg']

for fn in test_files:
    p_ru = os.path.join('text', 'russian', 'dialog', fn)
    tag_p = 0
    tag_th = 0
    if p_ru in p_entries:
        txt, _ = read_vfs_text(p_entries[p_ru])
        tag_p = len(re.findall(r'\{(\d+)\}\{([A-Za-z0-9_]+)\}', txt))
    if p_ru in th_entries:
        txt, _ = read_vfs_text(th_entries[p_ru])
        tag_th = len(re.findall(r'\{(\d+)\}\{([A-Za-z0-9_]+)\}', txt))
    print(f'{fn:15} | patch_tags: {tag_p:3} | th_tags: {tag_th:3}')
