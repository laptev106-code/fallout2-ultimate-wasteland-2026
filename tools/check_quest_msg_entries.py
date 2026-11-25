from audit_maps_quests import extract_file, base
import os

quest_ids_to_check = [421, 509, 513, 1120, 1121, 1122, 1123, 1411]

# Check quest.msg in rpu.dat and rpu_russian.dat and rpu_y_ecco.dat
for q_dat in ["rpu.dat", "rpu_russian.dat", "rpu_y_ecco.dat"]:
    q_file = "text/english/game/quest.msg" if "russian" not in q_dat else "text/russian/game/quest.msg"
    data = extract_file(os.path.join(base, q_dat), q_file)
    if not data:
        q_file = "text/russian/game/quest.msg"
        data = extract_file(os.path.join(base, q_dat), q_file)
    if data:
        text = data.decode('cp1251' if "russian" in q_dat else 'latin1', errors='replace')
        print(f"=== {q_dat} ({q_file}) ===")
        for q_id in quest_ids_to_check:
            found = False
            for line in text.splitlines():
                if line.strip().startswith(f"{{{q_id}}}"):
                    print(f"  Found {{{q_id}}}: {line.strip()[:60]}")
                    found = True
                    break
            if not found:
                print(f"  MISSING {{{q_id}}}!")
    else:
        print(f"=== {q_dat}: quest.msg not found ===")
