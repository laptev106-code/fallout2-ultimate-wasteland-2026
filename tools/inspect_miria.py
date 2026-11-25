import os

def check_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='latin1') as f:
            lines = f.readlines()
        print(f"{path}: {len(lines)} lines")
        # Print last 10 lines
        for l in lines[-10:]:
            print("  ", l.strip())

check_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\russian\dialog\mcmiria.msg")
check_file(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text\english\dialog\mcmiria.msg")
