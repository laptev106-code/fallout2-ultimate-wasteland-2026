#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOXX DIALOGUE NARRATIVE CRAFT FIXER & AUDITOR (2026)
Applies Black Isle 1998 authentic narrative polish:
1. eckaga3.msg: Replaces "крышек" / "caps" with "золотых монет" / "gold" (FO2 currency canon).
2. qcgranit.msg: Replaces "винтокрыл" with "наш корабль" (PMV Valdez tanker canon).
3. qcmartin.msg: Replaces "винтокрылу" with "кораблю".
4. epai37.msg: Places authentic CP1251 in Russian dialog, and clean English ANSI in English dialog.
"""

import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
DATA_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data\text"

def fix_eckaga3():
    ru_path = os.path.join(DATA_DIR, "russian", "dialog", "eckaga3.msg")
    with open(ru_path, "r", encoding="cp1251") as f:
        text = f.read()
    text = text.replace(
        "{260}{}{Сколько крышек ты спустил на этих наемников, Кага?",
        "{260}{}{Сколько золотых монет ты спустил на этих наемников, Кага?"
    )
    with open(ru_path, "w", encoding="cp1251") as f:
        f.write(text)
    print("  [+] Fixed eckaga3.msg (RU) -> caps replaced with gold coins.")

    en_path = os.path.join(DATA_DIR, "english", "dialog", "eckaga3.msg")
    with open(en_path, "r", encoding="latin-1") as f:
        text_en = f.read()
    text_en = text_en.replace(
        "You spent caps on scrap metal",
        "You spent good money on scrap metal"
    )
    text_en = text_en.replace(
        "How many caps did you blow on these mercenaries, Kaga?",
        "How much gold did you blow on these mercenaries, Kaga?"
    )
    with open(en_path, "w", encoding="latin-1") as f:
        f.write(text_en)
    print("  [+] Fixed eckaga3.msg (EN) -> caps replaced with good money / gold.")

def fix_qcgranit():
    ru_path = os.path.join(DATA_DIR, "russian", "dialog", "qcgranit.msg")
    with open(ru_path, "r", encoding="cp1251") as f:
        text = f.read()
    text = text.replace(
        "мы собьем его сервоприводы и выбьем винтокрыл.",
        "мы собьем его сервоприводы и прорвемся к нашему кораблю."
    )
    with open(ru_path, "w", encoding="cp1251") as f:
        f.write(text)
    print("  [+] Fixed qcgranit.msg (RU) -> vertibird replaced with ship.")

    en_path = os.path.join(DATA_DIR, "english", "dialog", "qcgranit.msg")
    with open(en_path, "r", encoding="latin-1") as f:
        text_en = f.read()
    text_en = text_en.replace(
        "sever his servos and secure the vertibird.",
        "sever his servos and punch through to our ship."
    )
    with open(en_path, "w", encoding="latin-1") as f:
        f.write(text_en)
    print("  [+] Fixed qcgranit.msg (EN) -> vertibird replaced with ship.")

def fix_qcmartin():
    ru_path = os.path.join(DATA_DIR, "russian", "dialog", "qcmartin.msg")
    with open(ru_path, "r", encoding="cp1251") as f:
        text = f.read()
    text = text.replace(
        "Беги наверх к винтокрылу, а мы подготовим эвакуацию!",
        "Беги наверх к кораблю, а мы подготовим эвакуацию!"
    )
    text = text.replace(
        "Затем ты побежишь наверх к моему винтокрылу.",
        "Затем ты побежишь наверх к моему кораблю."
    )
    with open(ru_path, "w", encoding="cp1251") as f:
        f.write(text)
    print("  [+] Fixed qcmartin.msg (RU) -> vertibird replaced with ship.")

    en_path = os.path.join(DATA_DIR, "english", "dialog", "qcmartin.msg")
    with open(en_path, "r", encoding="latin-1") as f:
        text_en = f.read()
    text_en = text_en.replace(
        "Run up to the vertibird, and we will prepare evacuation!",
        "Run up to the ship, and we will prepare evacuation!"
    )
    text_en = text_en.replace(
        "Then you run up to my vertibird. I am right behind you.",
        "Then you run up to my ship. I am right behind you."
    )
    with open(en_path, "w", encoding="latin-1") as f:
        f.write(text_en)
    print("  [+] Fixed qcmartin.msg (EN) -> vertibird replaced with ship.")

def fix_epai37():
    # 1. Current English file has Foxx Russian text in CP1251
    en_path = os.path.join(DATA_DIR, "english", "dialog", "epai37.msg")
    ru_path = os.path.join(DATA_DIR, "russian", "dialog", "epai37.msg")

    with open(en_path, "rb") as f:
        raw_ru = f.read()

    # Save to Russian dialog folder in CP1251
    with open(ru_path, "wb") as f:
        f.write(raw_ru)
    print("  [+] Deployed epai37.msg (RU) with full Russian text in CP1251.")

    # 2. Extract official English epai37.msg from rpu.dat
    from tools.engine_full_audit import read_dat2_directory, extract_dat2_file
    rpu_path = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
    rpu_dat = read_dat2_directory(rpu_path)
    en_base = extract_dat2_file(rpu_dat["text\\english\\dialog\\epai37.msg"]).decode("latin-1")

    # Add Foxx additions (Green hair, exit option, gender check, malfunction) in pure English
    additions_en = """
{418}{}{Alter Hairstyle (Green Hair).}
{419}{}{On second thought, I don't really have time for this right now. Bye.}

{650}{}{Sorry, but this procedure is unavailable for female subjects.}

{700}{}{I am deeply sorry, but an unexpected error occurred during the procedure. We apologize for the inconvenience and thank you for your contribution to science.}
{701}{}{Aw, shit...}
"""
    # Replace line {418} if present, or append
    if "{418}{}" in en_base:
        # line 418 in vanilla RPU was the exit option: replace it with Green Hair + line 419 exit
        en_base = en_base.replace(
            "{418}{}{On second thought, I don't really have time for this right now. Bye.}",
            "{418}{}{Alter Hairstyle (Green Hair).}\n{419}{}{On second thought, I don't really have time for this right now. Bye.}"
        )
        if "{650}{}" not in en_base:
            en_base += "\n{650}{}{Sorry, but this procedure is unavailable for female subjects.}\n\n{700}{}{I am deeply sorry, but an unexpected error occurred during the procedure. We apologize for the inconvenience and thank you for your contribution to science.}\n{701}{}{Aw, shit...}\n"
    else:
        en_base += additions_en

    with open(en_path, "w", encoding="latin-1") as f:
        f.write(en_base)
    print("  [+] Generated clean epai37.msg (EN) in Latin-1/ANSI.")

def main():
    print("=" * 70)
    print("  AUDITING & POLISHING FOXX DIALOGUES (NARRATIVE CRAFT 1998)")
    print("=" * 70)

    fix_eckaga3()
    fix_qcgranit()
    fix_qcmartin()
    fix_epai37()

    print("\n[✔] Dialogue fixes applied! Re-packing DAT and deploying...")
    from tools.build_foxx_tribute_pack import build_dat, deploy_and_register
    build_dat()
    deploy_and_register()

if __name__ == "__main__":
    main()
