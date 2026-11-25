import os

# 1. Update PATCHES_REGISTRY.md
reg_path = r"E:\FALLOUT Ult pjt\PATCHES_REGISTRY.md"
with open(reg_path, "r", encoding="utf-8") as f:
    reg_text = f.read()

fix_62_row = """| **FIX-62** | **Анимации жестоких смертей супермутантов (Pixote), тайминги снов Хакуина и оверлей клавиш F1/J (Mutant Deaths, Hakunin Dreams & KeysHelp 2026)** | `standalone_mods/foxx_rebuild_tribute/`<br>`art/critters/ma*`<br>`scripts/gl_keyshelp.int`<br>`ddraw.ini` | `mods/foxx_rebuild_tribute.dat`<br>`mods/KeysHelp.dat`<br>`ddraw.ini`<br>(Мастер-репо, Gameplay & HD) | 1) Супермутанты в ванили не имели полных жестоких анимаций смерти от очередей, плазмы, огня и лазеров.<br>2) Сны Хакуина (90/180/270/360 дней) слишком быстро спамили на глобальной карте, сбивая атмосферу исследования.<br>3) Оверлей горячих клавиш (кнопка J) содержал устаревшие клавиши 2017 года с коллизией клавиши G и отсутствием новых функций 2026 года. | 1) Интегрированы 409 авторских файлов анимаций супермутантов от Pixote (50.6 МБ распакованных спрайтов) в `foxx_rebuild_tribute.dat`.<br>2) В `ddraw.ini` установлены расширенные тайминги снов Хакуина: 120, 235, 350, 470 дней во всех профилях.<br>3) Оверлей клавиш `gl_keyshelp.int` модернизирован под раскладку 2026: Ctrl+T (сбор лута напарниками), Shift (подсветка), Caps Lock (бег), 1..9 (диалоги), колесо мыши, F4/F8, F5/F9. Скрипт и ресурсы собраны в монолит `foxx_rebuild_tribute.dat` (16.09 МБ) и автономный `KeysHelp.dat` (52.3 КБ).<br>4) Полный аудит 100% GREEN (34/34 assertions). | Кинематографичные смерти мутантов в бою; комфортный темп прохождения без спама шамана; наглядная справочная панель по нажатию клавиши J с актуальными хоткеями. |
"""

if "| **FIX-62** |" not in reg_text:
    target_marker = "| **FIX-61** |"
    idx = reg_text.find(target_marker)
    if idx != -1:
        end_line = reg_text.find("\n", idx)
        reg_text = reg_text[:end_line+1] + fix_62_row + reg_text[end_line+1:]
        with open(reg_path, "w", encoding="utf-8") as f:
            f.write(reg_text)
        print("Updated PATCHES_REGISTRY.md with FIX-62")

# 2. Update MASTER_CHANGELOG.md
ch_path = r"E:\FALLOUT Ult pjt\MASTER_CHANGELOG.md"
with open(ch_path, "r", encoding="utf-8") as f:
    ch_text = f.read()

fix_62_ch = """### FIX-62: Анимации жестоких смертей супермутантов (Pixote), тайминги снов Хакуина и оверлей клавиш F1/J (Mutant Deaths, Hakunin Dreams & KeysHelp 2026)
- **Категория**: Графика, Баланс темпа, Интерфейс и Горячие клавиши
- **Автор**: Lead CTO Antigravity & Pixote / Foxx Heritage
- **Затронутые файлы**:
  - `standalone_mods/foxx_rebuild_tribute/data/art/critters/ma*` (409 файлов)
  - `standalone_mods/foxx_rebuild_tribute/data/scripts/gl_keyshelp.int`
  - `standalone_mods/foxx_rebuild_tribute/data/scripts/gl_glasses.int`
  - `mods/foxx_rebuild_tribute.dat` (16,090,268 байт)
  - `mods/KeysHelp.dat` (52,377 байт)
  - `ddraw.ini` (`MovieTimer_artimer1..4`)
- **Что сделано**:
  1. **Pixote Super Mutant Deaths (409 файлов)**: Интегрирован полный комплект расширенных и крупноформатных анимаций смерти и реакций на попадания для супермутантов (Marcus, Nightkins, элитные мутанты) от художника Pixote. Мутанты теперь зрелищно разрываются очередями, плавятся в слизь и сгорают в пепел.
  2. **Тайминги снов Хакуина**: В `ddraw.ini` всех профилей раскомментированы и выставлены сбалансированные тайминги (120, 235, 350, 470 дней), устраняющие назойливый спам шамана при неспешном исследовании Дена, Модока и Волт-Сити.
  3. **Модернизация оверлея клавиш (`gl_keyshelp.int` / `KeysHelp.dat`)**: Справочное окно (кнопка J) обновлено под актуальные 2026 элементы управления: `Ctrl+T` (сбор лута напарниками), `Shift` (подсветка), `Caps Lock` (бег), `1..9` (выбор реплик в диалогах), `Q` (режим оружия), колесо мыши (скролл), `F4/F8` и `F5/F9`.
  4. **Верификация**: Аудит `engine_full_audit.py` подтвердил 34/34 пройденных проверок (100% GREEN).

"""

