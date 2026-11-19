/**
 * Application Core Logic: Navigation, Mod Catalog, Settings, Saves, and Feedback/Bug-Reports.
 */

const MODS_DATABASE = [
  {
    id: "rpu",
    title: "RESTORATION PROJECT UPDATED",
    category: "КВЕСТЫ",
    badge: "КОНТЕНТ МИРА",
    version: "v28.0",
    author: "killap, Burn, Darek, RPU Team",
    desc: "Грандиозная реставрация оригинального мира Fallout 2: Аббатство (The Abbey), Агентство охраны окружающей среды (EPA), Деревня Дикарей, лагерь работорговцев в Дыре и тайное Убежище 23.",
    cancels: "Вырезание контента релизом 1998 года, пустые локации и оборванные сюжетные цепочки.",
    specs: ["Новые локации: +6 крупных городов", "Квесты: +45 цепочек", "Персонажи: 80+ новых NPC", "Озвучка: восстановлены реплики"]
  },
  {
    id: "upu",
    title: "UNOFFICIAL PATCH UPDATED",
    category: "ДВИЖОК",
    badge: "1200+ ФИКСОВ",
    version: "v28.0",
    author: "killap, UPU Team",
    desc: "Фундамент технической стабильности: устранение более 1200 критических багов оригинальной игры 1998 года, защита от софтлоков, повреждения файлов сохранений и утечек памяти.",
    cancels: "Вылеты на Windows 10/11, тупики в диалогах, порчу сейвов и сбои скриптов при переходах между картами.",
    specs: ["Исправлено багов: 1200+", "Ошибок скриптов: 0", "Защита сохранений: Активна", "Совместимость: 100%"]
  },
  {
    id: "community_fixes",
    title: "COMMUNITY NARRATIVE FIXES 2026",
    category: "КВЕСТЫ",
    badge: "СЮЖЕТНЫЕ ДЫРЫ",
    version: "v1.0",
    author: "Antigravity & Community",
    desc: "Хирургическое исправление застарелых сюжетных тупиков Пустоши: Смитти и регулятор Хайвеймена, возврат амулета призрака Анны у Джоуи, крысиные улики на часах Корнелиуса, ветка Торра и братьев Дантонов при низком интеллекте, научная вакцина доктора Троя от Джета, багажник Т-Рея и лечение больного сердца Кэссиди.",
    cancels: "Потерю уникальных деталей, забывчивость NPC после передачи квестовых предметов и нелогичные софтлоки.",
    specs: ["Смитти и Хайвеймен: софтлок снят", "Призрак Анна и Джоуи: амулет возвращается", "Часы Корнелиуса: крысиные улики", "Доктор Трой: вакцина от Джета"]
  },
  {
    id: "talking_heads",
    title: "TALKING HEADS ADDON v3.7",
    category: "ВИЗУАЛ",
    badge: "3D-ГОЛОВЫ ЛИДЕРОВ",
    version: "v3.7",
    author: "Goat_Boy, ThatGuyCDude, RPU Team",
    desc: "Анимированные говорящие 3D-головы ключевых лидеров Пустоши 2241 года: Первая Гражданка Линетт, Президент НКР Танди, дикарь Сулик, работорговец Мецгер, босс мафии Джон Бишоп и ученый Горис. Включает сохранение тайны Гориса под теневым капюшоном до первой схватки.",
    cancels: "Плоские безликие текстовые окна, превращая диалоги с главными фигурами Северной Калифорнии в живое общение с мимикой и характером.",
    specs: ["Новые 3D-головы: Линетт, Танди, Сулик, Мецгер", "Горис: теневой капюшон до боя", "Рендер: 32-bit Head Graphics", "Синхронизация губ: 100%"]
  },
  {
    id: "sfall",
    title: "SFALL v4.4.8 ADVANCED ENGINE",
    category: "ДВИЖОК",
    badge: "DIRECTX 9 & 144HZ",
    version: "v4.4.8",
    author: "Timeslip, Crafty, Mr.Stalin",
    desc: "Аппаратный движок на DirectX 9 с поддержкой высокой частоты обновления (144-240 Гц), субпиксельного ввода мыши, колесика прокрутки и шейдеров четкости.",
    cancels: "Ограничение 30 FPS, статтеры на Windows 10/11, задержки ввода мыши и сбои таймингов на современных многоядерных процессорах.",
    specs: ["Рендерер: Direct3D 9", "Герцовка: 144/240 Гц", "Поддержка мыши: Raw Input", "Скриптовый расширитель: Активен"]
  },
  {
    id: "weapons",
    title: "COMBAT & WEAPON ANIMATIONS",
    category: "ВИЗУАЛ",
    badge: "ОРУЖИЕ",
    version: "v2.6",
    author: "RPU Animation Team, Continuum",
    desc: "Сотни новых кадров боевых спрайтов: охотничьи карабины, мечи вакидзаси, тяжелый огнемет, дульные вспышки и плавные перезарядки.",
    cancels: "Визуальную скупость оригинала: одинаковые спрайты для разного оружия, стрельбу без отдачи и отсутствие вспышек выстрелов.",
    specs: ["Оружие: 18 новых спрайтов", "Направления: 8 изометрических", "Синхронизация звука: 100%", "Тайминги AP: Родные"]
  },
  {
    id: "armor",
    title: "NPC ARMOR VISUAL EVOLUTION",
    category: "СПУТНИКИ",
    badge: "БРОНЯ НАПАРНИКОВ",
    version: "v3.1",
    author: "Continuum, Skynet, RPU Team",
    desc: "Напарники визуально меняют экипировку при смене брони: Сулик, Вик, Кэссиди, Мирия и Ангелина в кожаных куртках, боевых комплектах и Силовой Броне.",
    cancels: "Нелепость, когда спутники носили силовую броню в инвентаре, но на экране всегда оставались в рваных куртках или набедренных повязках.",
    specs: ["Сулик: все ранги брони", "Вик: полный набор спрайтов", "Женские напарники: боевая/силовая броня", "Силовая броня: Поддерживается"]
  },
  {
    id: "marcus",
    title: "MARCUS ARMOR & DOGMEAT KEVLAR",
    category: "СПУТНИКИ",
    badge: "ТЯЖЕЛЫЙ ЭКИП",
    version: "v1.8",
    author: "RPU Team, Continuum",
    desc: "Тяжелая броня супермутантов для шерифа Маркуса и кевларовый бронежилет для Псины — напарники больше не гибнут в финальной фазе от очередей патрулей Анклава.",
    cancels: "Беспомощность Маркуса и Псины в эндгейме из-за невозможности экипировать защитную броню.",
    specs: ["Броня Маркуса: +40% живучести", "Защита от плазмы: 50%", "Кевлар Псины: 35% DT", "Эндгейм-баланс: S-ранг"]
  },
  {
    id: "cassidy",
    title: "JOHN CASSIDY TALKING HEAD",
    category: "СПУТНИКИ",
    badge: "3D-ГОЛОВА",
    version: "v2.0",
    author: "Joey Bracken, RPU Team",
    desc: "Живая анимированная 3D-голова бармена Джона Кэссиди из Пригорода Города Убежища с мимикой ветерана Пустоши и профессиональной актерской озвучкой.",
    cancels: "Безликость одного из самых харизматичных спутников игры, превращая плоский текст в живую речь с характером.",
    specs: ["3D-модель: Пререндер", "Анимация губ: Синхронизирована", "Стиль: 1998 Black Isle CGI", "Качество звука: 44.1 кГц"]
  },
  {
    id: "angela",
    title: "ANGELA BISHOP COMPANION",
    category: "СПУТНИКИ",
    badge: "В РАЗРАБОТКЕ",
    version: "В РАЗРАБОТКЕ",
    author: "RP-CE Team, Antigravity Adapt",
    desc: "[В РАЗРАБОТКЕ] Дочь мафиозного дона Джона Бишопа в роли полноценного спутника Избранного. Планируется собственная ветка диалогов на русском языке, реакции на криминальные семьи Нью-Рено, смена брони и интеграция с Party Orders.",
    cancels: "Статичность семьи Бишоп, превращая авантюрную дочь криминального босса в опасного и дерзкого стрелка команды.",
    specs: ["Статус: В активной разработке", "Локализация: Литературный русский", "Оружие: Пистолеты и ПП", "Экипировка брони: В процессе интеграции"]
  },
  {
    id: "miria",
    title: "MIRIA COMPANION REWORK",
    category: "СПУТНИКИ",
    badge: "КОМПАНЬОН",
    version: "v2.0",
    author: "RPU Team, killap",
    desc: "Превращение навязанной жены из Модока в полноценного боевого компаньона: команда «Жди здесь», прокачка характеристик по уровням, экипировка боевой брони и цивилизованный развод в Нью-Рено.",
    cancels: "Бесполезность навязанных супругов в роли «мертвого груза» и их неизбежную гибель в первых же перестрелках.",
    specs: ["Команда ожидания: Добавлена", "Прокачка: Уровни 1-6", "Обмен вещами: Открыт", "Развод: Доступен через отца Тулли"]
  },
  {
    id: "damage",
    title: "YAAM & GLOVZ BALLISTICS REWORK",
    category: "ГЕЙМПЛЕЙ",
    badge: "БАЛАНС УРОНА",
    version: "v1.5",
    author: "Glovz, YAAM, sfall team",
    desc: "Исправление сломанной математики бронебойных пуль оригинала: AP-патроны теперь эффективно вскрывают металлическую и Силовую Броню, а экспансивные JHP наносят максимальный урон по незащищенным телам.",
    cancels: "Сломанную формулу урона оригинала, из-за которой экспансивные пули пробивали броню лучше бронебойных, а AP-патроны были бесполезны.",
    specs: ["Формула AP: Исправлена", "Пули JHP: Максимальный урон по мясу", "Длинные очереди: Сбалансированы", "Экипировка врагов: Адаптивна"]
  },
  {
    id: "doors",
    title: "AUTODOORS & LOOT PROTECTION",
    category: "ГЕЙМПЛЕЙ",
    badge: "АВТО-ДВЕРИ",
    version: "v2.4",
    author: "BGforge Net, sfall team",
    desc: "Автоматическое распахивание незапертых дверей перед идущим героем и сохранение ценного лута в кучке пепла при критической дезинтеграции врагов плазмой или лазером.",
    cancels: "Рутинные сотни лишних кликов на каждую дверь и безвозвратное испарение редких предметов при критических попаданиях энергией.",
    specs: ["Авто-двери: Мгновенно", "Потеря лута: 0%", "Энергетический пепел: Лутаемый", "Задержка: 0 мс"]
  },
  {
    id: "inventory",
    title: "ADVANCED INVENTORY & SORTING",
    category: "ГЕЙМПЛЕЙ",
    badge: "ИНВЕНТАРЬ",
    version: "v4.2",
    author: "sfall contributors",
    desc: "Прокрутка инвентаря колесиком мыши, мгновенная сортировка (оружие, броня, медикаменты, патроны), авто-перезарядка оружия при клике и 4 слота бартера у торговцев.",
    cancels: "Утомительный пиксель-хантинг и медленное перетаскивание предметов по одной штуке — добавляет колесо мыши и быстрый лут в 1 клик.",
    specs: ["Колесо мыши: Нативное", "Быстрый лут: 1 клик", "Бартер: 4 слота", "Сортировка: По категориям (J)"]
  },
  {
    id: "pip_timers",
    title: "PIP-BOY QUEST TIMERS",
    category: "ВИЗУАЛ",
    badge: "ТАЙМЕРЫ КВЕСТОВ",
    version: "v1.2",
    author: "Rotators, Lexx",
    desc: "Интерактивные таймеры на экране наручного Pip-Boy 2000: наглядный обратный отсчет до гибели деревни Арройо от засухи, аварии ядерного реактора в Гекко и нападения рейдеров на Деревню Дикарей.",
    cancels: "Необходимость высчитывать игровые сутки по календарю вслепую, защищая от внезапного провала сюжетных квестов.",
    specs: ["Таймер Арройо: Активен", "Реактор Гекко: Контроль времени", "Интерфейс: Волт-Тек CRT", "Шрифт: Моноширинный зеленый"]
  },
  {
    id: "mapblur",
    title: "INTERFACE UPSCALED & MAPBLUR FX",
    category: "ВИЗУАЛ",
    badge: "ЧЕТКИЙ ИНТЕРФЕЙС",
    version: "v2.0",
    author: "Rotators, Lexx, sfall team",
    desc: "Кристальный HD-апскейл всех панелей интерфейса в высоком разрешении, широкоформатная панорамная карта мира (ExpandWorldMap=1) и мягкое кинематографичное размытие фона при открытии диалогов, инвентаря и Пип-Боя.",
    cancels: "Размытые низкополигональные текстуры меню на современных мониторах и визуальный шум за диалоговыми окнами.",
    specs: ["HD-интерфейс: Кристальный апскейл", "Размытие фона: Шейдер MapBlur", "Карта мира: Панорама 16:9", "Шейдер четкости: LumaSharpen"]
  },
  {
    id: "audio_unlocked",
    title: "UNLOCKED WEAPON SFX",
    category: "ЗВУК",
    badge: "ЗВУКИ BLACK ISLE",
    version: "v1.1",
    author: "sfall team, Black Isle Archives",
    desc: "Разблокировка скрытых звуковых вариаций выстрелов, перезарядки и взрывов, записанных звукорежиссёрами Black Isle в 1998 году, но заблокированных из-за бага оригинального движка.",
    cancels: "Однообразный щелчок одного и того же звукового файла при каждом выстреле, возвращая натуральное разнообразие перестрелок.",
    specs: ["Аудиофайлы: 100% оригиналы Black Isle", "Хук движка: sFall Sound Engine", "Вариации: 2–3 звука на ствол", "Конфликты: Отсутствуют"]
  },
  {
    id: "music",
    title: "MARK MORGAN LOSSLESS REMASTER",
    category: "ЗВУК",
    badge: "ЗВУК 1 ГБ",
    version: "44.1 кГц",
    author: "Mark Morgan, BGforge Net",
    desc: "Культовый студийный эмбиент-саундтрек Марка Моргана: замена пожатого моно 22 кГц эпохи CD-ROM 1998 года на кристально чистый стереозвук студийного качества 44.1 кГц (31 трек), играющий без пауз даже в диалогах.",
    cancels: "Глухой моно-звук со сжатием 22 кГц эпохи CD-ROM, восстанавливая полный студийный стереозвук без потерь качества.",
    specs: ["Треков: 31 композиция", "Формат: Lossless ACM Stereo", "Битрейт: 1411 кбит/с", "Объем: 1.0 ГБ"]
  },
  {
    id: "crafting",
    title: "WASTELAND CRAFT & PIPE WEAPONS",
    category: "ГЕЙМПЛЕЙ",
    badge: "САМОПАЛЫ И КРАФТ",
    version: "v2.0",
    author: "phobos2077, EcCo Team",
    desc: "Аутентичный кустарный арсенал Пустоши: сборка трубчатых самопалов (Pipe Rifle), кустарных гранат, арбалетов и шипованных ловушек. Оружие распространено среди рейдеров и банд Дыры (строго без спавна в племени Арройо).",
    cancels: "Острый дефицит оружия на ранних этапах и нехватку кустарного вооружения у бродяг и рейдеров пустоши.",
    specs: ["Кустарное оружие: Pipe Rifle & Zip Gun", "Ловушки: Капканы и шипы EPA", "Распределение: Рейдеры и Дыра", "Храм и Арройо: 100% канон"]
  },
  {
    id: "hunting",
    title: "HUNTING, HARVESTING & FIELD SURVIVAL",
    category: "ГЕЙМПЛЕЙ",
    badge: "ОХОТА И РАЗДЕЛКА",
    version: "v2.0",
    author: "EcCo Team, RPU",
    desc: "Свежевание дичи ножом охотника: шкуры гекконов, мясо, железы и хвосты скорпионов для противоядий. Жарка чистого мяса на кострах в деревне без штрафов радиации.",
    cancels: "Бесполезность навыка «Скиталец», позволяя разделывать туши гекконов и скорпионов ножом для добычи ценных шкур, мяса и ядов.",
    specs: ["Разделка: Шкуры, мясо, хвосты", "Приготовление: Костры Арройо/Кламата", "Навык: Скиталец (Outdoorsman)", "Баланс: Стартовый капитал дикаря"]
  },
  {
    id: "highwayman",
    title: "HIGHWAYMAN OVERHAUL & TRUNK FIX",
    category: "ГЕЙМПЛЕЙ",
    badge: "АВТО ХАЙВЕЙМЕН",
    version: "v3.2",
    author: "phobos2077, sfall team",
    desc: "Полная защита багажника от пропажи вещей, оптимизированный расход ядерных микробатарей и возможность тюнинга турбонагнетателя у Смитти.",
    cancels: "Внезапное исчезновение вещей из багажника машины, баг покупки у Смитти и завышенный расход ядерных батарей.",
    specs: ["Багажник: Защита от пропажи лута", "Расход энергии: -30% с регулятором", "Скорость: Турбонагнетатель Смитти", "Скрипты: Стабильность 100%"]
  },
  {
    id: "encounters",
    title: "CURATED ENCOUNTERS & WORLD ENGINE",
    category: "ГЕЙМПЛЕЙ",
    badge: "БАЛАНС ВСТРЕЧ",
    version: "v4.4.8",
    author: "Ray, sfall team, RPU",
    desc: "Защита от спама встреч на современных процессорах (WorldMapEncounterFix). Редкие, атмосферные встречи вместо непрерывных засад каждые 2 секунды.",
    cancels: "Бесконечный спам одинаковых засад каждые три секунды пути, восстанавливая ценность и баланс редких спецвстреч.",
    specs: ["Спам встреч: Устранен (Fix=1)", "Частота: Откалибрована (Rate=7)", "Диалог выбора: По навыку Скитальца", "Широкоформатная карта: Включена"]
  },
  {
    id: "graphics",
    title: "NATIVE 2560x1440 32-BIT ARGB",
    category: "ВИЗУАЛ",
    badge: "2K NATIVE",
    version: "v4.1.8",
    author: "Mash, sfall team",
    desc: "Аппаратное билинейное сглаживание текстур GPU, поддержка 32-битного цвета ARGB8888 и нативное разрешение 2K QHD без лесенок.",
    cancels: "Размытие картинки, цветовую грязь 8-битной палитры (256 цветов) и некрасивое растягивание интерфейса на мониторах 1440p и 4K.",
    specs: ["Нативное разрешение: 2560x1440", "Цвет: 32-бит ARGB", "Фильтрация: Билинейная GPU", "Масштабирование: SCALE 2X"]
  },
  {
    id: "dustlight",
    title: "DUSTLIGHT VOLUMETRIC LIGHTING",
    category: "ВИЗУАЛ",
    badge: "ЛУЧЕВОЙ СВЕТ",
    version: "v1.4",
    author: "Dustlight Team, Community Edition",
    desc: "Объемный свет, динамический туман войны и реалистичные тени источников освещения (активно в профиле Community Edition).",
    cancels: "Плоское освещение без теней, создавая честные объемные лучи от ламп, костров и фонарей с динамическим туманом войны.",
    specs: ["Освещение: Raymarched Fog", "Туман войны: Динамический", "Движок: SDL2 Native", "Профиль: HD Visual"]
  },
  {
    id: "worldmap",
    title: "PANORAMIC EXPANDED WORLDMAP",
    category: "ВИЗУАЛ",
    badge: "ПАНОРАМА 16:9",
    version: "v3.0",
    author: "RPU Team, Mash, Lexx",
    desc: "Широкоформатная панорамная карта мира высокой четкости: полный обзор всей территории от Арройо до Сан-Франциско без черных полос и обрезки краев.",
    cancels: "Тесную квадратную рамку карты из 90-х годов на современных широкоформатных мониторах 16:9 и 21:9.",
    specs: ["Формат: 16:9 / 21:9", "Обзор: От края до края", "Интерфейс: Без обрезки", "Отображение: Высокая четкость"]
  }
];

