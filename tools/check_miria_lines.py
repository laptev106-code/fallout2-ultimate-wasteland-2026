with open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog\mcmiria.msg", 'r', encoding='cp1251') as f:
    r_lines = f.read()

for num in [270, 280, 420, 470]:
    print(f"Line {num} in Russian mcmiria.msg:", f"{{{num}}}" in r_lines)
