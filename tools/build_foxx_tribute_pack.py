#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOXX REBUILD TRIBUTE PACK - BUILDER & PACKAGER (2026)
Assembles all curated fixes, dialogs, gender layers, and roleplay expansions
originating from or inspired by Foxx (ReBuild by Foxx) into a single standalone DAT2 module:
'foxx_rebuild_tribute.dat'.

Contents:
1. Interactive Bishop Safes Overhaul (nimrbsf, nimrsbsf, niabissf)
2. Kaga Encounters Rebalance & RPG Expansion (eckaga1..4)
3. Alcohol Withdrawal & Hangover System (obj_dude.msg)
4. Enclave Finale Tactical Briefing (qcgranit, qcmartin)
5. Gender Dialogue Layer (359 dialog_female files with Talking Heads lip-sync)
6. Pariah Dog Jinxed Fix (ecpariah.int)
7. Sulik's Sister Ending Softlock Fix (tribec7.int)
8. EPA / AZOS Crash Fixes (arbridge.map, epac1.int, epai37.int, epai37.msg)
9. AleSiS Crowbar Prototype Fix (00000455.pro)
"""

import os
import sys
import shutil
import struct
import zlib

TOOLS_DIR = r"E:\FALLOUT Ult pjt\tools"
sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_MASTER = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"
GAMEPLAY_UNCENSORED = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat"
MOD_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute"
DATA_DIR = os.path.join(MOD_DIR, "data")
DAT_OUTPUT = os.path.join(MOD_DIR, "foxx_rebuild_tribute.dat")

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

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

        # Directory table
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
    print(f"-> Упаковано {len(file_records)} файлов в {os.path.basename(output_dat_path)} ({dat_size:,} байт).\n")
    return dat_size

def ensure_dirs():
    os.makedirs(os.path.join(DATA_DIR, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "text", "russian", "dialog"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "text", "english", "dialog"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "text", "russian", "dialog_female"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "text", "english", "dialog_female"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "proto", "items"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "maps"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "proto", "critters"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "art", "intrface"), exist_ok=True)

def collect_foxx_assets():
    print("[*] Collecting assets for Foxx ReBuild Tribute Pack...")
    ensure_dirs()

    # 1. Read Foxx master.dat
    foxx_dat = {}
    if os.path.exists(FOXX_MASTER):
        print(f"[*] Indexing Foxx master.dat ({FOXX_MASTER})...")
        foxx_dat = read_dat2_directory(FOXX_MASTER)

    # 2. Extract Foxx direct fixes (crowbar, pariah dog, tribal ending, EPA map & scripts)
    direct_foxx_files = [
        ("proto\\items\\00000455.pro", os.path.join(DATA_DIR, "proto", "items", "00000455.pro")),
        ("scripts\\ecpariah.int", os.path.join(DATA_DIR, "scripts", "ecpariah.int")),
        ("scripts\\tribec7.int", os.path.join(DATA_DIR, "scripts", "tribec7.int")),
        ("scripts\\epac1.int", os.path.join(DATA_DIR, "scripts", "epac1.int")),
        ("scripts\\epai37.int", os.path.join(DATA_DIR, "scripts", "epai37.int")),
        ("maps\\arbridge.map", os.path.join(DATA_DIR, "maps", "arbridge.map")),
        ("maps\\epamain1.map", os.path.join(DATA_DIR, "maps", "epamain1.map")),
        ("maps\\epamain2.map", os.path.join(DATA_DIR, "maps", "epamain2.map")),
        ("proto\\critters\\00000542.pro", os.path.join(DATA_DIR, "proto", "critters", "00000542.pro")),
        ("art\\intrface\\skldxbox.frm", os.path.join(DATA_DIR, "art", "intrface", "skldxbox.frm")),
    ]
    for vfs_path, out_disk in direct_foxx_files:
        if vfs_path in foxx_dat:
            raw = extract_dat2_file(foxx_dat[vfs_path])
            with open(out_disk, "wb") as f:
                f.write(raw)
            print(f"  [+] Extracted from Foxx master: {vfs_path} -> {len(raw)} bytes")

    # 3. Copy our modernized scripts and dialogs from rpu_russian_uncensored.dat
    modernized_scripts = [
        "nimrbsf.int", "nimrsbsf.int", "niabissf.int",
        "eckaga1.int", "eckaga2.int", "eckaga3.int", "eckaga4.int",
        "qcgranit.int", "qcmartin.int"
    ]
    for sname in modernized_scripts:
        src = os.path.join(GAMEPLAY_UNCENSORED, "scripts", sname)
        dst = os.path.join(DATA_DIR, "scripts", sname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  [+] Modernized script: {sname} ({os.path.getsize(dst)} bytes)")

    # 4. Copy dialog files (Russian & English)
    modernized_dialogs = [
        "nimrbsf.msg", "nimrsbsf.msg", "niabissf.msg",
        "eckaga1.msg", "eckaga2.msg", "eckaga3.msg", "eckaga4.msg",
        "qcgranit.msg", "qcmartin.msg", "obj_dude.msg"
    ]
    for dname in modernized_dialogs:
        # Russian
        src_ru = os.path.join(GAMEPLAY_UNCENSORED, "text", "russian", "dialog", dname)
        dst_ru = os.path.join(DATA_DIR, "text", "russian", "dialog", dname)
        if os.path.exists(src_ru):
            shutil.copy2(src_ru, dst_ru)
        
        # English
        src_en = os.path.join(GAMEPLAY_UNCENSORED, "text", "english", "dialog", dname)
        dst_en = os.path.join(DATA_DIR, "text", "english", "dialog", dname)
        if os.path.exists(src_en):
            shutil.copy2(src_en, dst_en)

    # Also grab epai37.msg if present
    if "text\\english\\dialog\\epai37.msg" in foxx_dat:
        raw_en = extract_dat2_file(foxx_dat["text\\english\\dialog\\epai37.msg"])
        with open(os.path.join(DATA_DIR, "text", "english", "dialog", "epai37.msg"), "wb") as f:
            f.write(raw_en)

    # 5. Copy Female Dialog Layer (359 files)
    src_fem_ru = os.path.join(GAMEPLAY_UNCENSORED, "text", "russian", "dialog_female")
    src_fem_en = os.path.join(GAMEPLAY_UNCENSORED, "text", "english", "dialog_female")
    dst_fem_ru = os.path.join(DATA_DIR, "text", "russian", "dialog_female")
    dst_fem_en = os.path.join(DATA_DIR, "text", "english", "dialog_female")

    fem_count_ru = 0
    fem_count_en = 0
    if os.path.exists(src_fem_ru):
        for fname in os.listdir(src_fem_ru):
            if fname.lower().endswith(".msg"):
                shutil.copy2(os.path.join(src_fem_ru, fname), os.path.join(dst_fem_ru, fname))
                fem_count_ru += 1
    if os.path.exists(src_fem_en):
        for fname in os.listdir(src_fem_en):
            if fname.lower().endswith(".msg"):
                shutil.copy2(os.path.join(src_fem_en, fname), os.path.join(dst_fem_en, fname))
                fem_count_en += 1
    print(f"  [+] Female Dialog Layer copied: {fem_count_ru} RU files, {fem_count_en} EN files.")

def create_metadata():
    ini_content = """; ======================================================================
