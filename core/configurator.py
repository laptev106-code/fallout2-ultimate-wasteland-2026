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
        key_pattern = re.compile(rf"^\s*;?\s*{re.escape(key)}\s*=.*$", re.IGNORECASE)
        
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
        """Настраивает sfall 4.5.1 под связку EcCo + MiniRework + Lossless Music."""
        if not os.path.exists(ddraw_path):
            return
            
        with open(ddraw_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Системные настройки и стабильность
        content = cls.patch_ini_key(content, "Misc", "AllowUnsafeScripting", 2)
        content = cls.patch_ini_key(content, "Misc", "SpeedInterfaceCounterAnims", 2)
        content = cls.patch_ini_key(content, "Misc", "ExtraMemory", 1)
        content = cls.patch_ini_key(content, "Misc", "SkipOpeningMovies", 1)
        content = cls.patch_ini_key(content, "Misc", "Language", "russian")
        content = cls.patch_ini_key(content, "Misc", "CodePage", 1251)
        content = cls.patch_ini_key(content, "Misc", "UseCustomFont", 1)
        # Разрешаем CRC модифицированного LAA (4GB) исполняемого файла fallout2.exe
        content = cls.patch_ini_key(content, "Debugging", "ExtraCRC", "0xf18aa577")
        content = cls.patch_ini_key(content, "Debugging", "SkipCompatModeCheck", 1)
        # Графика: когда f2_res.ini работает в режиме DirectX 9 (GRAPHICS_MODE=2),
        # в sfall ddraw.ini Mode должен оставаться 0 во избежание конфликта двух DX9 устройств
        content = cls.patch_ini_key(content, "Graphics", "Mode", 0)
        content = cls.patch_ini_key(content, "Graphics", "TextureFilter", 2)
        
        # Поддержка Lossless Music (DirectShow streaming для uncompressed WAV)
        content = cls.patch_ini_key(content, "Sound", "AllowDShowSound", 1)
        
        with open(ddraw_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def tune_minirework_ini(cls, game_dir: str):
        """
        Настраивает MiniRework 2.0.4.3:
        Отключает модули лечения, медицинских инструментов и краж для бесконфликтной передачи баланса в EcCo.
        Копирует преднастроенные Perks.ini и Drugs.ini, чтобы избежать разового принудительного перезапуска игры.
        """
        candidates = [
            os.path.join(game_dir, "mods", "F2MechanicsMiniRework.ini"),
            os.path.join(game_dir, "minirework.ini"),
            os.path.join(game_dir, "mods", "minirework.ini")
        ]
        
        for path in candidates:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                # Отключаем конфликтующие с EcCo модули, передавая их под управление EcCo
                content = cls.patch_ini_key(content, "MAIN", "RegenMod", 0)
                content = cls.patch_ini_key(content, "MAIN", "MedToolsMod", 0)
                content = cls.patch_ini_key(content, "MAIN", "StealRebalance", 0)
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

        # Обеспечиваем наличие директории mods/sfall и преднастроенных ini
        mods_dir = os.path.join(game_dir, "mods")
        if os.path.exists(mods_dir):
            os.makedirs(os.path.join(mods_dir, "sfall"), exist_ok=True)
            template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "mods")
            for ini_name in ["Perks.ini", "Drugs.ini"]:
                src = os.path.join(template_dir, ini_name)
                dst = os.path.join(mods_dir, ini_name)
                if os.path.exists(src) and not os.path.exists(dst):
                    try:
                        shutil.copy2(src, dst)
                    except Exception:
                        pass

    @classmethod
    def deploy_miria_mod(cls, game_dir: str):
        """Интегрирует проверенный патч расширения спутницы Мирии (Miria Can Wait + русские диалоги)."""
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "miria")
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for f in files:
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, template_dir)
                    dst = os.path.join(game_dir, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    try:
                        shutil.copy2(src, dst)
                    except Exception:
                        pass
        rpu_ini = os.path.join(game_dir, "mods", "rpu.ini")
        if os.path.exists(rpu_ini):
            with open(rpu_ini, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "miria_can_wait" not in content:
                content += "\n; Miria Can Wait patch\nmiria_can_wait=1\n"
                with open(rpu_ini, "w", encoding="utf-8") as f:
                    f.write(content)

    @classmethod
    def tune_fo2tweaks_ini(cls, game_dir: str):
        """
        Калибровочный профиль FO2Tweaks 14.7:
        СТРОГО 5 проверенных параметров от автора EcCo для защиты баллистики и боевого баланса.
        """
        candidates = [
            os.path.join(game_dir, "mods", "fo2tweaks.ini"),
            os.path.join(game_dir, "fo2tweaks.ini")
        ]
        
        # Официальный список автора EcCo: отключение конфликтующих расчетов урона и гранат
        ecco_compatibility_params = {
            "max_knockback": -1,
            "healing_revision": 0,
            "molotov_fire": 0,
            "damage_mod": 0,
            "ap_rollover": 0
        }
        
        for path in candidates:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                for k, v in ecco_compatibility_params.items():
                    content = cls.patch_ini_key(content, "main", k, v)
                    
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

    @classmethod
    def tune_f2_res_ini(cls, f2_res_path: str, screen_width: int = 2560, screen_height: int = 1440):
        """
        Настраивает High Resolution Patch (f2_res.ini):
        DirectX 9 режим, фикс мыши, фикс Alt+Tab и масштабирование интерфейса Scale 2x под 1440p/1080p.
        """
        if not os.path.exists(f2_res_path):
            return
            
        with open(f2_res_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        content = cls.patch_ini_key(content, "MAIN", "GRAPHICS_MODE", 2)  # DX9
        content = cls.patch_ini_key(content, "MAIN", "SCR_WIDTH", screen_width)
        content = cls.patch_ini_key(content, "MAIN", "SCR_HEIGHT", screen_height)
        content = cls.patch_ini_key(content, "MAIN", "COLOUR_BITS", 32)
        content = cls.patch_ini_key(content, "MAIN", "ALT_MOUSE_INPUT", 1)
        content = cls.patch_ini_key(content, "MAIN", "EXTRA_WIN_MSG_CHECKS", 1)
        content = cls.patch_ini_key(content, "MAIN", "SCALE_2X", 1)
        
        with open(f2_res_path, "w", encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def write_mods_order(cls, mods_dir: str):
        """Создает детерминированный список приоритетов загрузки в mods_order.txt со всеми установленными модами."""
        order_file = os.path.join(mods_dir, "mods_order.txt")
        order_content = (
            "; Fallout 2: Ultimate Wasteland 2026 - Master Priority Order\n"
            "; Base RPU Core\n"
            "rpu.dat\n\n"
            "; Additional Animations & Effects\n"
            "rpu_alternative_explosions.dat\n"
            "rpu_enhanced_worldmap.dat\n"
            "rpu_extended_flamer.dat\n"
            "rpu_improved_mysterious_stranger.dat\n"
            "rpu_rifle_animations.dat\n"
            "rpu_wakizashi_animations.dat\n\n"
            "; Companion Visuals & Audio\n"
            "cassidy_head.dat\n"
            "cassidy_voice_joey_bracken_hq.dat\n"
            "npc_armor.dat\n\n"
            "; Tactical & Quality of Life\n"
            "party_orders.dat\n"
            "fo2tweaks.dat\n"
            "InventoryFilter.dat\n\n"
            "; Overhaul & Mechanics\n"
            "rpu_y_ecco.dat\n"
            "F2MechanicsMiniRework.dat\n\n"
            "; Translations (Top Priority over English text)\n"
            "rpu_russian.dat\n"
            "upu_russian_sound.dat\n"
        )
        os.makedirs(mods_dir, exist_ok=True)
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
