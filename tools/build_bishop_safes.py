#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build and Deploy Script for New Reno Bishop Safes RPG Overhaul
Fixes:
- Mr. Bishop's Wall Safe (nimrbsf.ssl / nimrbsf.int / nimrbsf.msg)
- Mrs. Bishop's Wall Safe (nimrsbsf.ssl / nimrsbsf.int / nimrsbsf.msg)
- Angela Bishop's Safe (niabissf.ssl / niabissf.int / niabissf.msg)
"""

import os
import sys
import subprocess
import ctypes
import shutil

TOOLS_DIR = r"E:\FALLOUT Ult pjt\tools"
HEADERS_DIR = os.path.join(TOOLS_DIR, "headers")
COMPILER = os.path.join(TOOLS_DIR, "compile.exe")

MASTER_MOD_DIR = r"E:\FALLOUT Ult pjt\mods\rpu_russian_uncensored.dat"
GAMEPLAY_MOD_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat"
HD_MOD_DIR = r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat"

def get_short_path(path):
    buf = ctypes.create_unicode_buffer(500)
    ctypes.windll.kernel32.GetShortPathNameW(path, buf, 500)
    return buf.value if buf.value else path

# ---------------------------------------------------------------------------
# 1. MESSAGE FILES DEFINITIONS (RU: CP1251, EN: ANSI)
# ---------------------------------------------------------------------------

NIMRBSF_MSG_RU_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (BISHOP SAFES RPG OVERHAUL)
{500}{}{(В стене есть маленькая дверца. Может, за ней живет чилавешек? Посередине двери круглая блестящая ручка с цифирками.)}
{502}{}{Постучать в дверку: тук-тук, есть кто дома?}
{503}{}{Крутить блестящую штуку наугад!}
{504}{}{Уйти. Штука скучная.}
{510}{}{(Вы осматриваете тяжелый сейф марки «Вулкан», намертво вмурованный в кирпичную кладку. На полированной дверце виден прецизионный лимб кодового замка. Внизу под штукатуркой проглядывает едва заметный шов.)}
{512}{}{[Комбинация] Ввести кодовую комбинацию мистера Бишопа.}
{513}{}{[Ловушки] Обезвредить брикет пластита под сейфом.}
{514}{}{[Ремонт / Ловушки] Перенастроить взрыватель на комбинацию Бишопа.}
{515}{}{[Ловушки] Внимательно исследовать стыки дверцы и плинтус на предмет растяжек.}
{516}{}{[Взлом] Приложить ухо к корпусу и медленно вращать лимб, улавливая щелчки кулачков.}
{517}{}{Крутить диск наугад, надеясь на удачу.}
{518}{}{[Наука] Использовать электронный зонд для сканирования зазоров дискового механизма.}
{519}{}{Оставить сейф в покое.}
{520}{}{(Вы колотите кулаком по дверце сейфа. Рука начинает сильно болеть, а из маленького домика так никто и не выходит.)}
{525}{}{(Вы наугад вертите блестящую штуку... вдруг раздается громкое КРР-ЩЕЛК, и дверца распахивается настежь! Вот это удача!)}
{526}{}{Ура! Домик открылся!}
{527}{}{(Вы крутите штуку туда-сюда, но ничего не происходит.)}
{535}{}{(Вы набираете кодовую комбинацию мистера Бишопа. Лимб мягко встает в пазы, раздается щелчок ригеля, и тяжелая дверца сейфа открывается.)}
{536}{}{Заглянуть внутрь.}
{540}{}{(При внимательном осмотре плинтуса и стыков штукатурки вы замечаете армейский брикет пластита с детонатором, соединенным напрямую с ригелем замка. Любая ошибка при взломе привела бы к чудовищному взрыву!)}
{541}{}{(Вы тщательно исследуете дверцу и петли, но никаких признаков растяжек или взрывателей не замечаете.)}
{542}{}{[Ловушки] Попробовать аккуратно обезвредить заряд.}
{543}{}{[Ремонт / Ловушки] Попытаться перенастроить взрыватель на комбинацию хозяина.}
{544}{}{Вернуться к осмотру сейфа.}
{550}{}{(Хирургически точным движением вы перекусываете провод детонатора и осторожно извлекаете брикет пластита из гнезда в стене. Ловушка полностью обезврежена!)}
{551}{}{(Рука предательски дрогнула, щуп соскользнул с клеммы детонатора. К счастью, боек не сработал, но продолжать ковыряться наобум смертельно опасно.)}
{552}{}{Отлично. Теперь можно спокойно заняться замком.}
{560}{}{(Вы аккуратно меняете схему замыкания цепи. Теперь детонатор сработает именно тогда, когда хозяин сейфа введет свою "правильную" комбинацию. Мистера Бишопа ждет очень горячий сюрприз.)}
{561}{}{(Схема электроспуска слишком нестандартная. Вам не удается безопасно перенастроить контакты.)}
{562}{}{Превосходно. Теперь пора открыть дверцу.}
{575}{}{(В самый последний момент перед западанием третьего кулачка вы замечаете тончайшую проволоку, натягивающуюся вслед за ригелем! Еще миллиметр — и произошел бы подрыв. Вы замираете и осторожно возвращаете лимб назад. Сейф заминирован!)}
{576}{}{Уф... пронесло. Надо обезвредить заряд.}
{580}{}{(Приложив ухо к металлу, вы отчетливо слышите, как последний кулачок падает в паз. Раздается глухой щелчок «КРР-ЩЕЛК» — ригели расходятся, и сейф открыт!)}
{581}{}{Заглянуть внутрь сейфа.}
{582}{}{(Вы медленно вращаете лимб минут пятнадцать, но почувствовать западание сувальд не удается. Нужен более высокий навык взлома или специальный инструмент.)}
{585}{}{(Вы крутите лимб наугад, как вдруг он с мягким щелчком встает в стопор... затем раздается КРР-ЩЕЛК, и сейф отпирается! Чертовски повезло!)}
{586}{}{(Вы крутите диск наугад несколько минут, но ничего путного из этого не выходит.)}
{590}{}{(Электронный щуп регистрирует замкнутую слаботочную цепь, уходящую в стену под сейфом. Там заложен взрывной заряд!)}
{591}{}{Хорошо, что проверили. Надо сначала обезвредить его.}
{595}{}{(С помощью электронного зонда вы считываете акустический резонанс дисковой группы и безошибочно определяете все три цифры кода. Щелчок — и сейф открыт!)}
{596}{}{(Электроника не дает четкого сигнала сквозь толстую легированную сталь дверцы. Определить код не удается.)}
"""