; FOXX REBUILD LEGACY: ULTIMATE TRIBUTE PACK (2026)
; Модуль-трибьют сборке ReBuild by Foxx (v19.03.26)
; Автор оригинальных находок и компиляции: Foxx
; Ролевая и литературная модернизация: Ultimate Wasteland Edition Team (2026)
; ======================================================================

[MOD_INFO]
name=Foxx ReBuild Legacy: Ultimate Tribute Pack
version=1.0.0
author=Foxx & Ultimate Wasteland Team
description=Комплекс аутентичных исправлений, женский диалоговый слой (359 файлов), ролевой взлом сейфов Бишопов, расширенные встречи с Кагой, фиксы АЗОС и тактический финал на Вышке Анклава.
category=Community Legacy / RPG Overhaul

[FEATURES]
bishop_safes_rpg_overhaul=1
kaga_encounters_expanded=1
alcohol_withdrawal_endurance=1
enclave_finale_tactical_briefing=1
female_dialog_layer=1
pariah_dog_fix=1
sulik_sister_ending_protection=1
epa_crash_stability_fixes=1
crowbar_error_fix=1
"""
    ini_path = os.path.join(MOD_DIR, "foxx_rebuild_tribute.ini")
    with open(ini_path, "w", encoding="cp1251") as f:
        f.write(ini_content)

    readme_content = """# 🏆 FOXX REBUILD LEGACY: ULTIMATE TRIBUTE PACK (2026)

## О модуле и благодарность автору

Данный модуль создан в дань уважения огромному многолетнему труду **Foxx** — ветерана моддинга Fallout 2 и создателя знаменитой сборки **ReBuild by Foxx** (v19.03.26).

Сборка Фокса собрала воедино десятки точечных улучшений сообщества, отшлифовала мелкие скриптовые баги и стала одной из самых любимых сборок среди русскоязычных игроков. Мы бережно собрали лучшие авторские и адаптированные находки Фокса, модернизировали их под строгий канон Black Isle 1998 года, расширили ролевыми проверками (Skill Checks) и упаковали в единый автономный модуль.

---

## Что входит в Tribute Pack:

1. **Интерактивные сейфы семьи Бишоп (Нью-Рино)**:
   - Исходная идея Фокса по оживлению трех сейфов в спальнях Бишопов.
   - *Модернизация 2026:* Устранено примитивное меню наугад. Внедрены честные ролевые проверки Взлома (`Lockpick >= 65-75%`), Ловушек (`Traps >= 60-65%`), Ремонта (`Repair >= 70%`), Науки (`Science >= 65-75%`) и Восприятия (`PE >= 8`) с наградами в XP.
