with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_g_highlighting.tssl", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# find get_color function
idx = text.find("function get_color")
if idx != -1:
    print(text[idx:idx+1500])
