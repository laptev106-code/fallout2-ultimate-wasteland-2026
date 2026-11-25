#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOXX MODERNIZATION & EXPANSION MASTER SCRIPT (FIX-56)
Integrates:
1. Alcohol withdrawal & addiction strings in obj_dude.msg (RU CP1251 + EN Latin-1)
2. Enclave Finale RPG checks (Sergeant Granite tactical briefing & Martin Frobisher demolition calculation)
3. 359 female dialogue overrides (text/russian/dialog_female) with Talking Heads lip-sync preservation
4. ddraw.ini FemaleDialogMsgs=1 enablement across all profiles
5. KeysHelp F1 overlay modernization with current 2026 keybindings
"""

import os
import sys
sys.path.insert(0, r"E:\FALLOUT Ult pjt")
import ctypes
import struct
import zlib
import re
import shutil
import subprocess
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

TOOLS_DIR = r"E:\FALLOUT Ult pjt\tools"
HEADERS_DIR = os.path.join(TOOLS_DIR, "headers")
COMPILER = os.path.join(TOOLS_DIR, "compile.exe")
FOXX_DAT = r"E:\Games\Fallout 2 (Expansion Version)\master.dat"

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def get_short_path(long_path):
    buf = ctypes.create_unicode_buffer(500)
    res = ctypes.windll.kernel32.GetShortPathNameW(long_path, buf, 500)
    return buf.value if res > 0 else long_path

# ===========================================================================
# 1. OBJ_DUDE.MSG (ALCOHOL ADDICTION & WITHDRAWAL)
# ===========================================================================

OBJ_DUDE_RU_ADDITIONS = """
{500}{}{У вас развилась алкогольная зависимость. Жажда выпивки вскоре начнет терзать ваше тело.}
{800}{}{Тяга к алкоголю становится все сильнее.}
{801}{}{Все тело бьет крупная дрожь. В горле пересохло, накатывает тяжелая волна похмелья. Вам жизненно необходимо промочить горло чем-нибудь крепким.}
{802}{}{Вы ощущаете, как тяжелый груз спадает с плеч. Мучительная тяга к спиртному наконец-то отпустила вас.}
{1000}{}{Мысли путаются. Вы чувствуете непреодолимое желание вскрыть еще одну пачку карт «Трэджик».}
"""

OBJ_DUDE_EN_ADDITIONS = """
{500}{}{You have become addicted to alcohol. The craving for liquor will soon consume your body.}
{800}{}{Your craving for alcohol is growing worse.}
{801}{}{A severe tremor wracks your body. Your throat is parched and a crushing hangover sets in. You desperately need a stiff drink.}
{802}{}{A heavy weight lifts from your shoulders. The agonizing craving for alcohol has finally subsided.}
{1000}{}{Your thoughts are clouded. You feel an irresistible urge to open just one more pack of Tragic cards.}
"""

def update_obj_dude():
    print("\n--- [1/5] Updating obj_dude.msg ---")
    base_ru = os.path.join(TOOLS_DIR, "obj_dude_ru.msg")
    base_en = os.path.join(TOOLS_DIR, "obj_dude_en.msg")

    # Fetch from rpu_russian.dat and rpu.dat if not present
    rpu_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
    rpu_ru_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"

    files_ru = read_dat2_directory(rpu_ru_dat)
    ru_raw = extract_dat2_file(files_ru["text\\russian\\dialog\\obj_dude.msg"]).decode("cp1251", errors="replace")

    files_en = read_dat2_directory(rpu_dat)
    en_raw = extract_dat2_file(files_en["text\\english\\dialog\\obj_dude.msg"]).decode("latin-1", errors="replace")

    # Append lines
    ru_lines = [l for l in ru_raw.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [500, 800, 801, 802, 1000])]
    ru_final = "\n".join(ru_lines).strip() + "\n\n" + OBJ_DUDE_RU_ADDITIONS.strip() + "\n"

    en_lines = [l for l in en_raw.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [500, 800, 801, 802, 1000])]
    en_final = "\n".join(en_lines).strip() + "\n\n" + OBJ_DUDE_EN_ADDITIONS.strip() + "\n"

    # Deploy to all profiles
    for p in PROFILES:
        target_unc = os.path.join(p, "mods", "rpu_russian_uncensored.dat")
        if not os.path.exists(target_unc): continue
        ru_dir = os.path.join(target_unc, "text", "russian", "dialog")
        en_dir = os.path.join(target_unc, "text", "english", "dialog")
        os.makedirs(ru_dir, exist_ok=True)
        os.makedirs(en_dir, exist_ok=True)

        with open(os.path.join(ru_dir, "obj_dude.msg"), "w", encoding="cp1251") as f:
            f.write(ru_final)
        with open(os.path.join(en_dir, "obj_dude.msg"), "w", encoding="latin-1") as f:
            f.write(en_final)
        print(f"  [+] Deployed obj_dude.msg -> {p}")

# ===========================================================================
# 2. ENCLAVE FINALE (QCGlabels: qcgranit, qcmartin)
# ===========================================================================

QCGRANIT_RU_EXT = """
{170}{}{Сержант, взгляните на вещи трезво. Хорриган -- киборг, его лобовая броня непробиваема, но контуры гидравлики на спине открыты. Если ваше отделение возьмет на себя перекрестный огонь из тяжелых плазменных винтовок, мы собьем его сервоприводы и выбьем винтокрыл. Это ваш единственный шанс спасти людей.}
{171}{}{Черт побери... Звучит как чертовски грамотный боевой расчет. Мы солдаты, а не фанатики-самоубийцы, и не собираемся тонуть вместе с этой базой. Мои ребята поддержат тебя перекрестным огнем по сочленениям Хорригана. Встретимся в шлюзе!}
{172}{}{По позициям, сержант. Покажем этой твари, на что способны бойцы Пустоши и Анклава.}
"""

QCGRANIT_EN_EXT = """
{170}{}{Sergeant, face reality. Horrigan is a cyborg; his frontal armor is impenetrable, but the hydraulic conduits on his spine are exposed. If your squad lays down crossfire with heavy plasma rifles, we will shatter his servo-actuators and secure the vertibird. It is your squad's only chance to walk away alive.}
{171}{}{Damn it... That's a solid combat operational plan. We're soldiers, not suicidal zealots, and we're not drowning with this rig. My squad will lay down crossfire on Horrigan's actuator joints. See you at the airlock!}
{172}{}{Move into positions, Sergeant. Let's show this monster what true soldiers can do.}
"""

QCMARTIN_RU_EXT = """
{190}{}{[Инженерный расчет] Слепой подрыв терминала заблокирует спасательные люки. Установи детонатор с задержкой на обходную шину охлаждения -- тогда защитные поля спадут без взрыва в жилом блоке.}
{191}{}{Господи... ты прав. Если бы мы просто взорвали консоль, двери заклинило бы намертво. Я сделаю все в точности так, как ты рассчитал. Беги наверх к винтокрылу, а мы подготовим эвакуацию!}
{192}{}{Отличная идея. Я могу использовать взрывчатку, чтобы взорвать компьютер. Затем ты побежишь наверх к моему винтокрылу. Я -- прямо за тобой.}
"""

QCMARTIN_EN_EXT = """
{190}{}{[Engineering Calculation] Blindly detonating the console will seal the emergency bulkheads. Rig a timed charge directly to the coolant bypass bus -- the containment fields will drop without collapsing the habitation sector.}
{191}{}{My God... you're right. If we had just blasted the console, the blast doors would have welded shut permanently. I'll set the charges exactly as you calculated. Head up to the vertibird, we'll stage the evacuation!}
{192}{}{Good idea. I can use the explosives to destroy the computer. Then run up to my vertibird. I'm right behind you.}
"""

def update_enclave_finale():
    print("\n--- [2/5] Building Enclave Finale Upgrades ---")
    enclave_dir = os.path.join(TOOLS_DIR, "enclave")
    os.makedirs(enclave_dir, exist_ok=True)

    # 1. QCGRANIT SSL
    with open(os.path.join(TOOLS_DIR, "qcgranit.ssl"), "r", encoding="utf-8") as f:
        granit_code = f.read()

    granit_decl = "\nprocedure NodeTacticalBriefing;\n"
    granit_code = granit_code.replace("procedure Node017;", "procedure Node017;" + granit_decl, 1)

    old_node011 = """procedure Node011 begin
   Reply(145);

   NOption(146,Node011a,004);
   BOption(147,Node998,004);
   NOption(148,Node999,004);
end"""

    new_node011 = """procedure Node011 begin
   Reply(145);

   NOption(146,Node011a,004);
   if ((has_skill(dude_obj, SKILL_SPEECH) >= 80) and ((has_skill(dude_obj, SKILL_BIG_GUNS) >= 85) or (has_skill(dude_obj, SKILL_ENERGY_WEAPONS) >= 85))) then begin
      NOption(170, NodeTacticalBriefing, 004);
   end
   BOption(147,Node998,004);
   NOption(148,Node999,004);
end"""
    granit_code = granit_code.replace(old_node011, new_node011)

    granit_body = """
procedure NodeTacticalBriefing begin
   set_global_var(GVAR_ENCLAVE_GRANITE_JOINED, 1);
   give_xp(1000);
   inc_general_rep(15);
   Reply(171);
   GOption(172, Node999, 004);
end
"""
    granit_code = granit_code + "\n" + granit_body
    with open(os.path.join(enclave_dir, "qcgranit.ssl"), "w", encoding="utf-8") as f:
        f.write(granit_code)

    # 2. QCMARTIN SSL
    with open(os.path.join(TOOLS_DIR, "qcmartin.ssl"), "r", encoding="utf-8") as f:
        martin_code = f.read()

    martin_decl = "\nprocedure NodeDemolitionBriefing;\n"
    martin_code = martin_code.replace("procedure Node020;", "procedure Node020;" + martin_decl, 1)

    old_node015 = """procedure Node015 begin
   set_global_var(GVAR_ENCLAVE_POWER_PLANT,PLANT_KNOWN);

   Reply(167);

   if ((dude_item_count(PID_DYNAMITE)) or (dude_item_count(PID_PLASTIC_EXPLOSIVES))) then begin
      GOption(168,Node013,004);
   end else begin
      NOption(169,Node016,004);
   end
end"""

    new_node015 = """procedure Node015 begin
   set_global_var(GVAR_ENCLAVE_POWER_PLANT,PLANT_KNOWN);

   Reply(167);

   if ((has_skill(dude_obj, SKILL_TRAPS) >= 75) or (has_skill(dude_obj, SKILL_SCIENCE) >= 70)) then begin
      GOption(190, NodeDemolitionBriefing, 004);
   end
   if ((dude_item_count(PID_DYNAMITE)) or (dude_item_count(PID_PLASTIC_EXPLOSIVES))) then begin
      GOption(168,Node013,004);
   end else begin
      NOption(169,Node016,004);
   end
end"""
    martin_code = martin_code.replace(old_node015, new_node015)

    martin_body = """
procedure NodeDemolitionBriefing begin
   give_xp(300);
   Reply(191);
   GOption(192, Node013, 004);
end
"""
    martin_code = martin_code + "\n" + martin_body
    with open(os.path.join(enclave_dir, "qcmartin.ssl"), "w", encoding="utf-8") as f:
        f.write(martin_code)

    # 3. Update MSGs
    rpu_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"
    rpu_ru_dat = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
    files_ru = read_dat2_directory(rpu_ru_dat)
    files_en = read_dat2_directory(rpu_dat)

    # qcgranit
    g_ru = extract_dat2_file(files_ru["text\\russian\\dialog\\qcgranit.msg"]).decode("cp1251", errors="replace")
    g_en = extract_dat2_file(files_en["text\\english\\dialog\\qcgranit.msg"]).decode("latin-1", errors="replace")
    g_ru_lines = [l for l in g_ru.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [170, 171, 172])]
    g_en_lines = [l for l in g_en.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [170, 171, 172])]
    g_ru_final = "\n".join(g_ru_lines).strip() + "\n\n" + QCGRANIT_RU_EXT.strip() + "\n"
    g_en_final = "\n".join(g_en_lines).strip() + "\n\n" + QCGRANIT_EN_EXT.strip() + "\n"

    # qcmartin
    m_ru = extract_dat2_file(files_ru["text\\russian\\dialog\\qcmartin.msg"]).decode("cp1251", errors="replace")
    m_en = extract_dat2_file(files_en["text\\english\\dialog\\qcmartin.msg"]).decode("latin-1", errors="replace")
    m_ru_lines = [l for l in m_ru.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [190, 191, 192])]
    m_en_lines = [l for l in m_en.splitlines() if not any(l.strip().startswith(f"{{{num}}}") for num in [190, 191, 192])]
    m_ru_final = "\n".join(m_ru_lines).strip() + "\n\n" + QCMARTIN_RU_EXT.strip() + "\n"
    m_en_final = "\n".join(m_en_lines).strip() + "\n\n" + QCMARTIN_EN_EXT.strip() + "\n"

    # Save to enclave_dir
    with open(os.path.join(enclave_dir, "qcgranit_ru.msg"), "w", encoding="cp1251") as f: f.write(g_ru_final)
    with open(os.path.join(enclave_dir, "qcgranit_en.msg"), "w", encoding="latin-1") as f: f.write(g_en_final)
    with open(os.path.join(enclave_dir, "qcmartin_ru.msg"), "w", encoding="cp1251") as f: f.write(m_ru_final)
    with open(os.path.join(enclave_dir, "qcmartin_en.msg"), "w", encoding="latin-1") as f: f.write(m_en_final)

    # 4. Compile
    short_tools = get_short_path(TOOLS_DIR)
    compiler = os.path.join(short_tools, "compile.exe")
    headers = os.path.join(short_tools, "headers")

    for s in ["qcgranit", "qcmartin"]:
        cmd = [compiler, "-p", "-q", "-s", f"-I{headers}", "-O2", f"{s}.ssl", "-o", f"{s}.int"]
        res = subprocess.run(cmd, cwd=enclave_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[FAIL] Error compiling {s}.ssl:")
            print(res.stdout, res.stderr)
            sys.exit(1)
        int_size = os.path.getsize(os.path.join(enclave_dir, f"{s}.int"))
        print(f"  [OK] Compiled {s}.ssl -> {s}.int ({int_size} bytes)")

    # 5. Deploy
    for p in PROFILES:
        target_unc = os.path.join(p, "mods", "rpu_russian_uncensored.dat")
        if not os.path.exists(target_unc): continue
        scripts_dst = os.path.join(target_unc, "scripts")
        ru_dst = os.path.join(target_unc, "text", "russian", "dialog")
        en_dst = os.path.join(target_unc, "text", "english", "dialog")
        os.makedirs(scripts_dst, exist_ok=True)
        os.makedirs(ru_dst, exist_ok=True)
        os.makedirs(en_dst, exist_ok=True)

        for s in ["qcgranit", "qcmartin"]:
            shutil.copy2(os.path.join(enclave_dir, f"{s}.int"), os.path.join(scripts_dst, f"{s}.int"))
            shutil.copy2(os.path.join(enclave_dir, f"{s}_ru.msg"), os.path.join(ru_dst, f"{s}.msg"))
            shutil.copy2(os.path.join(enclave_dir, f"{s}_en.msg"), os.path.join(en_dst, f"{s}.msg"))

            # Remove loose copies
            loose = os.path.join(p, "DATA", "scripts", f"{s}.int")
            if os.path.exists(loose): os.remove(loose)

        print(f"  [+] Deployed Enclave fixes -> {p}")

# ===========================================================================
# 3. GENDER DIALOGUE LAYER (359 DIALOG_FEMALE FILES)
# ===========================================================================

def deploy_gender_dialogue_layer():
    print("\n--- [3/5] Deploying Gender Dialogue Layer (359 files) ---")
    foxx_files = read_dat2_directory(FOXX_DAT)
    female_keys = [k for k in foxx_files if "dialog_female" in k]
    print(f"  Found {len(female_keys)} dialog_female files in Foxx master.dat")

    # Read base talking head lip-sync tags from rpu_russian_uncensored.dat
    master_unc = os.path.join(r"E:\FALLOUT Ult pjt", "mods", "rpu_russian_uncensored.dat", "text", "russian", "dialog")

    def get_lip_sync_tags(msg_text):
        tags = {}
        for m in re.finditer(r'\{(\d+)\}\s*\{([A-Za-z0-9_]+)\}\s*\{', msg_text):
            tags[int(m.group(1))] = m.group(2)
        return tags

    def inject_lip_sync_tags(msg_text, tags):
        if not tags: return msg_text
        def repl(m):
            num = int(m.group(1))
            current_tag = m.group(2).strip()
            text_body = m.group(3)
            if not current_tag and num in tags:
                return f"{{{num}}}{{{tags[num]}}}{{{text_body}}}"
            return m.group(0)
        return re.sub(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}', repl, msg_text, flags=re.DOTALL)

    # Process all files into a temporary staging folder
    staging_dir = os.path.join(TOOLS_DIR, "dialog_female_staged")
    os.makedirs(staging_dir, exist_ok=True)

    synced_tags_count = 0
    for fk in female_keys:
        basename = os.path.basename(fk)
        raw_bytes = extract_dat2_file(foxx_files[fk])

        # Foxx's female dialogs are in CP1251
        text = raw_bytes.decode("cp1251", errors="replace")

        # Check if master base has lip sync tags for this file
        base_path = os.path.join(master_unc, basename)
        if os.path.exists(base_path):
            with open(base_path, "r", encoding="cp1251", errors="replace") as bf:
                base_text = bf.read()
            base_tags = get_lip_sync_tags(base_text)
            if base_tags:
                new_text = inject_lip_sync_tags(text, base_tags)
                if new_text != text:
                    synced_tags_count += 1
                    text = new_text

        out_file = os.path.join(staging_dir, basename)
        with open(out_file, "w", encoding="cp1251") as f:
            f.write(text)

    print(f"  Staged {len(female_keys)} dialog_female files (lip-sync mirrored for {synced_tags_count} files).")

    # Deploy to all profiles
    for p in PROFILES:
        target_unc = os.path.join(p, "mods", "rpu_russian_uncensored.dat")
        if not os.path.exists(target_unc): continue

        ru_fem_dir = os.path.join(target_unc, "text", "russian", "dialog_female")
        en_fem_dir = os.path.join(target_unc, "text", "english", "dialog_female")
        os.makedirs(ru_fem_dir, exist_ok=True)
        os.makedirs(en_fem_dir, exist_ok=True)

        for fname in os.listdir(staging_dir):
            src = os.path.join(staging_dir, fname)
            shutil.copy2(src, os.path.join(ru_fem_dir, fname))
            shutil.copy2(src, os.path.join(en_fem_dir, fname))

        print(f"  [+] Deployed 359 dialog_female files -> {target_unc}")

    # Clean staging
    shutil.rmtree(staging_dir, ignore_errors=True)

# ===========================================================================
# 4. DDRAW.INI FEMALEDIALOGMSGS=1 ACTIVATION
# ===========================================================================

def enable_female_dialog_msgs():
    print("\n--- [4/5] Activating FemaleDialogMsgs=1 in ddraw.ini ---")
    for p in PROFILES:
        ini_path = os.path.join(p, "ddraw.ini")
        if not os.path.exists(ini_path): continue

        with open(ini_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if "FemaleDialogMsgs=0" in content:
            content = content.replace("FemaleDialogMsgs=0", "FemaleDialogMsgs=1")
            with open(ini_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK] FemaleDialogMsgs=1 enabled in {ini_path}")
        elif "FemaleDialogMsgs=1" in content:
            print(f"  [OK] FemaleDialogMsgs=1 already active in {ini_path}")
        else:
            print(f"  [WARN] FemaleDialogMsgs setting not found in {ini_path}")

# ===========================================================================
# 5. KEYSHELP MODERNIZATION
# ===========================================================================

def modernize_keyshelp():
    print("\n--- [5/5] Modernizing KeysHelp F1 Overlay ---")

    # In gl_keyshelp.int, replace archaic strings with our 2026 controls
    # We match fixed size or patch string table
    sample_int = os.path.join(r"E:\Fallout2_Ultimate\Fallout2_Gameplay", "mods", "KeysHelp.dat", "scripts", "gl_keyshelp.int")
    if not os.path.exists(sample_int):
        print("  [WARN] KeysHelp not found")
        return

    with open(sample_int, "rb") as f:
        data = f.read()

    # Replacements (encoded as cp1251):
    replacements = [
        (b"F4: \xd1\xee\xf5\xf0\xe0\xed\xe5\xed\xe8\xe5 / F8: \xc7\xe0\xe3\xf0\xf3\xe7\xea\xe0", # F4: Сохранение / F8: Загрузка
         b"F5: QuickSave / F8: QuickLoad      "),
        (b"F5: \xc1\xfb\xf1\xf2\xf0\xee\xe5 \xf1\xee\xf5\xf0\xe0\xed\xe5\xed\xe8\xe5 / F9: \xc1\xfb\xf1\xf2\xf0\xe0\xff \xe7\xe0\xe3\xf0\xf3\xe7\xea\xe0", # F5: Быстрое / F9: Быстрая
         b"F9: \xcc\xe5\xed\xfe \xf1\xeb\xee\xf2\xee\xe2 / Caps Lock: \xcf\xee\xe4\xf1\xe2\xe5\xf2\xea\xe0        "), # F9: Меню слотов / Caps Lock: Подсветка
        (b"*G: \xd1\xee\xe1\xe8\xf0\xe0\xf2\xfc \xeb\xf3\xf2 / D: \xc8\xf1\xff\xee\xeb\xfc\xe7\xee\xe2\xe0\xf2\xfc \xee\xf7\xe5\xf0\xe5\xe4\xfc", # *G: Собирать лут
         b"Ctrl+T: \xd1\xe1\xee\xf0 \xeb\xf3\xf2\xe0 / D: \xce\xf7\xe5\xf0\xe5\xe4\xfc      "), # Ctrl+T: Сбор лута / D: Очередь
    ]

    for p in PROFILES:
        k_path = os.path.join(p, "mods", "KeysHelp.dat", "scripts", "gl_keyshelp.int")
        if not os.path.exists(k_path): continue
        with open(k_path, "rb") as f:
            cur = f.read()
        patched = cur
        for old_b, new_b in replacements:
            # adjust length to match exactly
            if len(old_b) > len(new_b):
                pad_new = new_b + b" " * (len(old_b) - len(new_b))
            elif len(new_b) > len(old_b):
                pad_new = new_b[:len(old_b)]
            else:
                pad_new = new_b
            if old_b in patched:
                patched = patched.replace(old_b, pad_new)

        with open(k_path, "wb") as f:
            f.write(patched)
        print(f"  [+] Patched modern keys into KeysHelp.dat -> {k_path}")

# ===========================================================================
# MAIN ENTRY POINT
# ===========================================================================

def main():
    print("=" * 65)
    print("  FOXX MODERNIZATION & EXPANSION MASTER PIPELINE (FIX-56)")
    print("=" * 65)

    update_obj_dude()
    update_enclave_finale()
    deploy_gender_dialogue_layer()
    enable_female_dialog_msgs()
    modernize_keyshelp()

    print("\n-> FOXX MODERNIZATION PIPELINE COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    main()
