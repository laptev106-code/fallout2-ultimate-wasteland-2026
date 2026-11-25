#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wasteland Voices // Живые Голоса Пустоши (v1.0.0)
Автономный скрипт компиляции и сборки мода в .dat
"""

import os
import sys
import struct
import zlib
import shutil
import subprocess

MOD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(MOD_DIR))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
SCRIPTS_DIR = os.path.join(MOD_DIR, "scripts")
TEXT_DIR = os.path.join(MOD_DIR, "text")
DIST_DIR = os.path.join(MOD_DIR, "dist")
OUTPUT_DAT = os.path.join(DIST_DIR, "wasteland_voices.dat")
CONFIG_INI = os.path.join(MOD_DIR, "wasteland_voices.ini")

GAME_PROFILES = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def get_short_path(path):
    """Возвращает 8.3 путь на Windows для защиты от пробелов в mcpp компиляторе."""
    import ctypes
    buf = ctypes.create_unicode_buffer(500)
    ctypes.windll.kernel32.GetShortPathNameW(path, buf, 500)
    return buf.value if buf.value else path

def compile_scripts():
    print("=" * 60)
    print("[1/4] Компиляция sFall SSL-скриптов...")
    print("=" * 60)

    short_tools = get_short_path(TOOLS_DIR)
    compiler = os.path.join(short_tools, "compile.exe")

    if not os.path.exists(compiler):
        print(f"[ERROR] Компилятор sFall не найден: {compiler}")
        return False

    ssl_files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ssl")]
    if not ssl_files:
        print("[WARNING] Файлы .ssl не найдены в scripts/")
        return True

    success_count = 0
    for ssl_name in ssl_files:
        base_name = os.path.splitext(ssl_name)[0]
        int_name = f"{base_name}.int"

        cmd = [
            compiler,
            "-p",
            "-q",
            "-s",
            f"-I{short_tools}",
            "-O2",
            ssl_name,
            "-o",
            int_name
        ]

        print(f"[*] Сборка: {ssl_name} -> {int_name}...")
        res = subprocess.run(cmd, cwd=SCRIPTS_DIR, capture_output=True, text=True)

        if res.returncode == 0:
            int_path = os.path.join(SCRIPTS_DIR, int_name)
            size = os.path.getsize(int_path) if os.path.exists(int_path) else 0
            print(f"    [OK] {int_name} скомпилирован успешно ({size} байт).")
            success_count += 1
        else:
            print(f"    [FAIL] Ошибка компиляции {ssl_name} (код {res.returncode}):")
            if res.stdout:
                print(res.stdout)
            if res.stderr:
                print(res.stderr)
            return False

    print(f"-> Успешно скомпилировано скриптов: {success_count}/{len(ssl_files)}\n")
    return True

def pack_to_dat2(source_dir, output_dat_path):
    files_to_pack = []
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, source_dir).replace('/', '\\')
            files_to_pack.append((rel_path, full_path))

    os.makedirs(os.path.dirname(output_dat_path), exist_ok=True)

    file_records = []
    with open(output_dat_path, 'wb') as out_f:
        for rel_path, full_path in files_to_pack:
            with open(full_path, 'rb') as src_f:
                raw_data = src_f.read()
            uncomp_size = len(raw_data)
            comp_data = zlib.compress(raw_data)
            comp_size = len(comp_data)
            offset = out_f.tell()
            out_f.write(comp_data)
            file_records.append((rel_path, uncomp_size, comp_size, offset))

        # Запись директории
        dir_start_offset = out_f.tell()
        out_f.write(struct.pack('<I', len(file_records)))

        for rel_path, uncomp_size, comp_size, offset in file_records:
            name_bytes = rel_path.encode('ascii')
            out_f.write(struct.pack('<I', len(name_bytes)))
            out_f.write(name_bytes)
            out_f.write(struct.pack('<BIII', 1, uncomp_size, comp_size, offset))

        dir_end_offset = out_f.tell()
        dir_size = dir_end_offset - dir_start_offset
        total_file_size = dir_end_offset + 8
        out_f.write(struct.pack('<II', dir_size, total_file_size))

    dat_size = os.path.getsize(output_dat_path)
    print(f"-> Упаковано {len(file_records)} файлов в {os.path.basename(output_dat_path)} ({dat_size} байт).\n")
    return True

def build_dat():
    print("=" * 60)
    print("[2/4] Подготовка файлов и упаковка в DAT2...")
    print("=" * 60)

    staging_dir = os.path.join(MOD_DIR, "_staging")
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    # 1. Копируем скомпилированные .int в staging/scripts/
    target_scripts = os.path.join(staging_dir, "scripts")
    os.makedirs(target_scripts, exist_ok=True)
    for f in os.listdir(SCRIPTS_DIR):
        if f.endswith(".int"):
            shutil.copy2(os.path.join(SCRIPTS_DIR, f), os.path.join(target_scripts, f))

    # 2. Копируем языковые деревья text/
    if os.path.exists(TEXT_DIR):
        shutil.copytree(TEXT_DIR, os.path.join(staging_dir, "text"), dirs_exist_ok=True)

    # 3. Упаковка в dist/wasteland_voices.dat
    os.makedirs(DIST_DIR, exist_ok=True)
    pack_to_dat2(staging_dir, OUTPUT_DAT)

    # Очистка временной папки
    shutil.rmtree(staging_dir)
    return True

def deploy():
    print("=" * 60)
    print("[3/4] Развертывание мода в игровые профили...")
    print("=" * 60)

    if not os.path.exists(OUTPUT_DAT):
        print(f"[ERROR] Собранный DAT не найден: {OUTPUT_DAT}")
        return False

    for profile in GAME_PROFILES:
        if not os.path.exists(profile):
            print(f"[SKIP] Профиль не найден: {profile}")
            continue

        mods_dir = os.path.join(profile, "mods")
        os.makedirs(mods_dir, exist_ok=True)

        # Копируем .dat и .ini
        target_dat = os.path.join(mods_dir, "wasteland_voices.dat")
        target_ini = os.path.join(mods_dir, "wasteland_voices.ini")

        shutil.copy2(OUTPUT_DAT, target_dat)
        if os.path.exists(CONFIG_INI):
            shutil.copy2(CONFIG_INI, target_ini)
        print(f"[+] Развернуто в {os.path.basename(profile)}: wasteland_voices.dat, wasteland_voices.ini")

        # Регистрация в mods_order.txt
        order_file = os.path.join(mods_dir, "mods_order.txt")
        if os.path.exists(order_file):
            with open(order_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l.strip() for l in f.readlines()]

            if "wasteland_voices.dat" not in lines:
                lines.append("wasteland_voices.dat")
                with open(order_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
                print(f"[+] Зарегистрирован в {order_file}")
            else:
                print(f"[OK] Уже зарегистрирован в {order_file}")

    print("\n-> Развертывание завершено успешно.\n")
    return True

def main():
    print("\n" + "=" * 60)
    print("  WASTELAND VOICES // СБОРОЧНЫЙ КОНВЕЙЕР МОДА v1.0.0")
    print("=" * 60 + "\n")

    if not compile_scripts():
        sys.exit(1)

    if not build_dat():
        sys.exit(1)

    if "--deploy" in sys.argv:
        if not deploy():
            sys.exit(1)

    print("=" * 60)
    print("[4/4] СБОРКА УСПЕШНО ЗАВЕРШЕНА (Exit Code 0)")
    print(f"Файл: {OUTPUT_DAT}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
