with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_g_highlighting.tssl", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find("function is_door")
if idx != -1:
    print(text[idx:idx+500])
else:
    print("is_door not found in gl_g_highlighting.tssl, searching in fo2tweaks.ts")