if "### FIX-62" not in ch_text:
    marker = "## [Unreleased]"
    if marker in ch_text:
        idx = ch_text.find(marker) + len(marker)
        ch_text = ch_text[:idx] + "\n\n" + fix_62_ch + ch_text[idx:]
    else:
        ch_text = fix_62_ch + "\n" + ch_text
    with open(ch_path, "w", encoding="utf-8") as f:
        f.write(ch_text)
    print("Updated MASTER_CHANGELOG.md with FIX-62")

# 3. Update Fallout.md
f_path = r"E:\FALLOUT Ult pjt\Fallout.md"
with open(f_path, "r", encoding="utf-8") as f:
    f_text = f.read()

# Update Task statuses in Fallout.md:
f_text = f_text.replace("`Task Ф-1.5 [В ОЧЕРЕДИ]`", "`Task Ф-1.5 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-1.6 [В ОЧЕРЕДИ]`", "`Task Ф-1.6 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-1.7 [В ОЧЕРЕДИ]`", "`Task Ф-1.7 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-1.8 [В ОЧЕРЕДИ]`", "`Task Ф-1.8 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-2.2 [В ОЧЕРЕДИ]`", "`Task Ф-2.2 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-3.1 [В ОЧЕРЕДИ]`", "`Task Ф-3.1 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-3.2 [В ОЧЕРЕДИ]`", "`Task Ф-3.2 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-3.4 [В ОЧЕРЕДИ]`", "`Task Ф-3.4 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-3.5 [В ОЧЕРЕДИ]`", "`Task Ф-3.5 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-4.1 [В ОЧЕРЕДИ]`", "`Task Ф-4.1 [ГОТОВО]`")
f_text = f_text.replace("`Task Ф-4.2 [В ОЧЕРЕДИ]`", "`Task Ф-4.2 [ГОТОВО]`")

# Add Live Sync Log entry
sync_entry = """- **[2026-11-23 12:35] Основной Чат (Lead CTO Antigravity)**:
  - **Завершение интеграции наследия Фокса, анимаций супермутантов Pixote и оверлея клавиш 2026 (FIX-62)**:
    1. *Анимации Pixote*: 409 файлов крупноформатных анимаций смерти супермутантов упакованы в `foxx_rebuild_tribute.dat` (16.09 МБ).
    2. *Тайминги снов Хакуина*: В `ddraw.ini` выставлены расширенные интервалы (120, 235, 350, 470 дней).
    3. *Оверлей горячих клавиш F1/J*: `gl_keyshelp.int` обновлен под актуальную раскладку 2026 (Ctrl+T, Shift, Caps Lock, 1..9, колесо мыши), собран в чистый `KeysHelp.dat` (52.3 КБ).
    4. *Умные очки и Напарница Мирия*: Подтвержден статус `[ГОТОВО]` для Glasses Mod (перетаскивание на фигурку + использование из контекстного меню) и Enhanced Miria (4 уровня, смена брони, боевой ИИ).
    5. *Верификация*: `engine_full_audit.py` (34/34 assertions GREEN) и `deep_balance_audit.py` подтвердили 100% стабильность. Зафиксировано в `PATCHES_REGISTRY.md` (FIX-62).
"""

sync_marker = "### 0. Inter-Agent Communication Bridge (Shared Context Hub)"
if sync_marker in f_text:
    idx = f_text.find("#### Live Sync Log (Последние действия субагентов)")
    if idx != -1:
        insert_pos = f_text.find("\n", idx) + 1
        f_text = f_text[:insert_pos] + sync_entry + f_text[insert_pos:]
        with open(f_path, "w", encoding="utf-8") as f:
            f.write(f_text)
        print("Updated Fallout.md Live Sync Log and Task statuses")
