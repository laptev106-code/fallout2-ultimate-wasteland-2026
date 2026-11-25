import sys
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools")
from check_ecpariah_msg import get_msg_from_dat
import re

RPU_ENG_DAT = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
raw = get_msg_from_dat(RPU_ENG_DAT, "scripts/artemple.int")
if raw:
    print(f"artemple.int size: {len(raw)} bytes")
    strings = re.findall(b"[a-zA-Z0-9_]{3,}", raw)
    print("Strings:", [s.decode('ascii') for s in strings])
else:
    print("Not found in rpu.dat")
