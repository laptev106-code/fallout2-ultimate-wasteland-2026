from audit_maps_quests import extract_file, base
import os

patch_torr_msg = extract_file(os.path.join(base, "talking_heads_that_rpu_map_update_patch.dat"), "text/russian/dialog/kctorr.msg")
th_torr_msg = extract_file(os.path.join(base, "talking_heads.dat"), "text/english/dialog/kctorr.msg")
uncens_torr_msg = open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog\kctorr.msg", "rb").read()

print("Patch msg size:", len(patch_torr_msg) if patch_torr_msg else "None")
print("TH msg size:", len(th_torr_msg) if th_torr_msg else "None")
print("Uncensored msg size:", len(uncens_torr_msg))

# Check for TORR tags in uncensored vs patch
import re
tags_uncens = re.findall(r"\{[A-Z0-9_]+\}", uncens_torr_msg.decode('cp1251', errors='ignore'))
print(f"Tags in uncensored: {len(tags_uncens)} -> Sample: {tags_uncens[:10]}")

if patch_torr_msg:
    tags_patch = re.findall(r"\{[A-Z0-9_]+\}", patch_torr_msg.decode('cp1251', errors='ignore'))
    print(f"Tags in patch: {len(tags_patch)} -> Sample: {tags_patch[:10]}")
