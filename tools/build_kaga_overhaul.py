#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KAGA ENCOUNTERS RPG OVERHAUL BUILDER (FIX-56)
- Adds Outdoorsman and Speech skill checks to Kaga encounters 1..4
- Preserves full 1998 Black Isle authenticity
- Full RU (CP1251) and EN (Latin-1) parity
- Compiles via sFall compiler and deploys to all game profiles
"""

import os
import sys
import ctypes
import subprocess
import shutil
import re

TOOLS_DIR = r"E:\FALLOUT Ult pjt\tools"
KAGA_DIR = os.path.join(TOOLS_DIR, "kaga")
HEADERS_DIR = os.path.join(TOOLS_DIR, "headers")
COMPILER = os.path.join(TOOLS_DIR, "compile.exe")

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def get_short_path(long_path):
    buf = ctypes.create_unicode_buffer(500)
    res = ctypes.windll.kernel32.GetShortPathNameW(long_path, buf, 500)
    return buf.value if res > 0 else long_path

# ---------------------------------------------------------------------------
# 1. DIALOGUE TEXTS
# ---------------------------------------------------------------------------

KAGA1_RU_EXT = """
{250}{}{[Заметив примятую траву и следы засады, резко уйти за валун и вскинуть оружие] Слишком шумно крадешься, Кага. Твоя засада шита белыми нитками.}
{251}{}{Проклятье! Ты заметил нас?! Убить его, живо!}
{252}{}{[Использовать замешательство врагов и атаковать первым]}
{260}{}{Кага, духи предков видят твое падение. Ты был лучшим охотником Арройо, а теперь опустился до лесного разбойника и падальщика? Неужели изгнание выжгло в тебе последние остатки чести?}
{261}{}{[Лицо Каги искажается от ярости и стыда. Его рука с копьем заметно дрожит.] Заткнись! Заткнись!! Ты ничего не знаешь об изгнании! Ты не смеешь поучать меня именем предков! Я... мы еще покончим с этим, но не здесь и не сейчас!}
{262}{}{[Позволить ему уйти] Убирайся, Кага. В следующий раз пощады не будет.}
{263}{}{Ты дрожишь, Кага. Твое копье пляшет в руках. Попробуй достать меня, если кишка не тонка.}
"""

KAGA1_EN_EXT = """
{250}{}{[Spotting trampled grass and signs of an ambush, you duck behind a boulder and raise your weapon] You tread too heavily, Kaga. Your ambush was obvious from a mile away.}
{251}{}{Curse you! You spotted us?! Kill him, now!}
{252}{}{[Take advantage of their confusion and strike first]}
{260}{}{Kaga, the spirits of our ancestors weep at your fall. You were Arroyo's finest hunter, and now you have devolved into a common bandit and scavenger? Did exile truly burn away the last shreds of your honor?}
{261}{}{[Kaga's face contorts with rage and shame. His spear hand trembles visibly.] Shut up! SHUT UP!! You know nothing of exile! You dare not lecture me in the name of our ancestors! I... we will settle this, but not here, and not today!}
{262}{}{[Let him go] Get out of here, Kaga. Next time there will be no mercy.}
{263}{}{You are trembling, Kaga. Your spear dances in your hands. Come and get me if you have the stomach for it.}
"""

KAGA2_RU_EXT = """
{250}{}{[Заметить свежие следы подкованных сапог и блеск заклепок в кустах] Кага, твои головорезы шумят как стадо браминов на водопое.}
{251}{}{Опять твои уловки дикаря! Неважно -- на этот раз вас окружат со всех сторон! Взять его!}
{252}{}{[Ударить по флангу, пока наемники не успели сомкнуть кольцо]}
{260}{}{Ты нанял отбросов Пустоши, чтобы спрятаться за их спинами? Великий воин Кага боится сойтись со мной один на один?}
{261}{}{[Кага багровеет и злобно рычит на своих людей.] Назад, бездельники! Этот щенок мой! Я лично выпущу ему кишки!}
{262}{}{[Приготовиться к дуэли] Вот теперь поговорим на равных.}
"""

KAGA2_EN_EXT = """
{250}{}{[Spotting fresh boot prints and the glint of leather studs in the brush] Kaga, your thugs make as much noise as a herd of brahmin at a waterhole.}
{251}{}{Your tribal tricks again! It matters not -- this time you are surrounded! Take him down!}
{252}{}{[Strike the flank before the mercenaries close the ring]}
{260}{}{You hired wasteland scum just to hide behind their backs? The great warrior Kaga is afraid to face me alone?}
{261}{}{[Kaga turns red with fury and snarls at his men.] Stand back, you dogs! This runt is mine! I will gut him with my own hands!}
{262}{}{[Prepare for the duel] Now we fight on equal terms.}
"""

KAGA3_RU_EXT = """
{250}{}{[Заметить оптический отблеск прицела на холме и укрыться за выступом скалы] Ты потратился на металлолом и наемников, Кага, но забыл замаскировать позиции.}
{251}{}{Хватит болтать! В этот металл пули не пройдут, дикарь! Огонь на поражение!}
{252}{}{[Открыть ответный огонь из выгодного укрытия]}
{260}{}{Сколько крышек ты спустил на этих наемников, Кага? Они бросят тебя в канаве при первых же потерях. Думаешь, чужие ружья вернут тебе потерянную гордость?}
{261}{}{[Наемники переглядываются, их боевой дух заметно падает.] Молчать! Я плачу вам за стрельбу, а не за сомнения! Стреляйте в него, идиоты!}
{262}{}{[Начать бой против деморализованных наемников]}
"""

KAGA3_EN_EXT = """
{250}{}{[Spotting the optical glint of a scope on the ridge and taking cover behind a rock] You spent caps on scrap metal and mercenaries, Kaga, but forgot to camouflage your positions.}
{251}{}{Enough talk! Your bullets won't pierce this steel, savage! Fire at will!}
{252}{}{[Open fire from advantageous cover]}
{260}{}{How many caps did you blow on these mercenaries, Kaga? They will abandon you in a ditch at the first sign of casualties. Do you truly think hired guns will restore your lost pride?}
{261}{}{[The mercenaries exchange uneasy glances, their morale visibly shaken.] Silence! I pay you to shoot, not to doubt! Shoot him, you idiots!}
{262}{}{[Engage the demoralized mercenaries]}
"""

KAGA4_RU_EXT = """
{250}{}{[Уловить запах оружейной смазки по ветру и обойти сектор обстрела] Твоя засада рассчитана на дилетантов, Кага. Я уже зашел тебе во фланг.}
{251}{}{Как ты... Черт подери! Разворачивайте пулеметы! Не дайте ему уйти!}
{252}{}{[Открыть огонь по незащищенному флангу отряда]}
"""

KAGA4_EN_EXT = """
{250}{}{[Catching the scent of gun oil on the wind and flanking their firing lane] Your ambush is meant for amateurs, Kaga. I am already on your flank.}
{251}{}{How did you... Damn it! Pivot the guns! Don't let him slip away!}
{252}{}{[Open fire on their exposed flank]}
"""

def update_msg_file(base_path, ext_text, out_path, encoding):
    with open(base_path, "r", encoding=encoding, errors="replace") as f:
        lines = f.readlines()
    clean_lines = []
    for l in lines:
        if l.strip().startswith("{25") or l.strip().startswith("{26"):
            continue
        clean_lines.append(l)
    content = "".join(clean_lines).strip() + "\n\n" + ext_text.strip() + "\n"
    with open(out_path, "w", encoding=encoding) as f:
        f.write(content)
    print(f"Updated {os.path.basename(out_path)} ({len(content)} chars, {encoding})")

# ---------------------------------------------------------------------------
# 2. SSL SCRIPT MODIFICATIONS
# ---------------------------------------------------------------------------

def build_eckaga1_ssl():
    ssl_file = os.path.join(KAGA_DIR, "eckaga1.ssl")
    with open(ssl_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Declarations
    decl = """
procedure NodeAmbushFlank;
procedure NodeAmbushCombat;
procedure NodeShameKaga;
procedure NodeKagaRetreat;
procedure NodeKagaFurious;
"""
    code = code.replace("procedure Node005;", "procedure Node005;" + decl, 1)

    # In Node001: inject options
    old_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   NLowOption(200,Node004);
end"""

    new_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   if (has_skill(dude_obj, SKILL_OUTDOORSMAN) >= 40) then begin
      NOption(250, NodeAmbushFlank, 004);
   end
   if ((has_skill(dude_obj, SKILL_SPEECH) >= 50) and (dude_charisma >= 6)) then begin
      NOption(260, NodeShameKaga, 004);
   end
   NLowOption(200,Node004);
end"""
    code = code.replace(old_node001, new_node001)

    # Append implementation procedures
    body = """
procedure NodeAmbushFlank begin
   give_xp(150);
   Reply(251);
   NOption(252, NodeAmbushCombat, 004);
end

procedure NodeAmbushCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack_setup(dude_obj, self_obj);
end

procedure NodeShameKaga begin
   Reply(261);
   NOption(262, NodeKagaRetreat, 004);
   NOption(263, NodeKagaFurious, 004);
end

procedure NodeKagaRetreat begin
   give_xp(250);
   inc_general_rep(5);
   set_kaga_1;
   set_kaga_met;
   set_local_var(LVAR_Defeated, 1);
   critter_set_flee_state(self_obj, 1);
   float_msg(self_obj, mstr(108), FLOAT_MSG_YELLOW);
end

procedure NodeKagaFurious begin
   give_xp(100);
   set_local_var(LVAR_Hostile, 2);
   attack(dude_obj);
end
"""
    code = code + "\n" + body
    out_ssl = os.path.join(KAGA_DIR, "gen_eckaga1.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(code)
    print("Generated gen_eckaga1.ssl")

def build_eckaga2_ssl():
    ssl_file = os.path.join(KAGA_DIR, "eckaga2.ssl")
    with open(ssl_file, "r", encoding="utf-8") as f:
        code = f.read()

    decl = """
procedure NodeAmbushFlank;
procedure NodeAmbushCombat;
procedure NodeDuelChallenge;
procedure NodeDuelCombat;
"""
    code = code.replace("procedure Node005;", "procedure Node005;" + decl, 1)

    old_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   NLowOption(200,Node004);
end"""

    new_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   if (has_skill(dude_obj, SKILL_OUTDOORSMAN) >= 55) then begin
      NOption(250, NodeAmbushFlank, 004);
   end
   if ((has_skill(dude_obj, SKILL_SPEECH) >= 65) and (dude_charisma >= 6)) then begin
      NOption(260, NodeDuelChallenge, 004);
   end
   NLowOption(200,Node004);
end"""
    code = code.replace(old_node001, new_node001)

    body = """
procedure NodeAmbushFlank begin
   give_xp(200);
   Reply(251);
   NOption(252, NodeAmbushCombat, 004);
end

procedure NodeAmbushCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack_setup(dude_obj, self_obj);
end

procedure NodeDuelChallenge begin
   give_xp(300);
   Reply(261);
   NOption(262, NodeDuelCombat, 004);
end

procedure NodeDuelCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack(dude_obj);
end
"""
    code = code + "\n" + body
    out_ssl = os.path.join(KAGA_DIR, "gen_eckaga2.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(code)
    print("Generated gen_eckaga2.ssl")

def build_eckaga3_ssl():
    ssl_file = os.path.join(KAGA_DIR, "eckaga3.ssl")
    with open(ssl_file, "r", encoding="utf-8") as f:
        code = f.read()

    decl = """
procedure NodeAmbushFlank;
procedure NodeAmbushCombat;
procedure NodeMercDemoralize;
procedure NodeMercCombat;
"""
    code = code.replace("procedure Node005;", "procedure Node005;" + decl, 1)

    old_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   NLowOption(200,Node004);
end"""

    new_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   if (has_skill(dude_obj, SKILL_OUTDOORSMAN) >= 70) then begin
      NOption(250, NodeAmbushFlank, 004);
   end
   if (has_skill(dude_obj, SKILL_SPEECH) >= 75) then begin
      NOption(260, NodeMercDemoralize, 004);
   end
   NLowOption(200,Node004);
end"""
    code = code.replace(old_node001, new_node001)

    body = """
procedure NodeAmbushFlank begin
   give_xp(250);
   Reply(251);
   NOption(252, NodeAmbushCombat, 004);
end

procedure NodeAmbushCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack_setup(dude_obj, self_obj);
end

procedure NodeMercDemoralize begin
   give_xp(350);
   Reply(261);
   NOption(262, NodeMercCombat, 004);
end

procedure NodeMercCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack(dude_obj);
end
"""
    code = code + "\n" + body
    out_ssl = os.path.join(KAGA_DIR, "gen_eckaga3.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(code)
    print("Generated gen_eckaga3.ssl")

def build_eckaga4_ssl():
    ssl_file = os.path.join(KAGA_DIR, "eckaga4.ssl")
    with open(ssl_file, "r", encoding="utf-8") as f:
        code = f.read()

    decl = """
procedure NodeAmbushFlank;
procedure NodeAmbushCombat;
"""
    code = code.replace("procedure Node005;", "procedure Node005;" + decl, 1)

    old_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   NLowOption(200,Node004);
end"""

    new_node001 = """procedure Node001 begin
   set_local_var(LVAR_Herebefore, 1);
   Reply(150);
   NOption(151,Node002,004);
   NOption(152,Node003,004);
   if (has_skill(dude_obj, SKILL_OUTDOORSMAN) >= 80) then begin
      NOption(250, NodeAmbushFlank, 004);
   end
   NLowOption(200,Node004);
end"""
    code = code.replace(old_node001, new_node001)

    body = """
procedure NodeAmbushFlank begin
   give_xp(300);
   Reply(251);
   NOption(252, NodeAmbushCombat, 004);
end

procedure NodeAmbushCombat begin
   set_local_var(LVAR_Hostile, 2);
   attack_setup(dude_obj, self_obj);
end
"""
    code = code + "\n" + body
    out_ssl = os.path.join(KAGA_DIR, "gen_eckaga4.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(code)
    print("Generated gen_eckaga4.ssl")

# ---------------------------------------------------------------------------
# 3. COMPILATION AND DEPLOYMENT
# ---------------------------------------------------------------------------

def compile_script(script_base):
    target_dir = KAGA_DIR
    short_tools = get_short_path(TOOLS_DIR)
    compiler = os.path.join(short_tools, "compile.exe")
    headers = os.path.join(short_tools, "headers")

    ssl_filename = f"gen_{script_base}.ssl"
    int_filename = f"{script_base}.int"

    cmd = [
        compiler,
        "-p",
        "-q",
        "-s",
        f"-I{headers}",
        "-O2",
        ssl_filename,
        "-o", int_filename
    ]
    res = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True)
    if res.returncode == 0:
        int_path = os.path.join(target_dir, int_filename)
        size = os.path.getsize(int_path) if os.path.exists(int_path) else 0
        print(f"[OK] Compiled {ssl_filename} -> {int_filename} ({size} bytes)")
        return True
    else:
        print(f"[FAIL] Error compiling {ssl_filename}:")
        if res.stdout: print(res.stdout)
        if res.stderr: print(res.stderr)
        return False

def deploy_kaga_overhaul():
    scripts_to_deploy = ["eckaga1", "eckaga2", "eckaga3", "eckaga4"]
    msgs_to_deploy = ["eckaga1", "eckaga2", "eckaga3", "eckaga4", "eckaga5"]

    for base in PROFILES:
        target_unc = os.path.join(base, "mods", "rpu_russian_uncensored.dat")
        if not os.path.exists(target_unc):
            continue

        scripts_dst = os.path.join(target_unc, "scripts")
        ru_dialog_dst = os.path.join(target_unc, "text", "russian", "dialog")
        en_dialog_dst = os.path.join(target_unc, "text", "english", "dialog")
        os.makedirs(scripts_dst, exist_ok=True)
        os.makedirs(ru_dialog_dst, exist_ok=True)
        os.makedirs(en_dialog_dst, exist_ok=True)

        # Deploy INTs
        for s in scripts_to_deploy:
            src_int = os.path.join(KAGA_DIR, f"{s}.int")
            if os.path.exists(src_int):
                shutil.copy2(src_int, os.path.join(scripts_dst, f"{s}.int"))

        # Deploy MSGs
        for m in msgs_to_deploy:
            ru_msg = os.path.join(KAGA_DIR, f"{m}_ru.msg")
            en_msg = os.path.join(KAGA_DIR, f"{m}_en.msg")
            if os.path.exists(ru_msg):
                shutil.copy2(ru_msg, os.path.join(ru_dialog_dst, f"{m}.msg"))
            if os.path.exists(en_msg):
                shutil.copy2(en_msg, os.path.join(en_dialog_dst, f"{m}.msg"))

        # Also remove any loose copies from DATA/scripts to maintain clean DAT priority
        loose_scripts = os.path.join(base, "DATA", "scripts")
        for s in scripts_to_deploy:
            loose_file = os.path.join(loose_scripts, f"{s}.int")
            if os.path.exists(loose_file):
                os.remove(loose_file)

        print(f"[+] Deployed Kaga Overhaul -> {base}")

def main():
    print("=" * 60)
    print("  KAGA ENCOUNTERS RPG OVERHAUL BUILD & DEPLOY")
    print("=" * 60)

    # 1. Update MSG files
    update_msg_file(os.path.join(KAGA_DIR, "eckaga1_ru.msg"), KAGA1_RU_EXT, os.path.join(KAGA_DIR, "eckaga1_ru.msg"), "cp1251")
    update_msg_file(os.path.join(KAGA_DIR, "eckaga1_en.msg"), KAGA1_EN_EXT, os.path.join(KAGA_DIR, "eckaga1_en.msg"), "latin-1")

    update_msg_file(os.path.join(KAGA_DIR, "eckaga2_ru.msg"), KAGA2_RU_EXT, os.path.join(KAGA_DIR, "eckaga2_ru.msg"), "cp1251")
    update_msg_file(os.path.join(KAGA_DIR, "eckaga2_en.msg"), KAGA2_EN_EXT, os.path.join(KAGA_DIR, "eckaga2_en.msg"), "latin-1")

    update_msg_file(os.path.join(KAGA_DIR, "eckaga3_ru.msg"), KAGA3_RU_EXT, os.path.join(KAGA_DIR, "eckaga3_ru.msg"), "cp1251")
    update_msg_file(os.path.join(KAGA_DIR, "eckaga3_en.msg"), KAGA3_EN_EXT, os.path.join(KAGA_DIR, "eckaga3_en.msg"), "latin-1")

    update_msg_file(os.path.join(KAGA_DIR, "eckaga4_ru.msg"), KAGA4_RU_EXT, os.path.join(KAGA_DIR, "eckaga4_ru.msg"), "cp1251")
    update_msg_file(os.path.join(KAGA_DIR, "eckaga4_en.msg"), KAGA4_EN_EXT, os.path.join(KAGA_DIR, "eckaga4_en.msg"), "latin-1")

    # 2. Build SSLs
    build_eckaga1_ssl()
    build_eckaga2_ssl()
    build_eckaga3_ssl()
    build_eckaga4_ssl()

    # 3. Compile
    success = True
    for s in ["eckaga1", "eckaga2", "eckaga3", "eckaga4"]:
        res = compile_script(s)
        if not res:
            success = False

    if not success:
        print("[ERROR] Compilation failed!")
        sys.exit(1)

    # 4. Deploy
    deploy_kaga_overhaul()
    print("\n-> KAGA OVERHAUL SUCCESSFULLY BUILT AND DEPLOYED.")

if __name__ == "__main__":
    main()