class LauncherApp {
  constructor() {
    this.currentView = 'launch';
    this.currentFilter = 'ALL';
    this.activeProfile = 'gameplay';
    this.config = {
      resolution: '2560x1440',
      mode: 'fullscreen',
      scale: '2x',
      filtering: 'bilinear',
      musicVol: 80,
      sfxVol: 80
    };
    
    this.initElements();
    this.bindEvents();
    this.renderCatalog();
    this.loadInitialConfig();
    this.loadSavesInfo();
  }

  initElements() {
    // Navigation items
    this.navItems = document.querySelectorAll('.nav-item');
    this.views = document.querySelectorAll('.view-page');
    this.crtToggleBtn = document.getElementById('btn-toggle-crt');
    this.audioToggleBtn = document.getElementById('btn-toggle-sound');
    this.modalOverlay = document.getElementById('modal-overlay');

    // Dynamic catalog counter
    const navCatalog = document.getElementById('nav-catalog-label');
    if (navCatalog) {
      navCatalog.textContent = `КАТАЛОГ МОДОВ (${MODS_DATABASE.length})`;
    }
  }

  bindEvents() {
    // Tab switching
    this.navItems.forEach(item => {
      item.addEventListener('click', (e) => {
        const targetView = item.dataset.view;
        this.switchView(targetView);
        if (window.pipAudio) window.pipAudio.playRelayClick();
      });
    });

    // CRT Toggle
    if (this.crtToggleBtn) {
      this.crtToggleBtn.addEventListener('click', () => {
        const crt = document.getElementById('crt-overlay');
        if (crt) {
          const isHidden = crt.style.display === 'none';
          crt.style.display = isHidden ? 'block' : 'none';
          this.crtToggleBtn.textContent = isHidden ? 'CRT: ON' : 'CRT: OFF';
        }
        if (window.pipAudio) window.pipAudio.playSwitchSnap();
      });
    }

    // Audio Toggle
    if (this.audioToggleBtn) {
      this.audioToggleBtn.addEventListener('click', () => {
        if (window.pipAudio) {
          const enabled = window.pipAudio.toggleSound();
          this.audioToggleBtn.textContent = enabled ? 'SOUND: ON' : 'SOUND: OFF';
          if (enabled) window.pipAudio.playSwitchSnap();
        }
      });
    }

    // Launch buttons
    document.getElementById('btn-launch-gameplay')?.addEventListener('click', () => {
      this.launchProfile('gameplay');
    });

    document.getElementById('btn-launch-hd')?.addEventListener('click', () => {
      this.launchProfile('hd');
    });

    // Catalog Filter Pills
    document.querySelectorAll('.filter-pill:not(#btn-toggle-thumbs)').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.filter-pill:not(#btn-toggle-thumbs)').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentFilter = pill.dataset.filter;
        this.renderCatalog();
        if (window.pipAudio) window.pipAudio.playRelayClick();
      });
    });

    // Catalog View Toggle (Compact vs Thumbnails)
    this.setupCatalogViewToggle();

    // Settings Save Button
    document.getElementById('btn-save-settings')?.addEventListener('click', () => {
      this.saveCurrentSettings();
    });

    // Sliders input
    const sliderMusic = document.getElementById('slider-music');
    const labelMusic = document.getElementById('val-music');
    sliderMusic?.addEventListener('input', (e) => {
      labelMusic.textContent = `${e.target.value}%`;
    });

    const sliderSfx = document.getElementById('slider-sfx');
    const labelSfx = document.getElementById('val-sfx');
    sliderSfx?.addEventListener('input', (e) => {
      labelSfx.textContent = `${e.target.value}%`;
    });

    // Modal Close
    document.getElementById('modal-close')?.addEventListener('click', () => {
      this.closeModal();
    });

    this.modalOverlay?.addEventListener('click', (e) => {
      if (e.target === this.modalOverlay) this.closeModal();
    });

    // Saves actions
    document.getElementById('btn-backup-saves')?.addEventListener('click', () => {
      this.backupSaves();
    });
    document.getElementById('btn-open-saves-dir')?.addEventListener('click', () => {
      this.openSavesDir();
    });

    // Bug Report & Feedback
    document.getElementById('btn-submit-report')?.addEventListener('click', () => {
      this.submitBugReport();
    });
    document.getElementById('btn-copy-report')?.addEventListener('click', () => {
      this.copyReportToClipboard();
    });

    // Social Links
    document.querySelectorAll('.channel-card').forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const url = card.dataset.url;
        if (url) this.openExternal(url);
      });
    });
  }

  setupCatalogViewToggle() {
    const btn = document.getElementById('btn-toggle-thumbs');
    const container = document.getElementById('catalog-cards-container');
    if (!btn || !container) return;

    let isCompact = localStorage.getItem('nextgen_catalog_compact') === 'true';
    const updateUI = () => {
      container.classList.toggle('compact-view', isCompact);
      btn.textContent = isCompact ? '☰ БЕЗ КАРТИНОК (КОМПАКТ)' : '📷 СО СКРИНШОТАМИ';
      btn.classList.toggle('active', !isCompact);
    };

    updateUI();
    btn.addEventListener('click', () => {
      isCompact = !isCompact;
      localStorage.setItem('nextgen_catalog_compact', isCompact);
      updateUI();
      if (window.pipAudio) window.pipAudio.playRelayClick();
    });
  }

  switchView(viewId) {
    this.currentView = viewId;
    this.navItems.forEach(n => n.classList.toggle('active', n.dataset.view === viewId));
    this.views.forEach(v => v.classList.toggle('active', v.id === `view-${viewId}`));
  }

  renderCatalog() {
    const container = document.getElementById('catalog-cards-container');
    if (!container) return;

    container.innerHTML = '';
    const filtered = MODS_DATABASE.filter(m => {
      if (this.currentFilter === 'ALL') return true;
      return m.category.includes(this.currentFilter);
    });

    filtered.forEach(mod => {
      const card = document.createElement('div');
      card.className = 'mod-card';
      card.innerHTML = `
        <div class="mod-thumb-container">
          <img class="mod-thumb-img" src="assets/posters/${mod.id}.png" alt="${mod.title}" loading="lazy" onerror="this.src='assets/new_reno_hero.png'">
        </div>
        <div class="mod-info">
          <div class="mod-header-row">
            <span class="mod-cat-badge">${mod.category}</span>
            <span style="font-size: 10px; color: var(--phosphor-dim);">${mod.version}</span>
          </div>
          <div class="mod-card-title">${mod.title}</div>
          <div class="mod-card-desc">${mod.desc}</div>
          ${mod.cancels ? `
          <div class="mod-cancels-box">
            <span class="cancels-highlight">Отменяет:</span> ${mod.cancels}
          </div>` : ''}
          <div class="mod-card-footer">
            <span>Автор: ${mod.author.split(',')[0]}</span>
            <span style="color: var(--phosphor-primary);">Инфо ▹</span>
          </div>
        </div>
      `;

      card.addEventListener('click', () => {
        this.openModModal(mod);
      });

      container.appendChild(card);
    });
  }

  openModModal(mod) {
    const modal = document.getElementById('modal-overlay');
    if (!modal) return;

    document.getElementById('modal-title-text').textContent = mod.title;
    const poster = document.getElementById('modal-poster-view');
    if (poster) {
      poster.src = `assets/posters/${mod.id}.png`;
      poster.onerror = () => { poster.src = 'assets/new_reno_hero.png'; };
    }
    document.getElementById('modal-desc-view').textContent = mod.desc;
    const authorEl = document.getElementById('modal-author-view');
    if (authorEl) {
      authorEl.innerHTML = `<span style="color: var(--phosphor-dim);">Оригинальные авторы:</span> <strong style="color: var(--phosphor-primary);">${mod.author}</strong>`;
    }

    let cancelsEl = document.getElementById('modal-cancels-view');
    if (!cancelsEl) {
      cancelsEl = document.createElement('div');
      cancelsEl.id = 'modal-cancels-view';
      cancelsEl.className = 'modal-cancels-box';
      const descView = document.getElementById('modal-desc-view');
      if (descView && descView.parentNode) {
        descView.parentNode.insertBefore(cancelsEl, descView.nextSibling);
      }
    }
    if (cancelsEl) {
      if (mod.cancels) {
        cancelsEl.style.display = 'block';
        cancelsEl.innerHTML = `<span class="cancels-highlight">ЧТО ОТМЕНЯЕТ И ИСПРАВЛЯЕТ:</span><br>${mod.cancels}`;
      } else {
        cancelsEl.style.display = 'none';
      }
    }

    const specsList = document.getElementById('modal-specs-list');
    specsList.innerHTML = '';
    mod.specs.forEach(s => {
      const li = document.createElement('li');
      li.textContent = s;
      specsList.appendChild(li);
    });

    modal.classList.add('active');
    if (window.pipAudio) window.pipAudio.playRelayClick();
  }

  closeModal() {
    this.modalOverlay?.classList.remove('active');
    if (window.pipAudio) window.pipAudio.playSwitchSnap();
  }

  async launchProfile(profile) {
    if (window.pipAudio) window.pipAudio.playLaunchSiren();
    
    // Status animation
    const btn = profile === 'gameplay' 
      ? document.getElementById('btn-launch-gameplay') 
      : document.getElementById('btn-launch-hd');
      
    const originalText = btn.innerHTML;
    btn.innerHTML = `ЗАПУСК ДВИЖКА...`;
    btn.style.opacity = '0.7';

    try {
      if (window.pywebview && window.pywebview.api) {
        const result = await window.pywebview.api.launch_profile(profile);
        console.log("Launch result:", result);
      } else {
        console.log(`[Dev Simulation] Launched profile: ${profile}`);
      }
    } catch (e) {
      console.error("Launch error:", e);
      alert(`Ошибка запуска профиля ${profile}: ${e}`);
    } finally {
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.opacity = '1';
      }, 2500);
    }
  }

  async loadInitialConfig() {
    try {
      if (window.pywebview && window.pywebview.api) {
        const remoteCfg = await window.pywebview.api.read_config();
        if (remoteCfg) {
          this.config = remoteCfg;
          this.applyConfigToUI();
        }
      }
    } catch (e) {
      console.warn("Could not read remote config", e);
    }
  }

  applyConfigToUI() {
    const selRes = document.getElementById('select-res');
    if (selRes) selRes.value = this.config.resolution || '2560x1440';

    const selMode = document.getElementById('select-mode');
    if (selMode) selMode.value = this.config.mode || 'fullscreen';

    const selScale = document.getElementById('select-scale');
    if (selScale) selScale.value = this.config.scale || '2x';

    const selFilter = document.getElementById('select-filter');
    if (selFilter) selFilter.value = this.config.filtering || 'bilinear';

    const sMusic = document.getElementById('slider-music');
    if (sMusic) {
      sMusic.value = this.config.musicVol ?? 80;
      document.getElementById('val-music').textContent = `${sMusic.value}%`;
    }

    const sSfx = document.getElementById('slider-sfx');
    if (sSfx) {
      sSfx.value = this.config.sfxVol ?? 80;
      document.getElementById('val-sfx').textContent = `${sSfx.value}%`;
    }
  }

  async saveCurrentSettings() {
    this.config.resolution = document.getElementById('select-res').value;
    this.config.mode = document.getElementById('select-mode').value;
    this.config.scale = document.getElementById('select-scale').value;
    this.config.filtering = document.getElementById('select-filter').value;
    this.config.musicVol = parseInt(document.getElementById('slider-music').value, 10);
    this.config.sfxVol = parseInt(document.getElementById('slider-sfx').value, 10);

    const btn = document.getElementById('btn-save-settings');
    btn.textContent = 'СОХРАНЕНИЕ...';

    try {
      if (window.pywebview && window.pywebview.api) {
        await window.pywebview.api.save_config(this.config);
      }
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      btn.textContent = '✓ НАСТРОЙКИ ПРИМЕНЕНЫ';
      setTimeout(() => { btn.textContent = '💾 СОХРАНИТЬ И ПРИМЕНИТЬ НАСТРОЙКИ'; }, 1800);
    } catch (e) {
      alert(`Ошибка сохранения: ${e}`);
      btn.textContent = '💾 СОХРАНИТЬ И ПРИМЕНИТЬ НАСТРОЙКИ';
    }
  }

  async loadSavesInfo() {
    try {
      if (window.pywebview && window.pywebview.api) {
        const saves = await window.pywebview.api.get_saves_info();
        this.renderSavesGrid(saves);
      }
    } catch (e) {
      console.warn("Could not load saves info", e);
    }
  }

  renderSavesGrid(saves) {
    const container = document.getElementById('saves-slots-container');
    if (!container || !saves) return;

    container.innerHTML = '';
    saves.forEach(s => {
      const card = document.createElement('div');
      card.className = 'save-slot-card';
      card.innerHTML = `
        <div class="save-slot-header">
          <span>СЛОТ ${s.slot}</span>
          <span style="color: ${s.hasData ? 'var(--phosphor-bright)' : 'var(--border-muted)'};">${s.hasData ? '● ЗАНЯТ' : '○ ПУСТО'}</span>
        </div>
        <div class="save-slot-name">${s.title || 'Свободный слот'}</div>
        <div class="save-slot-meta">${s.timestamp || 'Нет данных'} | Размер: ${s.size || '0 КБ'}</div>
      `;
      container.appendChild(card);
    });
  }

  async backupSaves() {
    try {
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      if (window.pywebview && window.pywebview.api) {
        const res = await window.pywebview.api.backup_saves();
        alert(`Резервная копия сохранений успешно создана:\n${res}`);
      } else {
        alert("Бэкап сохранений сохранен в папку Backups (симуляция)");
      }
    } catch (e) {
      alert(`Ошибка бэкапа: ${e}`);
    }
  }

  openSavesDir() {
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.open_saves_folder();
    }
  }

  openExternal(url) {
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.open_external_url(url);
    } else {
      window.open(url, '_blank');
    }
  }

  buildReportText() {
    const type = document.getElementById('report-type').value;
    const profile = document.getElementById('report-profile').value;
    const msg = document.getElementById('report-text').value.trim();
    const attachDiag = document.getElementById('report-attach-diag').checked;

    let text = `🚨 [ОТЧЕТ FALLOUT 2 ULTIMATE 2026]\n`;
    text += `Тип: ${type}\n`;
    text += `Профиль: ${profile}\n`;
    text += `Сообщение: ${msg || 'Без пояснений'}\n`;

    if (attachDiag) {
      text += `\n--- ДИАГНОСТИКА СИСТЕМЫ ---\n`;
      text += `Экран: ${window.screen.width}x${window.screen.height} (DPI ${window.devicePixelRatio})\n`;
      text += `Конфиг: ${this.config.resolution} (${this.config.mode}, ${this.config.scale}, ${this.config.filtering})\n`;
      text += `Движок: WebView2 Hardware Accelerated\n`;
    }

    return text;
  }

  submitBugReport() {
    const text = this.buildReportText();
    const msg = document.getElementById('report-text').value.trim();
    if (!msg) {
      alert("Пожалуйста, напишите пару слов о найденном баге или предложении перед отправкой.");
      return;
    }

    if (window.pipAudio) window.pipAudio.playSwitchSnap();
    
    // We provide direct copy & external link jump
    navigator.clipboard.writeText(text);
    alert("Отчет сформирован и скопирован в буфер обмена!\nСейчас откроется Telegram-канал для связи с автором.");
    this.openExternal("https://t.me/fallout2_ultimate_wasteland");
  }

  copyReportToClipboard() {
    const text = this.buildReportText();
    navigator.clipboard.writeText(text);
    alert("Диагностический отчет скопирован в буфер обмена!\nВы можете вставить его в Telegram, Discord или комментарии Boosty.");
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new LauncherApp();
});
