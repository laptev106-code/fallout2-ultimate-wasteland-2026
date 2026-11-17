"""
Surgical Configurator & INI Tuning Engine
"""

import os
import re
from typing import Dict, Any, List

class Configurator:
    @staticmethod
    def patch_ini_key(content: str, section: str, key: str, value: Any) -> str:
        """Безопасно обновляет или добавляет ключ в INI файл."""
        lines = content.splitlines()
        section_pattern = re.compile(rf"^\s*\[{re.escape(section)}\]\s*$", re.IGNORECASE)
        key_pattern = re.compile(rf"^\s*{re.escape(key)}\s*=.*$", re.IGNORECASE)
        
        in_target_section = False
        key_replaced = False
        new_lines = []
        
        for line in lines:
            if line.strip().startswith("[") and line.strip().endswith("]"):
                if in_target_section and not key_replaced:
                    new_lines.append(f"{key}={value}")
                    key_replaced = True
                in_target_section = bool(section_pattern.match(line))
                new_lines.append(line)
                continue
                
            if in_target_section and key_pattern.match(line):
                new_lines.append(f"{key}={value}")
                key_replaced = True
                continue
                
            new_lines.append(line)
            
        if in_target_section and not key_replaced:
            new_lines.append(f"{key}={value}")
            key_replaced = True
        elif not in_target_section and not key_replaced:
            new_lines.append(f"\n[{section}]")
            new_lines.append(f"{key}={value}")
            
        return "\n".join(new_lines) + "\n"

    @classmethod
    def tune_ddraw_ini(cls, ddraw_path: str):
        """Настраивает sfall 4.5.1 под связку EcCo + MiniRework."""
        if not os.path.exists(ddraw_path):
            return
            
        with open(ddraw_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        content = cls.patch_ini_key(content, "Misc", "AllowUnsafeScripting", 2)
        content = cls.patch_ini_key(content, "Misc", "SpeedInterfaceCounterAnims", 2)
        content = cls.patch_ini_key(content, "Misc", "ExtraMemory", 1)
        content = cls.patch_ini_key(content, "Misc", "SkipOpeningMovies", 1)
        content = cls.patch_ini_key(content, "Graphics", "Mode", 4)  # DX9
        content = cls.patch_ini_key(content, "Graphics", "GPUMemory", 1)
        
        with open(ddraw_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def tune_minirework_ini(cls, minirework_path: str):
        """Настраивает MiniRework 2.0.4.3 для идеального симбиоза с EcCo 1.0.0."""
        if not os.path.exists(minirework_path):
            return
            
        with open(minirework_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        content = cls.patch_ini_key(content, "MAIN", "RegenMod", 0)
        content = cls.patch_ini_key(content, "MAIN", "MedToolsMod", 0)
        content = cls.patch_ini_key(content, "MAIN", "StealRebalance", 1)
        content = cls.patch_ini_key(content, "MAIN", "FO2_ECCO", 1)
        
        with open(minirework_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def tune_fo2tweaks_ini(cls, fo2tweaks_path: str):
        """
        Калибровочный профиль FO2Tweaks 14.7:
        Полное устранение конфликтов с EcCo и исключение читов.
        """
        if not os.path.exists(fo2tweaks_path):
            return
            
        with open(fo2tweaks_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Настройки совместимости с балансом EcCo
        ecco_compatibility_params = {
            "max_knockback": -1,
            "healing_revision": 0,
            "molotov_fire": 0,
            "damage_mod": 0,
            "ap_rollover": 0,
            "no_scope_penalty": 0,
            "improved_grenades": 0,
            "autodoors": 1,
            "ammobox": 1,
            "highlighting": 1,
            "auto_reload": 1,
            "modoc_brahmin": 1,
            "no_drop_items_on_death": 1,
            "carry_weight": 0,
            "trunk_space": 0,
            "unlimited_party": 0,
            "party_level_match": 0,
            "speedup": 0,
            "run_speed": 0
        }
        
        for k, v in ecco_compatibility_params.items():
            content = cls.patch_ini_key(content, "main", k, v)
            
        with open(fo2tweaks_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def write_mods_order(cls, mods_dir: str):
        """Создает детерминированный список приоритетов загрузки в mods_order.txt."""
        order_file = os.path.join(mods_dir, "mods_order.txt")
        order_content = (
            "# Fallout 2: Ultimate Mega Rework 2026 - Master Priority Order\n"
            "rpu\n"
            "rpu_translations\n"
            "ecco\n"
            "ecco_hf1\n"
            "that_rpu_patch\n"
            "talking_heads\n"
            "minirework\n"
            "fo2tweaks\n"
            "bunker21\n"
            "vock\n"
        )
        with open(order_file, "w", encoding="utf-8") as f:
            f.write(order_content)

    @classmethod
    def merge_scripts_lst(cls, base_scripts_path: str, add_scripts: List[str]):
        """Безопасно объединяет список скриптов без затирания таблицы RPU."""
        if not os.path.exists(base_scripts_path):
            return
            
        with open(base_scripts_path, "r", encoding="utf-8", errors="ignore") as f:
            existing = [line.strip().lower() for line in f if line.strip()]
            
        to_append = []
        for s in add_scripts:
            s_clean = s.strip()
            if s_clean and s_clean.lower() not in existing:
                to_append.append(s_clean)
                
        if to_append:
            with open(base_scripts_path, "a", encoding="utf-8") as f:
                for s in to_append:
                    f.write(f"\n{s}")
