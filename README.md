# ☢️ FALLOUT 2: ULTIMATE MEGA REWORK 2026
### Master Installer, Dual-Profile Engine & Compatibility Pipeline

Единая автоматизированная инженерная система сборки, валидации и развертывания ультимативной модификации **Fallout 2: Ultimate Mega Rework** на базе проверенных релизов 2026 года.

---

## 🎯 Архитектурная концепция: Два профиля (Dual-Profile)

Из-за фундаментального различия в рантаймах движков сборка поддерживает установку в двух независимых режимах или параллельно:

| Режим | Движок / Стек | Ключевые компоненты | Назначение |
| :--- | :--- | :--- | :--- |
| **01: Ultimate Gameplay Edition** | `Fallout2.exe` + `sfall 4.5.1` (DirectX 9) | RPU 2.4.34 + EcCo 1.0.0 hf1 + MiniRework 2.0.4.3 + FO2Tweaks 14.7 + Talking Heads 3.7 + THAT 0.4.0 + V.O.C.K. 1.14 + Bunker 21 | **Основное прохождение**: глубокий ребаланс урона, брони, крафт, ловушки, яды, скрытность, новые локации, квесты и озвучка |
| **02: Ultimate HD Edition** | `Fallout 2 Community Edition` (SDL2) | RPU 2.4.34 + Dustlight HD 0.9.0-beta + AI Upscale 2×/3× + Динамическое цветное освещение | **Визуальное погружение**: максимальная четкость спрайтов, мягкие тени и атмосферные темные ночи |

---

## ⚡ Обязательные инженерные параметры совместимости

1. **Fallout Mechanics MiniRework (`minirework.ini`)**:
   - `[MAIN] RegenMod=0 MedToolsMod=0 StealRebalance=1 FO2_ECCO=1`
   - Лечение и медицина отдаются EcCo, кражи согласованы, формула урона управляется EcCo.
2. **FO2Tweaks 14.7 (`fo2tweaks.ini`)**:
   - `max_knockback=-1 healing_revision=0 molotov_fire=0 damage_mod=0 ap_rollover=0 no_scope_penalty=0 improved_grenades=0 autodoors=1 ammobox=1 highlighting=1 auto_reload=1 modoc_brahmin=1 no_drop_items_on_death=1 carry_weight=0 trunk_space=0 unlimited_party=0 party_level_match=0 speedup=0 run_speed=0`
   - Полное устранение конфликтов с баллистикой и гранатами EcCo, исключение читерских упрощений (безлимитный вес/багажник), сохранение чистого QoL.
3. **Движок sfall (Ветка 4.5.x из RPU)**:
   - **Запрет на sfall 5**: sfall 5 ломает хуки EcCo 1.0.0. Используется стабильная версия, поставляемая с RPU 2.4.34.
   - `AllowUnsafeScripting=2`, `SpeedInterfaceCounterAnims=2`, `ExtraMemory=1`.
4. **Bunker 21 & Truck Locations 1.00**:
   - Безопасное слияние (merge) таблицы `scripts.lst` без затирания скриптов RPU.
5. **Патч Large Address Aware (LAA 4GB)**:
   - Автоматический PE-патч флага `0x0020` в заголовке `fallout2.exe` (защита от краша при 2GB лимите памяти).
6. **Строгий порядок загрузки (`mods_order.txt`)**:
   - `RPU -> Translations -> EcCo -> EcCo HF1 -> THAT Patch -> Talking Heads -> MiniRework -> FO2Tweaks -> Bunker 21 -> VOCK`.

---

## 🚫 Сознательно исключенные моды (Обоснование)

* **MIB88 MegaMod 2.47.8**: отдельная несогласованная тотальная сборка со старыми несовместимыми скриптами.
* **Inventory Filter 2.3.1**: требует sfall 5 (несовместим с EcCo) и ломает окно бартера SmartBarter.
* **Companion Expansion 0.50.x**: патч совместимости с EcCo есть только под старую версию 0.9.2, под 1.0.0 не адаптирован.
* **Lootable Armor / Weapons Redone / Damage Formula Tweak**: разрушают математический баланс брони и оружия EcCo.

---

## 🚀 Как запустить инсталлятор

1. Запустите файл **`Run_Installer.bat`** (или `python installer_gui.py`).
2. Укажите папку с чистой Fallout 2 (Steam / GOG / 1.02d).
3. Выберите нужный пресет («Gameplay Ultimate», «HD Visual Dustlight» или «Dual Profile»).
4. Нажмите **«Собрать и установить сборку»**.
5. Запускайте игру через созданный **`launcher.py`**!
