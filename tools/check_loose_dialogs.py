import os
import sys

sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from audit_all_texts import read_dat

def compare_file(msg_name):
    print(f"\n=================== {msg_name} ===================")
    rpu_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
    rpu_rus_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
    data_rus = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog", msg_name)
    data_eng = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\english\dialog", msg_name)
    uncensored_rus = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\text\russian\dialog", msg_name)

    print(f"data_rus exists: {os.path.exists(data_rus)}")
    print(f"data_eng exists: {os.path.exists(data_eng)}")
    print(f"uncensored_rus exists: {os.path.exists(uncensored_rus)}")

for f in ["mcmiria.msg", "vccasidy.msg", "vcdrtroy.msg", "mccornel.msg", "kcdunton.msg", "kctorr.msg", "door.msg"]:
    compare_file(f)
