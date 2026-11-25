import os
import shutil

gameplay_uncensored = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat"
hd_uncensored = r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat"

gameplay_data = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA"
hd_data = r"E:\Fallout2_Ultimate\Fallout2_HD\DATA"

print("=== Comparing Gameplay vs HD uncensored files ===")
for root, dirs, files in os.walk(gameplay_uncensored):
    for f in files:
        gp_f = os.path.join(root, f)
        rel = os.path.relpath(gp_f, gameplay_uncensored)
        hd_f = os.path.join(hd_uncensored, rel)
        if not os.path.exists(hd_f):
            print(f"Missing in HD: {rel}")
        else:
            s_gp = os.path.getsize(gp_f)
            s_hd = os.path.getsize(hd_f)
            if s_gp != s_hd:
                print(f"Size mismatch {rel}: GP={s_gp}, HD={s_hd}")

print("\n=== Loose files in Gameplay DATA/text ===")
for root, dirs, files in os.walk(os.path.join(gameplay_data, "text")):
    for f in files:
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, gameplay_data)
        print(" ", rel)
