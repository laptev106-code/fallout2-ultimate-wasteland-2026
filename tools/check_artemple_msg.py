import sys
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from check_ecpariah_msg import get_msg_from_dat

RPU_ENG_DAT = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
RPU_RUS_DAT = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"

eng_msg = get_msg_from_dat(RPU_ENG_DAT, "text/english/dialog/artemple.msg")
rus_msg = get_msg_from_dat(RPU_RUS_DAT, "text/russian/dialog/artemple.msg")

print("=== English artemple.msg ===")
if eng_msg:
    print(eng_msg.decode('latin1'))

print("=== Russian artemple.msg ===")
if rus_msg:
    print(rus_msg.decode('cp1251'))