NIMRBSF_MSG_EN_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (BISHOP SAFES RPG OVERHAUL)
{500}{}{(There is a tiny door in the wall. Maybe a tiny little man lives inside? In the middle of the door is a shiny round knob with numbers on it.)}
{502}{}{Knock on the little door: hello, is anybody home?}
{503}{}{Spin the shiny knob randomly!}
{504}{}{Leave. This thing is boring.}
{510}{}{(You examine the heavy 'Vulcan' safe, securely embedded in the brickwork. A precision combination dial is visible on the door. Beneath the plaster at the bottom, you notice a faint suspicious seam.)}
{512}{}{[Combination] Enter Mr. Bishop's combination.}
{513}{}{[Traps] Disarm the plastic explosive block beneath the safe.}
{514}{}{[Repair / Traps] Rewire the trigger to Bishop's combination.}
{515}{}{[Traps] Carefully examine the seams and baseboard for tripwires and traps.}
{516}{}{[Lockpick] Put your ear to the door and slowly spin the dial, listening for tumbler clicks.}
{517}{}{Spin the dial randomly, hoping for pure luck.}
{518}{}{[Science] Use an electronic probe to scan the dial mechanism clearances.}
{519}{}{Leave the safe alone.}
{520}{}{(You pound your fist on the safe door. Your hand starts hurting, and nobody answers from inside the tiny house.)}
{525}{}{(You spin the shiny thing around... suddenly there's a loud KER-KLANK, and the door swings wide open! Pure dumb luck!)}
{526}{}{Yay! The house opened!}
{527}{}{(You spin the dial back and forth, but nothing happens.)}
{535}{}{(You dial Mr. Bishop's combination. The tumblers glide smoothly into place, the deadbolt clicks, and the heavy safe door swings open.)}
{536}{}{Look inside.}
{540}{}{(Upon close examination beneath the plaster, you spot a military block of plastic explosive wired directly into the lock bolt. Any mistake while picking it would have caused a massive detonation!)}
{541}{}{(You search the door seams and hinges thoroughly, but find no obvious signs of traps.)}
{542}{}{[Traps] Try to carefully disarm the explosive charge.}
{543}{}{[Repair / Traps] Try to rewire the detonator to the owner's combination.}
{544}{}{Return to examining the safe.}
{550}{}{(With surgical precision, you snip the detonator leads and ease the plastic explosive block out from the wall. The trap is completely disarmed!)}
{551}{}{(Your hand slips slightly and the probe scrapes against the detonator terminal. Fortunately it didn't ignite, but trying again blindly is too dangerous.)}
{552}{}{Excellent. Now the lock can be picked safely.}
{560}{}{(You carefully reverse the circuit wiring. Now the detonator will trigger whenever the owner dials his 'correct' combination. Mr. Bishop is in for quite a blast.)}
{561}{}{(The circuit layout is too complex. You can't safely rewire the trigger without detonating it.)}
{562}{}{Splendid. Now let's open the safe.}
{575}{}{(At the very last instant before the third tumbler drops, you spot a hairline wire stretching behind the bolt! Another millimeter and it would have blown. You freeze and slowly back off the dial. The safe is rigged with explosives!)}
{576}{}{Whew... that was close. Need to disarm the charge first.}
{580}{}{(With your ear pressed against the cold steel, you distinctly hear the last tumbler drop into the slot. A muffled KER-KLANK echoes as the bolts retract. The safe is unlocked!)}
{581}{}{Look inside the safe.}
{582}{}{(You turn the dial slowly for fifteen minutes, but you can't feel the tumblers catching. You need a higher lockpick skill or specialized tools.)}
{585}{}{(You spin the dial randomly, when suddenly it catches with a soft click... then comes a KER-KLANK, and the safe unlocks! Incredible luck!)}
{586}{}{(You spin the dial randomly for several minutes, but achieve nothing.)}
{590}{}{(The electronic sensor detects a closed low-voltage circuit running into the wall under the safe. An explosive charge is concealed there!)}
{591}{}{Good thing I checked. Gotta disarm it first.}
{595}{}{(Using the electronic probe, you read the acoustic resonance of the dial group and precisely identify all three numbers. Click -- and the safe is unlocked!)}
{596}{}{(The electronics fail to pick up a clear signal through the heavy alloy steel door. Cannot determine the code.)}
"""

NIMRSBSF_MSG_RU_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (MRS BISHOP SAFE)
{500}{}{(Маленькая дверка в стене. Внутри, наверное, прячутся блестящие бусики!)}
{502}{}{Постучать в дверку.}
{503}{}{Крутить ручку наугад.}
{504}{}{Уйти.}
{510}{}{(Вы осматриваете компактный настенный сейф в спальне миссис Бишоп. Замок механический, трехосевой.)}
{512}{}{[Комбинация] Ввести комбинацию, которую шепнула миссис Бишоп в постели.}
{513}{}{[Взлом] Попробовать вскрыть замок отмычками.}
{514}{}{Крутить диск наугад, надеясь на удачу.}
{515}{}{[Внимательность] Тщательно прощупать нижнюю панель сейфа в поисках потайного отделения.}
{516}{}{Забрать ценности из сейфа.}
{519}{}{Оставить сейф в покое.}
{520}{}{(Вы стучите по дверце. Никто не отвечает.)}
{525}{}{(Вы крутите диск наугад... раздается КРР-ЩЕЛК, и сейф открывается!)}
{526}{}{Ура!}
{527}{}{(Ничего не происходит.)}
{530}{}{(Вы нажимаете на скрытый фиксатор в углу — и фальшивое дно отщелкивается! В тайнике лежит странный модуль для Пип-Боя.)}
{531}{}{Забрать модуль.}
{535}{}{(Вы набираете секретные цифры миссис Бишоп. Замок мягко отщелкивается.)}
{536}{}{Осмотреть содержимое.}
{540}{}{(Вы аккуратно орудуете отмычками. Минут через десять замок поддается: КРР-ЩЕЛК!)}
{541}{}{(Сувальды соскальзывают, замок не удается вскрыть.)}
{542}{}{Осмотреть сейф.}
{545}{}{(Вы крутите лимб наугад... неожиданно раздается щелчок, и замок открывается!)}
{546}{}{Вот это везение.}
{547}{}{(Вы крутите диск, но ничего не происходит.)}
"""

NIMRSBSF_MSG_EN_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (MRS BISHOP SAFE)
{500}{}{(There's a little door in the wall. Maybe shiny beads are hidden inside!)}
{502}{}{Knock on the door.}
{503}{}{Spin the knob randomly.}
{504}{}{Leave.}
{510}{}{(You examine the compact wall safe in Mrs. Bishop's bedroom. It features a three-wheel mechanical lock.)}
{512}{}{[Combination] Enter the combination Mrs. Bishop whispered in bed.}
{513}{}{[Lockpick] Attempt to pick the lock with lockpicks.}
{514}{}{Spin the dial randomly, hoping for luck.}
{515}{}{[Perception] Carefully feel along the bottom panel for a hidden compartment.}
{516}{}{Take valuables from the safe.}
{519}{}{Leave the safe alone.}
{520}{}{(You knock on the door. Nobody answers.)}
{525}{}{(You spin the knob randomly... there's a KER-KLANK, and the safe opens!)}
{526}{}{Yay!}
{527}{}{(Nothing happens.)}
{530}{}{(You press a concealed catch in the corner -- the false bottom unlatches! Inside is an odd-looking Pip-Boy module.)}
{531}{}{Take the module.}
{535}{}{(You dial Mrs. Bishop's secret numbers. The lock yields smoothly.)}
{536}{}{Examine the contents.}
{540}{}{(You work the lockpicks delicately. After ten minutes, the lock gives way: KER-KLANK!)}
{541}{}{(The tumblers slip away; you fail to open the lock.)}
{542}{}{Examine the safe.}
{545}{}{(You spin the dial blindly... suddenly a click resonates, and the safe unlocks!)}
{546}{}{Pure luck.}
{547}{}{(You spin the dial, but nothing happens.)}
"""

NIABISSF_MSG_RU_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (ANGELA BISHOP SAFE)
{500}{}{(На стене висит блестящая коробка с кнопочками, которые весело пищат.)}
{502}{}{Нажимать на все кнопки подряд!}
{504}{}{Уйти.}
{510}{}{(Вы осматриваете личный настенный сейф Анджелы Бишоп. Он оснащен электронной сенсорной панелью ввода.)}
{512}{}{[Память] Ввести памятную дату, о которой болтала Анджела.}
{513}{}{[Наука] Проанализировать микропотертости на клавишах и перебрать вероятные комбинации.}
{514}{}{[Взлом] Подключить отмычку к сервисному разъему под панелью.}
{515}{}{Нажимать клавиши наугад, надеясь на удачу.}
{519}{}{Оставить сейф в покое.}
{520}{}{(Вы хаотично жмете на светящиеся кнопки. Панель издает протяжный писк «БИИИП» и заклинивает на минуту.)}
{525}{}{(Вы тыкаете в случайные клавиши... вдруг панель зеленеет, раздается «ПИК-ЩЕЛК» — и сейф открывается!)}
{526}{}{Ура! Пищалка открылась!}
{530}{}{(Вы вспоминаете, какую дату Анджела непрестанно твердила в постели. Набираете цифры на сенсорной панели — замок тихо щелкает и открывается.)}
{531}{}{Заглянуть внутрь.}
{535}{}{(Присмотревшись к отраженному свету, вы замечаете налет на клавишах 1, 3, 7 и 9. Быстрый математический перебор — и панель выдает подтверждающий сигнал!)}
{536}{}{Сейф открыт.}
{537}{}{(Вам не удается расшифровать логику шифра. Замок блокируется на несколько минут.)}
{540}{}{(Вы аккуратно подсоединяете тонкий зонд к шине сервисного разъема. Замыкание триггера — и ригели отщелкиваются!)}
{541}{}{(Зонд соскальзывает с контакта, не замкнув реле.)}
{545}{}{(Вы тыкаете наугад... невероятно, но комбинация совпала! Зеленый огонек — и сейф открыт.)}
{546}{}{Повезло так повезло.}
{547}{}{(Панель моргает красным: неверный код.)}
"""

NIABISSF_MSG_EN_EXT = """
# INTERACTIVE DIALOGUE SYSTEM (ANGELA BISHOP SAFE)
{500}{}{(A shiny box hangs on the wall with buttons that beep cheerfully.)}
{502}{}{Press all the buttons at once!}
{504}{}{Leave.}
{510}{}{(You examine Angela Bishop's private wall safe. It is secured with an electronic digital keypad.)}
{512}{}{[Memory] Enter the memorable date Angela chatted about.}
{513}{}{[Science] Analyze the keypad wear patterns and calculate probable permutations.}
{514}{}{[Lockpick] Connect a lockpick probe to the service connector beneath the panel.}
{515}{}{Punch numbers randomly, hoping for luck.}
{519}{}{Leave the safe alone.}
{520}{}{(You randomly smash the glowing keys. The keypad emits an angry BEEP and locks up for a minute.)}
{525}{}{(You randomly poke the keys... suddenly the panel flashes green, a BEEP-CLICK echoes -- and the safe unlatches!)}
{526}{}{Yay! The beeper opened!}
{530}{}{(You recall the date Angela kept blabbing about in bed. You tap the digits into the keypad -- the lock clicks open quietly.)}
{531}{}{Look inside.}
{535}{}{(Angling the light, you notice distinct smudge marks on keys 1, 3, 7, and 9. A quick mathematical permutation -- and the panel flashes an access granted tone!)}
{536}{}{The safe is open.}
{537}{}{(You fail to deduce the cipher logic. The lock locks out for several minutes.)}
{540}{}{(You delicately clip a bypass probe into the service bus. Triggering the bypass relay pops the deadbolt open!)}
{541}{}{(The probe slips off the trace without tripping the relay.)}
{545}{}{(You punch numbers blindly... miraculously, you hit the jackpot! The green LED blinks and the safe pops open.)}
{546}{}{Talk about luck.}
{547}{}{(The keypad blinks red: access denied.)}
"""

def append_to_msg(source_path, extension_text, out_path, encoding):
    with open(source_path, "r", encoding=encoding, errors="ignore") as f:
        orig = f.read()
    lines = orig.splitlines()
    clean_lines = []
    for l in lines:
        if l.strip().startswith("{5") or l.strip().startswith("{6"):
            continue
        clean_lines.append(l)
    new_content = "\n".join(clean_lines).strip() + "\n\n" + extension_text.strip() + "\n"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding=encoding) as f:
        f.write(new_content)
    print(f"Updated {out_path} ({len(new_content)} bytes, {encoding})")

# ---------------------------------------------------------------------------
# 2. SSL SCRIPT GENERATORS
# ---------------------------------------------------------------------------

def build_nimrbsf_ssl():
    with open(os.path.join(TOOLS_DIR, "bishop_safes", "nimrbsf_clean.ssl"), "r", encoding="utf-8") as f:
        orig = f.read()

    # Add procedure declarations
    decl = """
procedure Node999;
procedure Node001;
procedure NodeStupidKnock;
procedure NodeStupidSpin;
procedure NodeComboUnlock;
procedure NodeInspectTraps;
procedure NodeDisarmTrap;
procedure NodeRewireTrap;
procedure NodeLockpick;
procedure NodeSpinRandom;
procedure NodeScience;
"""
    orig = orig.replace("procedure use_obj_on_p_proc;", "procedure use_obj_on_p_proc;" + decl)

    # Replace use_p_proc to enter dialog when closed
    new_use = """procedure use_p_proc begin
   variable send_warning := false;
   set_mr_bishop_safe(mr_bishop_safe_touched);
   check_safe_tamper(send_warning)
   if (send_warning == false) then begin
      if (obj_is_open(self_obj)) then begin
         // Already open: loot window
      end else begin
         script_overrides;
         start_gdialog(NAME, self_obj, 4, -1, -1);
         gsay_start;
            call Node001;
         gsay_end;
         end_dialogue;
      end
   end
end"""

    # Replace the old use_p_proc block up to use_obj_on_p_proc
    import re
    orig = re.sub(r'procedure use_p_proc begin[\s\S]*?procedure use_obj_on_p_proc', new_use + "\n\nprocedure use_obj_on_p_proc", orig)

    # Append dialogue nodes at the end
    dialog_nodes = """
procedure Node999 begin
end

procedure Node001 begin
   if (dude_is_stupid) then begin
      Reply(500);
      NLowOption(502, NodeStupidKnock);
      NLowOption(503, NodeStupidSpin);
      NLowOption(504, Node999);
   end else begin
      Reply(510);
      if (mr_bishop_safe(mr_bishop_safe_know)) then begin
         NOption(512, NodeComboUnlock, 004);
      end
      if (found_trap) then begin
         NOption(513, NodeDisarmTrap, 004);
         NOption(514, NodeRewireTrap, 004);
      end else begin
         NOption(515, NodeInspectTraps, 004);
      end
      NOption(516, NodeLockpick, 004);
      NOption(517, NodeSpinRandom, 004);
      if ((has_skill(dude_obj, SKILL_SCIENCE) >= 60) or (obj_is_carrying_obj_pid(dude_obj, PID_ELECTRONIC_LOCKPICKS) > 0) or (obj_is_carrying_obj_pid(dude_obj, PID_ELEC_LOCKPICK_MKII) > 0)) then begin
         NOption(518, NodeScience, 004);
      end
      NOption(519, Node999, 004);
   end
end

procedure NodeStupidKnock begin
   Reply(520);
   NLowOption(503, NodeStupidSpin);
   NLowOption(504, Node999);
end

procedure NodeStupidSpin begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(200);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(525);
      NLowOption(526, Node999);
   end else if (trap_on_safe) then begin
      set_boomw(boomw_boom);
   end else begin
      Reply(527);
      NLowOption(504, Node999);
   end
end

procedure NodeComboUnlock begin
   give_xp(100);
   obj_unlock(self_obj);
   obj_open(self_obj);
   Reply(535);
   NOption(536, Node999, 004);
end

procedure NodeInspectTraps begin
   variable the_roll;
   the_roll := roll_vs_skill(dude_obj, SKILL_TRAPS, -15);
   if ((is_success(the_roll)) or (mrs_bishop_warning)) then begin
      set_found_trap;
      give_xp(150);
      Reply(540);
      NOption(542, NodeDisarmTrap, 004);
      NOption(543, NodeRewireTrap, 004);
      NOption(519, Node999, 004);
   end else begin
      Reply(541);
      NOption(544, Node001, 004);
   end
end

procedure NodeDisarmTrap begin
   variable the_roll;
   the_roll := roll_vs_skill(dude_obj, SKILL_TRAPS, -20);
   if (is_success(the_roll)) then begin
      set_boomw(boomw_disarmed);
      give_xp(250);
      Reply(550);
      NOption(552, Node001, 004);
   end else if (is_critical(the_roll)) then begin
      set_boomw(boomw_boom);
   end else begin
      Reply(551);
      NOption(519, Node999, 004);
   end
end

procedure NodeRewireTrap begin
   if ((has_skill(dude_obj, SKILL_REPAIR) >= 70) or (has_skill(dude_obj, SKILL_TRAPS) >= 70)) then begin
      set_boomw(boomw_trapped);
      give_xp(350);
      Reply(560);
      NOption(562, Node001, 004);
   end else begin
      Reply(561);
      NOption(519, Node999, 004);
   end
end

procedure NodeLockpick begin
   variable the_roll, bonus;
   if ((trap_on_safe) and (found_trap == false)) then begin
      the_roll := roll_vs_skill(dude_obj, SKILL_TRAPS, -10);
      if (is_success(the_roll)) then begin
         set_found_trap;
         Reply(575);
         NOption(576, Node001, 004);
      end else begin
         set_boomw(boomw_boom);
      end
   end else begin
      bonus := 0;
      if ((obj_is_carrying_obj_pid(dude_obj, PID_LOCKPICKS) > 0) or (obj_is_carrying_obj_pid(dude_obj, PID_EXP_LOCKPICK_SET) > 0)) then begin
         bonus := 20;
      end
      the_roll := roll_vs_skill(dude_obj, SKILL_LOCKPICK, -20 + bonus);
      if (is_success(the_roll)) then begin
         give_xp(250);
         obj_unlock(self_obj);
         obj_open(self_obj);
         Reply(580);
         NOption(581, Node999, 004);
      end else begin
         Reply(582);
         NOption(519, Node999, 004);
      end
   end
end

procedure NodeSpinRandom begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(150);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(585);
      NOption(581, Node999, 004);
   end else if (trap_on_safe) then begin
      set_boomw(boomw_boom);
   end else begin
      Reply(586);
      NOption(519, Node999, 004);
   end
end

procedure NodeScience begin
   variable the_roll;
   if ((trap_on_safe) and (found_trap == false)) then begin
      set_found_trap;
      Reply(590);
      NOption(591, Node001, 004);
   end else begin
      the_roll := roll_vs_skill(dude_obj, SKILL_SCIENCE, -15);
      if (is_success(the_roll)) then begin
         give_xp(250);
         obj_unlock(self_obj);
         obj_open(self_obj);
         Reply(595);
         NOption(581, Node999, 004);
      end else begin
         Reply(596);
         NOption(519, Node999, 004);
      end
   end
end
"""
    out_ssl = os.path.join(TOOLS_DIR, "bishop_safes", "nimrbsf.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(orig + "\n" + dialog_nodes)
    print("Generated enhanced nimrbsf.ssl")

def build_nimrsbsf_ssl():
    with open(os.path.join(TOOLS_DIR, "bishop_safes", "nimrsbsf_clean.ssl"), "r", encoding="utf-8") as f:
        orig = f.read()

    decl = """
procedure Node999;
procedure Node001;
procedure NodeStupidKnock;
procedure NodeStupidSpin;
procedure NodeComboUnlock;
procedure NodeLockpick;
procedure NodeSpinRandom;
procedure NodeFindCompartment;
"""
    orig = orig.replace("procedure use_obj_on_p_proc;", "procedure use_obj_on_p_proc;" + decl)

    new_use = """procedure use_p_proc begin
   if (obj_is_open(self_obj)) then begin
      if ((compartment) and (found_compartment == false)) then begin
         script_overrides;
         start_gdialog(NAME, self_obj, 4, -1, -1);
         gsay_start;
            call NodeFindCompartment;
         gsay_end;
         end_dialogue;
      end
   end else begin
      script_overrides;
      start_gdialog(NAME, self_obj, 4, -1, -1);
      gsay_start;
         call Node001;
      gsay_end;
      end_dialogue;
   end
end"""

    import re
    orig = re.sub(r'procedure use_p_proc begin[\s\S]*?procedure use_obj_on_p_proc', new_use + "\n\nprocedure use_obj_on_p_proc", orig)

    dialog_nodes = """
procedure Node999 begin
end

procedure Node001 begin
   if (dude_is_stupid) then begin
      Reply(500);
      NLowOption(502, NodeStupidKnock);
      NLowOption(503, NodeStupidSpin);
      NLowOption(504, Node999);
   end else begin
      Reply(510);
      if (know_mrs_bishop_combination) then begin
         NOption(512, NodeComboUnlock, 004);
      end
      NOption(513, NodeLockpick, 004);
      NOption(514, NodeSpinRandom, 004);
      if (obj_is_open(self_obj)) then begin
         if (found_compartment == false) then begin
            if ((compartment) or (dude_perception >= 8) or (has_skill(dude_obj, SKILL_REPAIR) >= 60)) then begin
               NOption(515, NodeFindCompartment, 004);
            end
         end
         NOption(516, Node999, 004);
      end
      NOption(519, Node999, 004);
   end
end

procedure NodeStupidKnock begin
   Reply(520);
   NLowOption(503, NodeStupidSpin);
   NLowOption(504, Node999);
end

procedure NodeStupidSpin begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(150);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(525);
      NLowOption(526, Node999);
   end else begin
      Reply(527);
      NLowOption(504, Node999);
   end
end

procedure NodeComboUnlock begin
   obj_unlock(self_obj);
   obj_open(self_obj);
   Reply(535);
   if (found_compartment == false) then begin
      if ((compartment) or (dude_perception >= 8) or (has_skill(dude_obj, SKILL_REPAIR) >= 60)) then begin
         NOption(515, NodeFindCompartment, 004);
      end
   end
   NOption(536, Node999, 004);
end

procedure NodeLockpick begin
   variable the_roll;
   the_roll := roll_vs_skill(dude_obj, SKILL_LOCKPICK, -15);
   if (is_success(the_roll)) then begin
      give_xp(200);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(540);
      if (found_compartment == false) then begin
         if ((compartment) or (dude_perception >= 8) or (has_skill(dude_obj, SKILL_REPAIR) >= 60)) then begin
            NOption(515, NodeFindCompartment, 004);
         end
      end
      NOption(542, Node999, 004);
   end else begin
      Reply(541);
      NOption(519, Node999, 004);
   end
end

procedure NodeSpinRandom begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(100);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(545);
      if (found_compartment == false) then begin
         if ((compartment) or (dude_perception >= 8) or (has_skill(dude_obj, SKILL_REPAIR) >= 60)) then begin
            NOption(515, NodeFindCompartment, 004);
         end
      end
      NOption(546, Node999, 004);
   end else begin
      Reply(547);
      NOption(519, Node999, 004);
   end
end

procedure NodeFindCompartment begin
   set_found_compartment;
   Reply(530);
   NOption(531, Node999, 004);
end
"""
    out_ssl = os.path.join(TOOLS_DIR, "bishop_safes", "nimrsbsf.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(orig + "\n" + dialog_nodes)
    print("Generated enhanced nimrsbsf.ssl")

def build_niabissf_ssl():
    with open(os.path.join(TOOLS_DIR, "bishop_safes", "niabissf_clean.ssl"), "r", encoding="utf-8") as f:
        orig = f.read()

    decl = """
procedure Node999;
procedure Node001;
procedure NodeStupidButtons;
procedure NodeMemoryUnlock;
procedure NodeScience;
procedure NodeLockpick;
procedure NodeSpinRandom;
"""
    orig = orig.replace("procedure use_obj_on_p_proc;", "procedure use_obj_on_p_proc;" + decl)

    new_use = """procedure use_p_proc begin
   if (obj_is_open(self_obj)) then begin
      // Already open: loot window
   end else begin
      script_overrides;
      start_gdialog(NAME, self_obj, 4, -1, -1);
      gsay_start;
         call Node001;
      gsay_end;
      end_dialogue;
   end
end"""

    import re
    orig = re.sub(r'procedure use_p_proc begin[\s\S]*?procedure use_obj_on_p_proc', new_use + "\n\nprocedure use_obj_on_p_proc", orig)

    dialog_nodes = """
procedure Node999 begin
end

procedure Node001 begin
   if (dude_is_stupid) then begin
      Reply(500);
      NLowOption(502, NodeStupidButtons);
      NLowOption(504, Node999);
   end else begin
      Reply(510);
      if (angela_banged) then begin
         NOption(512, NodeMemoryUnlock, 004);
      end
      NOption(513, NodeScience, 004);
      NOption(514, NodeLockpick, 004);
      NOption(515, NodeSpinRandom, 004);
      NOption(519, Node999, 004);
   end
end

procedure NodeStupidButtons begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(150);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(525);
      NLowOption(526, Node999);
   end else begin
      Reply(520);
      NLowOption(504, Node999);
   end
end

procedure NodeMemoryUnlock begin
   give_xp(150);
   obj_unlock(self_obj);
   obj_open(self_obj);
   Reply(530);
   NOption(531, Node999, 004);
end

procedure NodeScience begin
   variable the_roll;
   the_roll := roll_vs_skill(dude_obj, SKILL_SCIENCE, -10);
   if (is_success(the_roll)) then begin
      give_xp(250);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(535);
      NOption(536, Node999, 004);
   end else begin
      Reply(537);
      NOption(519, Node999, 004);
   end
end

procedure NodeLockpick begin
   variable the_roll;
   the_roll := roll_vs_skill(dude_obj, SKILL_LOCKPICK, -15);
   if (is_success(the_roll)) then begin
      give_xp(200);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(540);
      NOption(536, Node999, 004);
   end else begin
      Reply(541);
      NOption(519, Node999, 004);
   end
end

procedure NodeSpinRandom begin
   if (random(1, 100) <= dude_luck) then begin
      give_xp(100);
      obj_unlock(self_obj);
      obj_open(self_obj);
      Reply(545);
      NOption(546, Node999, 004);
   end else begin
      Reply(547);
      NOption(519, Node999, 004);
   end
end
"""
    out_ssl = os.path.join(TOOLS_DIR, "bishop_safes", "niabissf.ssl")
    with open(out_ssl, "w", encoding="utf-8") as f:
        f.write(orig + "\n" + dialog_nodes)
    print("Generated enhanced niabissf.ssl")

# ---------------------------------------------------------------------------
# 3. COMPILATION & DEPLOYMENT
# ---------------------------------------------------------------------------

def compile_script(ssl_filename, int_filename):
    target_dir = os.path.join(TOOLS_DIR, "bishop_safes")
    short_tools = get_short_path(TOOLS_DIR)
    compiler = os.path.join(short_tools, "compile.exe")
    headers = os.path.join(short_tools, "headers")

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

def deploy_to_profiles():
    target_dir = os.path.join(TOOLS_DIR, "bishop_safes")
    profiles = [MASTER_MOD_DIR, GAMEPLAY_MOD_DIR, HD_MOD_DIR]

    scripts_to_deploy = ["nimrbsf.int", "nimrsbsf.int", "niabissf.int"]
    msgs_to_deploy = [
        ("nimrbsf.msg.ru", r"text\russian\dialog\nimrbsf.msg"),
        ("nimrbsf.msg.en", r"text\english\dialog\nimrbsf.msg"),
        ("nimrsbsf.msg.ru", r"text\russian\dialog\nimrsbsf.msg"),
        ("nimrsbsf.msg.en", r"text\english\dialog\nimrsbsf.msg"),
        ("niabissf.msg.ru", r"text\russian\dialog\niabissf.msg"),
        ("niabissf.msg.en", r"text\english\dialog\niabissf.msg"),
    ]

    for p in profiles:
        # Deploy scripts
        scripts_target = os.path.join(p, "scripts")
        os.makedirs(scripts_target, exist_ok=True)
        for s in scripts_to_deploy:
            src = os.path.join(target_dir, s)
            dst = os.path.join(scripts_target, s)
            shutil.copy2(src, dst)

        # Deploy msgs
        for src_name, rel_target in msgs_to_deploy:
            src = os.path.join(target_dir, src_name)
            dst = os.path.join(p, rel_target)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

        print(f"[+] Deployed scripts & dialogs -> {os.path.basename(p)}")

def main():
    print("=" * 60)
    print("  BISHOP SAFES RPG OVERHAUL BUILD & DEPLOY")
    print("=" * 60)

    # 1. Update MSG files in workspace
    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrbsf_ru.msg"),
        NIMRBSF_MSG_RU_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrbsf.msg.ru"),
        "cp1251"
    )
    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "rpu_nimrbsf_en.msg"),
        NIMRBSF_MSG_EN_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrbsf.msg.en"),
        "latin-1"
    )

    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrsbsf_ru.msg"),
        NIMRSBSF_MSG_RU_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrsbsf.msg.ru"),
        "cp1251"
    )
    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "rpu_nimrsbsf_en.msg"),
        NIMRSBSF_MSG_EN_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "nimrsbsf.msg.en"),
        "latin-1"
    )

    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "niabissf_ru.msg"),
        NIABISSF_MSG_RU_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "niabissf.msg.ru"),
        "cp1251"
    )
    append_to_msg(
        os.path.join(TOOLS_DIR, "bishop_safes", "rpu_niabissf_en.msg"),
        NIABISSF_MSG_EN_EXT,
        os.path.join(TOOLS_DIR, "bishop_safes", "niabissf.msg.en"),
        "latin-1"
    )

    # 2. Build SSL scripts
    build_nimrbsf_ssl()
    build_nimrsbsf_ssl()
    build_niabissf_ssl()

    # 3. Compile scripts
    ok1 = compile_script("nimrbsf.ssl", "nimrbsf.int")
    ok2 = compile_script("nimrsbsf.ssl", "nimrsbsf.int")
    ok3 = compile_script("niabissf.ssl", "niabissf.int")

    if not (ok1 and ok2 and ok3):
        print("[ERROR] Compilation failed!")
        sys.exit(1)

    # 4. Deploy to profiles
    deploy_to_profiles()
    print("\n-> ALL BISHOP SAFES SUCCESSFULLY BUILT AND DEPLOYED.")

if __name__ == "__main__":
    main()
