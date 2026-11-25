import os
import sys
import struct
import shutil

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.build_foxx_tribute_pack import pack_to_dat2

FOXX_KEYSHELP = r"E:\Games\Fallout 2 (Expansion Version)\mods\KeysHelp.dat"
OUTPUT_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\keyshelp_staging"
OUTPUT_DAT = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\KeysHelp.dat"

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def build_patched_keyshelp_int():
    src_int = os.path.join(FOXX_KEYSHELP, "scripts", "gl_keyshelp.int")
    with open(src_int, "rb") as f:
        orig = f.read()

    # The 18 strings in the string table:
    # 0: Help_Window
    # 1: PCX/tipwndw.pcx
    # 2: Fallout Keys Help (Title)
    # 3: Header 1 (Party Orders)
    # 4: Line 1
    # 5: Line 2
    # 6: Line 3
    # 7: Line 4
    # 8: Header 2 (Combat & Controls)
    # 9: Line 5
    # 10: Line 6
    # 11: Line 7
    # 12: Line 8
    # 13: Line 9
    # 14: BTN_close
    # 15: PCX/tipcldwn.pcx
    # 16: PCX/tipclup.pcx
    # 17: PCX/mouse2.pcx

    new_strings = [
        "Help_Window",
        "PCX/tipwndw.pcx",
        "Справка горячих клавиш (Ultimate Wasteland 2026)",
        " НАПАРНИКИ И СВЯЗЬ (Party Orders)",
        "Ctrl+T: Сбор лута / D: Очередь",
        "R / X: Напарники: Собраться / Разойтись",
        "F / H: Подлечиться / Убрать оружие",
        "Shift: Подсветка лута / Caps Lock: Бег",
        " УПРАВЛЕНИЕ, БОЙ И ДИАЛОГИ",
        "1..9: Выбор вариантов в диалогах",
        "A / E: Начать бой (Прицел) / Закончить ход",
        "Q: Режим оружия / Колесо мыши: Скролл",
        "W / T: Карта мира / Карта города",
        "F4/F8: Сохранить/Загрузить | F5/F9: Быстрые",
        "BTN_close",
        "PCX/tipcldwn.pcx",
        "PCX/tipclup.pcx",
        "PCX/mouse2.pcx"
    ]

    # Build new string table
    # Each entry in string table:
    # [length: 2 bytes or 4 bytes? Let's check original format]
    # In original:
    # 0x00E4: 0x00 0x0C 'Help_Window' 0x00
    # Let's inspect exact entry header
    new_str_table = bytearray()
    offsets = []
    for s in new_strings:
        encoded = s.encode("cp1251") + b"\x00"
        offsets.append(len(new_str_table))
        # Write 2-byte big endian length of encoded string including null
        new_str_table.extend(struct.pack(">H", len(encoded)))
        new_str_table.extend(encoded)

    print(f"Built new string table: {len(new_str_table)} bytes (original was 478 bytes)")

    # Read original up to string table start (0x00E8)
    prefix = orig[:0x00E8]
    # Code starts at orig after old string table (0x0326)
    code = bytearray(orig[0x0326:])

    # The difference in string table size:
    delta = len(new_str_table) - (0x0326 - 0x00E8)
    print(f"String table delta: {delta} bytes")

    # In bytecode, the string table offsets were passed to opcode 0x90 0x01
    # Let's update the string offsets in code:
    # List of original string offsets:
    # 0: Help_Window -> 0
    # 1: PCX/tipwndw.pcx -> 14
    # 2: Title -> 32
    # 3: Header 1 -> 52
    # 4: Line 1 -> 86
    # 5: Line 2 -> 118
    # 6: Line 3 -> 154
    # 7: Line 4 -> 198
    # 8: Header 2 -> 234
    # 9: Line 5 -> 268
    # 10: Line 6 -> 304
    # 11: Line 7 -> 336
    # 12: Line 8 -> 384
    # 13: Line 9 -> 442
    # 14: BTN_close -> 488
    # 15: tipcldwn -> 500
    # 16: tipclup -> 520
    # 17: mouse2 -> 538

    # Let's map old string offsets to new string offsets:
    orig_offsets = [0, 14, 38, 58, 92, 122, 158, 202, 238, 272, 308, 340, 388, 446, 492, 504, 524, 542]
    # In code, operands to sfall_func / push_str:
    # We replace each orig_offset with new offset!
    for i in range(len(code) - 5):
        if code[i] == 0x90 and code[i+1] == 0x01:
            val = struct.unpack(">I", code[i+2:i+6])[0]
            if val in orig_offsets:
                idx = orig_offsets.index(val)
                new_val = offsets[idx]
                code[i+2:i+6] = struct.pack(">I", new_val)

    # In start procedure, let's also allow F1 (0x3B) in addition to J (0x24)
    # At 0x0364 in original (offset in code = 0x0364 - 0x0326 = 0x3E):
    # code[0x3E .. 0x44] pushes 0x24
    # Let's inspect code[0x30:0x50]:
    print("Code around key check:", code[0x30:0x50].hex())

    # Update procedure table offsets in prefix:
    # 4 procedures:
    # proc 0 (start): 0x0326 + delta
    # proc 1 (create): 0x03B4 + delta
    # proc 2 (close): 0x06E0 + delta
    # proc 3 (none): 0x0704 + delta
    prefix_arr = bytearray(prefix)
    for p_off in [0x0040, 0x0058, 0x0070, 0x0088, 0x00A0]:
        val = struct.unpack(">I", prefix_arr[p_off:p_off+4])[0]
        if val >= 0x0326:
            prefix_arr[p_off:p_off+4] = struct.pack(">I", val + delta)

    # String table length in header (0x0012 or similar)
    # Let's update string table size at 0x000E:
    orig_str_tbl_size = struct.unpack(">I", prefix_arr[0x000C:0x0010])[0]
    print(f"Original string table size field at 0x0C: {orig_str_tbl_size}")
    prefix_arr[0x000C:0x0010] = struct.pack(">I", len(new_str_table) + 10)

    final_int = bytes(prefix_arr) + bytes(new_str_table) + bytes(code)
    print(f"Final gl_keyshelp.int size: {len(final_int)} bytes (orig was {len(orig)})")
    return final_int

