with open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\scripts\gl_glasses.int", "rb") as f:
    data = f.read()

# Find strings in binary
import re
strings = re.findall(b"[\x20-\x7E\x80-\xFF]{4,}", data)
for s in strings:
    try:
        print("CP1251:", s.decode('cp1251'))
    except:
        print("Raw:", s)
