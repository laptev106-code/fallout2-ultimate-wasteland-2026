from audit_maps_quests import extract_file, base
import os

for root, dirs, files in os.walk(r"E:\Fallout2_Ultimate\Fallout2_Gameplay"):
    for f in files:
        if f.lower().endswith(".dat"):
            p = os.path.join(root, f)
            data = extract_file(p, "text/english/game/quests.msg") or extract_file(p, "text/english/game/quest.msg") or extract_file(p, "text/russian/game/quests.msg") or extract_file(p, "text/russian/game/quest.msg")
            if data:
                print(f"Found in {f}: {len(data)} bytes")
