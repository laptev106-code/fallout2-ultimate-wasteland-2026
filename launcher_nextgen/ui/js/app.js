/**
 * Fallout 2 Ultimate Wasteland Edition 2026 // Pip-Boy 3000 Mk IV
 * Application Core Logic: Navigation, Mod Catalog, Settings, Saves, and Feedback/Bug-Reports.
 */

class LauncherApp {
  constructor() {
    this.currentView = 'launch';
    this.currentFilter = 'ALL';
    this.activeProfile = 'gameplay';
    this.savesProfile = 'gameplay';
    this.config = {
      resolution: '2560x1440',
      mode: 'borderless',
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

    // Play authentic CRT terminal boot sound and start hum
    if (window.pipAudio && window.pipAudio.enabled) {
      window.pipAudio.playLauncherBoot();
    }

    window.addEventListener('pywebviewready', () => {
      this.loadInitialConfig();
      this.runSmartHealthCheck(false);
    });
    setTimeout(() => this.loadInitialConfig(), 150);
    setTimeout(() => {
      this.loadInitialConfig();
      this.runSmartHealthCheck(false);
    }, 500);
    setTimeout(() => {
      this.loadInitialConfig();
      this.runSmartHealthCheck(false);
    }, 1200);
  }

  initElements() {
    // Navigation items
    this.navItems = document.querySelectorAll('.nav-item');
    this.views = document.querySelectorAll('.view-page');
    this.crtToggleBtn = document.getElementById('btn-toggle-crt');
    this.audioToggleBtn = document.getElementById('btn-toggle-sound');
    this.modalOverlay = document.getElementById('modal-overlay');

    // Dynamic catalog counter and badges
    const count = (typeof MODS_DATABASE !== 'undefined' && Array.isArray(MODS_DATABASE)) ? MODS_DATABASE.length : 28;
    const navCatalog = document.getElementById('nav-catalog-label');
    if (navCatalog) {
      navCatalog.textContent = `КАТАЛОГ МОДОВ (${count})`;
    }

    const badgeOverlay = document.getElementById('badge-gameplay-mods');
    if (badgeOverlay) {
      badgeOverlay.textContent = `МАКСИМАЛЬНОЕ КОЛИЧЕСТВО МОДОВ (${count} МОДУЛЕЙ)`;
    }

    const storyDesc = document.getElementById('gameplay-story-desc');
    if (storyDesc) {
      storyDesc.textContent = storyDesc.textContent.replace(/\b\d+\s*модификац/g, `${count} модификаций`);
    }

    const filterAll = document.querySelector('.filter-pill[data-filter="ALL"]');
    if (filterAll) {
      filterAll.textContent = `ВСЕ (${count} МОДОВ)`;
    }
  }

  bindEvents() {
    // Tab switching
    this.navItems.forEach(item => {
      item.addEventListener('click', () => {
        const targetView = item.dataset.view;
        this.switchView(targetView);
        if (window.pipAudio) window.pipAudio.playTabSwitch();
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
    document.querySelectorAll('.filter-pill:not(#btn-toggle-thumbs):not([data-profile])').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.filter-pill:not(#btn-toggle-thumbs):not([data-profile])').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentFilter = pill.dataset.filter;
        this.renderCatalog();
        if (window.pipAudio) window.pipAudio.playTabSwitch();
      });
    });

    // Catalog View Toggle (Compact vs Thumbnails)
    this.setupCatalogViewToggle();
    // Hover sounds disabled to prevent audio fatigue on mouse movement

    // Sound on select changes
    document.querySelectorAll('.form-select').forEach(el => {
      el.addEventListener('change', () => {
        if (window.pipAudio) window.pipAudio.playPipClick();
      });
    });

    // Sound on slider drag (debounced)
    let sliderDebounce = 0;
    document.querySelectorAll('.form-slider').forEach(el => {
      el.addEventListener('input', () => {
        const now = Date.now();
        if (now - sliderDebounce > 70) {
          sliderDebounce = now;
          if (window.pipAudio) window.pipAudio.playPipSelect();
        }
      });
    });


    // Settings Save Button & Auto-Save on Change
    document.getElementById('btn-save-settings')?.addEventListener('click', () => {
      this.saveCurrentSettings();
    });

    ['select-res', 'select-mode', 'select-scale', 'select-filter', 'select-reshade', 'select-fps'].forEach(id => {
      document.getElementById(id)?.addEventListener('change', () => {
        this.saveCurrentSettings(true);
      });
    });

    // Target highlight synchronization (Quick select on View 1 & Full select on View 3)
    const syncTargetHighlight = (val) => {
      const q = document.getElementById('quick-select-target-highlight');
      const s = document.getElementById('select-target-highlight');
      if (q) q.value = String(val);
      if (s) s.value = String(val);
      this.config.targetHighlight = parseInt(val, 10);
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      this.saveCurrentSettings(true);
    };
    document.getElementById('quick-select-target-highlight')?.addEventListener('change', (e) => syncTargetHighlight(e.target.value));
    document.getElementById('select-target-highlight')?.addEventListener('change', (e) => syncTargetHighlight(e.target.value));

    // Sync and Auto-Save for QoL toggles (Quick Bar and Settings page)
    const qolToggles = [
      { quick: 'quick-toggle-alwaysrun', full: 'toggle-alwaysrun', key: 'alwaysRun' },
      { quick: 'quick-toggle-autoreload', full: 'toggle-autoreload', key: 'autoReload' },
      { quick: 'quick-toggle-temple-tutorial', full: 'toggle-temple-tutorial', key: 'templeTutorial' },
      { quick: 'quick-toggle-hl-master', full: 'toggle-hl-master', key: 'hlMaster' },
      { quick: 'quick-toggle-hl-checklos', full: 'toggle-hl-checklos', key: 'hlCheckLOS' },
      { quick: 'quick-toggle-qol-clickoutside', full: 'toggle-qol-clickoutside', key: 'qolClickOutside' }
    ];

    qolToggles.forEach(({ quick, full, key }) => {
      const elQuick = document.getElementById(quick);
      const elFull = document.getElementById(full);

      const handleToggle = (checked) => {
        if (elQuick) elQuick.checked = checked;
        if (elFull) elFull.checked = checked;
        this.config[key] = checked;
        if (window.pipAudio) window.pipAudio.playSwitchSnap();
        this.saveCurrentSettings(true);
      };

      elQuick?.addEventListener('change', (e) => handleToggle(e.target.checked));
      elFull?.addEventListener('change', (e) => handleToggle(e.target.checked));
    });

    // Settings-only extra QoL toggles
    ['toggle-hl-skipempty', 'toggle-qol-closeontakeall'].forEach(id => {
      const key = (id === 'toggle-hl-skipempty') ? 'hlSkipEmpty' : 'qolCloseOnTakeAll';
      const el = document.getElementById(id);
      el?.addEventListener('change', (e) => {
        this.config[key] = e.target.checked;
        if (window.pipAudio) window.pipAudio.playSwitchSnap();
        this.saveCurrentSettings(true);
      });
    });

    // Highlight category toggles event listeners
    const hlToggleKeys = [
      { id: 'toggle-hl-items', key: 'hlItems' },
      { id: 'toggle-hl-containers', key: 'hlContainers' },
      { id: 'toggle-hl-empty-cont', key: 'hlEmptyContainers' },
      { id: 'toggle-hl-corpses', key: 'hlCorpses' },
      { id: 'toggle-hl-empty-corp', key: 'hlEmptyCorpses' },
      { id: 'toggle-hl-scenery', key: 'hlScenery' },
      { id: 'toggle-hl-doors', key: 'hlDoors' }
    ];
    hlToggleKeys.forEach(({ id, key }) => {
      const el = document.getElementById(id);
      el?.addEventListener('change', (e) => {
        this.config[key] = e.target.checked;
        if (window.pipAudio) window.pipAudio.playSwitchSnap();
        this.saveCurrentSettings(true);
      });
    });

    // Sliders input
    const sliderMusic = document.getElementById('slider-music');
    const labelMusic = document.getElementById('val-music');
    sliderMusic?.addEventListener('input', (e) => {
      labelMusic.textContent = `${e.target.value}%`;
      this.saveCurrentSettings(true);
    });

    const sliderSfx = document.getElementById('slider-sfx');
    const labelSfx = document.getElementById('val-sfx');
    sliderSfx?.addEventListener('input', (e) => {
      labelSfx.textContent = `${e.target.value}%`;
      this.saveCurrentSettings(true);
    });

    // Modal Close
    document.getElementById('modal-close')?.addEventListener('click', () => {
      this.closeModal();
    });

    this.modalOverlay?.addEventListener('click', (e) => {
      if (e.target === this.modalOverlay) this.closeModal();
    });

    // Saves profile switcher
    document.getElementById('btn-saves-profile-gameplay')?.addEventListener('click', () => {
      this.switchSavesProfile('gameplay');
    });
    document.getElementById('btn-saves-profile-hd')?.addEventListener('click', () => {
      this.switchSavesProfile('hd');
    });

    // Saves actions
    document.getElementById('btn-backup-saves')?.addEventListener('click', () => {
      this.backupSaves();
    });
    document.getElementById('btn-open-saves-dir')?.addEventListener('click', () => {
      this.openSavesDir();
    });
    document.getElementById('btn-restore-save')?.addEventListener('click', () => {
      this.restoreSelectedBackup();
    });

    // Bug Report & Feedback
    document.getElementById('btn-submit-report')?.addEventListener('click', () => {
      this.submitBugReport();
    });
    document.getElementById('btn-copy-report')?.addEventListener('click', () => {
      this.copyReportToClipboard();
    });
    document.getElementById('btn-run-integrity')?.addEventListener('click', () => {
      this.runIntegrityCheck();
    });

    // Smart Health & Compatibility
    document.getElementById('btn-run-smart-health')?.addEventListener('click', () => {
      if (window.pipAudio) window.pipAudio.playRelayClick();
      this.runSmartHealthCheck(true);
    });
    document.getElementById('btn-quick-doctor')?.addEventListener('click', () => {
      this.switchView('feedback');
      if (window.pipAudio) window.pipAudio.playTabSwitch();
      this.runSmartHealthCheck(true);
    });

    const isolateHandler = async () => {
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      if (window.pywebview && window.pywebview.api && window.pywebview.api.isolate_legacy_conflicts) {
        const res = await window.pywebview.api.isolate_legacy_conflicts();
        alert(res.message);
        await this.runSmartHealthCheck(true);
      }
    };
    document.getElementById('btn-quick-isolate')?.addEventListener('click', isolateHandler);
    document.getElementById('btn-isolate-conflicts')?.addEventListener('click', isolateHandler);

    // Social Links
    document.querySelectorAll('.channel-card').forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const url = card.dataset.url;
        if (url) this.openExternal(url);
      });
    });

    // Changelog View handlers
    document.getElementById('btn-open-changelog-file')?.addEventListener('click', async () => {
      if (window.pipAudio) window.pipAudio.playRelayClick();
      if (window.pywebview && window.pywebview.api && window.pywebview.api.open_changelog_file) {
        await window.pywebview.api.open_changelog_file();
      } else {
        alert("Файл CHANGELOG_2026.txt расположен в корневой папке игры.");
      }
    });

    document.getElementById('btn-copy-changelog')?.addEventListener('click', () => {
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      const container = document.getElementById('changelog-container');
      if (container && this.rawChangelog) {
        navigator.clipboard.writeText(this.rawChangelog).then(() => {
          const btn = document.getElementById('btn-copy-changelog');
          if (btn) {
            const orig = btn.textContent;
            btn.textContent = '✓ СКОПИРОВАНО!';
            setTimeout(() => { btn.textContent = orig; }, 1800);
          }
        });
      }
    });

    const searchInput = document.getElementById('changelog-search-input');
    searchInput?.addEventListener('input', (e) => {
      const term = e.target.value.trim();
      if (this.rawChangelog) {
        this.renderChangelogText(this.rawChangelog, term);
      }
    });

    document.getElementById('btn-reset-changelog-search')?.addEventListener('click', () => {
      if (window.pipAudio) window.pipAudio.playRelayClick();
      if (searchInput) searchInput.value = '';
      if (this.rawChangelog) {
        this.renderChangelogText(this.rawChangelog, '');
      }
    });
  }

  setupCatalogViewToggle() {
    const btn = document.getElementById('btn-toggle-thumbs');
    const container = document.getElementById('catalog-cards-container');
    if (!btn || !container) return;

    let isCompact = localStorage.getItem('nextgen_catalog_compact') === 'true';
    const updateUI = () => {
      container.classList.toggle('compact-view', isCompact);
      btn.textContent = isCompact ? '[≡] СПИСОК (ТЕКСТ)' : '[▤] ПОСТЕРЫ: ВКЛ';
      btn.title = isCompact ? 'Включить отображение постеров модификаций' : 'Переключить в компактный текстовый список';
      btn.classList.remove('active');
      btn.classList.toggle('view-active', !isCompact);
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
    this.views.forEach(v => v.classList.toggle('active', v.id === 'view-' + viewId));
    if (viewId === 'feedback') {
      this.runSmartHealthCheck(true);
    }
    if (viewId === 'changelog') {
      this.loadChangelog();
    }
  }

  async loadChangelog() {
    const container = document.getElementById('changelog-container');
    if (!container) return;

    if (this.rawChangelog) {
      this.renderChangelogText(this.rawChangelog);
      return;
    }

    container.textContent = 'Чтение журнала изменений...';
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.get_changelog_text) {
        const text = await window.pywebview.api.get_changelog_text();
        this.rawChangelog = text;
        this.renderChangelogText(text);
      } else {
        const resp = await fetch('../../CHANGELOG_2026.txt');
        if (resp.ok) {
          const text = await resp.text();
          this.rawChangelog = text;
          this.renderChangelogText(text);
        } else {
          container.textContent = 'Журнал изменений доступен в файле CHANGELOG_2026.txt в корне игры.';
        }
      }
    } catch (e) {
      container.textContent = 'Ошибка загрузки журнала: ' + e.message;
    }
  }

  renderChangelogText(text, filterTerm = '') {
    const container = document.getElementById('changelog-container');
    if (!container) return;
    if (!filterTerm) {
      container.textContent = text;
      return;
    }

    const term = filterTerm.toLowerCase();
    const blocks = text.split(/--------------------------------------------------------------------------------/);
    const matchedBlocks = blocks.slice(1).filter(b => b.toLowerCase().includes(term));

    if (matchedBlocks.length === 0) {
      container.textContent = `[ПОИСК ПО ЗАПРОСУ "${filterTerm}"]: Совпадений не найдено.\nНажмите "СБРОС" для возврата к полному списку.`;
    } else {
      container.textContent = `[НАЙДЕНО ${matchedBlocks.length} ИСПРАВЛЕНИЙ ПО ЗАПРОСУ "${filterTerm}"]:\n\n` + 
        matchedBlocks.join('\n--------------------------------------------------------------------------------\n');
    }
  }

  renderCatalog() {
    const container = document.getElementById('catalog-cards-container');
    if (!container) return;

    container.innerHTML = '';
    const database = (typeof MODS_DATABASE !== 'undefined') ? MODS_DATABASE : [];
    const filtered = database.filter(m => {
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
    // 1. Автоматическое сохранение выбранных настроек перед запуском
    await this.saveCurrentSettings(true);

    if (window.pipAudio) window.pipAudio.playGameLaunch();
    
    const btn = profile === 'gameplay' 
      ? document.getElementById('btn-launch-gameplay') 
      : document.getElementById('btn-launch-hd');
      
    const originalText = btn.innerHTML;
    btn.innerHTML = `ЗАПУСК ДВИЖКА...`;
    btn.style.opacity = '0.7';

    try {
      if (window.pywebview && window.pywebview.api) {
        const result = await window.pywebview.api.launch_profile(profile);
        if (result && result.status === 'error') {
          alert(`Внимание: ${result.message}`);
        }
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
    if (selRes) {
      if (this.config.nativeResolution) {
        const nat = this.config.nativeResolution;
        let exists = false;
        for (let opt of selRes.options) {
          if (opt.value === nat) {
            exists = true;
            opt.textContent = `${nat} (Нативное разрешение вашего монитора — Рекомендуется)`;
            break;
          }
        }
        if (!exists) {
          const opt = document.createElement('option');
          opt.value = nat;
          opt.textContent = `${nat} (Нативное разрешение вашего монитора — Рекомендуется)`;
          selRes.insertBefore(opt, selRes.firstChild);
        }
      }
      selRes.value = this.config.resolution || this.config.nativeResolution || '1920x1080';
    }

    const selMode = document.getElementById('select-mode');
    if (selMode) selMode.value = this.config.mode || 'borderless';

    const selScale = document.getElementById('select-scale');
    if (selScale) selScale.value = this.config.scale || '2x';

    const headerRes = document.getElementById('header-res-pill');
    if (headerRes && this.config.resolution) {
      headerRes.textContent = `ЭКРАН: ${this.config.resolution}`;
    }

    const selFilter = document.getElementById('select-filter');
    if (selFilter) selFilter.value = this.config.filtering || 'bilinear';

    const selReShade = document.getElementById('select-reshade');
    if (selReShade) selReShade.value = this.config.reshade || 'off';
    const selFps = document.getElementById('select-fps');
    if (selFps) selFps.value = this.config.fpsLock || '60';

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

    const chkReload = document.getElementById('toggle-autoreload');
    const quickReload = document.getElementById('quick-toggle-autoreload');
    const autoReloadVal = !!this.config.autoReload;
    if (chkReload) chkReload.checked = autoReloadVal;
    if (quickReload) quickReload.checked = autoReloadVal;

    const chkRun = document.getElementById('toggle-alwaysrun');
    const quickRun = document.getElementById('quick-toggle-alwaysrun');
    const alwaysRunVal = this.config.alwaysRun !== false;
    if (chkRun) chkRun.checked = alwaysRunVal;
    if (quickRun) quickRun.checked = alwaysRunVal;

    const chkTutorial = document.getElementById('toggle-temple-tutorial');
    const quickTutorial = document.getElementById('quick-toggle-temple-tutorial');
    const templeTutVal = this.config.templeTutorial !== false;
    if (chkTutorial) chkTutorial.checked = templeTutVal;
    if (quickTutorial) quickTutorial.checked = templeTutVal;

    // Target highlight (0 = Off, 1 = Under cursor, 2 = All targets in combat)
    const targetVal = this.config.targetHighlight !== undefined ? String(this.config.targetHighlight) : '2';
    const qTarget = document.getElementById('quick-select-target-highlight');
    const sTarget = document.getElementById('select-target-highlight');
    if (qTarget) qTarget.value = targetVal;
    if (sTarget) sTarget.value = targetVal;

    // Master loot highlight (Shift / Caps Lock)
    const hlMasterVal = this.config.hlMaster !== false;
    const chkHlMaster = document.getElementById('toggle-hl-master');
    const quickHlMaster = document.getElementById('quick-toggle-hl-master');
    if (chkHlMaster) chkHlMaster.checked = hlMasterVal;
    if (quickHlMaster) quickHlMaster.checked = hlMasterVal;

    // CheckLOS line-of-sight check
    const checkLOSVal = this.config.hlCheckLOS !== false;
    const chkLOS = document.getElementById('toggle-hl-checklos');
    const quickLOS = document.getElementById('quick-toggle-hl-checklos');
    if (chkLOS) chkLOS.checked = checkLOSVal;
    if (quickLOS) quickLOS.checked = checkLOSVal;

    // Click outside closes inventory
    const clickOutsideVal = this.config.qolClickOutside !== false;
    const chkClickOut = document.getElementById('toggle-qol-clickoutside');
    const quickClickOut = document.getElementById('quick-toggle-qol-clickoutside');
    if (chkClickOut) chkClickOut.checked = clickOutsideVal;
    if (quickClickOut) quickClickOut.checked = clickOutsideVal;

    // Skip empty containers & Close on Take All
    const chkSkipEmpty = document.getElementById('toggle-hl-skipempty');
    if (chkSkipEmpty) chkSkipEmpty.checked = this.config.hlSkipEmpty !== false;

    const chkTakeAll = document.getElementById('toggle-qol-closeontakeall');
    if (chkTakeAll) chkTakeAll.checked = this.config.qolCloseOnTakeAll !== false;

    // Highlighting category toggles
    const hlKeys = [
      { id: 'toggle-hl-items', key: 'hlItems' },
      { id: 'toggle-hl-containers', key: 'hlContainers' },
      { id: 'toggle-hl-empty-cont', key: 'hlEmptyContainers' },
      { id: 'toggle-hl-corpses', key: 'hlCorpses' },
      { id: 'toggle-hl-empty-corp', key: 'hlEmptyCorpses' },
      { id: 'toggle-hl-scenery', key: 'hlScenery' },
      { id: 'toggle-hl-doors', key: 'hlDoors' }
    ];
    hlKeys.forEach(({ id, key }) => {
      const el = document.getElementById(id);
      if (el) el.checked = this.config[key] !== false;
    });
  }

  async saveCurrentSettings(silent = false) {
    const selRes = document.getElementById('select-res');
    const selMode = document.getElementById('select-mode');
    const selScale = document.getElementById('select-scale');
    const selFilter = document.getElementById('select-filter');
    const selReShade = document.getElementById('select-reshade');
    const sMusic = document.getElementById('slider-music');
    const sSfx = document.getElementById('slider-sfx');

    if (selRes) this.config.resolution = selRes.value;
    if (selMode) this.config.mode = selMode.value;
    if (selScale) this.config.scale = selScale.value;
    if (selFilter) this.config.filtering = selFilter.value;
    if (selReShade) this.config.reshade = selReShade.value;
    const selFps = document.getElementById('select-fps');
    if (selFps) this.config.fpsLock = selFps.value;
    if (sMusic) this.config.musicVol = parseInt(sMusic.value, 10);
    if (sSfx) this.config.sfxVol = parseInt(sSfx.value, 10);

    const selTarget = document.getElementById('select-target-highlight') || document.getElementById('quick-select-target-highlight');
    if (selTarget) this.config.targetHighlight = parseInt(selTarget.value, 10);

    const chkReload = document.getElementById('toggle-autoreload') || document.getElementById('quick-toggle-autoreload');
    const chkRun = document.getElementById('toggle-alwaysrun') || document.getElementById('quick-toggle-alwaysrun');
    const chkTutorial = document.getElementById('toggle-temple-tutorial') || document.getElementById('quick-toggle-temple-tutorial');
    const chkHlMaster = document.getElementById('toggle-hl-master') || document.getElementById('quick-toggle-hl-master');
    const chkLOS = document.getElementById('toggle-hl-checklos') || document.getElementById('quick-toggle-hl-checklos');
    const chkClickOut = document.getElementById('toggle-qol-clickoutside') || document.getElementById('quick-toggle-qol-clickoutside');
    const chkSkipEmpty = document.getElementById('toggle-hl-skipempty');
    const chkTakeAll = document.getElementById('toggle-qol-closeontakeall');

    if (chkReload) this.config.autoReload = chkReload.checked;
    if (chkRun) this.config.alwaysRun = chkRun.checked;
    if (chkTutorial) this.config.templeTutorial = chkTutorial.checked;
    if (chkHlMaster) this.config.hlMaster = chkHlMaster.checked;
    if (chkLOS) this.config.hlCheckLOS = chkLOS.checked;
    if (chkClickOut) this.config.qolClickOutside = chkClickOut.checked;
    if (chkSkipEmpty) this.config.hlSkipEmpty = chkSkipEmpty.checked;
    if (chkTakeAll) this.config.qolCloseOnTakeAll = chkTakeAll.checked;

    const hlKeysSave = [
      { id: 'toggle-hl-items', key: 'hlItems' },
      { id: 'toggle-hl-containers', key: 'hlContainers' },
      { id: 'toggle-hl-empty-cont', key: 'hlEmptyContainers' },
      { id: 'toggle-hl-corpses', key: 'hlCorpses' },
      { id: 'toggle-hl-empty-corp', key: 'hlEmptyCorpses' },
      { id: 'toggle-hl-scenery', key: 'hlScenery' },
      { id: 'toggle-hl-doors', key: 'hlDoors' }
    ];
    hlKeysSave.forEach(({ id, key }) => {
      const el = document.getElementById(id);
      if (el) this.config[key] = el.checked;
    });

    const headerRes = document.getElementById('header-res-pill');
    if (headerRes && this.config.resolution) {
      headerRes.textContent = `ЭКРАН: ${this.config.resolution}`;
    }

    const btn = document.getElementById('btn-save-settings');
    if (!silent && btn) btn.textContent = 'СОХРАНЕНИЕ...';

    try {
      if (window.pywebview && window.pywebview.api) {
        const res = await window.pywebview.api.save_config(this.config);
        if (res && res.status === 'error' && !silent) {
          alert(`Предупреждение: ${res.message}`);
        }
      }
      if (!silent) {
        if (window.pipAudio) window.pipAudio.playSwitchSnap();
        if (btn) {
          btn.textContent = '✓ НАСТРОЙКИ ПРИМЕНЕНЫ';
          setTimeout(() => { btn.textContent = '💾 СОХРАНИТЬ И ПРИМЕНИТЬ НАСТРОЙКИ'; }, 1800);
        }
      }
    } catch (e) {
      if (!silent) {
        alert(`Ошибка сохранения: ${e}`);
        if (btn) btn.textContent = '💾 СОХРАНИТЬ И ПРИМЕНИТЬ НАСТРОЙКИ';
      }
    }
  }

  switchSavesProfile(profile) {
    this.savesProfile = profile;
    document.getElementById('btn-saves-profile-gameplay')?.classList.toggle('active', profile === 'gameplay');
    document.getElementById('btn-saves-profile-hd')?.classList.toggle('active', profile === 'hd');
    this.loadSavesInfo();
    if (window.pipAudio) window.pipAudio.playRelayClick();
  }

  async loadSavesInfo() {
    try {
      if (window.pywebview && window.pywebview.api) {
        const saves = await window.pywebview.api.get_saves_info(this.savesProfile);
        this.renderSavesGrid(saves);
      }
    } catch (e) {
      console.warn("Could not load saves info", e);
    }
    this.loadBackupsList();
  }

  renderSavesGrid(saves) {
    const container = document.getElementById('saves-slots-container');
    if (!container || !saves) return;

    container.innerHTML = '';
    saves.forEach(s => {
      const card = document.createElement('div');
      card.className = `save-slot-card ${s.hasData ? 'has-data' : 'is-empty'}`;
      card.style.background = s.hasData ? 'rgba(0, 255, 102, 0.04)' : 'rgba(0, 0, 0, 0.4)';
      card.style.border = s.hasData ? '1px solid rgba(0, 255, 102, 0.35)' : '1px solid var(--border-muted)';
      card.style.borderRadius = '4px';
      card.style.padding = '12px';
      card.style.transition = 'all 0.15s ease';

      card.innerHTML = `
        <div class="save-slot-header" style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span style="font-family: var(--font-mono); font-weight: bold; color: var(--phosphor-primary);">[СЛОТ ${s.slot}]</span>
          <span style="color: ${s.hasData ? 'var(--phosphor-bright)' : 'var(--phosphor-dim)'}; font-weight: bold; font-size: 11px;">${s.hasData ? '[● ЗАНЯТ]' : '[○ ПУСТО]'}</span>
        </div>
        <div class="save-slot-name" style="color: ${s.hasData ? '#ffffff' : 'var(--phosphor-dim)'}; font-size: 13px; font-weight: bold; margin: 4px 0; letter-spacing: 0.5px;">${s.title || '[Свободный слот]'}</div>
        <div class="save-slot-meta" style="font-size: 11px; color: var(--phosphor-dim);">${s.timestamp ? `Время: ${s.timestamp} | ${s.size}` : 'Данные отсутствуют'}</div>
      `;
      container.appendChild(card);
    });
  }

  async loadBackupsList() {
    const select = document.getElementById('select-backups-list');
    if (!select) return;
    try {
      if (window.pywebview && window.pywebview.api) {
        const backups = await window.pywebview.api.list_backups();
        if (backups && backups.length > 0) {
          select.innerHTML = '';
          backups.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b.fileName;
            opt.textContent = `${b.fileName} (${b.date}, ${b.size})`;
            select.appendChild(opt);
          });
        } else {
          select.innerHTML = '<option value="">(Архивы бэкапов пока не созданы)</option>';
        }
      }
    } catch (e) {
      console.warn("Could not load backups list", e);
    }
  }

  async backupSaves() {
    try {
      if (window.pipAudio) window.pipAudio.playSwitchSnap();
      if (window.pywebview && window.pywebview.api) {
        const res = await window.pywebview.api.backup_saves(this.savesProfile);
        if (res.status === 'success') {
          alert(`Резервная копия сохранений (${this.savesProfile.toUpperCase()}) создана:\nФайл: ${res.zipName}\nРазмер: ${res.sizeKb} КБ (${res.fileCount} файлов)`);
          this.loadBackupsList();
        } else {
          alert(`Ошибка бэкапа: ${res.message}`);
        }
      } else {
        alert("Бэкап сохранений сохранен в папку Backups (симуляция)");
      }
    } catch (e) {
      alert(`Ошибка бэкапа: ${e}`);
    }
  }

  async restoreSelectedBackup() {
    const select = document.getElementById('select-backups-list');
    const zipName = select ? select.value : '';
    if (!zipName) {
      alert("Выберите файл архива из списка для восстановления.");
      return;
    }
    const targetLabel = this.savesProfile === 'gameplay' ? 'GAMEPLAY ULTIMATE' : 'REWORK HD';
    if (!confirm(`Восстановить сохранения из архива "${zipName}" в профиль ${targetLabel}?\n\nВнимание: перед перезаписью будет автоматически сделан резервный снапшот текущих сохранений.`)) {
      return;
    }
    try {
      if (window.pywebview && window.pywebview.api) {
        const res = await window.pywebview.api.restore_save_backup(zipName, this.savesProfile);
        if (res.status === 'success') {
          alert(res.message);
          this.loadSavesInfo();
        } else {
          alert(`Ошибка восстановления: ${res.message}`);
        }
      }
    } catch (e) {
      alert(`Сбой восстановления: ${e}`);
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

  async getDiagnosticReportContent() {
    const type = document.getElementById('report-type').value;
    const profile = document.getElementById('report-profile').value;
    const msg = document.getElementById('report-text').value.trim();

    try {
      if (window.pywebview && window.pywebview.api) {
        const res = await window.pywebview.api.generate_diagnostic_report(msg, type, profile);
        if (res.status === 'success') {
          return {
            text: res.reportText,
            path: res.savedPath
          };
        }
      }
    } catch (e) {
      console.warn("Backend diagnostic report failed, falling back to local format", e);
    }

    // Client-side fallback
    let text = `🚨 [ОТЧЕТ FALLOUT 2 ULTIMATE 2026]\n`;
    text += `Тип: ${type}\n`;
    text += `Профиль: ${profile}\n`;
    text += `Сообщение: ${msg || 'Без пояснений'}\n`;
    text += `\n--- ДИАГНОСТИКА СИСТЕМЫ ---\n`;
    text += `Экран: ${window.screen.width}x${window.screen.height} (DPI ${window.devicePixelRatio})\n`;
    text += `Конфиг: ${this.config.resolution} (${this.config.mode}, ${this.config.scale}, ${this.config.filtering})\n`;
    text += `Движок: WebView2 Hardware Accelerated\n`;
    return { text, path: null };
  }

  async submitBugReport() {
    const msg = document.getElementById('report-text').value.trim();
    if (!msg) {
      alert("Пожалуйста, напишите пару слов о найденном баге или предложении перед отправкой.");
      return;
    }

    if (window.pipAudio) window.pipAudio.playSwitchSnap();
    
    const diag = await this.getDiagnosticReportContent();
    navigator.clipboard.writeText(diag.text);
    
    let alertMsg = "Диагностический отчет успешно сформирован и скопирован в буфер обмена!";
    if (diag.path) {
      alertMsg += `\nФайл отчета сохранен на диск: ${diag.path}`;
    }
    alertMsg += "\nСейчас откроется Telegram-канал для связи с автором.";
    alert(alertMsg);
    this.openExternal("https://t.me/fallout2_ultimate_wasteland");
  }

  async copyReportToClipboard() {
    const diag = await this.getDiagnosticReportContent();
    navigator.clipboard.writeText(diag.text);
    let alertMsg = "Диагностический отчет скопирован в буфер обмена!\nВы можете вставить его в Telegram, Discord или комментарии Boosty.";
    if (diag.path) {
      alertMsg += `\n\nТакже отчет сохранен в файл: ${diag.path}`;
    }
    alert(alertMsg);
  }

  async runSmartHealthCheck(renderDetails = false) {
    const quickBanner = document.getElementById('quick-health-banner');
    const quickIcon = document.getElementById('quick-health-icon');
    const quickTitle = document.getElementById('quick-health-title');
    const quickDesc = document.getElementById('quick-health-desc');
    const quickIsolateBtn = document.getElementById('btn-quick-isolate');

    const badge = document.getElementById('smart-health-badge');
    const isolateBtn = document.getElementById('btn-isolate-conflicts');
    const resultsContainer = document.getElementById('smart-health-results');

    if (!window.pywebview || !window.pywebview.api || !window.pywebview.api.check_smart_health) {
      if (quickDesc) quickDesc.textContent = 'Движок готов к сессии';
      return;
    }

    try {
      const res = await window.pywebview.api.check_smart_health();
      if (res.status === 'success') {
        // 1. Update quick banner on Launch screen
        if (quickBanner) {
          quickBanner.className = 'quick-health-bar ' + res.overall;
        }
        if (quickIcon) {
          quickIcon.textContent = res.overall === 'ok' ? '[✓]' : res.overall === 'warning' ? '[!]' : '[✗]';
        }
        if (quickTitle) {
          quickTitle.textContent = res.status_text;
        }
        if (quickDesc) {
          if (res.overall === 'ok') {
            quickDesc.textContent = 'Полный доступ UAC, оригинальные архивы DAT2 и чистые скрипты.';
          } else if (res.overall === 'warning') {
            quickDesc.textContent = res.has_foreign_mods 
              ? 'Обнаружены посторонние скрипты (' + res.foreign_count + ' шт.) от старых модов.' 
              : 'Обнаружены некритичные предупреждения окружения.';
          } else {
            quickDesc.textContent = 'Критические блокировки! Проверьте папку игры через диагностику.';
          }
        }
        if (quickIsolateBtn) {
          quickIsolateBtn.style.display = res.has_foreign_mods ? 'inline-block' : 'none';
        }

        // 2. Update Doctor section badge and isolate button
        if (badge) {
          badge.style.display = 'inline-block';
          badge.textContent = res.overall === 'ok' ? '100% СОВМЕСТИМО' : res.overall === 'warning' ? 'ВНИМАНИЕ' : 'БЛОКИРОВКА';
          badge.className = res.overall === 'ok' ? 'badge badge-canon' : 'badge badge-warning';
        }
        if (isolateBtn) {
          isolateBtn.style.display = res.has_foreign_mods ? 'inline-block' : 'none';
        }

        // 3. Render detailed audit cards if requested or in doctor view
        if (resultsContainer && (renderDetails || resultsContainer.style.display === 'block')) {
          resultsContainer.style.display = 'block';
          let html = '';
          res.checks.forEach(c => {
            const bClass = c.status === 'ok' ? 'badge-ok' : c.status === 'warning' ? 'badge-warn' : c.status === 'critical' ? 'badge-crit' : 'badge-ok';
            html += '<div class="health-audit-item ' + c.status + '">';
            html += '<div class="health-audit-header">';
            html += '<span class="health-audit-name">' + c.title + '</span>';
            html += '<span class="health-audit-badge ' + bClass + '">' + c.badge + '</span>';
            html += '</div>';
            html += '<div class="health-audit-msg">' + c.message + '</div>';
            html += '</div>';
          });
          resultsContainer.innerHTML = html;
        }
      }
    } catch (err) {
      console.warn('Smart health check failed:', err);
    }
  }

  async runIntegrityCheck() {
    const btn = document.getElementById('btn-run-integrity');
    const badge = document.getElementById('integrity-badge');
    const results = document.getElementById('integrity-results');
    if (!btn || !results) return;

    if (window.pipAudio) window.pipAudio.playSwitchSnap();

    btn.disabled = true;
    btn.textContent = '⏳ ВЫЧИСЛЕНИЕ ХЕШЕЙ SHA-256...';
    results.style.display = 'block';
    results.innerHTML = '<div style="color: var(--pip-green);">Чтение архивов и сверка контрольных сумм SHA-256...</div>';

    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api.verify_integrity) {
        const res = await window.pywebview.api.verify_integrity();
        if (res.status === 'success') {
          let html = `<div style="margin-bottom: 6px; font-weight: bold; color: ${res.overall === 'ok' ? '#00ff66' : '#ffb000'};">`;
          html += `ИТОГ: ${res.passed} из ${res.total} файлов валидны (Ошибок: ${res.failed}, Отсутствует: ${res.missing})</div>`;
          res.details.forEach(item => {
            const color = item.status === 'ok' ? '#00ff66' : item.status === 'missing' ? '#ffb000' : '#ff3333';
            const icon = item.status === 'ok' ? '✓' : item.status === 'missing' ? '?' : '✗';
            html += `<div style="color: ${color}; margin-top: 2px;">${icon} [${item.name}]: ${item.message}</div>`;
          });
          results.innerHTML = html;
          if (badge) {
            badge.style.display = 'inline-block';
            badge.textContent = res.overall === 'ok' ? '100% ВАЛИДЕН' : 'ЕСТЬ ПРЕДУПРЕЖДЕНИЯ';
            badge.className = res.overall === 'ok' ? 'badge badge-canon' : 'badge badge-warning';
          }
        } else {
          results.innerHTML = `<div style="color: #ff3333;">Ошибка: ${res.message}</div>`;
        }
      } else {
        results.innerHTML = '<div style="color: #00ff66;">✓ [ИНТЕГРАЦИЯ]: Запустите десктопный лаунчер для полного дискового аудита SHA-256.</div>';
      }
    } catch (e) {
      results.innerHTML = `<div style="color: #ff3333;">Исключение при проверке: ${e.message}</div>`;
    } finally {
      btn.disabled = false;
      btn.textContent = '🔍 ПЕРЕПРОВЕРИТЬ ЦЕЛОСТНОСТЬ ФАЙЛОВ';
      if (window.pipAudio) window.pipAudio.playRelayClick();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new LauncherApp();
});
