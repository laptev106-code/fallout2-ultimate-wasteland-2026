"""
Fallout 2: Ultimate Wasteland Edition 2026 - Master Launcher
Стилизованный Pip-Boy лаунчер с каталогом модов, памяткой игрока и запуском двух профилей.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# Цветовая палитра Pip-Boy / CRT Terminal
BG_MAIN = "#0a0f0a"
BG_PANEL = "#111811"
BG_CARD = "#162216"
BG_CARD_HOVER = "#1f301f"
BORDER_COLOR = "#224422"
PHOSPHOR_GREEN = "#2bf558"
BRIGHT_GREEN = "#55ff77"
TEXT_MAIN = "#d2ecd2"
TEXT_MUTED = "#739973"
AMBER_COLOR = "#ffb833"
BLUE_COLOR = "#3fa9f5"
BLUE_PANEL = "#111f2b"
BLUE_BORDER = "#1f4a6b"

# Данные о всех установленных модификациях
MODS_CATALOG = [
    {
        "id": "rpu",
        "title": "Restoration Project Updated (RPU v2.4.34 / v28)",
        "badge": "ГЛОБАЛЬНЫЙ СЮЖЕТ",
        "author": "Killap, BGforge Net, debrouxl",
        "summary": "Главный фундамент сборки: полная каноничная реставрация контента Black Isle Studios.",
        "details": (
            "Восстанавливает весь пласт сюжетного контента, который оригинальные разработчики "
            "не успели выпустить в 1998 году:\n\n"
            "• 6 НОВЫХ КРУПНЫХ ЛОКАЦИЙ:\n"
            "  - Аббатство Братства Стали (The Abbey) — монастырь хранителей знаний;\n"
            "  - Исследовательский центр EPA — заброшенный правительственный комплекс со своими тайнами;\n"
            "  - Деревня Дикарей (Primitive Tribe) — родное поселение племени Сулика на побережье;\n"
            "  - Жилой квартал Дыры (The Den Residential) — новые жители, квесты и сироты;\n"
            "  - Китайская подлодка «Ши» в Сан-Франциско;\n"
            "  - База Вертибердов и посадочные площадки Анклава.\n\n"
            "• СЮЖЕТНЫЕ ЦЕПОЧКИ И ПЕРСОНАЖИ:\n"
            "  - Спасение сестры Сулика из лап работорговцев Мецгера;\n"
            "  - Заклятый враг Избранного — отвергнутый соплеменник Кага (5 встреч по мере прокачки);\n"
            "  - Новые спутники из комплекса EPA: харизматичный Кэт Джулс, ловкая Кицунэ и Декстер;\n"
            "  - Расширенные квесты Хабологов и репликаторов в Сан-Франциско;\n"
            "  - Сотни исправлений багов оригинального скриптового движка."
        )
    },
    {
        "id": "ecco",
        "title": "EcCo — Economy & Combat Overhaul (v0.9.8.3)",
        "badge": "БОЕВАЯ СИСТЕМА И ЭКОНОМИКА",
        "author": "phobos2077",
        "summary": "Глубокая переработка баллистики, честная бронебойность и устранение гиперинфляции крышек.",
        "details": (
            "Исправляет фундаментальные ошибки боевого движка Fallout 2, существовавшие 25 лет:\n\n"
            "• РЕМОНТ БРОНЕБОЙНЫХ ПАТРОНОВ (AP):\n"
            "  В оригинале патроны AP были забагованы и наносили меньше урона, чем обычные JHP. "
            "  В EcCo реализована честная физическая модель: бронебойные пули реально пробивают "
            "  силовую и металлическую броню, а экспансивные рвут легкие цели.\n\n"
            "• БАЛАНС ЭКОНОМИКИ:\n"
            "  Устранена проблема, когда к середине игры Избранный становился миллионером с тоннами "
            "  бесполезного оружия. Цены, бартер и ценность боеприпасов теперь ощущаются реалистично.\n\n"
            "• ПЕРЕРАБОТКА МЕДИЦИНЫ И ПЕРКОВ:\n"
            "  Стимуляторы и препараты работают по новой тактической схеме, а ранее бесполезные перки "
            "  получили реальную ценность в бою."
        )
    },
    {
        "id": "minirework",
        "title": "Fallout Mechanics MiniRework (v2.0.4.3)",
        "badge": "ФИЗИКА СТРЕЛЬБЫ И ТАКТИКА",
        "author": "dekrus",
        "summary": "Альтернативные режимы огня оружия, пробивание Гаусса, цепные молнии и динамический яд.",
        "details": (
            "Превращает перестрелки Fallout 2 в глубокую тактику современного уровня:\n\n"
            "• ВТОРИЧНЫЕ РЕЖИМЫ АТАКИ (активируются прицельным выстрелом в корпус):\n"
            "  - Винтовки Гаусса: бронебойный гиперзвуковой выстрел, прошивающий строй врагов насквозь;\n"
            "  - Импульсное оружие: электрический разряд бьет цепной молнией по соседним врагам;\n"
            "  - Лазерное оружие: сфокусированный луч прорезает нескольких противников на линии огня;\n"
            "  - Пистолеты и ПП: прицельный двойной выстрел в корпус за цену одного обычного;\n"
            "  - Дробовики: мощный останавливающий эффект с отбрасыванием и нокдауном;\n"
            "  - Автоматы и пулеметы: управляемая короткая очередь с кучным разлетом пуль.\n\n"
            "• ДИНАМИЧЕСКИЙ ЯД:\n"
            "  Яд наносит периодический урон всем существам на поле боя, делая скорпионов опасными врагами.\n\n"
            "• TRAITS PLUS:\n"
            "  Расширение всех начальных особенностей персонажа с русскими описаниями."
        )
    },
    {
        "id": "invenfilter",
        "title": "Inventory Filter (v2.0.4, официальная русская версия)",
        "badge": "ИНТЕРФЕЙС И УДОБСТВО",
        "author": "Mr.Stalin",
        "summary": "Фильтрация инвентаря по вкладкам [Оружие/Патроны/Броня/Химия], умный бартер и кнопка 'Сбросить всё'.",
        "details": (
            "Устраняет самую мучительную проблему Fallout 2 — бесконечный поиск нужного предмета "
            "среди 200 единиц лута:\n\n"
            "• ВКЛАДКИ КАТЕГОРИЙ В ИНВЕНТАРЕ И БАРТЕРЕ:\n"
            "  [Все] [Оружие] [Патроны] [Броня] [Медикаменты] [Разное].\n"
            "  Клик средней кнопкой мыши по «Оружию» и «Патронам» показывает их одновременно.\n\n"
            "• КНОПКА «ПОЛОЖИТЬ ВСЁ»:\n"
            "  Мгновенная выгрузка всей добычи в багажник Хайвеймена или сундук одним нажатием.\n\n"
            "• ИНФОРМАЦИЯ И БАРТЕР:\n"
            "  Отображение чистого веса выбранной категории и счетчик наличных крышек у торговца.\n"
            "  Быстрое переключение между инвентарями спутников в окне торговли без закрытия меню.\n\n"
            "• ГОРЯЧИЕ КЛАВИШИ:\n"
            "  Q, 1, 2, 3, 4, 5 — категории Избранного; W, 6, 7, 8, 9, 0 — категории напарника."
        )
    },
    {
        "id": "npcarmor",
        "title": "NPC Armor Mod (B-Team Mod, финальная редакция RPU)",
        "badge": "ВИЗУАЛ СПУТНИКОВ",
        "author": "BGforge Net, B-Team",
        "summary": "Напарники визуально меняют свой внешний вид при надевании любого типа брони (82.6 МБ спрайтов).",
        "details": (
            "Один из самых долгожданных визуальных модов:\n\n"
            "• ВИЗУАЛЬНАЯ СМЕНА БРОНИ:\n"
            "  Сулик, Вик, Кэссиди, Майрон, Кицунэ, Кэт Джулс и Мирия физически меняют модельку "
            "  на экране при передаче им брони:\n"
            "  - Кожаная куртка (Leather Jacket);\n"
            "  - Кожаная броня (Leather Armor);\n"
            "  - Металлическая броня (Metal Armor);\n"
            "  - Боевая броня (Combat Armor);\n"
            "  - Силовая броня (Power Armor и Улучшенная APA);\n"
            "  - Мантия послушника (Robe).\n\n"
            "• ПОЛНАЯ АНИМАЦИЯ:\n"
            "  Спутники имеют индивидуальные спрайты ходьбы, бега, укрытий и стрельбы из всех видов оружия."
        )
    },
    {
        "id": "partyorders",
        "title": "Party Orders (v1.0.4)",
        "badge": "ТАКТИКА ОТРЯДА",
        "author": "phobos2077, sfall team",
        "summary": "Тактический пульт приказов спутникам прямо в бою и во время исследования карты.",
        "details": (
            "Превращает напарников из хаотичных мишеней в дисциплинированный спецотряд:\n\n"
            "• ОПЕРАТИВНЫЕ ПРИКАЗЫ КЛАВИШАМИ:\n"
            "  - H (Оружие в кобуру): приказ убрать оружие, чтобы не провоцировать охрану городов;\n"
            "  - F (Лечение): напарники оценивают здоровье и используют стимуляторы;\n"
            "  - G (Сбор лута): спутники собирают разбросанные по земле вещи вокруг себя;\n"
            "  - R (Перегруппировка): все напарники немедленно стягиваются к Избранному;\n"
            "  - X (Рассредоточиться): бойцы занимают дистанцию в бою, избегая очередей врага;\n"
            "  - Ctrl+B: переключение напарников на бронебойные или экспансивные патроны."
        )
    },
    {
        "id": "miria",
        "title": "Miria Companion Expansion (Miria Can Wait + RU Dialogs)",
        "badge": "РАСШИРЕНИЕ СПУТНИКОВ",
        "author": "innerbytes, debrouxl",
        "summary": "Жена/муж из Модока становится полноценным напарником с командой «Жди здесь» и прокачкой.",
        "details": (
            "Исправляет главную несправедливость оригинала по отношению к Мирии (или Дэвину):\n\n"
            "• ТАКТИКА И БЕЗОПАСНОСТЬ:\n"
            "  В оригинале Мирия навязывалась после свадьбы и неотвратимо погибала в первом же серьезном бою, "
            "  так как ей нельзя было приказать остаться в безопасном месте.\n"
            "  Теперь в диалоге доступна полноценная опция «Подожди меня здесь» и возможность взять её снова.\n\n"
            "• СОВМЕСТИМОСТЬ С БРОНЕЙ:\n"
            "  Благодаря моду NPC Armor Мирия корректно экипирует любую броню и меняет свой внешний вид.\n\n"
            "• ПОЛНЫЙ РУССКИЙ ПЕРЕВОД:\n"
            "  Все новые диалоговые ветки переведены на литературный русский язык."
        )
    },
    {
        "id": "music",
        "title": "Lossless Studio Music Remaster (Mark Morgan 44.1 kHz Stereo)",
        "badge": "ЗВУК И АТМОСФЕРА",
        "author": "BGforge Net, Mark Morgan",
        "summary": "Замена моно-звука 1998 года (22 кГц) на кристально чистый стереозвук 44.1 кГц (1 ГБ).",
        "details": (
            "Оригинальный Fallout 2 был сжат до предела ради формата CD-ROM: вся музыка была "
            "пережата в глухое моно с частотой 22 кГц и фоновым шипением.\n\n"
            "В нашей сборке установлен полный отреставрированный пакет саундтрека композитора Марка Моргана:\n"
            "• Формат 44.1 кГц Stereo без потери качества (Lossless);\n"
            "• Каждый трек города и пустоши весит по 15–20 МБ;\n"
            "• Мощные глубокие басы, объемная панорама и потрясающий эффект погружения."
        )
    },
    {
        "id": "cassidy",
        "title": "Cassidy Talking Head & HQ Voiceover",
        "badge": "ВИЗУАЛ И ОЗВУЧКА",
        "author": "Joey Bracken, RPU Team",
        "summary": "Живая анимированная 3D-голова для Кэссиди с профессиональной студийной озвучкой.",
        "details": (
            "Один из самых колоритных спутников пустоши — Джон Кэссиди из бара в Пригороде Города Убежища — "
            "теперь оживает в диалогах:\n\n"
            "• Анимированная говорящая голова с богатой мимикой и синхронизацией губ;\n"
            "• Полная высококачественная озвучка от актера Джоуи Брэкена (Joey Bracken);\n"
            "• 100% стабильность без рассинхрона диалоговых веток."
        )
    },
    {
        "id": "fo2tweaks",
        "title": "FO2Tweaks (Пакет современных удобств)",
        "badge": "ИНТЕРФЕЙС И QOL",
        "author": "BGforge Net",
        "summary": "Авто-двери (AutoDoors), сбор лута одной кнопкой, защита выпадения вещей при взрывах.",
        "details": (
            "Набор умных микро-модулей, делающих прохождение комфортным:\n\n"
            "• АВТО-ДВЕРИ (AutoDoors):\n"
            "  Незапертые двери автоматически открываются перед бегущим Избранным — больше никаких тысяч кликов!\n\n"
            "• ПОДБОР ЛУТА ПО SHIFT:\n"
            "  Зажав клавишу Shift, Избранный мгновенно собирает лут с трупов и пола без открытия инвентаря каждого тела.\n\n"
            "• ЗАЩИТА ЛУТА ОТ ДЕЗИНТЕГРАЦИИ:\n"
            "  Когда враг распадается в пепел от лазера или взрывается на куски от плазмы, его вещи больше "
            "  не разлетаются по окрестным гексам, а остаются доступными в кучке останков."
        )
    },
    {
        "id": "marcus_armor",
        "title": "Super Mutant Armor & Dogmeat Kevlar",
        "badge": "СНАРЯЖЕНИЕ СПУТНИКОВ",
        "author": "RPU Team, Continuum",
        "summary": "Уникальная броня для супермутанта Маркуса и кевларовый жилет для Псины.",
        "details": (
            "Решает главную проблему поздней игры оригинала, где Маркус мгновенно погибал от очередей Анклава:\n\n"
            "• БРОНЯ СУПЕРМУТАНТА:\n"
            "  В локации Аббатство (The Abbey) у внешнего торговца продается комплект тяжелой брони мутантов. "
            "  При надевании Маркус меняет спрайт на бронированного лейтенанта из Fallout 1 и получает "
            "  колоссальную защиту от пуль и энергооружия.\n\n"
            "• ЖИЛЕТ ДЛЯ ПСИНЫ:\n"
            "  Псина экипирует специальный кевларовый жилет с уникальным внешним видом."
        )
    },
    {
        "id": "anims",
        "title": "Уникальные оружейные анимации и эффекты",
        "badge": "АНИМАЦИИ И ГРАФИКА",
        "author": "RPU Team, Skynet",
        "summary": "Восстановленные анимации винтовок, мечей вакидзаси, улучшенное пламя огнемета и взрывы.",
        "details": (
            "Восстанавливает вырезанные спрайты движений персонажей:\n\n"
            "• Удары восточным клинком Вакидзаси (Wakizashi animations);\n"
            "• Стрельба и прицеливание из охотничьих и штурмовых винтовок;\n"
            "• Плавная и реалистичная струя огня для тяжелого огнемета;\n"
            "• Кинематографичные вспышки взрывов гранат и динамита."
        )
    },
    {
        "id": "sfall",
        "title": "sfall v4.4.5 + Large Address Aware (4GB Patch)",
        "badge": "ЯДРО И СТАБИЛЬНОСТЬ",
        "author": "Timeslip, Crafty, Mr.Stalin",
        "summary": "Снятие ограничений памяти до 4 ГБ, поддержка Windows 10/11, встроенный обход CRC.",
        "details": (
            "Главный системный мост между игрой 1998 года и современными компьютерами:\n\n"
            "• 4GB LAA PATCH:\n"
            "  Файл fallout2.exe модифицирован флагом Large Address Aware, позволяя движку адресовать до 4 ГБ "
            "  виртуальной памяти вместо старых 2 ГБ. Это исключает вылеты от нехватки памяти при загрузке тяжелых модов.\n\n"
            "• СТАБИЛЬНОСТЬ И CRC:\n"
            "  Встроенная таблица ExtraCRC исключает ошибки несовместимости, а поддержка массивов sfall "
            "  предотвращает порчу сохранений к финалу игры."
        )
    },
    {
        "id": "dustlight",
        "title": "Fallout 2 Community Edition + Dustlight (Профиль HD Visual)",
        "badge": "HD ГРАФИКА И СВЕТ",
        "author": "AlexBatalov, Dustlight Team",
        "summary": "Движок на C++/SDL2 с динамическим мягким освещением факелов/костров и поддержкой 120+ FPS.",
        "details": (
            "Второй профиль в лаунчере, полностью переписанный на современный C++:\n\n"
            "• ДИНАМИЧЕСКИЙ СВЕТ И ТЕНИ:\n"
            "  Факелы, костры, фонари и плазма отбрасывают мягкий теплый свет с честными динамическими тенями.\n\n"
            "• ЧЕСТНЫЙ 4K AI-АПСКЕЙЛ:\n"
            "  Текстуры окружения и карты обработаны нейросетью UltraSharpV2 без мыла и искажений.\n\n"
            "• СОВРЕМЕННЫЙ ДВИЖОК:\n"
            "  Работает на Direct3D 11, поддерживает мониторы 144–240 Гц со сверхплавной прокруткой."
        )
    }
]

class FalloutLauncherApp(tk.Tk):
    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.gameplay_dir = os.path.join(root_dir, "Fallout2_Gameplay")
        self.hd_dir = os.path.join(root_dir, "Fallout2_HD")
        
        self.title("VAULT-TEC OS // Fallout 2: Ultimate Wasteland Edition 2026")
        self.geometry("960x720")
        self.minsize(880, 640)
        self.configure(bg=BG_MAIN)
        
        # Настройка шрифтов и стилей
        self.setup_styles()
        self.build_ui()
        self.show_tab("dashboard")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TScrollbar", background=BG_PANEL, troughcolor=BG_MAIN, bordercolor=BORDER_COLOR, arrowcolor=PHOSPHOR_GREEN)

    def build_ui(self):
        # 1. Верхняя панель Pip-Boy Header
        header = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
        header.pack(fill="x", padx=12, pady=(12, 6))

        # Левый блок логотипа
        logo_frame = tk.Frame(header, bg=BG_PANEL, padx=15, pady=10)
        logo_frame.pack(side="left")

        lbl_sys = tk.Label(logo_frame, text="VAULT-TEC OS  ::  MODEL PIP-BOY 3000", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_PANEL)
        lbl_sys.pack(anchor="w")

        lbl_title = tk.Label(logo_frame, text="FALLOUT 2: ULTIMATE WASTELAND 2026", font=("Consolas", 16, "bold"), fg=PHOSPHOR_GREEN, bg=BG_PANEL)
        lbl_title.pack(anchor="w")

        # Правый статус терминала
        status_box = tk.Frame(header, bg=BG_CARD, padx=12, pady=6, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
        status_box.pack(side="right", padx=15, pady=10)

        lbl_stat_title = tk.Label(status_box, text="СТАТУС СИСТЕМЫ:", font=("Consolas", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
        lbl_stat_title.pack(anchor="e")

        self.lbl_system_status = tk.Label(status_box, text="● ГОТОВ К РАБОТЕ (100% СТАБИЛЬНО)", font=("Consolas", 9, "bold"), fg=BRIGHT_GREEN, bg=BG_CARD)
        self.lbl_system_status.pack(anchor="e")

        # 2. Навигационные вкладки Pip-Boy (Кнопки терминала)
        nav_bar = tk.Frame(self, bg=BG_MAIN)
        nav_bar.pack(fill="x", padx=12, pady=(0, 6))

        self.tab_buttons = {}
        tabs = [
            ("dashboard", "⚡ ПУЛЬТ ЗАПУСКА"),
            ("catalog", "📚 КАТАЛОГ МОДОВ (ПОДРОБНО)"),
            ("manual", "📖 ПАМЯТКА И ДИСКЛЕЙМЕР"),
            ("configs", "⚙ КОНФИГУРАЦИЯ И ФАЙЛЫ"),
        ]

        for tab_id, tab_label in tabs:
            btn = tk.Button(
                nav_bar,
                text=tab_label,
                font=("Consolas", 10, "bold"),
                fg=TEXT_MUTED,
                bg=BG_PANEL,
                activebackground=BG_CARD,
                activeforeground=PHOSPHOR_GREEN,
                bd=1,
                relief="solid",
                padx=14,
                pady=6,
                cursor="hand2",
                command=lambda tid=tab_id: self.show_tab(tid)
            )
            btn.pack(side="left", padx=(0, 6))
            self.tab_buttons[tab_id] = btn

        # 3. Основная рабочая область контейнера
        self.container = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.container.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        # Создаем страницы
        self.pages = {}
        self.pages["dashboard"] = self.create_dashboard_page(self.container)
        self.pages["catalog"] = self.create_catalog_page(self.container)
        self.pages["manual"] = self.create_manual_page(self.container)
        self.pages["configs"] = self.create_configs_page(self.container)

        # 4. Нижний статус-бар
        footer = tk.Frame(self, bg=BG_MAIN)
        footer.pack(fill="x", padx=12, pady=(0, 8))

        self.status_msg_var = tk.StringVar(value="Система откалибрована. Выберите игровой профиль для погружения в Пустошь.")
        lbl_footer = tk.Label(footer, textvariable=self.status_msg_var, font=("Consolas", 9), fg=TEXT_MUTED, bg=BG_MAIN, anchor="w")
        lbl_footer.pack(side="left")

        lbl_version = tk.Label(footer, text="v2.026.4 // RPU+EcCo+MiniRework Edition", font=("Consolas", 8), fg="#446644", bg=BG_MAIN)
        lbl_version.pack(side="right")

    def show_tab(self, tab_id: str):
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.configure(bg=BG_CARD, fg=PHOSPHOR_GREEN, relief="sunken")
            else:
                btn.configure(bg=BG_PANEL, fg=TEXT_MUTED, relief="solid")

        for page in self.pages.values():
            page.pack_forget()

        self.pages[tab_id].pack(fill="both", expand=True, padx=14, pady=14)

    # -------------------------------------------------------------------------
    # СТРАНИЦА 1: ПУЛЬТ ЗАПУСКА (DASHBOARD)
    # -------------------------------------------------------------------------
    def create_dashboard_page(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        # Приветственный баннер
        welcome_box = tk.Frame(frame, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1, padx=16, pady=12)
        welcome_box.pack(fill="x", pady=(0, 14))

        tk.Label(
            welcome_box,
            text="ДОБРО ПОЖАЛОВАТЬ В БЕЗКОМПРОМИССНЫЙ FALLOUT 2 (2026)",
            font=("Consolas", 12, "bold"),
            fg=PHOSPHOR_GREEN,
            bg=BG_CARD
        ).pack(anchor="w")

        intro_text = (
            "Перед вами полная каноничная сборка Fallout 2, доведенная до технического идеала. "
            "В неё интегрирован весь массив вырезанного контента Black Isle (RPU v28), честная баллистика "
            "и экономика EcCo, физика стрельбы MiniRework, современный фильтр инвентаря от Mr.Stalin "
            "и студийный саундтрек 44.1 кГц. Никаких битых сохранений и фанатского бреда — только канон и чистая стабильность."
        )
        tk.Label(
            welcome_box,
            text=intro_text,
            font=("Segoe UI", 9),
            fg=TEXT_MAIN,
            bg=BG_CARD,
            wraplength=860,
            justify="left"
        ).pack(anchor="w", pady=(6, 0))

        # Две карточки профилей запуска
        profiles_container = tk.Frame(frame, bg=BG_PANEL)
        profiles_container.pack(fill="both", expand=True)

        # --- Профиль 1: Gameplay Ultimate ---
        card_gp = tk.Frame(profiles_container, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1, padx=16, pady=14)
        card_gp.pack(side="left", fill="both", expand=True, padx=(0, 8))

        lbl_gp_badge = tk.Label(card_gp, text="КЛАССИКА // РЕКОМЕНДУЕМЫЙ ВЫБОР", font=("Consolas", 8, "bold"), fg=AMBER_COLOR, bg=BG_CARD)
        lbl_gp_badge.pack(anchor="w")

        lbl_gp_title = tk.Label(card_gp, text="FALLOUT 2: GAMEPLAY ULTIMATE", font=("Consolas", 13, "bold"), fg=PHOSPHOR_GREEN, bg=BG_CARD)
        lbl_gp_title.pack(anchor="w", pady=(2, 6))

        gp_desc = (
            "• Движок: Оригинальный sfall v4.4.5 + патч 4GB LAA.\n"
            "• Разрешение: Четкий 1440p (DirectX 9, Scale 2X) без размытия.\n"
            "• Контент: Полный RPU v28 (6 новых городов, Кага, сестра Сулика).\n"
            "• Боевка: EcCo + MiniRework (пробивающий Гаусс, честные AP-пули).\n"
            "• Интерфейс: Удобные вкладки инвентаря [Mr.Stalin] и авто-двери.\n"
            "• Напарники: Смена брони (NPC Armor) + пульт тактики Party Orders.\n"
            "• Звук: Полный Lossless-саундтрек 44.1 кГц + озвучка Кэссиди."
        )
        tk.Label(card_gp, text=gp_desc, font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_CARD, justify="left").pack(anchor="w", pady=(0, 14))

        btn_launch_gp = tk.Button(
            card_gp,
            text="▶ ЗАПУСК: GAMEPLAY ULTIMATE",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#184018",
            activebackground="#256025",
            activeforeground="#ffffff",
            bd=2,
            relief="raised",
            pady=10,
            cursor="hand2",
            command=self.launch_gameplay
        )
        btn_launch_gp.pack(fill="x", side="bottom")

        # --- Профиль 2: HD Visual Dustlight ---
        card_hd = tk.Frame(profiles_container, bg=BLUE_PANEL, bd=1, relief="solid", highlightbackground=BLUE_BORDER, highlightthickness=1, padx=16, pady=14)
        card_hd.pack(side="right", fill="both", expand=True, padx=(8, 0))

        lbl_hd_badge = tk.Label(card_hd, text="СОВРЕМЕННЫЙ ДВИЖОК // HD СВЕТ", font=("Consolas", 8, "bold"), fg=BLUE_COLOR, bg=BLUE_PANEL)
        lbl_hd_badge.pack(anchor="w")

        lbl_hd_title = tk.Label(card_hd, text="FALLOUT 2: HD VISUAL DUSTLIGHT", font=("Consolas", 13, "bold"), fg="#ffffff", bg=BLUE_PANEL)
        lbl_hd_title.pack(anchor="w", pady=(2, 6))

        hd_desc = (
            "• Движок: Fallout 2 Community Edition (C++ / SDL2).\n"
            "• Рендеринг: Прямой Direct3D 11, поддержка 120–240 Гц.\n"
            "• Графика: Нейросетевой AI-апскейл всех текстур 4x-UltraSharpV2.\n"
            "• Освещение: Мягкий свет от костров, факелов и ламп (Dustlight).\n"
            "• Атмосфера: Реалистичные тени, честные темные ночи.\n"
            "• Совместимость: Базовый контент RPU на современной платформе."
        )
        tk.Label(card_hd, text=hd_desc, font=("Segoe UI", 9), fg="#d0e2ec", bg=BLUE_PANEL, justify="left").pack(anchor="w", pady=(0, 14))

        btn_launch_hd = tk.Button(
            card_hd,
            text="✦ ЗАПУСК: HD VISUAL DUSTLIGHT",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#1b3c59",
            activebackground="#28567d",
            activeforeground="#ffffff",
            bd=2,
            relief="raised",
            pady=10,
            cursor="hand2",
            command=self.launch_hd
        )
        btn_launch_hd.pack(fill="x", side="bottom")

        # Нижняя панель быстрых утилит
        quick_bar = tk.Frame(frame, bg=BG_PANEL, pady=10)
        quick_bar.pack(fill="x")

        tk.Button(
            quick_bar,
            text="📁 Папка сохранений (Savegame)",
            font=("Segoe UI", 9),
            fg=TEXT_MAIN,
            bg=BG_CARD,
            activebackground=BG_CARD_HOVER,
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.open_saves
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            quick_bar,
            text="⚙ Настройки экрана (f2_res.ini)",
            font=("Segoe UI", 9),
            fg=TEXT_MAIN,
            bg=BG_CARD,
            activebackground=BG_CARD_HOVER,
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.open_res_config
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            quick_bar,
            text="📖 Подробная памятка и клавиши",
            font=("Segoe UI", 9),
            fg=AMBER_COLOR,
            bg=BG_CARD,
            activebackground=BG_CARD_HOVER,
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda: self.show_tab("manual")
        ).pack(side="right")

        return frame

    # -------------------------------------------------------------------------
    # СТРАНИЦА 2: ДЕТАЛЬНЫЙ КАТАЛОГ МОДОВ (CATALOG)
    # -------------------------------------------------------------------------
    def create_catalog_page(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        top_info = tk.Frame(frame, bg=BG_PANEL)
        top_info.pack(fill="x", pady=(0, 8))

        tk.Label(top_info, text="ДЕТАЛЬНЫЙ РЕЕСТР УСТАНОВЛЕННЫХ МОДИФИКАЦИЙ", font=("Consolas", 12, "bold"), fg=PHOSPHOR_GREEN, bg=BG_PANEL).pack(anchor="w")
        tk.Label(top_info, text="Выберите модуль в списке слева для просмотра подробного описания и авторских особенностей.", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")

        content_box = tk.Frame(frame, bg=BG_PANEL)
        content_box.pack(fill="both", expand=True)

        # Левая колонка: список модов
        left_frame = tk.Frame(content_box, width=280, bg=BG_PANEL)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        self.mod_listbox = tk.Listbox(
            left_frame,
            font=("Consolas", 9, "bold"),
            bg=BG_CARD,
            fg=TEXT_MAIN,
            selectbackground="#1e441e",
            selectforeground=PHOSPHOR_GREEN,
            bd=1,
            relief="solid",
            highlightthickness=0,
            activestyle="none"
        )
        self.mod_listbox.pack(side="left", fill="both", expand=True)

        sb_list = ttk.Scrollbar(left_frame, orient="vertical", command=self.mod_listbox.yview)
        sb_list.pack(side="right", fill="y")
        self.mod_listbox.configure(yscrollcommand=sb_list.set)

        for mod in MODS_CATALOG:
            self.mod_listbox.insert("end", f" {mod['title'].split('(')[0].strip()}")

        self.mod_listbox.bind("<<ListboxSelect>>", self.on_mod_select)

        # Правая колонка: детальное описание
        right_frame = tk.Frame(content_box, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1, padx=16, pady=14)
        right_frame.pack(side="right", fill="both", expand=True)

        self.lbl_card_badge = tk.Label(right_frame, text="", font=("Consolas", 8, "bold"), fg=AMBER_COLOR, bg=BG_CARD)
        self.lbl_card_badge.pack(anchor="w")

        self.lbl_card_title = tk.Label(right_frame, text="", font=("Consolas", 13, "bold"), fg=PHOSPHOR_GREEN, bg=BG_CARD, wraplength=520, justify="left")
        self.lbl_card_title.pack(anchor="w", pady=(2, 2))

        self.lbl_card_author = tk.Label(right_frame, text="", font=("Segoe UI", 8, "italic"), fg=TEXT_MUTED, bg=BG_CARD)
        self.lbl_card_author.pack(anchor="w", pady=(0, 10))

        # Текстовое поле с прокруткой для описания
        self.txt_mod_detail = ScrolledText(
            right_frame,
            wrap="word",
            font=("Segoe UI", 9),
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            bd=1,
            relief="solid",
            padx=10,
            pady=10
        )
        self.txt_mod_detail.pack(fill="both", expand=True)

        # Выбираем первый по умолчанию
        self.mod_listbox.select_set(0)
        self.display_mod_info(0)

        return frame

    def on_mod_select(self, event):
        sel = self.mod_listbox.curselection()
        if sel:
            self.display_mod_info(sel[0])

    def display_mod_info(self, index: int):
        mod = MODS_CATALOG[index]
        self.lbl_card_badge.configure(text=f"КАТЕГОРИЯ: {mod['badge']}")
        self.lbl_card_title.configure(text=mod['title'])
        self.lbl_card_author.configure(text=f"Автор(ы): {mod['author']}")

        self.txt_mod_detail.configure(state="normal")
        self.txt_mod_detail.delete("1.0", "end")

        full_body = f"{mod['summary']}\n\n{'='*60}\nПОДРОБНЫЙ ТЕХНИЧЕСКИЙ РАЗБОР:\n{'='*60}\n\n{mod['details']}"
        self.txt_mod_detail.insert("1.0", full_body)
        self.txt_mod_detail.configure(state="disabled")

    # -------------------------------------------------------------------------
    # СТРАНИЦА 3: ПАМЯТКА И ДИСКЛЕЙМЕР (MANUAL)
    # -------------------------------------------------------------------------
    def create_manual_page(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        txt_manual = ScrolledText(frame, wrap="word", font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MAIN, bd=1, relief="solid", padx=16, pady=14)
        txt_manual.pack(fill="both", expand=True)

        manual_content = (
            "========================================================================================\n"
            "         РУКОВОДСТВО ВЫЖИВАНИЯ И ВАЖНЫЕ СОВЕТЫ // FALLOUT 2 ULTIMATE 2026\n"
            "========================================================================================\n\n"
            "1. ВАЖНЫЙ ДИСКЛЕЙМЕР ПО ПЕРВОМУ ЗАПУСКУ:\n"
            "----------------------------------------------------------------------------------------\n"
            "В нашей сборке все файлы способностей и перков (Perks.ini, Drugs.ini) уже предварительно\n"
            "сгенерированы и вложены в сборку. Поэтому игра сразу запустится без лишних окон.\n\n"
            "Однако, если при самом первом старте новой игры вы вдруг увидите служебное уведомление\n"
            "мода MiniRework («All set. Restart the game»):\n"
            "  -> Нажмите кнопку [ГОТОВО] (игра плавно закроется для сохранения параметров);\n"
            "  -> Запустите игру снова через лаунчер и создайте персонажа;\n"
            "  -> Больше это окно никогда не появится, и игра пойдет непрерывно до финала.\n\n\n"
            "2. СПРАВОЧНИК ГОРЯЧИХ КЛАВИШ (QoL УПРАВЛЕНИЕ):\n"
            "----------------------------------------------------------------------------------------\n"
            "• SHIFT (удержание в игре):\n"
            "  - Подсвечивает ВСЕ предметы на земле, открытые контейнеры и тела врагов (без пиксель-хантинга);\n"
            "  - Позволяет мгновенно собирать лут с трупов прямо на карте без открытия экрана инвентаря.\n\n"
            "• УПРАВЛЕНИЕ ФИЛЬТРОМ ИНВЕНТАРЯ (InventoryFilter):\n"
            "  - Кнопки категорий вверху экрана: [Все] [Оружие] [Патроны] [Броня] [Медикаменты] [Разное];\n"
            "  - Клик СРЕДНЕЙ кнопкой мыши по «Оружию» и «Патронам» показывает оружие и боеприпасы к нему;\n"
            "  - Кнопка «Положить всё» (Drop All) — быстрая выгрузка всего хабара в сундук или багажник машины;\n"
            "  - Быстрое переключение категорий игрока: клавиши Q, 1, 2, 3, 4, 5;\n"
            "  - Быстрое переключение категорий напарника в обмене: клавиши W, 6, 7, 8, 9, 0;\n"
            "  - F11 — вызов меню настроек фильтра инвентаря.\n\n"
            "• ТАКТИЧЕСКИЙ ПУЛЬТ ПРИКАЗОВ СПУТНИКАМ (Party Orders):\n"
            "  - H — приказ напарникам убрать оружие в кобуру (чтобы не злить стражу городов);\n"
            "  - F — приказ применить стимуляторы и залечить травмы;\n"
            "  - G — напарники собирают разбросанный вокруг лут;\n"
            "  - R — немедленная перегруппировка к позиции Избранного;\n"
            "  - X — рассредоточение в бою, чтобы не попадать под очереди врагов;\n"
            "  - Ctrl + B — переключение напарников на бронебойные (AP) или обычные (JHP) патроны.\n\n\n"
            "3. ТАКТИЧЕСКИЕ СОВЕТЫ ПО ПРОХОЖДЕНИЮ:\n"
            "----------------------------------------------------------------------------------------\n"
            "• ХРАМ ИСПЫТАНИЙ (СТАРТ):\n"
            "  В финале Храма с воином Камероном вовсе не обязательно драться кулаками! Если у вашего героя\n"
            "  прокачан навык «Красноречие», его можно убедить словами без единого удара. Также ключ от двери\n"
            "  можно незаметно украсть навыком «Воровство».\n\n"
            "• ПЕРВЫЙ СПУТНИК (СУЛИК):\n"
            "  Находится в первом же городе — Кламате (в трактире Мамы). После освобождения у него открывается\n"
            "  большая ветка диалогов и личный квест по поиску сестры в Деревне Дикарей (Primitive Tribe).\n\n"
            "• БРОНЯ МАРКУСА:\n"
            "  Супермутант Маркус из Брокен Хиллз может носить уникальную тяжелую броню супермутантов.\n"
            "  Она продается у торговца возле ворот Аббатства (The Abbey). С ней Маркус становится танком.\n\n"
            "• СПАСЕНИЕ МИРИИ:\n"
            "  Если вы женились в Модоке, не переживайте за жизнь супруги — теперь ей можно сказать «Жди здесь»,\n"
            "  а также надеть на неё любую броню (она визуально сменит спрайт)."
        )

        txt_manual.insert("1.0", manual_content)
        txt_manual.configure(state="disabled")
        return frame

    # -------------------------------------------------------------------------
    # СТРАНИЦА 4: КОНФИГУРАЦИЯ И ФАЙЛЫ (CONFIGS)
    # -------------------------------------------------------------------------
    def create_configs_page(self, parent):
        frame = tk.Frame(parent, bg=BG_PANEL)

        tk.Label(frame, text="СИСТЕМНЫЕ ФАЙЛЫ И ПРЯМАЯ НАСТРОЙКА", font=("Consolas", 12, "bold"), fg=PHOSPHOR_GREEN, bg=BG_PANEL).pack(anchor="w", pady=(0, 4))
        tk.Label(frame, text="Открытие системных файлов конфигурации в текстовом редакторе для тонкой подстройки.", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(0, 14))

        configs = [
            ("f2_res.ini", "Настройки разрешения экрана, режима DirectX 9 и масштабирования (Scale 2X).", self.open_res_config),
            ("ddraw.ini", "Главный конфигуратор sfall: лимиты памяти, скорость счетчиков, функции мыши.", lambda: self.open_file_relative("ddraw.ini")),
            ("fo2tweaks.ini", "Настройки автоматического открытия дверей, быстрого лута и подсветки.", lambda: self.open_file_relative(os.path.join("mods", "fo2tweaks.ini"))),
            ("InvenFilter.ini", "Параметры фильтрации инвентаря, настройки горячих клавиш и отображения веса.", lambda: self.open_file_relative(os.path.join("mods", "InventoryFilter.dat", "InvenFilter.ini"))),
            ("mods_order.txt", "Список строгого порядка приоритетов загрузки файлов модификаций sfall.", lambda: self.open_file_relative(os.path.join("mods", "mods_order.txt"))),
            ("fallout2.cfg", "Базовый конфигурационный файл игры: пути к ресурсам, язык и громкость звука.", lambda: self.open_file_relative("fallout2.cfg")),
        ]

        for fname, desc, cmd in configs:
            row = tk.Frame(frame, bg=BG_CARD, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1, padx=12, pady=10)
            row.pack(fill="x", pady=4)

            btn_box = tk.Frame(row, bg=BG_CARD)
            btn_box.pack(side="left", padx=(0, 15))

            tk.Button(
                btn_box,
                text=f"Открыть {fname}",
                font=("Consolas", 9, "bold"),
                fg=PHOSPHOR_GREEN,
                bg="#1a2e1a",
                activebackground="#264726",
                bd=1,
                relief="solid",
                width=20,
                pady=4,
                cursor="hand2",
                command=cmd
            ).pack()

            info_box = tk.Frame(row, bg=BG_CARD)
            info_box.pack(side="left", fill="both", expand=True)

            tk.Label(info_box, text=fname, font=("Consolas", 10, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
            tk.Label(info_box, text=desc, font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")

        return frame

    # -------------------------------------------------------------------------
    # ЛОГИКА ЗАПУСКА И ДЕЙСТВИЙ
    # -------------------------------------------------------------------------
    def launch_gameplay(self):
        exe = os.path.join(self.gameplay_dir, "fallout2.exe")
        if not os.path.exists(exe):
            exe = os.path.join(self.root_dir, "fallout2.exe")

        if os.path.exists(exe):
            self.status_msg_var.set("Запуск Fallout 2: Gameplay Ultimate (sfall 4.4)...")
            try:
                subprocess.Popen([exe], cwd=os.path.dirname(exe))
                self.status_msg_var.set("Игра запущена. Приятного погружения в Пустошь!")
            except Exception as e:
                messagebox.showerror("Ошибка запуска", f"Не удалось запустить процесс:\n{e}")
        else:
            messagebox.showerror(
                "Файл не найден",
                f"Исполняемый файл fallout2.exe не найден по пути:\n{exe}\n"
                "Убедитесь, что игра установлена через инсталлятор."
            )

    def launch_hd(self):
        for candidate in ["dustlight.exe", "fallout2-ce.exe"]:
            exe = os.path.join(self.hd_dir, candidate)
            if not os.path.exists(exe):
                exe = os.path.join(self.root_dir, candidate)
            if os.path.exists(exe):
                self.status_msg_var.set(f"Запуск HD Visual Dustlight ({candidate})...")
                try:
                    subprocess.Popen([exe], cwd=os.path.dirname(exe))
                    self.status_msg_var.set("HD-движок запущен. Приятной игры!")
                    return
                except Exception as e:
                    messagebox.showerror("Ошибка запуска", f"Не удалось запустить HD-процесс:\n{e}")
                    return

        messagebox.showerror(
            "Файл не найден",
            f"Исполняемый файл HD Dustlight не найден в папке:\n{self.hd_dir}\n"
            "Установите HD-профиль через мастер-инсталлятор!"
        )

    def open_saves(self):
        target = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir
        saves_dir = os.path.join(target, "DATA", "SAVEGAME")
        os.makedirs(saves_dir, exist_ok=True)
        try:
            os.startfile(saves_dir)
            self.status_msg_var.set(f"Открыта папка сохранений: {saves_dir}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")

    def open_res_config(self):
        self.open_file_relative("f2_res.ini")

    def open_file_relative(self, rel_path: str):
        target = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir
        path = os.path.join(target, rel_path)
        if os.path.exists(path):
            try:
                os.startfile(path)
                self.status_msg_var.set(f"Открыт файл: {rel_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
        else:
            messagebox.showinfo("Информация", f"Файл {rel_path} пока не найден. Он создается после первого запуска игры.")

if __name__ == "__main__":
    try:
        app = FalloutLauncherApp(os.path.dirname(os.path.abspath(__file__)))
        app.mainloop()
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        try:
            import tkinter as tk
            from tkinter import messagebox
            r = tk.Tk()
            r.withdraw()
            messagebox.showerror("Fallout 2 Launcher - Ошибка", f"Критическая ошибка запуска лаунчера:\n\n{err}")
        except Exception:
            with open("launcher_crash.log", "w", encoding="utf-8") as f:
                f.write(err)
