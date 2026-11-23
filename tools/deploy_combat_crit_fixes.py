"""
DEPLOY COMBAT, CRITTER & SCREEN SETTINGS FIXES (FIX-46)
1. Merge 139 Miria combat float lines (42800..42973) into text/russian/game/combatai.msg with 12 typo fixes.
2. Merge 4 Miria level lines (55000..55301) and localize 54000/54100 in text/russian/game/pro_crit.msg.
3. Clean Fallout: Nevada relic in text/russian/game/scrnset.msg and text/english/game/scrnset.msg.
4. Deploy to workspace and both runtime profiles (Fallout2_Gameplay and Fallout2_HD).
"""

import os
import sys
import re
import shutil

sys.path.insert(0, os.path.abspath("."))
import tools.engine_full_audit as efa

WORKSPACE_UNCENS = r"mods\rpu_russian_uncensored.dat"
PROFILES = [
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat",
    r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat"
]

GP_MODS = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"

def main():
    print("[*] Starting FIX-46 Deployment...")
    dats_rpu = efa.read_dat2_directory(os.path.join(GP_MODS, 'rpu_russian.dat'))
    dats_mir = efa.read_dat2_directory(os.path.join(GP_MODS, 'DB_Enchanced_Miria.dat'))
    dats_res = efa.read_dat2_directory(os.path.join(GP_MODS, 'f2_res.dat'))

    # =========================================================================
    # 1. COMBATAI.MSG
    # =========================================================================
    print("[1/3] Processing combatai.msg...")
    cai_raw = efa.extract_dat2_file(dats_rpu['text\\russian\\game\\combatai.msg'])
    cai_text = cai_raw.decode('cp1251')

    mir_raw = efa.extract_dat2_file(dats_mir['text\\english\\game\\combatai.msg'])
    mir_text = mir_raw.decode('cp1251')

    # Extract Miria lines
    mir_dict = {}
    for line in mir_text.splitlines():
        m = re.match(r'^\{(\d+)\}\{.*\}\{(.*)\}', line.strip())
        if m:
            num = int(m.group(1))
            if 42800 <= num <= 42999:
                mir_dict[num] = m.group(2)

    # Apply 12 typo fixes
    corrections = {
        42814: ('Не трож мои руки!', 'Не трожь мои руки!'),
        42825: ('Я не чувствую правую руки!', 'Я не чувствую правой руки!'),
        42847: ('беспокоится о диете', 'беспокоиться о диете'),
        42852: ('могут вывалится в', 'могут вывалиться в'),
        42860: ('На какое то время', 'На какое-то время'),
        42863: ('унести меня от сюда', 'унести меня отсюда'),
        42892: ('Мы будем охотится на вас.', 'Мы будем охотиться на вас.'),
        42893: ('Я хочу что бы у меня', 'Я хочу чтобы у меня'),
        42914: ('кто смог утянул меня в', 'кто смог утянуть меня в'),
        42940: ('Какие то вопросы?', 'Какие-то вопросы?'),
        42953: ('Платишь будешь ты.', 'Платить будешь ты.'),
        42971: ('пялится на мои сиськи.', 'пялиться на мои сиськи.')
    }
    for num, (old, new) in corrections.items():
        if num in mir_dict:
            mir_dict[num] = mir_dict[num].replace(old, new)

    # Parse original messages
    msg_dict = {}
    for line in cai_text.splitlines():
        line_s = line.strip()
        m = re.match(r'^\{(\d+)\}', line_s)
        if m:
            msg_dict[int(m.group(1))] = line_s

    # Add Miria lines
    for num, txt in mir_dict.items():
        msg_dict[num] = f"{{{num}}}{{}}{{{txt}}}"

    # Build sorted text
    sorted_cai_lines = [msg_dict[k] for k in sorted(msg_dict.keys())]
    cai_output_text = "\r\n".join(sorted_cai_lines) + "\r\n"
    cai_output_bytes = cai_output_text.encode('cp1251')
    print(f"    combatai.msg: total messages = {len(msg_dict)}, bytes = {len(cai_output_bytes)}")

    # =========================================================================
    # 2. PRO_CRIT.MSG
    # =========================================================================
    print("[2/3] Processing pro_crit.msg...")
    crit_raw = efa.extract_dat2_file(dats_rpu['text\\russian\\game\\pro_crit.msg'])
    crit_text = crit_raw.decode('cp1251')

    crit_dict = {}
    for line in crit_text.splitlines():
        line_s = line.strip()
        m = re.match(r'^\{(\d+)\}', line_s)
        if m:
            crit_dict[int(m.group(1))] = line_s

    # Localize English names
    crit_dict[54000] = "{54000}{}{Миниган Джим}"
    crit_dict[54100] = "{54100}{}{Бофаст}"

    # Add Miria level descriptions
    crit_dict[55000] = "{55000}{}{Мария - Уровень 1}"
    crit_dict[55001] = "{55001}{}{}"
    crit_dict[55100] = "{55100}{}{Мария - Уровень 2}"
    crit_dict[55101] = "{55101}{}{}"
    crit_dict[55200] = "{55200}{}{Мария - Уровень 3}"
    crit_dict[55201] = "{55201}{}{}"
    crit_dict[55300] = "{55300}{}{Мария - Уровень 4}"
    crit_dict[55301] = "{55301}{}{}"

    sorted_crit_lines = [crit_dict[k] for k in sorted(crit_dict.keys())]
    crit_output_text = "\r\n".join(sorted_crit_lines) + "\r\n"
    crit_output_bytes = crit_output_text.encode('cp1251')
    print(f"    pro_crit.msg: total messages = {len(crit_dict)}, bytes = {len(crit_output_bytes)}")

    # =========================================================================
    # 3. SCRNSET.MSG
    # =========================================================================
    print("[3/3] Processing scrnset.msg...")
    res_raw = efa.extract_dat2_file(dats_res['text\\english\\game\\scrnset.msg'])
    res_text = res_raw.decode('cp1251')
    # Replace Fallout: Nevada with Fallout 2
    res_text_clean = res_text.replace("Fallout: Nevada", "Fallout 2")
    res_output_bytes = res_text_clean.encode('cp1251')
    print(f"    scrnset.msg: bytes = {len(res_output_bytes)}")

    # =========================================================================
    # 4. DEPLOY TO WORKSPACE AND ALL PROFILES
    # =========================================================================
    destinations = [WORKSPACE_UNCENS] + PROFILES
    for dest in destinations:
        print(f"[*] Deploying to {dest}...")
        # text/russian/game/
        rus_game_dir = os.path.join(dest, "text", "russian", "game")
        os.makedirs(rus_game_dir, exist_ok=True)
        with open(os.path.join(rus_game_dir, "combatai.msg"), "wb") as f:
            f.write(cai_output_bytes)
        with open(os.path.join(rus_game_dir, "pro_crit.msg"), "wb") as f:
            f.write(crit_output_bytes)
        with open(os.path.join(rus_game_dir, "scrnset.msg"), "wb") as f:
            f.write(res_output_bytes)

        # text/english/game/ (for scrnset.msg fallback)
        eng_game_dir = os.path.join(dest, "text", "english", "game")
        os.makedirs(eng_game_dir, exist_ok=True)
        with open(os.path.join(eng_game_dir, "scrnset.msg"), "wb") as f:
            f.write(res_output_bytes)

    print("[SUCCESS] All FIX-46 assets successfully deployed and synchronized across all environments!")

if __name__ == "__main__":
    main()
