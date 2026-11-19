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
    desc: "Грандиозная реставрация оригинального контента Fallout 2: Аббатство (The Abbey), Агентство охраны окружающей среды (EPA), Деревня Дикарей, Лагерь Работорговцев в Дыре и тайное Убежище 23.",
    specs: ["Новые локации: +6 крупных городов", "Квесты: +45 цепочек", "Персонажи: 80+ новых NPC", "Озвучка: восстановлены реплики"]
  },
  {
    id: "upu",
    title: "UNOFFICIAL PATCH UPDATED",
    category: "СТАБИЛЬНОСТЬ",
    badge: "1000+ ФИКСОВ",
    version: "v28.0",
    author: "killap, UPU Team",
    desc: "Фундамент стабильности: полное устранение критических багов оригинальной игры 1998 года, защита от софтлоков, утечек памяти и порчи файлов сохранений.",
    specs: ["Исправлено багов: 1200+", "Ошибок скриптов: 0", "Защита от вылетов: Активна", "Совместимость: 100%"]
  },
  {
    id: "sfall",
    title: "SFALL v4.4.8 ADVANCED ENGINE",
    category: "ДВИЖОК",
    badge: "DIRECTX 9 & 144HZ",
    version: "v4.4.8",
    author: "Timeslip, Crafty, Mr.Stalin",
    desc: "Аппаратный движок на DirectX 9 с поддержкой высокой частоты обновления (144-240 Гц), субпиксельного ввода мыши, колесика прокрутки и шейдеров.",
    specs: ["Рендерер: Direct3D 9", "Герцовка: 144/240 Гц", "Поддержка мыши: Raw Input", "Скриптовый расширитель: Активен"]
  },
  {
    id: "weapons",
    title: "COMBAT & WEAPON ANIMATIONS",
    category: "ВИЗУАЛ",
    badge: "ОРУЖИЕ",
    version: "v2.6",
    author: "RPU Animation Team, Continuum",
    desc: "Сотни новых кадров боевых спрайтов: охотничьи винтовки, мечи вакидзаси, тяжелый огнемет, дульные вспышки и плавные перезарядки.",
    specs: ["Оружие: 18 новых спрайтов", "Направления: 8 изометрических", "Синхронизация звука: 100%", "Тайминги AP: Родные"]
  },
  {
    id: "armor",
    title: "NPC ARMOR VISUAL EVOLUTION",
    category: "СПУТНИКИ",
    badge: "БРОНЯ НАПАРНИКОВ",
    version: "v3.1",
    author: "Continuum, Skynet, RPU Team",
    desc: "Напарники меняют спрайты при экипировке любой брони: Сулик, Вик, Мирия и Дэвин в кожаных куртках, боевой и силовой броне.",
    specs: ["Сулик: все уровни брони", "Вик: полный набор спрайтов", "Мирия/Дэвин: боевая броня", "Силовая броня: Поддерживается"]
  },
  {
    id: "marcus",
    title: "MARCUS ARMOR & DOGMEAT KEVLAR",
    category: "СПУТНИКИ",
    badge: "ТЯЖЕЛЫЙ ЭКИП",
    version: "v1.8",
    author: "RPU Team, Continuum",
    desc: "Тяжелая броня супермутантов для Маркуса и кевларовый бронежилет для Псины — напарники больше не гибнут в финальной фазе от очередей Анклава.",
    specs: ["Прирост живучести Маркуса: +40%", "Защита от плазмы: 50%", "Кевлар Псины: 35% DT", "Эндгейм-баланс: S-ранг"]
  },
  {
    id: "cassidy",
    title: "JOHN CASSIDY TALKING HEAD",
    category: "ОЗВУЧКА",
    badge: "3D-ГОЛОВА",
    version: "v2.0",
    author: "Joey Bracken, RPU Team",
    desc: "Живая анимированная 3D-голова бармена Джона Кэссиди из Города Убежища с профессиональной актерской озвучкой от Джоуи Брэкена.",
    specs: ["3D-модель: Пререндер", "Анимация губ: Синхронизирована", "Актер: Joey Bracken", "Качество звука: 44.1 кГц"]
  },
  {
    id: "music",
    title: "MARK MORGAN LOSSLESS REMASTER",
    category: "ЗВУК",
    badge: "ЗВУК 1 ГБ",
    version: "44.1 кГц",
    author: "Mark Morgan, BGforge Net",
    desc: "Отреставрированный студийный саундтрек: замена глухого моно 22 кГц 1998 года на кристально чистый стереозвук 44.1 кГц (31 трек).",
    specs: ["Треков: 31 композиция", "Формат: Lossless ACM Stereo", "Битрейт: 1411 кбит/с", "Объем: 1.0 ГБ"]
  },
  {
    id: "doors",
    title: "AUTODOORS & LOOT PROTECTION",
    category: "ГЕЙМПЛЕЙ",
    badge: "QOL ТВЕРДО",
    version: "v2.4",
    author: "BGforge Net, sfall team",
    desc: "Автоматическое открытие дверей перед бегущим героем и сохранение лута в кучке праха при дезинтеграции врага из энергооружия.",
    specs: ["Авто-двери: Мгновенно", "Потеря лута: 0%", "Инвентарь: Защищен", "Задержка: 0 мс"]
  },
  {
    id: "inventory",
    title: "ADVANCED INVENTORY & SORTING",
    category: "ГЕЙМПЛЕЙ",
    badge: "ИНВЕНТАРЬ",
    version: "v4.2",
    author: "sfall contributors",
    desc: "Прокрутка инвентаря колесиком мыши, быстрое перемещение предметов, авто-перезарядка оружия и расширенная таблица бартера на 4 слота.",
    specs: ["Колесо мыши: Нативное", "Быстрый лут: 1 клик", "Бартер: 4 слота", "Сортировка: Умная"]
  },
  {
    id: "miria",
    title: "MIRIA COMPANION REWORK",
    category: "СПУТНИКИ",
    badge: "КОМПАНЬОН",
    version: "v2.0",
    author: "RPU Team, killap",
    desc: "Полноценная боевая напарница: команда «Жди здесь», прокачка характеристик по уровням, экипировка брони и квест на цивилизованный развод.",
    specs: ["Команда ожидания: Добавлена", "Прокачка: Уровни 1-6", "Обмен вещами: Открыт", "Развод: Доступен"]
  },
  {
    id: "damage",
    title: "YAAM & GLOVZ BALLISTICS REWORK",
    category: "ГЕЙМПЛЕЙ",
    badge: "БАЛАНС УРОНА",
    version: "v1.5",
    author: "Glovz, YAAM, sfall team",
    desc: "Исправление сломанной формулы урона бронебойных пуль оригинала: AP-патроны теперь пробивают тяжелую броню солдат Анклава.",
    specs: ["Формула AP: Исправлена", "Пули JHP: Урон по мясу", "Очереди: Сбалансированы", "Экипировка врагов: Адаптивна"]
  },
  {
    id: "worldmap",
    title: "ENHANCED WORLDMAP & ENCOUNTERS",
    category: "ГЕЙМПЛЕЙ",
    badge: "КАРТА МИРА",
    version: "v3.0",
    author: "RPU Team, Mash",
    desc: "Широкоформатная карта мира и нормализация частоты случайных встреч на современных процессорах.",
    specs: ["Разрешение: 890x720+", "Частота встреч: Нормализована", "Багажник машины: Доступен", "Спецвстречи: 100% рабочие"]
  },
  {
    id: "graphics",
    title: "NATIVE 2560x1440 32-BIT ARGB",
    category: "ВИЗУАЛ",
    badge: "2K NATIVE",
    version: "v4.1.8",
    author: "Mash, sfall team",
    desc: "Аппаратное билинейное сглаживание текстур GPU, поддержка 32-битного цвета ARGB8888 и нативное разрешение 2K QHD без лесенок.",
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
    specs: ["Освещение: Raymarched Fog", "Туман войны: Динамический", "Движок: SDL2 Native", "Профиль: HD Visual"]
  },
  {
    id: "crafting",
    title: "WASTELAND CRAFT & PIPE WEAPONS",
    category: "ГЕЙМПЛЕЙ",
    badge: "САМОПАЛЫ И КРАФТ",
    version: "v2.0",
    author: "phobos2077, EcCo Team",
    desc: "Кустарный арсенал Пустоши: трубчатые самопалы (Pipe Rifle), самодельные гранаты, арбалеты, капканы и сборка ловушек. Распределены строго среди рейдеров и бродяг (без спавна в Арройо).",
    specs: ["Кустарное оружие: Pipe Rifle & Zip Gun", "Ловушки: Капканы и шипы EPA", "Распределение: Рейдеры и Дыра", "Храм и Арройо: 100% канон"]
  },
  {
    id: "hunting",
    title: "HUNTING, HARVESTING & FIELD SURVIVAL",
    category: "ГЕЙМПЛЕЙ",
    badge: "ОХОТА И РАЗДЕЛКА",
    version: "v2.0",
    author: "EcCo Team, RPU",
    desc: "Свежевание дичи ножом: шкуры гекконов, мясо, железы и хвосты скорпионов для противоядий. Жарка мяса на кострах в деревне без штрафов радиации.",
    specs: ["Разделка: Шкуры, мясо, хвосты", "Приготовление: Костры Арройо/Кламата", "Навык: Скиталец (Outdoorsman)", "Баланс: Стартовый капитал дикаря"]
  },
  {
    id: "highwayman",
    title: "HIGHWAYMAN OVERHAUL & TRUNK FIX",
    category: "ГЕЙМПЛЕЙ",
    badge: "АВТО ХАЙВЕЙМЕН",
    version: "v3.2",
    author: "phobos2077, sfall team",
    desc: "Полная защита багажника от пропажи вещей, оптимизированный расход ядерных микробатарей и возможность тюнинга нагнетателя у Смитти.",
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
    specs: ["Спам встреч: Устранен (Fix=1)", "Частота: Откалибрована (Rate=7)", "Диалог выбора: По навыку Скитальца", "Широкоформатная карта: Включена"]
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
    document.querySelectorAll('.filter-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentFilter = pill.dataset.filter;
        this.renderCatalog();
        if (window.pipAudio) window.pipAudio.playRelayClick();
      });
    });

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
          <img class="mod-thumb-img" src="assets/posters/${mod.id}.png" alt="${mod.title}" loading="lazy">
        </div>
        <div class="mod-info">
          <div class="mod-header-row">
            <span class="mod-cat-badge">${mod.category}</span>
            <span style="font-size: 10px; color: var(--phosphor-dim);">${mod.version}</span>
          </div>
          <div class="mod-card-title">${mod.title}</div>
          <div class="mod-card-desc">${mod.desc}</div>
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
    document.getElementById('modal-poster-view').src = `assets/posters/${mod.id}.png`;
    document.getElementById('modal-desc-view').textContent = mod.desc;

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
