import os

def dump_section(ini_path, section_name):
    print(f"=== {ini_path} [{section_name}] ===")
    if not os.path.exists(ini_path):
        print("Not found")
        return
    with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
        in_sec = False
        for line in f:
            stripped = line.strip()
            if stripped.startswith("["):
                if stripped.lower() == f"[{section_name.lower()}]":
                    in_sec = True
                elif in_sec:
                    break
            elif in_sec:
                print(line.rstrip())

print("DUMPING CONTROLS CONFIGS:")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\ddraw.ini", "Input")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "highlighting")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "keymap")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "main")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "inventory")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "combat")
dump_section(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\fo2tweaks.ini", "party_orders")
