#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve all English leaks in Talking Heads 7700+ dialogue lines,
merge EcCo mechanics (crafting, recipes, dynamic fees),
and deploy to master patch rpu_russian_uncensored.dat across both profiles and workspace.
"""

import os
import sys
import re
import shutil

sys.path.append(os.path.dirname(__file__))
from engine_full_audit import read_dat2_directory, extract_dat2_file

PROJECT_ROOT = r"E:\FALLOUT Ult pjt"
GAMEPLAY_PATCH = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat"
HD_PATCH = r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat"

TH_DAT_PATH = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\talking_heads_that_rpu_map_update_patch.dat"
ECCO_DAT_PATH = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat"
RU_DAT_PATH = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian.dat"
RPU_DAT_PATH = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu.dat"

# 30 targeted canonical translations for composite/variant lines
MANUAL_TRANSLATIONS = {
    ("actemvil.msg", 7700): "Приветствую, Избранный. Мне выпала честь стать твоим последним испытанием. Чтобы продолжить свой путь, ты должен победить меня в рукопашном бою. Начнем?",
    ("actemvil.msg", 7702): "Да. Оружие отдаляет нас от боя и притупляет последствия наших действий против других. Когда бьешь человека голыми кулаками, ты и видишь, и чувствуешь боль, которую причиняешь. Тогда битва становится очень личной и слишком реальной. Это важный урок для тебя, Избранный.",
    ("actemvil.msg", 7704): "Отлично! Твое снаряжение останется в сундуке снаружи комнаты. Сможешь забрать его после боя. Да начнется бой! Удачи тебе, Избранный.",
    ("fcfmatt.msg", 7700): "Здравствуй, Странник. Чем могу помочь?",
    ("hcsteve.msg", 7700): "О. Снова ты. Хочешь узнать больше?",
    ("hcsteve.msg", 7701): "Привет еще раз. Хочешь узнать больше?",
    ("hcsteve.msg", 7702): "С возвращением. Хочешь узнать больше?",
    ("mcbaltha.msg", 7700): "Ты сказал — Чужак? Да, кажется, я слышал о тебе. Один из охранников проходящего каравана хорошо отзывался о человеке с таким именем. Знаю, мы едва знакомы, но мне очень нужна твоя помощь.",
    ("nckitty.msg", 7716): "Поверь мне, милый, оно стоит этих фишек. (Она медленно облизывает губы)",
    ("nckitty.msg", 7718): "Ну конечно же, можешь. Мы называем это «Особый Кестинг». Если у тебя есть фишки, можем пойти прилечь и просто поболтать.",
    ("nckitty.msg", 7725): "Любимый! Я так рада, что ты вернулся. От одного присутствия такого героя, как ты, дела просто расцветают: рисковать жизнью, бросить вызов Анклаву... Это самый смелый поступок, о котором я слышала.",
    ("ncliljes.msg", 7716): "Хмммм... Не знаю, чика... В смысле, я БЫ МОГ сделать исключение для такой женщины, как ты, но у меня не так много свободного времени... а бой на ножах — это ИСКУССТВО, сечешь?",
    ("ncmason.msg", 7707): "Давно пора. Уж не знаю, зачем мистеру Сальваторе нанимать порно-отбросы, но я не стану лезть к нему с вопросами. Этого бродягу, который обокрал мистера Сальваторе, зовут Ллойд. Мистер Сальваторе хочет его смерти и возврата украденных денег. Выполнишь работу — доложи МНЕ, ясно? Думаешь, справишься?",
    ("ncmason.msg", 7713): "(Ворчит.) Эй, слышь... Мистер Сальваторе передал о твоем повышении. Поздравляю. Тут кое-что для тебя... дай поглядеть... (Он вручает вам охапку предметов.) Осторожнее с этим добром...",
    ("ncmason.msg", 7714): "(Мейсон замирает, прислушиваясь к чему-то, чего вы не слышите. Через секунду он стискивает зубы.) Мистер Сальваторе говорит, ты можешь войти, Странник.",
    ("ncrenesc.msg", 7702): "(Шокированно пялится.) ...очередная жертва неудавшегося аборта в постапокалиптическом мире, кишащем полоумными великовозрастными недоумками. (Вскидывает кулаки.) Вон из моей лавки! Немедленно вон! И чтоб духу твоего здесь не было, слышишь?!",
    ("ncrenesc.msg", 7705): "Ты, ТУПОЙ ублюдок. Я же СКАЗАЛ тебе не называть его имя здесь. Вон! Увижу тебя снова — ПРИСТРЕЛЮ НА МЕСТЕ. Если мистер Райт придет за мной, думая, что я убил его пацана, ТЫ сдохнешь первым.",
    ("ncrenesc.msg", 7706): "Ты, ТУПАЯ сука. Я же СКАЗАЛ тебе не называть его имя здесь. Вон! Увижу тебя снова — ПРИСТРЕЛЮ НА МЕСТЕ. Если мистер Райт придет за мной, думая, что я убил его пацана, ТЫ сдохнешь первой.",
    ("ncrenesc.msg", 7709): "...очередная жертва неудавшегося аборта в постапокалиптическом мире, кишащем полоумными великовозрастными недоумками. (Вскидывает кулаки.) Вон из моей лавки! Немедленно вон! И чтоб духу твоего здесь не было, слышишь?!",
    ("ncrenesc.msg", 7710): "ГЭКК? В смысле «Генератор Эдемских Кущ Компактный»? Поставляется с базовым репликатором, считывателем голодисков с подборкой из библиотеки Конгресса и маленьким фонариком-ручкой?",
    ("ncsalvat.msg", 7702): "Садись, Путник. Ты сделал... все, о чем я просил. Я хочу предложить тебе войти в семью Сальваторе и стать... одним из моих людей.",
    ("ncsalvat.msg", 7703): "Это... прискорбно. Я не могу пойти на риск, уповая на то, что ты будешь... молчать о том, что видел в пустыне. Прощай, Путник.",
    ("ncstulit.msg", 7704): "Значит, хочешь остаться с этим именем, а? Ну ладно. Хорошо, пошли надерем пару задниц.",
    ("ncstulit.msg", 7719): "(Стюарт кивает.) Лады, Чемпион. Рад познакомиться. Чем могу помочь?",
    ("scwestin.msg", 7700): "Ну и ладно. Ты делаешь работу — я плачу. Откажешься — живым отсюда не выйдешь. Ну так что?",
    ("vcdrtroy.msg", 7700): "Рад познакомиться, Гражданин. Если вам когда-нибудь понадобятся мои услуги, вы всегда найдете меня здесь.",
    ("vcdrtroy.msg", 7701): "Да, именно для этого мне и был нужен образец Джета. Это смертельное зелье нужно остановить, пока оно не распространилось дальше. Да что там... с теми данными, что вы принесли, мы сможем изготовить противоядие прямо сейчас! Подождите минутку.",
    ("vcdrtroy.msg", 7702): "Да... и безуспешно. Это смертельное зелье нужно остановить, пока оно не распространилось дальше. Да что там... с теми данными, что вы принесли, мы сможем изготовить противоядие прямо сейчас! Подождите минутку.",
    ("vcdrtroy.msg", 7703): "Правда? Превосходно! Спасибо вам, друг мой... вы даже не представляете, как это важно для моей работы. Вот ваша плата, как я и обещал.",
    ("vcdrtroy.msg", 7704): "У меня отличные новости. Мне удалось синтезировать противоядие из того образца Джета, что вы мне принесли. При приеме оно полностью снимает синдром ломки и к тому же... устраняет эйфорию, вызываемую наркотиком.",
    ("vcdrtroy.msg", 7705): "Отличные новости... На основе предоставленных вами данных мне удалось создать противоядие. При приеме оно полностью снимает синдром ломки и к тому же... устраняет эйфорию, вызываемую наркотиком.",
    ("vcmclure.msg", 7708): "Да, вы уже говорили об этом. Отличная работа, Гражданин.",
    ("vcmclure.msg", 7709): "Да, вы уже говорили об этом. Отличная работа, Капитан.",
    ("vcmclure.msg", 7710): "Да, вы уже говорили об этом. Отличная работа.",
    ("vcwalace.msg", 7703): "Хмммм. Очень хорошо. За Дневной пропуск для торговцев взимается сбор в пятьсот долларов. Он дает полное право дневной торговли в стенах Города Убежища и действует в течение пяти лет со дня выдачи.",
    ("dcmom.msg", 7700): "Ну, милок, выглядишь ты так, будто совсем запутался. Не могу смотреть, как страдает живая душа. Хочешь покушать?",
    ("dcmom.msg", 222): "Ну, милок, выглядишь ты так, будто совсем запутался. Не могу смотреть, как страдает живая душа. Хочешь покушать?",
}

def clean_str(t):
    return re.sub(r'\s+', ' ', t).strip().lower()

def deploy_data(rel_path, data):
    for root in [PROJECT_ROOT, GAMEPLAY_PATCH, HD_PATCH]:
        dest = os.path.join(root, rel_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(data)

def process_dialogs():
    print("[*] Reading DAT archives...")
    th_dat = read_dat2_directory(TH_DAT_PATH)
    ecco_dat = read_dat2_directory(ECCO_DAT_PATH)
    ru_dat = read_dat2_directory(RU_DAT_PATH)
    rpu_dat = read_dat2_directory(RPU_DAT_PATH)

    # 1. Process 25 files with 7700+ leaks
    ru_files = sorted(k for k in th_dat if k.startswith('text\\russian\\dialog\\'))
    leaks_found = 0
    leaks_fixed = 0

    for k in ru_files:
        fname = os.path.basename(k)
        th_ru_txt = extract_dat2_file(th_dat[k]).decode('cp1251', errors='replace')
        en_key = k.replace('text\\russian\\', 'text\\english\\')
        en_src = th_dat.get(en_key) or rpu_dat.get(en_key)
        en_txt = extract_dat2_file(en_src).decode('latin1', errors='replace') if en_src else ""
        
        ru_src = ru_dat.get(k)
        ru_txt = extract_dat2_file(ru_src).decode('cp1251', errors='replace') if ru_src else th_ru_txt

        en_dict = {int(m.group(1)): m.group(3) for m in re.finditer(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', en_txt)}
        ru_dict = {int(m.group(1)): m.group(3) for m in re.finditer(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', ru_txt)}

        # If file is mcbaltha.msg or vcmainwk.msg or dcmom.msg, we also want to incorporate ECCO lines!
        ecco_lines_to_add = {}
        if k in ecco_dat:
            ecco_txt = extract_dat2_file(ecco_dat[k]).decode('cp1251', errors='replace')
            for m in re.finditer(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', ecco_txt):
                num = int(m.group(1))
                tag = m.group(2)
                body = m.group(3)
                # Keep extra lines like 1001-1003 or 501-502
                ecco_lines_to_add[num] = (tag, body)

        lines = th_ru_txt.splitlines()
        new_lines = []
        modified = False

        existing_nums = set()
        for line in lines:
            m = re.match(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', line.strip())
            if m:
                num = int(m.group(1))
                tag = m.group(2)
                body = m.group(3)
                existing_nums.add(num)

                # Check if manual translation exists
                if (fname, num) in MANUAL_TRANSLATIONS:
                    body = MANUAL_TRANSLATIONS[(fname, num)]
                    leaks_fixed += 1
                    modified = True
                elif num >= 7700 and re.search(r'[a-zA-Z]{4,}', body) and not re.search(r'[а-яА-ЯёЁ]{4,}', body):
                    leaks_found += 1
                    # Intra-file match
                    c_body = clean_str(body)
                    best_line = None
                    for l_num, l_txt in en_dict.items():
                        if l_num < 7700 and clean_str(l_txt) == c_body:
                            best_line = l_num
                            break
                    if not best_line:
                        for l_num, l_txt in en_dict.items():
                            if l_num < 7700:
                                cl = clean_str(l_txt)
                                if len(cl) > 25 and (cl in c_body or c_body in cl):
                                    best_line = l_num
                                    break
                    if best_line and best_line in ru_dict:
                        body = ru_dict[best_line]
                        leaks_fixed += 1
                        modified = True
                    else:
                        print(f"  [UNRESOLVED] {fname} line {num}: {body[:50]}")

                new_lines.append(f"{{{num}}}{{{tag}}}{{{body}}}")
            else:
                new_lines.append(line)

        # Append missing ECCO lines if applicable
        if ecco_lines_to_add:
            for num in sorted(ecco_lines_to_add.keys()):
                if num not in existing_nums and num < 7700:
                    tag, body = ecco_lines_to_add[num]
                    new_lines.append(f"{{{num}}}{{{tag}}}{{{body}}}")
                    modified = True

        if modified:
            out_text = "\n".join(new_lines) + "\n"
            data_bytes = out_text.encode('cp1251')
            rel_path = os.path.join('text', 'russian', 'dialog', fname)
            deploy_data(rel_path, data_bytes)
            print(f"[OK] Fixed and deployed {fname} ({len(data_bytes)} bytes)")

    print(f"[*] Total leaks checked: {leaks_found}, fixed: {leaks_fixed}")

    # 2. Deploy specific ECCO dialogue files that were overwritten by rpu_russian.dat
    extra_ecco_dialogs = [
        'dcmom.msg', 'schenry.msg', 'gcskeetr.msg', 'dcvic.msg',
        'fcdrfung.msg', 'rcdrjohn.msg', 'vcandy.msg'
    ]

    for fn in extra_ecco_dialogs:
        rel_ru = f"text\\russian\\dialog\\{fn}"
        if rel_ru in ecco_dat:
            e_txt = extract_dat2_file(ecco_dat[rel_ru]).decode('cp1251', errors='replace')
            lines = e_txt.splitlines()
            out_lines = []
            for l in lines:
                m = re.match(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', l.strip())
                if m:
                    num = int(m.group(1))
                    tag = m.group(2)
                    body = m.group(3)
                    if (fn, num) in MANUAL_TRANSLATIONS:
                        body = MANUAL_TRANSLATIONS[(fn, num)]
                    out_lines.append(f"{{{num}}}{{{tag}}}{{{body}}}")
                else:
                    out_lines.append(l)
            out_text = "\n".join(out_lines) + "\n"
            deploy_data(os.path.join('text', 'russian', 'dialog', fn), out_text.encode('cp1251'))
            print(f"[OK] Deployed ECCO dialogue {fn}")

    # 3. Deploy 16 RPU-compatible ECCO scripts
    ecco_scripts = [
        'dcmom.int', 'dcvic.int', 'fclaocho.int', 'gcbrain.int', 'gcskeetr.int',
        'kcmaida.int', 'mcbaltha.int', 'mcvegeir.int', 'nceldrid.int', 'ocgrutha.int',
        'rcascort.int', 'rcmarge.int', 'vcdwnbar.int', 'vcmainwk.int', 'vcmclure.int', 'vcstark.int'
    ]
    for s in ecco_scripts:
        rel_k = f"scripts\\{s}"
        data = extract_dat2_file(ecco_dat[rel_k])
        deploy_data(os.path.join('scripts', s), data)
        print(f"[OK] Deployed ECCO script {s} ({len(data)} bytes)")

if __name__ == '__main__':
    process_dialogs()
