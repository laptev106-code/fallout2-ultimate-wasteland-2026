import os
import shutil
import re

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)

TARGET_DIRS = [
    PROJECT_ROOT,
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def update_ini_value(filepath, section, key, new_val):
    if not os.path.exists(filepath):
        print(f"[WARN] File not found: {filepath}")
        return False
        
    with open(filepath, 'r', encoding='latin-1') as f:
        lines = f.readlines()
        
    in_section = False
    key_found = False
    new_lines = []
    sec_pat = re.compile(rf'^\s*\[{re.escape(section)}\]\s*$', re.IGNORECASE)
    key_pat = re.compile(rf'^\s*{re.escape(key)}\s*=', re.IGNORECASE)
    
    for line in lines:
        if sec_pat.match(line):
            in_section = True
            new_lines.append(line)
            continue
        elif in_section and line.strip().startswith('['):
            if not key_found:
                new_lines.append(f"{key}={new_val}\n")
                key_found = True
            in_section = False
        elif in_section and key_pat.match(line):
            new_lines.append(f"{key}={new_val}\n")
            key_found = True
            continue
        new_lines.append(line)
        
    if in_section and not key_found:
        new_lines.append(f"{key}={new_val}\n")
        key_found = True
        
    with open(filepath, 'w', encoding='latin-1') as f:
        f.writelines(new_lines)
    print(f"  [OK] {os.path.basename(filepath)} [{section}] {key}={new_val}")
    return True

def apply_fixes():
    print("[*] Starting FIX-68 deployment: Mouse Cursor Smoothness & Combat Speed Up...")
    
    # 1. Deploy gl_k_walking_speed.int
    src_script = os.path.join(TOOLS_DIR, "gl_k_walking_speed.int")
    if not os.path.exists(src_script):
        print(f"[ERROR] Source script not found: {src_script}")
        return False
        
    for base_dir in TARGET_DIRS:
        scripts_dir = os.path.join(base_dir, "mods", "rpu_russian_uncensored.dat", "scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        dest_script = os.path.join(scripts_dir, "gl_k_walking_speed.int")
        shutil.copy2(src_script, dest_script)
        print(f"  [OK] Deployed gl_k_walking_speed.int -> {dest_script}")
        
        # Ensure mods\upu.ini exists
        upu_ini = os.path.join(base_dir, "mods", "upu.ini")
        if not os.path.exists(upu_ini):
            src_upu = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\upu.ini")
            if os.path.exists(src_upu):
                shutil.copy2(src_upu, upu_ini)
                print(f"  [OK] Copied upu.ini -> {upu_ini}")
        if os.path.exists(upu_ini):
            update_ini_value(upu_ini, "main", "critters_walk_faster", "1")
            update_ini_value(upu_ini, "main", "goris_derobing_speed", "50")

    # 2. Update ddraw.ini across all directories
    for base_dir in TARGET_DIRS:
        ddraw_ini = os.path.join(base_dir, "ddraw.ini")
        if os.path.exists(ddraw_ini):
            print(f"[*] Updating {ddraw_ini}...")
            # Graphics
            update_ini_value(ddraw_ini, "Graphics", "Mode", "4")
            update_ini_value(ddraw_ini, "Graphics", "GraphicsWidth", "1280")
            update_ini_value(ddraw_ini, "Graphics", "GraphicsHeight", "720")
            update_ini_value(ddraw_ini, "Graphics", "LimitFPS", "1")
            update_ini_value(ddraw_ini, "Graphics", "WindowData", "-1")
            # Input
            update_ini_value(ddraw_ini, "Input", "BackgroundMouse", "0")
            update_ini_value(ddraw_ini, "Input", "BackgroundKeyboard", "0")
            update_ini_value(ddraw_ini, "Input", "MouseSensitivity", "100")
            # Speed
            update_ini_value(ddraw_ini, "Speed", "SpeedMultiInitial", "110")
            update_ini_value(ddraw_ini, "Speed", "Enable", "0")
            # Misc
            update_ini_value(ddraw_ini, "Misc", "AnimationsAtOnceLimit", "120")
            update_ini_value(ddraw_ini, "Misc", "CombatPanelAnimDelay", "500")
            update_ini_value(ddraw_ini, "Misc", "SpeedInterfaceCounterAnims", "1")
            update_ini_value(ddraw_ini, "Misc", "DebugMode", "0")
            update_ini_value(ddraw_ini, "Misc", "SingleCore", "0")
            update_ini_value(ddraw_ini, "Misc", "ProcessorIdle", "1")

    # 3. Update f2_res.ini across all directories
    for base_dir in TARGET_DIRS:
        f2_res_ini = os.path.join(base_dir, "f2_res.ini")
        if not os.path.exists(f2_res_ini) and base_dir == PROJECT_ROOT:
            src_f2 = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\f2_res.ini")
            if os.path.exists(src_f2):
                shutil.copy2(src_f2, f2_res_ini)
                print(f"  [OK] Synchronized f2_res.ini to workspace root")
                
        if os.path.exists(f2_res_ini):
            print(f"[*] Updating {f2_res_ini}...")
            update_ini_value(f2_res_ini, "MAIN", "WINDOWED", "0")
            update_ini_value(f2_res_ini, "MAIN", "WINDOWED_FULLSCREEN", "0")
            update_ini_value(f2_res_ini, "INPUT", "EXTRA_WIN_MSG_CHECKS", "1")
            update_ini_value(f2_res_ini, "INPUT", "ALT_MOUSE_INPUT", "0")
            update_ini_value(f2_res_ini, "OTHER_SETTINGS", "CPU_USAGE_FIX", "0")

    # 4. Update fallout2.cfg across all directories
    for base_dir in TARGET_DIRS:
        fallout_cfg = os.path.join(base_dir, "fallout2.cfg")
        if not os.path.exists(fallout_cfg) and base_dir == PROJECT_ROOT:
            src_cfg = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\fallout2.cfg")
            if os.path.exists(src_cfg):
                shutil.copy2(src_cfg, fallout_cfg)
                print(f"  [OK] Synchronized fallout2.cfg to workspace root")
                
        if os.path.exists(fallout_cfg):
            print(f"[*] Updating {fallout_cfg}...")
            update_ini_value(fallout_cfg, "system", "cycle_speed_factor", "1.550000")
            update_ini_value(fallout_cfg, "preferences", "combat_speed", "50")
            update_ini_value(fallout_cfg, "preferences", "player_speedup", "1")
            update_ini_value(fallout_cfg, "preferences", "running", "1")
            update_ini_value(fallout_cfg, "preferences", "mouse_sensitivity", "1.000000")

    print("[SUCCESS] All FIX-68 files deployed and configurations updated.")
    return True

if __name__ == "__main__":
    apply_fixes()
