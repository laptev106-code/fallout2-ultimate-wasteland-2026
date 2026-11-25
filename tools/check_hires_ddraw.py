with open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\ddraw.ini", "r", encoding="cp1251", errors="ignore") as f:
    for line in f:
        if "hires" in line.lower():
            print(line.strip())
