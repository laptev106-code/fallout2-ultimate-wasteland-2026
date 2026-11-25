from audit_weapon_anim_collision import extract_file, base
import os

for fname in ["data/aibdymsg.txt", "data/aigenmsg.txt"]:
    f_rpu = extract_file(os.path.join(base, "rpu.dat"), fname)
    f_miria = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), fname)
    f_rus = extract_file(os.path.join(base, "rpu_russian.dat"), fname)
    
    print(f"=== {fname} ===")
    print(f"  RPU size: {len(f_rpu) if f_rpu else 'None'}")
    print(f"  Miria size: {len(f_miria) if f_miria else 'None'}")
    print(f"  Russian size: {len(f_rus) if f_rus else 'None'}")
    if f_miria and f_rpu:
        lines_rpu = f_rpu.decode('latin1').splitlines()
        lines_miria = f_miria.decode('latin1').splitlines()
        print(f"  Lines in RPU: {len(lines_rpu)} vs Miria: {len(lines_miria)}")
        added = [l for l in lines_miria if l not in lines_rpu]
        print(f"  Added lines in Miria: {len(added)}")
        for a in added[:5]:
            print("   +", a)