def main():
    print("=" * 70)
    print("  BUILDING MODERNIZED KEYSHELP OVERLAY & REPACKING KEYSHELP.DAT")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "pcx"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "scripts"), exist_ok=True)

    # Copy PCX assets from Foxx KeysHelp
    for pcx_name in ["tipwndw.pcx", "tipclup.pcx", "tipcldwn.pcx", "mouse2.pcx"]:
        src_pcx = os.path.join(FOXX_KEYSHELP, "pcx", pcx_name)
        dst_pcx = os.path.join(OUTPUT_DIR, "pcx", pcx_name)
        shutil.copy2(src_pcx, dst_pcx)
        print(f"[+] Copied {pcx_name}")

    # Build patched gl_keyshelp.int
    patched_int = build_patched_keyshelp_int()
    dst_int = os.path.join(OUTPUT_DIR, "scripts", "gl_keyshelp.int")
    with open(dst_int, "wb") as f:
        f.write(patched_int)
    print(f"[✔] Wrote patched gl_keyshelp.int ({len(patched_int)} bytes)")

    # Also place into tribute pack data folder
    tribute_pcx = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data\pcx"
    tribute_scripts = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data\scripts"
    os.makedirs(tribute_pcx, exist_ok=True)
    for pcx_name in ["tipwndw.pcx", "tipclup.pcx", "tipcldwn.pcx", "mouse2.pcx"]:
        shutil.copy2(os.path.join(FOXX_KEYSHELP, "pcx", pcx_name), os.path.join(tribute_pcx, pcx_name))
    shutil.copy2(dst_int, os.path.join(tribute_scripts, "gl_keyshelp.int"))

    # Repack foxx_rebuild_tribute.dat
    tribute_dat = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\foxx_rebuild_tribute.dat"
    tribute_src = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data"
    pack_to_dat2(tribute_src, tribute_dat)
    print(f"[✔] Repacked foxx_rebuild_tribute.dat with KeysHelp assets ({os.path.getsize(tribute_dat):,} bytes)")

    # Build standalone KeysHelp.dat as well
    pack_to_dat2(OUTPUT_DIR, OUTPUT_DAT)
    print(f"[✔] Built standalone KeysHelp.dat ({os.path.getsize(OUTPUT_DAT):,} bytes)")

    # Deploy KeysHelp.dat and foxx_rebuild_tribute.dat to all profiles
    for prof in PROFILES:
        mods_dir = os.path.join(prof, "mods")
        if os.path.exists(mods_dir):
            shutil.copy2(tribute_dat, os.path.join(mods_dir, "foxx_rebuild_tribute.dat"))
            # If KeysHelp.dat was a folder, remove or replace with clean DAT
            kh_target = os.path.join(mods_dir, "KeysHelp.dat")
            if os.path.isdir(kh_target):
                shutil.rmtree(kh_target)
            shutil.copy2(OUTPUT_DAT, kh_target)
            print(f"  [+] Deployed to {kh_target}")

if __name__ == "__main__":
    main()
