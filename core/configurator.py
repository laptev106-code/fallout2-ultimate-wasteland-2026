"""
Surgical Configurator & INI Tuning Engine
"""

import os
import re
from typing import Dict, Any

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
            # Секция не найдена — добавляем в конец
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
            
        # Критические настройки sfall
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
        """Отключает дублирующие боевые модули в FO2Tweaks."""
        if not os.path.exists(fo2tweaks_path):
            return
            
        with open(fo2tweaks_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        content = cls.patch_ini_key(content, "main", "healing_revision", 0)
        content = cls.patch_ini_key(content, "main", "damage_mod", 0)
        content = cls.patch_ini_key(content, "main", "ap_rollover", 0)
        content = cls.patch_ini_key(content, "main", "max_knockback", -1)
        content = cls.patch_ini_key(content, "main", "molotov_fire", 0)
        
        with open(fo2tweaks_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def write_mods_order(cls, mods_dir: str):
        """Создает детерминированный список приоритетов загрузки в mods_order.txt."""
        order_file = os.path.join(mods_dir, "mods_order.txt")
        order_content = (
            "# Fallout 2 Ultimate Wasteland Edition 2026 - Master Priority Order\n"
            "rpu\n"
            "rpu_translations\n"
            "ecco\n"
            "ecco_hf1\n"
            "that_rpu_patch\n"
            "talking_heads\n"
            "minirework\n"
            "fo2tweaks\n"
            "vock\n"
        )
        with open(order_file, "w", encoding="utf-8") as f:
            f.write(order_content)
