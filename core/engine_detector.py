"""
Engine & Clean Fallout 2 Installation Detector
"""

import os
import winreg
from typing import Optional, Dict, List

COMMON_STEAM_PATHS = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Fallout 2",
    r"D:\Steam\steamapps\common\Fallout 2",
    r"E:\Steam\steamapps\common\Fallout 2",
    r"D:\SteamLibrary\steamapps\common\Fallout 2",
    r"E:\SteamLibrary\steamapps\common\Fallout 2"
]

COMMON_GOG_PATHS = [
    r"E:\Fallout 2",
    r"D:\Fallout 2",
    r"C:\Fallout 2",
    r"E:\Games\Fallout 2",
    r"E:\Games\Fallout2",
    r"C:\GOG Games\Fallout 2",
    r"D:\GOG Games\Fallout 2",
    r"E:\GOG Games\Fallout 2",
    r"C:\Games\Fallout 2",
    r"D:\Games\Fallout 2"
]

def check_fallout_dir(path: str) -> Dict[str, bool]:
    """Проверяет корректность папки с Fallout 2."""
    if not path or not os.path.exists(path):
        return {"valid": False, "reason": "Директория не найдена"}
    
    files = [f.lower() for f in os.listdir(path)]
    has_master = "master.dat" in files
    has_critter = "critter.dat" in files
    has_exe = any(f.endswith(".exe") and "fallout" in f for f in files)
    
    if not (has_master and has_critter):
        return {
            "valid": False,
            "has_master": has_master,
            "has_critter": has_critter,
            "has_exe": has_exe,
            "reason": "Отсутствуют оригинальные игровые архивы master.dat или critter.dat"
        }
        
    # Проверка прав записи
    test_file = os.path.join(path, ".test_write_perm")
    try:
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        writable = True
    except Exception:
        writable = False
        
    return {
        "valid": True,
        "has_master": has_master,
        "has_critter": has_critter,
        "has_exe": has_exe,
        "writable": writable,
        "path": os.path.abspath(path)
    }

def autodetect_clean_fallout() -> Optional[str]:
    """Автоматически ищет установку Fallout 2 через реестр и популярные пути."""
    candidates = []
    
    # Реестр Windows (GOG & Steam)
    registry_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\GOG.com\Games\1440169206", "PATH"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GOG.com\Games\1440169206", "PATH"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Interplay\Fallout2", "Path"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Interplay\Fallout2", "Path")
    ]
    
    for hkey, subkey, val_name in registry_keys:
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                val, _ = winreg.QueryValueEx(key, val_name)
                if val and os.path.exists(val):
                    candidates.append(val)
        except Exception:
            pass
            
    candidates.extend(COMMON_STEAM_PATHS)
    candidates.extend(COMMON_GOG_PATHS)
    
    for c in candidates:
        res = check_fallout_dir(c)
        if res.get("valid"):
            return os.path.abspath(c)
            
    return None
