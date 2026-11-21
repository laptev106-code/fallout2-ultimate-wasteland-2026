import os, sys, json
sys.path.insert(0, r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen")
from main import LauncherBridge

print("=== TESTING LAUNCHER BRIDGE READ/SAVE ===")
bridge = LauncherBridge(r"E:\Fallout2_Ultimate")

# 1. Read config
cfg = bridge.read_config()
print("Initial config read:", cfg)

# 2. Modify settings
test_cfg = {
    "resolution": "1920x1080",
    "mode": "fullscreen",
    "scale": "2x",
    "filtering": "bilinear",
    "musicVol": 85,
    "sfxVol": 75,
    "alwaysRun": True,
    "autoReload": True,
    "templeTutorial": True
}
res = bridge.save_config(test_cfg)
print("Save config result:", res)

# 3. Read back config
cfg2 = bridge.read_config()
print("Read back config:", cfg2)

# Assertions
assert cfg2["resolution"] == "1920x1080", f"Resolution mismatch: {cfg2['resolution']}"
assert cfg2["alwaysRun"] is True, "alwaysRun mismatch"
assert cfg2["autoReload"] is True, "autoReload mismatch"
assert cfg2["templeTutorial"] is True, "templeTutorial mismatch"
assert cfg2["musicVol"] == 85, "musicVol mismatch"

# 4. Verify ddraw.ini TempleTutorial=1
with open(os.path.join(bridge.gameplay_dir, "ddraw.ini"), "r", encoding="cp1251", errors="ignore") as f:
    ddraw_txt = f.read()
assert "TempleTutorial=1" in ddraw_txt, "TempleTutorial=1 missing in ddraw.ini"

# 5. Verify fallout2.cfg running=1
with open(os.path.join(bridge.gameplay_dir, "fallout2.cfg"), "r", encoding="utf-8", errors="ignore") as f:
    cfg_txt = f.read()
assert "running=1" in cfg_txt, "running=1 missing in fallout2.cfg"

# 6. Verify fo2tweaks.ini auto_reload=1
with open(os.path.join(bridge.gameplay_dir, "mods", "fo2tweaks.ini"), "r", encoding="utf-8", errors="ignore") as f:
    tweaks_txt = f.read()
assert "auto_reload=1" in tweaks_txt or "auto_reload = 1" in tweaks_txt, "auto_reload=1 missing in fo2tweaks.ini"

print("ALL BRIDGE READ/SAVE ASSERTIONS PASSED CLEANLY (100% GREEN)!")
