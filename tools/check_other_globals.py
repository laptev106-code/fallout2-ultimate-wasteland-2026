for name in ["gl_highlighting.ssl", "gl_laststand.ssl"]:
    p = os.path.join(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools", name)
    if os.path.exists(p):
        with open(p, 'r', encoding='cp1251', errors='ignore') as f:
            lines = [l.strip() for l in f if "display_msg" in l]
        print(f"=== {name} display_msg calls ===")
        for l in lines:
            print(" ", l)
