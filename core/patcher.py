"""
Binary and Script Patcher (LAA 4GB Patch & CodePage Fixes)
"""

import os
import struct

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
                # Читаем DOS заголовок
                dos_header = f.read(64)
                if len(dos_header) < 64 or dos_header[:2] != b"MZ":
                    return False
                    
                # Смещение к PE заголовку (offset 0x3C)
                pe_offset = struct.unpack("<I", dos_header[0x3C:0x40])[0]
                
                f.seek(pe_offset)
                pe_sig = f.read(4)
                if pe_sig != b"PE\x00\x00":
                    return False
                    
                # Characteristics находится на offset pe_offset + 4 + 18 = pe_offset + 22 (2 байта)
                char_offset = pe_offset + 4 + 18
                f.seek(char_offset)
                characteristics = struct.unpack("<H", f.read(2))[0]
                
                IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020
                if not (characteristics & IMAGE_FILE_LARGE_ADDRESS_AWARE):
                    characteristics |= IMAGE_FILE_LARGE_ADDRESS_AWARE
                    f.seek(char_offset)
                    f.write(struct.pack("<H", characteristics))
                    return True
                return True # Уже установлен
        except Exception:
            return False
