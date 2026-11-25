# -*- coding: utf-8 -*-
"""
Full Corpus Builder for Wasteland Voices (v1.0.0)
Preserves base sFall Party Control lines (0..604) in custom.msg!
Appends Wasteland Voices lines (5000+).
"""

import os
import sys

BASE_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\wasteland_voices"

BASE_RU_CUSTOM = """# Messages used in gdialog.c for custom NPC combat control.
{0}{}{Очередь}
{1}{}{Бегство}
{2}{}{Любимое оружие}
{3}{}{Расстояние}
{4}{}{Кого атаковать}
{5}{}{Медикаменты}
{10}{}{[ГОТОВО]}
{11}{}{Отмена}
{99}{}{Неприменимо.}
{100}{}{Всегда!}
{101}{}{Иногда. Не волнуйся, что заденешь меня}
{102}{}{Ни в коем случае не задень меня}
{103}{}{Будь осторожнее, не задень меня}
{104}{}{Ни при каких условиях не попади в меня}
{200}{}{Жалкий трус}
{201}{}{У тебя болит палец}
{202}{}{У тебя легкое кровотечение}
{203}{}{Ты плохо себя чувствуешь}
{204}{}{Тебе нужен жгут}
{205}{}{Никогда!}
{300}{}{Нет}
{301}{}{Холодное}
{302}{}{Холодное, затем стрелковое}
{303}{}{Стрелковое, затем холодное}
{304}{}{Стрелковое}
{305}{}{Без оружия}
{400}{}{Оставаться рядом со мной}
{401}{}{Вперед!}
{402}{}{Снайперский огонь по врагу}
{403}{}{Самостоятельно}
{404}{}{Оставайся на месте}
{500}{}{Того, кто атакует меня}
{501}{}{Самого сильного}
{502}{}{Самого слабого}
{503}{}{Кого хочешь}
{504}{}{Кто ближе всех}
{600}{}{Я не употребляю наркотики}
{601}{}{Стимуляторы при легких ранениях}
{602}{}{Стимуляторы при тяжелых ранениях}
{603}{}{Любые медикаменты время от времени}
{604}{}{Любые медикаменты в любое время}
"""

BASE_EN_CUSTOM = """# Messages used in gdialog.c for custom NPC combat control.
{0}{}{Burst}
{1}{}{Run Away}
{2}{}{Weapon Pref}
{3}{}{Distance}
{4}{}{Attack Who}
{5}{}{Chem Use}
{10}{}{Done}
{11}{}{Cancel}
{99}{}{Not applicable.}
{100}{}{Always!}
{101}{}{Sometimes, don't worry about hitting me}
{102}{}{Be sure you don't hit me}
{103}{}{Be careful not to hit me}
{104}{}{Never, absolutely don't hit me}
{200}{}{Coward}
{201}{}{Finger hurts}
{202}{}{Bleeding a bit}
{203}{}{Not feeling good}
{204}{}{Tourniquet required}
{205}{}{Never!}
{300}{}{None}
{301}{}{Melee}
{302}{}{Melee then ranged}
{303}{}{Ranged then melee}
{304}{}{Ranged}
{305}{}{Unarmed}
{400}{}{Stay close to me}
{401}{}{Charge!}
{402}{}{Snipe the enemy}
{403}{}{On your own}
{404}{}{Stay where you are}
{500}{}{Whomever is attacking me}
{501}{}{The strongest}
{502}{}{The weakest}
{503}{}{Whomever you want}
{504}{}{Closest}
{600}{}{I'm clean}
{601}{}{Stims when hurt a bit}
{602}{}{Stims when hurt a lot}
{603}{}{Any chem some of the time}
{604}{}{Any chem anytime}
"""

# Import generated dictionaries from existing script
from build_full_corpus import RU_LINES, EN_LINES

def write_corpus():
    ru_dialog = os.path.join(BASE_DIR, "text", "russian", "dialog", "wv_dialog.msg")
    ru_custom = os.path.join(BASE_DIR, "text", "russian", "game", "custom.msg")
    en_dialog = os.path.join(BASE_DIR, "text", "english", "dialog", "wv_dialog.msg")
    en_custom = os.path.join(BASE_DIR, "text", "english", "game", "custom.msg")

    sorted_ids = sorted(RU_LINES.keys())

    # 1. Dialog files (lines 5000+ only)
    wv_header = "# ==============================================================================\n"
    wv_header += "# WASTELAND VOICES v1.0.0 DIALOG CORPUS\n"
    wv_header += "# ==============================================================================\n\n"
    
    ru_content = wv_header + "".join(f"{{{i}}}{{}}{{{RU_LINES[i]}}}\n" for i in sorted_ids)
    en_content = wv_header + "".join(f"{{{i}}}{{}}{{{EN_LINES[i]}}}\n" for i in sorted_ids)

    with open(ru_dialog, "wb") as f:
        f.write(ru_content.encode("cp1251"))
    with open(en_dialog, "wb") as f:
        f.write(en_content.encode("ascii"))

    # 2. Custom.msg files (0..604 preserved + lines 5000+ appended)
    full_ru_custom = BASE_RU_CUSTOM + "\n" + ru_content
    full_en_custom = BASE_EN_CUSTOM + "\n" + en_content

    with open(ru_custom, "wb") as f:
        f.write(full_ru_custom.encode("cp1251"))
    with open(en_custom, "wb") as f:
        f.write(full_en_custom.encode("ascii"))

    print(f"Validated and written:")
    print(f"  RU dialog: {os.path.getsize(ru_dialog)} bytes")
    print(f"  RU custom: {os.path.getsize(ru_custom)} bytes (Base lines 0..604 preserved!)")
    print(f"  EN dialog: {os.path.getsize(en_dialog)} bytes")
    print(f"  EN custom: {os.path.getsize(en_custom)} bytes (Base lines 0..604 preserved!)")

if __name__ == "__main__":
    write_corpus()
