"""
FIX-38: Dialogue Syntax Sanitization & Grammar Polishing:
- vcconnar.msg: Resolve syntax error (unclosed brace on line 814 and orphan {813}), fix grammar and typos in lines 813, 814, 819.
- dcvic.msg: Fix typos in line 5113 ('сдесь' -> 'здесь', 'еффективный' -> 'эффективный').
- dcmom.msg: Fix hyphenation in lines 2005, 2017 ('кое что' -> 'кое-что').
- ncmason.msg, nctray.msg, scmerk.msg: Fix hyphenation ('кое что' -> 'кое-что').
"""

import os
import re

GAMEPLAY_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
HD_DIR = r"E:\Fallout2_Ultimate\Fallout2_HD"
WORKSPACE_DIR = r"E:\FALLOUT Ult pjt"
TARGET_DAT_FOLDER = "rpu_russian_uncensored.dat"

def deploy(rel_path, data_bytes):
    targets = [
        os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel_path),
        os.path.join(HD_DIR, "mods", TARGET_DAT_FOLDER, rel_path),
        os.path.join(WORKSPACE_DIR, rel_path)
    ]
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        with open(t, "wb") as f:
            f.write(data_bytes)
    print(f"  [DEPLOYED] {rel_path} ({len(data_bytes)} bytes)")

def fix_vcconnar():
    rel = os.path.join("text", "russian", "dialog", "vcconnar.msg")
    p = os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel)
    with open(p, "r", encoding="cp1251", errors="ignore") as f:
        txt = f.read()

    # Broken section:
    # {813}{}{мне надо подумать об этом.}
    # {814}{}{Вам ясно, что тебя послали сюда только что-бы всех нас сделать рабами?
    # {813}
    # {815}{}{Окей, есть другие вопросы?}
    
    # Replace broken section
    old_target = "{813}{}{мне надо подумать об этом.}\n{814}{}{Вам ясно, что тебя послали сюда только что-бы всех нас сделать рабами?\n{813}\n{815}{}{Окей, есть другие вопросы?}"
    old_target_crlf = "{813}{}{мне надо подумать об этом.}\r\n{814}{}{Вам ясно, что тебя послали сюда только что-бы всех нас сделать рабами?\r\n{813}\r\n{815}{}{Окей, есть другие вопросы?}"
    
    replacement = "{813}{}{Мне надо подумать об этом.}\r\n{814}{}{Вам ясно, что вас послали сюда только затем, чтобы всех нас сделать рабами?}\r\n{815}{}{Окей, есть другие вопросы?}"

    if old_target_crlf in txt:
        txt = txt.replace(old_target_crlf, replacement)
    elif old_target in txt:
        txt = txt.replace(old_target, replacement)
    else:
        # Regex replacement if exact whitespace differs
        txt = re.sub(
            r'\{813\}\{\}\{мне надо подумать об этом\.\}[\r\n]+'
            r'\{814\}\{\}\{Вам ясно, что тебя послали сюда только что-бы всех нас сделать рабами\?[\r\n]+'
            r'\{813\}[\r\n]+'
            r'\{815\}\{\}\{Окей, есть другие вопросы\?\}',
            replacement,
            txt
        )

    # Fix line 819 typo: Пока-что -> Пока что
    txt = txt.replace("{819}{}{Пока-что мы их удерживаем.", "{819}{}{Пока что мы их удерживаем.")

    deploy(rel, txt.encode("cp1251", errors="replace"))

def fix_dcvic():
    rel = os.path.join("text", "russian", "dialog", "dcvic.msg")
    p = os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel)
    with open(p, "r", encoding="cp1251", errors="ignore") as f:
        txt = f.read()

    # Line 5113: сдесь -> здесь, еффективный -> эффективный
    txt = txt.replace("сдесь было больше пушек", "здесь было больше пушек")
    txt = txt.replace("еффективный товар", "эффективный товар")

    deploy(rel, txt.encode("cp1251", errors="replace"))

def fix_dcmom():
    rel = os.path.join("text", "russian", "dialog", "dcmom.msg")
    p = os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel)
    with open(p, "r", encoding="cp1251", errors="ignore") as f:
        txt = f.read()

    txt = txt.replace("рыбный суп и кое что еще.", "рыбный суп и кое-что еще.")
    txt = txt.replace("узнать кое что еще?", "узнать кое-что еще?")

    deploy(rel, txt.encode("cp1251", errors="replace"))

def fix_hyphenations():
    for fn in ["ncmason.msg", "nctray.msg", "scmerk.msg"]:
        rel = os.path.join("text", "russian", "dialog", fn)
        p = os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel)
        if not os.path.exists(p):
            p = os.path.join(WORKSPACE_DIR, rel)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="cp1251", errors="ignore") as f:
            txt = f.read()
        new_txt = re.sub(r'\bкое что\b', 'кое-что', txt)
        if new_txt != txt:
            deploy(rel, new_txt.encode("cp1251", errors="replace"))

if __name__ == '__main__':
    print("--- Executing FIX-38: Dialogue Syntax & Typo Sanitization ---")
    fix_vcconnar()
    fix_dcvic()
    fix_dcmom()
    fix_hyphenations()
    print("FIX-38 completed successfully!")
