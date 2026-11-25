import os
import re

loose_base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog"
uncensored_base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog"

files = ["kcdunton.msg", "kctorr.msg", "mccornel.msg", "vccasidy.msg", "vcdrtroy.msg", "mcmiria.msg", "door.msg"]

for fn in files:
    p = os.path.join(loose_base, fn)
    if not os.path.exists(p):
        p = os.path.join(uncensored_base, fn)
    if os.path.exists(p):
        with open(p, 'r', encoding='cp1251', errors='ignore') as f:
            content = f.read()
        entries = re.findall(r"\{(\d+)\}\{[^}]*\}\{([^}]*)\}", content)
        print(f"\n=== {fn} ({len(entries)} entries) ===")
        # Print numbers > 500 or modded sections
        high_entries = [(num, text) for num, text in entries if int(num) >= 500 or (fn=="kctorr.msg" and int(num) in [120, 122, 130, 132, 140, 142, 150, 152, 160, 162])]
        print(f"Custom/Extended lines: {len(high_entries)}")
        for num, text in high_entries:
            print(f"  {{{num}}}{{}}{{{text}}}")
