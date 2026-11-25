import re, os

def update_f2_res(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    settings = {
        "SCR_WIDTH": 1280,
        "SCR_HEIGHT": 720,
        "SCALE_2X": 1,
        "GRAPHICS_MODE": 0,
        "WINDOWED": 0,
        "WINDOWED_FULLSCREEN": 0,
        "EXTRA_WIN_MSG_CHECKS": 0,
        "SCALE_BUTTONS_AND_TEXT_MENU": 0
    }
    
    seen = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        matched = False
        for k, v in settings.items():
            if stripped.startswith(f"{k}=") or stripped.startswith(f"{k} ="):
                if k not in seen:
                    new_lines.append(f"{k}={v}\n")
                    seen.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)
            
    for k, v in settings.items():
        if k not in seen:
            new_lines.append(f"{k}={v}\n")
            
    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.writelines(new_lines)
    print(f"Updated {file_path}")

for root in ["E:/Fallout2_Ultimate/Fallout2_Gameplay", "E:/Fallout2_Ultimate/Fallout2_HD"]:
    update_f2_res(os.path.join(root, "f2_res.ini"))
