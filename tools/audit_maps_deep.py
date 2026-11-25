import sys
sys.path.insert(0, '.')
import tools.engine_full_audit as efa
import os, re

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
maps_info = vfs.get('data\\maps.txt')
scripts_info = vfs.get('scripts\\scripts.lst')

maps_txt, _ = efa.read_vfs_text(maps_info)
scripts_txt, _ = efa.read_vfs_text(scripts_info)

script_lines = [l.strip().split(';')[0].strip().lower() for l in scripts_txt.splitlines() if l.strip() and not l.strip().startswith(';')]
script_names = set(script_lines)

# Parse maps.txt
pattern = re.compile(r'\[Map\s*(\d+)\]([^\[]+)', re.IGNORECASE)
missing_scripts = []
missing_map_files = []
total_maps = 0

for m in pattern.finditer(maps_txt):
    total_maps += 1
    map_id = int(m.group(1))
    body = m.group(2)
    name_m = re.search(r'map_name\s*=\s*([^\r\n]+)', body, re.IGNORECASE)
    script_m = re.search(r'script\s*=\s*([^\r\n]+)', body, re.IGNORECASE)
    lookup_name_m = re.search(r'lookup_name\s*=\s*([^\r\n]+)', body, re.IGNORECASE)
    
    map_name = name_m.group(1).strip() if name_m else None
    script_name = script_m.group(1).strip().lower() if script_m else None
    
    # Check map file presence in VFS
    if map_name:
        map_file = map_name if map_name.lower().endswith('.map') else (map_name + '.map')
        if map_file.lower().endswith('.map.map'):
            map_file = map_file[:-4]
        map_rel = f"maps\\{map_file.lower()}"
        # In Fallout 2, master.dat or mods contain maps
        if map_rel not in vfs:
            missing_map_files.append((map_id, map_file))
        
    if script_name and script_name not in ['-1', 'none', '']:
        script_name_int = script_name if script_name.endswith('.int') else (script_name + '.int')
        if script_name_int not in script_names:
            missing_scripts.append((map_id, map_name, script_name))

print(f"Total maps defined in maps.txt: {total_maps}")
print(f"Missing map scripts in scripts.lst: {len(missing_scripts)}")
for m_id, m_name, s_name in missing_scripts:
    print(f"  Map {m_id} ({m_name}): script '{s_name}' NOT in scripts.lst!")

print(f"Maps defined without .map file in VFS: {len(missing_map_files)}")
for m_id, l_name in missing_map_files:
    print(f"  Map {m_id}: 'maps/{l_name}.map' not found in VFS")
