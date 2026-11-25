import re

with open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog\kctorr.msg", "r", encoding="cp1251") as f:
    rus_torr = f.read()

entries = re.findall(r"\{(\d+)\}\{[^}]*\}\{([^}]*)\}", rus_torr)
for num, text in entries:
    if int(num) in [247, 248, 256, 257, 900, 901, 902, 903]:
        print(f"{{{num}}}{{}}{{{text}}}")
