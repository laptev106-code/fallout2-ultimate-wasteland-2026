"""
Binary, Script and Configuration Patcher (LAA 4GB Patch & Russian CodePage Fixes)
"""

import os
import struct
import re

class Patcher:
    @staticmethod
    def apply_4gb_laa_patch(exe_path: str) -> bool:
        """
        Устанавливает флаг IMAGE_FILE_LARGE_ADDRESS_AWARE (0x0020) в PE-заголовке exe.
        Позволяет 32-битному процессу Fallout 2 адресовать до 4 ГБ виртуальной памяти.
        """
        if not os.path.exists(exe_path):
            return False
            
        try:
            with open(exe_path, "r+b") as f:
                dos_header = f.read(64)
                if len(dos_header) < 64 or dos_header[:2] != b"MZ":
                    return False
                    
                pe_offset = struct.unpack("<I", dos_header[0x3C:0x40])[0]
                
                f.seek(pe_offset)
                pe_sig = f.read(4)
                if pe_sig != b"PE\x00\x00":
                    return False
                    
                char_offset = pe_offset + 4 + 18
                f.seek(char_offset)
                characteristics = struct.unpack("<H", f.read(2))[0]
                
                IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020
                if not (characteristics & IMAGE_FILE_LARGE_ADDRESS_AWARE):
                    characteristics |= IMAGE_FILE_LARGE_ADDRESS_AWARE
                    f.seek(char_offset)
                    f.write(struct.pack("<H", characteristics))
                    return True
                return True
        except Exception:
            return False

    @staticmethod
    def apply_codepage_fix(target_dir: str) -> bool:
        """
        Устраняет кракозябры и неверную кодировку шрифтов в русской версии Fallout 2 / RPU.
        Настраивает ddraw.ini (Language=russian, CodePage=1251) и f2_res.ini.
        """
        ddraw_path = os.path.join(target_dir, "ddraw.ini")
        if os.path.exists(ddraw_path):
            try:
                with open(ddraw_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Установка русского языка и кодовой страницы 1251 в [Misc]
                from core.configurator import Configurator
                content = Configurator.patch_ini_key(content, "Misc", "Language", "russian")
                content = Configurator.patch_ini_key(content, "Misc", "CodePage", 1251)
                content = Configurator.patch_ini_key(content, "Misc", "UseCustomFont", 1)

                with open(ddraw_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                return False
        return True

    @staticmethod
    def ensure_fallout_cfg(target_dir: str) -> bool:
        """
        Создает или валидирует fallout2.cfg с корректными путями к архивам и звукам.
        Предотвращает фатальный вылет 'Error loading master.dat' / 'Could not find sound.dat'.
        """
        cfg_path = os.path.join(target_dir, "fallout2.cfg")
        cfg_template = (
            "[debug]\n"
            "mode=environment\n"
            "output_map_data_info=0\n"
            "show_load_info=0\n"
            "show_script_messages=0\n"
            "show_tile_num=0\n\n"
            "[sound]\n"
            "music_path1=data\\sound\\music\\\n"
            "music_path2=data\\sound\\music\\\n\n"
            "[system]\n"
            "critter_dat=critter.dat\n"
            "critter_patches=data\n"
            "master_dat=master.dat\n"
            "master_patches=data\n"
            "language=russian\n"
        )
        
        try:
            if not os.path.exists(cfg_path):
                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.write(cfg_template)
            else:
                with open(cfg_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                from core.configurator import Configurator
                content = Configurator.patch_ini_key(content, "system", "critter_dat", "critter.dat")
                content = Configurator.patch_ini_key(content, "system", "master_dat", "master.dat")
                content = Configurator.patch_ini_key(content, "system", "critter_patches", "data")
                content = Configurator.patch_ini_key(content, "system", "master_patches", "data")
                content = Configurator.patch_ini_key(content, "system", "language", "russian")
                content = Configurator.patch_ini_key(content, "sound", "music_path1", "data\\sound\\music\\")
                content = Configurator.patch_ini_key(content, "sound", "music_path2", "data\\sound\\music\\")
                
                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.write(content)
            return True
        except Exception:
            return False

