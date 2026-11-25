import re, os

def update_ini(file_path, settings):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="cp1251", errors="ignore") as f:
        content = f.read()
    
    for key, val in settings.items():
        pattern = rf"(?m)^({re.escape(key)}\s*=).*$"
        if re.search(pattern, content):
            content = re.sub(pattern, rf"\g<1>{val}", content)
        else:
            content += f"\n{key}={val}\n"
            
    with open(file_path, "w", encoding="cp1251", errors="ignore") as f:
        f.write(content)
    print(f"Updated {file_path}")

settings = {
    "Mode": 6,
    "GraphicsWidth": 0,
    "GraphicsHeight": 0,
    "TextureFilter": 2,
    "WindowData": 0,
    "BackgroundKeyboard": 1,
    "BackgroundMouse": 1,
    "SpeedInventoryPCRotation": 600,
    "CombatPanelAnimDelay": 90,
    "WorldMapEncounterRate": 14,
    "SkipCompatModeCheck": 1
}

for root in ["E:/Fallout2_Ultimate/Fallout2_Gameplay", "E:/Fallout2_Ultimate/Fallout2_HD"]:
    update_ini(os.path.join(root, "ddraw.ini"), settings)
