with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\main.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Reading TempleTutorial from ddraw.ini
target_read = """        cfg["autoReload"] = False
        if os.path.exists(fo2tweaks_cfg):
            try:
                with open(fo2tweaks_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("auto_reload="):
                            cfg["autoReload"] = line.split("=")[1].strip() == "1"
            except Exception:
                pass"""

new_read = """        cfg["autoReload"] = False
        if os.path.exists(fo2tweaks_cfg):
            try:
                with open(fo2tweaks_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("auto_reload="):
                            cfg["autoReload"] = line.split("=")[1].strip() == "1"
            except Exception:
                pass

        # 5. Temple Tutorial in ddraw.ini
        cfg["templeTutorial"] = True
        ddraw_cfg = os.path.join(self.gameplay_dir, "ddraw.ini")
        if os.path.exists(ddraw_cfg):
            try:
                with open(ddraw_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("TempleTutorial="):
                            cfg["templeTutorial"] = line.split("=")[1].strip() == "1"
            except Exception:
                pass"""

code = code.replace(target_read, new_read)

# 2. Writing TempleTutorial to ddraw.ini
target_write = """            auto_reload_val = 1 if cfg.get("autoReload", False) else 0
            running_val = 1 if cfg.get("alwaysRun", True) else 0"""

new_write = """            auto_reload_val = 1 if cfg.get("autoReload", False) else 0
            running_val = 1 if cfg.get("alwaysRun", True) else 0
            temple_tut_val = 1 if cfg.get("templeTutorial", True) else 0"""

code = code.replace(target_write, new_write)

target_ddraw_write = """                    "Mode": ddraw_mode,
                    "GraphicsWidth": ddraw_gw,
                    "GraphicsHeight": ddraw_gh,
                    "GPUBlt": ddraw_gpublt,
                    "TextureFilter": ddraw_filter"""

new_ddraw_write = """                    "Mode": ddraw_mode,
                    "GraphicsWidth": ddraw_gw,
                    "GraphicsHeight": ddraw_gh,
                    "GPUBlt": ddraw_gpublt,
                    "TextureFilter": ddraw_filter,
                    "TempleTutorial": temple_tut_val"""

code = code.replace(target_ddraw_write, new_ddraw_write)

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\main.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated launcher_nextgen/main.py successfully!")