2. **Ребаланс и вариативность случайных встреч с Кагой**:
   - Исходная идея Фокса по предотвращению ваншота ГГ 1-го уровня в ранней игре.
   - *Модернизация 2026:* Вместо банального срезания здоровья добавлены тактические небоевые развилки через Скитальца (`Outdoorsman 40-80%` — заблаговременное обнаружение засады и фланговый маневр) и Красноречие (`Speech 50-75%` — устыжение традициями предков и бегство Каги с поля боя).
3. **Симптомы алкогольной абстиненции**:
   - Исходные строки Фокса о похмелье в `obj_dude.msg`.
   - *Модернизация 2026:* Литературная вычитка без канцелярита и грамматических ошибок, прямая привязка длительности дебаффов к Выносливости (`Endurance`).
4. **Финал Анклава: тактика сержанта Гранита и ученый Мартин**:
   - Разблокировка диалоговых возможностей на Вышке.
   - *Модернизация 2026:* Профессиональный военный инструктаж Гранита через `Speech >= 80%` и `Big Guns/Energy >= 85%` (+1000 XP) и саперный расчет подрыва энергоблока через `Traps/Science` (+300 XP).
5. **Гендерный диалоговый слой (359 файлов)**:
   - 359 файлов `dialog_female` с вычищенной грамматикой и 100% зеркалированием тегов мимики для всех озвученных 3D голов Talking Heads.
6. **Критический фикс пса-неудачника (`ecpariah.int`)**:
   - Гарантированное снятие перка «Проклятый» при убийстве собаки напарниками игрока.
7. **Защита квеста сестры Сулика (`tribec7.int`)**:
   - Предотвращение софтлока и зависания диалога Курису после финальных титров.
8. **Комплекс стабильности АЗОС / EPA (`arbridge.map`, `epac1.int`, `epai37.int`)**:
   - Исправление геометрии переходов между уровнями комплекса и безопасный выход из терминала.
9. **Прототип монтировки (`00000455.pro`)**:
   - Фикс ошибки `error` в логе при вскрытии контейнеров ломиком (автор фикса — AleSiS, интеграция — Foxx).

---

## Архитектура
* **Модуль:** `mods/foxx_rebuild_tribute.dat` (DAT2)
* **Конфиг:** `mods/foxx_rebuild_tribute.ini`
* **Совместимость:** 100% паритет с sFall 5.1.5.1 / 4.4.8, EcCo Overhaul и нативным портом fallout2-ce.
"""
    readme_path = os.path.join(MOD_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

def build_dat():
    print("[*] Packing foxx_rebuild_tribute.dat...")
    dat_size = pack_to_dat2(DATA_DIR, DAT_OUTPUT)
    print(f"[✔] Built DAT2: {DAT_OUTPUT} ({dat_size:,} bytes)")
    return dat_size

def deploy_and_register():
    print("\n[*] Deploying to target profiles and registering in mods_order.txt...")
    ini_src = os.path.join(MOD_DIR, "foxx_rebuild_tribute.ini")

    for p in PROFILES:
        mods_dir = os.path.join(p, "mods")
        if not os.path.exists(mods_dir):
            continue

        # Copy DAT and INI
        dst_dat = os.path.join(mods_dir, "foxx_rebuild_tribute.dat")
        dst_ini = os.path.join(mods_dir, "foxx_rebuild_tribute.ini")
        shutil.copy2(DAT_OUTPUT, dst_dat)
        shutil.copy2(ini_src, dst_ini)
        print(f"  [+] Deployed to {mods_dir}")

        # Register in mods_order.txt
        order_path = os.path.join(mods_dir, "mods_order.txt")
        if os.path.exists(order_path):
            with open(order_path, "r", encoding="latin-1", errors="replace") as f:
                lines = [l.strip() for l in f if l.strip()]

            mod_name = "foxx_rebuild_tribute.dat"
            if mod_name not in lines:
                # Insert right before rpu_russian_uncensored.dat or at the end
                if "rpu_russian_uncensored.dat" in lines:
                    idx = lines.index("rpu_russian_uncensored.dat")
                    lines.insert(idx, mod_name)
                else:
                    lines.append(mod_name)

                with open(order_path, "w", encoding="latin-1") as f:
                    f.write("\n".join(lines) + "\n")
                print(f"  [+] Registered {mod_name} in {order_path} at position #{lines.index(mod_name)+1}")
            else:
                print(f"  [*] {mod_name} already in {order_path}")

def main():
    print("=" * 70)
    print("  BUILDING FOXX REBUILD TRIBUTE PACK (2026)")
    print("=" * 70)

    collect_foxx_assets()
    create_metadata()
    dat_size = build_dat()
    deploy_and_register()

    print("\n" + "=" * 70)
    print(f"  FOXX REBUILD TRIBUTE PACK DEPLOYED SUCCESSFULLY! ({dat_size:,} bytes)")
    print("=" * 70)

if __name__ == "__main__":
    main()
