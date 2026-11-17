# ☢️ FALLOUT 2: ULTIMATE MEGA REWORK 2026
### Master Installer, Dual-Profile Engine & Compatibility Pipeline

Единая автоматизированная инженерная система сборки, валидации и развертывания ультимативной модификации **Fallout 2: Ultimate Mega Rework** на базе проверенных релизов 2026 года.

---

## 🎯 Архитектурная концепция: Два профиля (Dual-Profile)

Из-за фундаментального различия в рантаймах движков сборка поддерживает установку в двух независимых режимах или параллельно:

| Режим | Движок / Стек | Ключевые компоненты | Назначение |
| :--- | :--- | :--- | :--- |
| **01: Ultimate Gameplay Edition** | `Fallout2.exe` + `sfall 4.5.1` (DirectX 9) | RPU 2.4.34 + EcCo 1.0.0 hf1 + THAT Patch v2 + MiniRework 2.0.4.3 + FO2Tweaks 14.7 + Lossless Music (WAV 44.1kHz) + Talking Heads 3.7 + THAT 0.4.0 | **Основное проверенное прохождение**: строгий баланс урона и брони EcCo, крафт, ловушки, яды, скрытность, Talking Heads диалоги и аудиофильский саундтрек без риска для скриптов |
| **02: Ultimate HD Edition** | `Fallout 2 Community Edition` (SDL2) | RPU 2.4.34 + Dustlight HD 0.9.4-beta + AI Upscale 2×/3× + Динамическое цветное освещение | **Визуальное погружение**: максимальная четкость спрайтов, мягкие тени и атмосферные темные ночи на нативном движке |

---

## ⚡ Обязательные инженерные параметры совместимости

1. **Fallout Mechanics MiniRework (`mods/F2MechanicsMiniRework.ini`)**:
   - `[MAIN] RegenMod=0 MedToolsMod=0 StealRebalance=0`
   - Полное отключение дублирующих механик лечения, медицинских инструментов и краж для бесконфликтной передачи баланса под управление EcCo.
2. **FO2Tweaks 14.7 (`mods/fo2tweaks.ini`)**:
   - Официальный подтвержденный релиз 14.7 (вместо незарелиженного черновика 15.0).
   - СТРОГО 5 калибровочных параметров, предписанных автором EcCo:
     `max_knockback=-1 healing_revision=0 molotov_fire=0 damage_mod=0 ap_rollover=0`
   - Исключение читерских упрощений (безлимитный вес, бесконечный багажник, оверлевел партии) и сохранение чистого QoL (подсветка контейнеров, авто-двери, авто-перезарядка).
3. **Lossless Music v8.1 (WAV 44.1 kHz)**:
   - Аудиофильский оригинальный саундтрек Марка Моргана без сжатия ACM.
   - Включение потокового декодирования DirectShow в `ddraw.ini`: `[Sound] AllowDShowSound=1` и привязка `music_path1=data\sound\music\`.
4. **Движок sfall (Ветка 4.5.x из RPU)**:
   - **Запрет на sfall 5**: sfall 5 ломает хуки EcCo 1.0.0. Используется стабильная версия, поставляемая с RPU 2.4.34. При распаковке модов встроен фильтр защиты `ddraw.dll`.
   - `AllowUnsafeScripting=2`, `SpeedInterfaceCounterAnims=2`, `ExtraMemory=1`.
5. **Russian CodePage & Fonts Fix (`ddraw.ini` + `fallout2.cfg`)**:
   - Автоматическая установка `Language=russian`, `CodePage=1251`, `UseCustomFont=1` в `ddraw.ini`.
   - Генерация валидного `fallout2.cfg` с путями `master.dat`, `critter.dat`, `sound.dat` (защита от краша при запуске).
6. **Патч Large Address Aware (LAA 4GB)**:
   - Автоматический PE-патч флага `0x0020` в заголовке `fallout2.exe` (защита от краша при 2GB лимите памяти).
7. **Строгий порядок загрузки (`mods/mods_order.txt`)**:
   - `rpu.dat -> npc_armor.dat -> rpu_russian.dat -> upu_russian_sound.dat -> talking_heads.dat -> talking_heads_audio.dat -> talking_heads_that_rpu_map_update_patch.dat -> rpu_y_ecco.dat -> F2MechanicsMiniRework.dat -> fo2tweaks.dat`.

---

## 🚫 Статус спорных и исключенных компонентов

* **Bunker 21 & Truck Locations**: исключен из основного проверенного профиля (перенесен в изолированное тестирование) из-за избытка халявной добычи, нарушающей экономику EcCo, и опасного требования автора удалять `scripts.lst`.
* **Companion Expansion 0.50.4**: оставлен строго для отдельного тестового профиля. Частичная совместимость с EcCo не гарантирует отсутствие багов напарников.
* **V.O.C.K. 1.15 & VaultVox 1.1**: опциональные голосовые модули. VOCK содержит английские реплики (требует оценки на слух в русской локализации), VaultVox использует синтез речи (TTS).
* **MIB88 MegaMod 2.47.8**: отдельная несогласованная тотальная сборка со старыми несовместимыми скриптами.
* **Inventory Filter 2.3.1**: требует sfall 5 (несовместим с EcCo) и ломает окно бартера SmartBarter.
* **Weapons Redone / Lootable Armor / Damage Formula Tweak**: разрушают математический баланс брони и оружия EcCo.

---

## 🚀 Как запустить инсталлятор

1. Запустите файл **`Run_Installer.bat`** (или `python installer_gui.py`).
2. Укажите папку с чистой Fallout 2 (Steam / GOG / 1.02d).
3. Выберите нужный пресет («Gameplay Ultimate», «HD Visual Dustlight» или «Dual Profile»).
4. Нажмите **«Собрать и установить сборку»**.
5. Запускайте игру через созданный **`launcher.py`**!
