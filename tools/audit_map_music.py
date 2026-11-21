import os, sys, re
sys.path.append(r'D:\AG games mods\fallout2-ultimate-wasteland-2026\tools')
from engine_full_audit import build_profile_vfs, read_dat2_directory, read_vfs_text

print('=== AUDIT: MAP MUSIC TRACKS ===')

def check_map_music(pname, pdir):
    vfs, collisions, order, stats = build_profile_vfs(pdir)
    master_entries = read_dat2_directory(os.path.join(pdir, 'master.dat'))
    
    # Check maps.txt
    maps_txt_info = vfs.get(r'data\maps.txt')
    if not maps_txt_info:
        print(f'[{pname}] maps.txt not in VFS, checking master.dat')
        maps_txt_info = master_entries.get(r'data\maps.txt')
        
    if not maps_txt_info:
        print(f'[{pname}] maps.txt not found!')
        return
        
    txt, _ = read_vfs_text(maps_txt_info)
    
    # Look for music= lines
    music_tracks = set()
    for line in txt.splitlines():
        line = line.strip()
        if line.lower().startswith('music='):
            track = line.split('=')[1].strip().lower()
            if track:
                music_tracks.add(track)
                
    print(f'[{pname}] Found {len(music_tracks)} unique music tracks referenced in maps.txt:')
    
    # Check if they exist in data/sound/music or VFS
    music_dir = os.path.join(pdir, 'data', 'sound', 'music')
    disk_tracks = set(f.lower() for f in os.listdir(music_dir)) if os.path.exists(music_dir) else set()
    
    missing_tracks = []
    for t in music_tracks:
        # Check track with .acm
        acm_name = t if t.endswith('.acm') else f'{t}.acm'
        in_disk = acm_name in disk_tracks
        in_vfs = f'sound\\music\\{acm_name}' in vfs
        in_master = f'sound\\music\\{acm_name}' in master_entries
        if not in_disk and not in_vfs and not in_master:
            missing_tracks.append(t)
            
    print(f'[{pname}] Missing music tracks: {len(missing_tracks)}')
    if missing_tracks:
        print('  Missing tracks:', missing_tracks)

check_map_music('Gameplay', r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
check_map_music('HD', r'E:\Fallout2_Ultimate\Fallout2_HD')
