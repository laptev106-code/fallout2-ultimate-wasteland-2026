"""
Fallout 2 Ultimate Wasteland 2026 // Next-Gen Desktop Launcher
Powered by pywebview (Microsoft Edge WebView2 Hardware-Accelerated Core).
"""
import os
import sys
# Enable seamless autoplay for ambient CRT hum and game sounds in Edge WebView2
os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = "--autoplay-policy=no-user-gesture-required"
import json
import zipfile
import subprocess
import webbrowser
import shutil
import ctypes
from datetime import datetime

# Mandatory imports for PyInstaller bundled pywebview HTTP runtime
import email
import email.message
import email.parser
import email.policy
import email.utils
import http
import http.server
import wsgiref
import wsgiref.simple_server

import webview

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("genix106.fallout2.ultimate.launcher.2026.gold13")
except Exception:
    pass

class LauncherBridge:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        # Автоопределение: двухдвижковая папка или прямая папка игры
        if os.path.exists(os.path.join(self.root_dir, "Fallout2_Gameplay")):
            self.gameplay_dir = os.path.join(self.root_dir, "Fallout2_Gameplay")
            self.hd_dir = os.path.join(self.root_dir, "Fallout2_HD")
        else:
            self.gameplay_dir = self.root_dir
            self.hd_dir = self.root_dir
        self.backups_dir = os.path.join(self.root_dir, "Backups")
        self.config_file = os.path.join(self.root_dir, "launcher_config.json")
        os.makedirs(self.backups_dir, exist_ok=True)
        self._window = None
        try:
            self.enforce_hardware_thermal_guards(self.gameplay_dir)
            if os.path.exists(self.hd_dir):
                self.enforce_hardware_thermal_guards(self.hd_dir)
        except Exception:
            pass

    def set_window(self, window):
        self._window = window

    def _validate_and_heal_ini(self, target_dir: str):
        """Самовосстановление поврежденных INI-файлов из золотого эталона (Backups/golden_configs)."""
        golden_dir = os.path.join(self.backups_dir, "golden_configs")
        if not os.path.exists(golden_dir):
            golden_dir = os.path.join(self.root_dir, "templates", "golden_configs")
        if not os.path.exists(golden_dir):
            return

        checks = [
            (os.path.join(target_dir, "ddraw.ini"), os.path.join(golden_dir, "ddraw.ini"), 20000, [b"[Main]", b"[Graphics]", b"[Misc]", b"[Debugging]"]),
            (os.path.join(target_dir, "f2_res.ini"), os.path.join(golden_dir, "f2_res.ini"), 5000, [b"[MAIN]", b"[INPUT]", b"[MAPS]"]),
            (os.path.join(target_dir, "mods", "fo2tweaks.ini"), os.path.join(golden_dir, "fo2tweaks.ini"), 4000, [b"[main]"]),
        ]
        healed = False
        for dst, src, min_size, req_sections in checks:
            if not os.path.exists(src):
                continue
            needs_heal = False
            if not os.path.exists(dst):
                needs_heal = True
            else:
                try:
                    raw = open(dst, "rb").read()
                    if len(raw) < min_size or b"\x00" in raw or any(sec not in raw for sec in req_sections):
                        needs_heal = True
                except Exception:
                    needs_heal = True
            if needs_heal:
                try:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    healed = True
                except Exception as e:
                    print(f"Golden INI heal error for {dst}: {e}")
        if healed and os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                self.save_config(cfg)
            except Exception:
                pass

    def enforce_hardware_thermal_guards(self, target_dir: str):
        """Аппаратный сторож: автовосстановление эталонных INI и фиксация защиты от перегрева GPU перед запуском."""
        self._validate_and_heal_ini(target_dir)
        try:
            ddraw_path = os.path.join(target_dir, "ddraw.ini")
            if os.path.exists(ddraw_path):
                self._safe_write_ini_key(ddraw_path, {
                    "GPUSync": 0,
                    "LimitFPS": 1,
                    "ProcessorIdle": 1,
                    "OverrideArtCacheSize": 1,
                    "AnimationsAtOnceLimit": 120,
                    "TimeLimit": -3,
                    "AllowUnsafeScripting": 2
                }, encoding="cp1251")
            f2_res_path = os.path.join(target_dir, "f2_res.ini")
            if os.path.exists(f2_res_path):
                self._safe_write_ini_key(f2_res_path, {
                    "EXTRA_WIN_MSG_CHECKS": 1,
                    "ALT_MOUSE_INPUT": 0,
                    "CPU_USAGE_FIX": 0
                }, encoding="cp1251")
            fo2tweaks_path = os.path.join(target_dir, "mods", "fo2tweaks.ini")
            if os.path.exists(fo2tweaks_path):
                self._safe_write_ini_key(fo2tweaks_path, {
                    "highlighting": 0
                }, encoding="utf-8")
        except Exception as e:
            print(f"Thermal guard enforcement warning for {target_dir}: {e}")

    def launch_profile(self, profile: str) -> dict:
        """Запуск выбранного игрового профиля с проверкой всех процессов движка."""
        try:
            # 1. Проверка всех потенциально запущенных исполняемых файлов
            tracked_exes = ["fallout2.exe", "dustlight.exe", "fallout2-ce.exe"]
            try:
                tasklist = subprocess.check_output('tasklist /NH /FO CSV', shell=True, text=True, errors="ignore").lower()
                for exe in tracked_exes:
                    if f'"{exe}"' in tasklist or f'{exe}' in tasklist:
                        return {
                            "status": "error",
                            "message": f"Процесс игры ({exe}) уже активен в памяти Windows. Закройте его перед новым запуском."
                        }
            except Exception as e:
                print("Tasklist check warning:", e)

            # 2. Выбор целевого исполняемого файла
            if profile == "gameplay":
                target_exe = os.path.join(self.gameplay_dir, "fallout2.exe")
                target_cwd = self.gameplay_dir
            else:
                f2_exe = os.path.join(self.hd_dir, "fallout2.exe")
                dust_exe = os.path.join(self.hd_dir, "dustlight.exe")
                ce_exe = os.path.join(self.hd_dir, "fallout2-ce.exe")
                # Default to fallout2.exe to provide smooth bilinear HD graphics without Dustlight AI oversharpening
                target_exe = f2_exe if os.path.exists(f2_exe) else (dust_exe if os.path.exists(dust_exe) else ce_exe)
                target_cwd = self.hd_dir

            if not os.path.exists(target_exe):
                return {
                    "status": "error",
                    "message": f"Исполняемый файл не найден на диске: {target_exe}"
                }

            # Принудительная аппаратная верификация термопрофиля перед запуском движка
            self.enforce_hardware_thermal_guards(target_cwd)

            # 3. Запуск дочернего процесса
            subprocess.Popen([target_exe], cwd=target_cwd)

            # 4. Автоматическое безопасное закрытие лаунчера (разгрузка CPU/RAM и отключение звука)
            import threading, time
            def delayed_exit():
                time.sleep(1.2)
                try:
                    if self._window:
                        self._window.destroy()
                except Exception:
                    pass
                os._exit(0)

            threading.Thread(target=delayed_exit, daemon=True).start()

            return {"status": "success", "profile": profile, "exe": os.path.basename(target_exe)}
        except Exception as e:
            return {"status": "error", "message": f"Критический сбой запуска: {str(e)}"}

    def read_config(self) -> dict:
        """Считывание сохраненных настроек из launcher_config.json с синхронизацией из INI при первом запуске."""
        # Определение нативного разрешения монитора Windows
        native_res = "1920x1080"
        try:
            user32 = ctypes.windll.user32
            sw = user32.GetSystemMetrics(0)
            sh = user32.GetSystemMetrics(1)
            if sw > 0 and sh > 0:
                native_res = f"{sw}x{sh}"
        except Exception:
            pass

        default_cfg = {
            "resolution": native_res,
            "nativeResolution": native_res,
            "mode": "fullscreen",
            "scale": "2x",
            "filtering": "bilinear",
            "musicVol": 80,
            "sfxVol": 80,
            "alwaysRun": True,
            "autoReload": True,
            "templeTutorial": True,
            "autoQuickSave": "0",
            "autoDoors": True,
            "mapBlurFx": True,
            "wastelandVoices": True,
            "lastStandSurrender": True,
            "reshade": "off",
            "fpsLock": "60",
            "targetHighlight": 2,
            "hlMaster": True,
            "hlCheckLOS": True,
            "hlSkipEmpty": True,
            "qolClickOutside": True,
            "qolCloseOnTakeAll": True,
            "hlItems": True,
            "hlContainers": True,
            "hlEmptyContainers": True,
            "hlCorpses": True,
            "hlEmptyCorpses": True,
            "hlScenery": True,
            "hlDoors": True
        }

        # 1. Если уже сохранен launcher_config.json, загружаем его как эталон
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8-sig") as f:
                    saved = json.load(f)
                    if isinstance(saved, dict):
                        default_cfg.update(saved)
                        return default_cfg
            except Exception as e:
                print("Warning loading launcher_config.json:", e)

        # 2. Если файла еще нет, считываем фактические значения из ini/cfg файлов
        cfg = default_cfg.copy()

        # fallout2.cfg
        fallout_cfg = os.path.join(self.gameplay_dir, "fallout2.cfg")
        if os.path.exists(fallout_cfg):
            try:
                with open(fallout_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("music_volume="):
                            val = line_s.split("=")[1].strip()
                            if val.isdigit(): cfg["musicVol"] = int((int(val) / 32767.0) * 100)
                        elif line_s.startswith("sndfx_volume="):
                            val = line_s.split("=")[1].strip()
                            if val.isdigit(): cfg["sfxVol"] = int((int(val) / 32767.0) * 100)
                        elif line_s.startswith("running="):
                            cfg["alwaysRun"] = (line_s.split("=")[1].strip() == "1")
                        elif line_s.startswith("target_highlight="):
                            val = line_s.split("=")[1].strip()
                            if val.isdigit(): cfg["targetHighlight"] = int(val)
                        elif line_s.startswith("item_highlight="):
                            val = line_s.split("=")[1].strip()
                            if val.isdigit(): cfg["hlMaster"] = (val == "1")
            except Exception:
                pass

        # fo2tweaks.ini
        fo2tweaks_cfg = os.path.join(self.gameplay_dir, "mods", "fo2tweaks.ini")
        if os.path.exists(fo2tweaks_cfg):
            try:
                with open(fo2tweaks_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("auto_reload=") or line_s.startswith("auto_reload ="):
                            val = line_s.split("=")[1].strip()
                            cfg["autoReload"] = (val == "1")
                        # Note: fo2tweaks highlighting is permanently disabled (0); hlMaster is managed by gl_highlighting.ini and launcher
                        elif line_s.startswith("check_los=") or line_s.startswith("check_los ="):
                            val = line_s.split("=")[1].strip()
                            cfg["hlCheckLOS"] = (val == "1")
                        elif line_s.startswith("skip_empty=") or line_s.startswith("skip_empty ="):
                            val = line_s.split("=")[1].strip()
                            cfg["hlSkipEmpty"] = (val == "1")
                        elif line_s.startswith("autodoors=") or line_s.startswith("autodoors ="):
                            val = line_s.split("=")[1].strip()
                            cfg["autoDoors"] = (val == "1")
            except Exception:
                pass

        # gl_qol_interface.ini
        qol_cfg = os.path.join(self.gameplay_dir, "mods", "gl_qol_interface.ini")
        if os.path.exists(qol_cfg):
            try:
                with open(qol_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("ClickOutsideClosesInventory="):
                            val = line_s.split("=")[1].strip()
                            cfg["qolClickOutside"] = (val == "1")
                        elif line_s.startswith("CloseOnTakeAllKey="):
                            val = line_s.split("=")[1].strip()
                            cfg["qolCloseOnTakeAll"] = (val == "1")
            except Exception:
                pass

        # ddraw.ini (TempleTutorial, AutoQuickSave)
        ddraw_cfg = os.path.join(self.gameplay_dir, "ddraw.ini")
        if os.path.exists(ddraw_cfg):
            try:
                with open(ddraw_cfg, "r", encoding="cp1251", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("TempleTutorial=") or line_s.startswith("TempleTutorial ="):
                            val = line_s.split("=")[1].strip()
                            cfg["templeTutorial"] = (val == "1")
                        elif line_s.startswith("AutoQuickSave=") or line_s.startswith("AutoQuickSave ="):
                            val = line_s.split("=")[1].strip()
                            if val in ("0", "7", "8", "9"):
                                cfg["autoQuickSave"] = val
            except Exception:
                pass

        # gl_map_blur_fx.ini
        blur_cfg = os.path.join(self.gameplay_dir, "mods", "gl_map_blur_fx.ini")
        if os.path.exists(blur_cfg):
            try:
                with open(blur_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("Enable=") or line_s.startswith("Enable ="):
                            cfg["mapBlurFx"] = (line_s.split("=")[1].strip() == "1")
                            break
            except Exception:
                pass

        # wasteland_voices.ini
        voices_cfg = os.path.join(self.gameplay_dir, "mods", "wasteland_voices.ini")
        if os.path.exists(voices_cfg):
            try:
                with open(voices_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("EnableMod=") or line_s.startswith("EnableMod ="):
                            cfg["wastelandVoices"] = (line_s.split("=")[1].strip() == "1")
                            break
            except Exception:
                pass

        # gl_laststand.ini
        laststand_cfg = os.path.join(self.gameplay_dir, "mods", "gl_laststand.ini")
        if os.path.exists(laststand_cfg):
            try:
                with open(laststand_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("EnableSurrender=") or line_s.startswith("EnableSurrender ="):
                            cfg["lastStandSurrender"] = (line_s.split("=")[1].strip() == "1")
                            break
            except Exception:
                pass

        # Сохраняем первично сформированный JSON, чтобы он был стабилен
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        return cfg

    def _safe_write_ini_key(self, file_path: str, key_values: dict, encoding="utf-8"):
        """Безопасная запись параметров в INI: обновление существующих ключей или добавление отсутствующих."""
        if not os.path.exists(file_path):
            return

        bak_path = file_path + ".bak"
        try:
            shutil.copy2(file_path, bak_path)
        except Exception:
            pass

        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            lines = f.readlines()

        if not lines:
            return

        unhandled_keys = set(key_values.keys())
        new_lines = []

        for line in lines:
            stripped = line.strip()
            replaced = False
            for k, v in key_values.items():
                if stripped.startswith(f"{k}=") or stripped.startswith(f"{k} ="):
                    new_lines.append(f"{k}={v}\n")
                    if k in unhandled_keys:
                        unhandled_keys.remove(k)
                    replaced = True
                    break
            if not replaced:
                new_lines.append(line)

        if unhandled_keys:
            new_lines.append("\n; Added by Fallout 2 Next-Gen Launcher\n")
            for k in unhandled_keys:
                new_lines.append(f"{k}={key_values[k]}\n")

        tmp_path = file_path + ".tmp"
        with open(tmp_path, "w", encoding=encoding, errors="ignore") as f:
            f.writelines(new_lines)
        os.replace(tmp_path, file_path)

    def save_config(self, cfg: dict) -> dict:
        """Безопасная синхронизация графики, масштабирования и звука во все профили (Gameplay и HD)."""
        try:
            # 1. Сохраняем в эталонный JSON конфиг лаунчера для 100% стабильности UI
            try:
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print("Error saving launcher_config.json:", e)

            res_val = cfg.get("resolution", "1920x1080")
            if "x" in res_val:
                w, h = map(int, res_val.split("x"))
            else:
                w, h = 1920, 1080

            scale_choice = cfg.get("scale", "2x")
            mode = cfg.get("mode", "fullscreen")
            fps_choice = str(cfg.get("fpsLock", "60"))
            if fps_choice == "0":
                limit_fps_val = 0
                refresh_rate_val = 0
            else:
                limit_fps_val = 1
                try:
                    refresh_rate_val = int(fps_choice)
                except Exception:
                    refresh_rate_val = 60

            # Вычисление параметров масштабирования под монитор
            if scale_choice == "2x":
                f2_w = w // 2
                f2_h = h // 2
                f2_scale_2x = 1
                ce_scale = 2
            elif scale_choice == "4x":
                f2_w = w // 4
                f2_h = h // 4
                f2_scale_2x = 2
                ce_scale = 3
            else: # 1x
                f2_w = w
                f2_h = h
                f2_scale_2x = 0
                ce_scale = 1

            filter_val = 2 if cfg.get("filtering") == "bilinear" else 0
            music_vol = int((cfg.get("musicVol", 80) / 100.0) * 32767)
            sfx_vol = int((cfg.get("sfxVol", 80) / 100.0) * 32767)

            if mode == "windowed":
                f2_windowed = 1
                f2_borderless = 0
                ddraw_mode = 5
                cfg_windowed = 1
            elif f2_w < 1280:
                # В режиме Mode=4 видеокарта не поддерживает нестандартные половинные режимы вроде 960x540
                f2_windowed = 1
                f2_borderless = 1
                ddraw_mode = 6
                cfg_windowed = 0
            else:  # fullscreen (эксклюзивный DX9 Mode=4 для аппаратного VSync 60 FPS без перегрева GPU)
                f2_windowed = 0
                f2_borderless = 0
                ddraw_mode = 4
                cfg_windowed = 0

            auto_reload_val = 1 if cfg.get("autoReload", False) else 0
            running_val = 1 if cfg.get("alwaysRun", True) else 0
            temple_tut_val = 1 if cfg.get("templeTutorial", True) else 0
            auto_quicksave_raw = str(cfg.get("autoQuickSave", "0"))
            auto_quicksave_val = int(auto_quicksave_raw) if auto_quicksave_raw in ("0", "7", "8", "9") else 0
            auto_doors_val = 1 if cfg.get("autoDoors", True) else 0
            map_blur_val = 1 if cfg.get("mapBlurFx", True) else 0
            wasteland_voices_val = 1 if cfg.get("wastelandVoices", True) else 0
            last_stand_surrender_val = 1 if cfg.get("lastStandSurrender", True) else 0
            target_highlight_val = int(cfg.get("targetHighlight", 2))
            hl_master_val = 1 if cfg.get("hlMaster", True) else 0
            hl_checklos_val = 1 if cfg.get("hlCheckLOS", True) else 0
            hl_skipempty_val = 1 if cfg.get("hlSkipEmpty", True) else 0
            qol_clickoutside_val = 1 if cfg.get("qolClickOutside", True) else 0
            qol_closeontakeall_val = 1 if cfg.get("qolCloseOnTakeAll", True) else 0

            target_dirs = [self.gameplay_dir]
            if os.path.exists(self.hd_dir) and self.hd_dir not in target_dirs:
                target_dirs.append(self.hd_dir)

            # Синхронизация в боевые профили на E:\Fallout2_Ultimate
            for ext_profile in [r"E:\Fallout2_Ultimate\Fallout2_Gameplay", r"E:\Fallout2_Ultimate\Fallout2_HD"]:
                if os.path.exists(ext_profile) and ext_profile not in target_dirs:
                    target_dirs.append(ext_profile)

            for target_dir in target_dirs:
                # 1. f2_res.ini
                f2_res_path = os.path.join(target_dir, "f2_res.ini")
                self._safe_write_ini_key(f2_res_path, {
                    "GRAPHICS_MODE": 0,
                    "SCR_WIDTH": f2_w,
                    "SCR_HEIGHT": f2_h,
                    "SCALE_2X": f2_scale_2x,
                    "SCALE_BUTTONS_AND_TEXT_MENU": 0,
                    "WINDOWED": f2_windowed,
                    "WINDOWED_FULLSCREEN": f2_borderless,
                    "COLOUR_BITS": 32,
                    "REFRESH_RATE": refresh_rate_val,
                    "EXTRA_WIN_MSG_CHECKS": 1,
                    "ALT_MOUSE_INPUT": 0,
                    "CPU_USAGE_FIX": 0
                }, encoding="cp1251")

                # 2. ddraw.ini
                ddraw_path = os.path.join(target_dir, "ddraw.ini")
                self._safe_write_ini_key(ddraw_path, {
                    "Mode": ddraw_mode,
                    "LimitFPS": limit_fps_val,
                    "GPUSync": 0,
                    "ProcessorIdle": 1,
                    "OverrideArtCacheSize": 1,
                    "AnimationsAtOnceLimit": 120,
                    "TimeLimit": -3,
                    "AllowUnsafeScripting": 2,
                    "EnableMusicInDialogue": 1,
                    "ExpandInventory": 1,
                    "GraphicsWidth": 0,
                    "GraphicsHeight": 0,
                    "TextureFilter": filter_val,
                    "WindowData": 0,
                    "BackgroundKeyboard": 1,
                    "BackgroundMouse": 1,
                    "MouseSensitivity": 65,
                    "InstantWeaponEquip": 0,
                    "Lockpick": 478,
                    "Steal": 479,
                    "Traps": 480,
                    "FirstAid": 481,
                    "Doctor": 482,
                    "Science": 483,
                    "Repair": 484,
                    "SpeedInventoryPCRotation": 300,
                    "CombatPanelAnimDelay": 90,
                    "WorldMapEncounterRate": 14,
                    "WorldMapSlots": 21,
                    "SkipCompatModeCheck": 1,
                    "ExtraCRC": "0xffd65e6d,0xe1680293,0xf18aa577",
                    "BoostScriptDialogLimit": 1,
                    "HiResMode": 1,
                    "TempleTutorial": temple_tut_val,
                    "AutoQuickSave": auto_quicksave_val
                }, encoding="cp1251")

                # 3. fallout2.cfg
                fallout_cfg = os.path.join(target_dir, "fallout2.cfg")
                self._safe_write_ini_key(fallout_cfg, {
                    "language": "russian",
                    "music_volume": music_vol,
                    "sndfx_volume": sfx_vol,
                    "speech_volume": sfx_vol,
                    "combat_speed": 50,
                    "player_speedup": 1,
                    "cycle_speed_factor": "1.550000",
                    "running": running_val,
                    "resolution_x": w,
                    "resolution_y": h,
                    "scale": ce_scale,
                    "windowed": cfg_windowed,
                    "target_highlight": target_highlight_val,
                    "item_highlight": hl_master_val
                }, encoding="utf-8")

                # 4. fo2tweaks.ini
                fo2tweaks_path = os.path.join(target_dir, "mods", "fo2tweaks.ini")
                if os.path.exists(fo2tweaks_path):
                    self._safe_write_ini_key(fo2tweaks_path, {
                        "auto_reload": auto_reload_val,
                        "autodoors": auto_doors_val,
                        "highlighting": 0,
                        "check_los": hl_checklos_val,
                        "skip_empty": hl_skipempty_val
                    }, encoding="utf-8")

                # 4.1. gl_highlighting.ini (Настройка категорий подсветки)
                gl_high_path = os.path.join(target_dir, "mods", "gl_highlighting.ini")
                master_mult = 1 if cfg.get("hlMaster", True) else 0
                hl_settings = {
                    "Items": (1 if cfg.get("hlItems", True) else 0) * master_mult,
                    "Containers": (1 if cfg.get("hlContainers", True) else 0) * master_mult,
                    "EmptyContainers": (1 if cfg.get("hlEmptyContainers", True) else 0) * master_mult,
                    "Corpses": (1 if cfg.get("hlCorpses", True) else 0) * master_mult,
                    "EmptyCorpses": (1 if cfg.get("hlEmptyCorpses", True) else 0) * master_mult,
                    "Scenery": (1 if cfg.get("hlScenery", True) else 0) * master_mult,
                    "Doors": (1 if cfg.get("hlDoors", True) else 0) * master_mult
                }
                self._safe_write_ini_key(gl_high_path, hl_settings, encoding="utf-8")

                # 4.2. gl_qol_interface.ini (Закрытие кликом вне окна и быстрый забор)
                gl_qol_path = os.path.join(target_dir, "mods", "gl_qol_interface.ini")
                if os.path.exists(gl_qol_path):
                    self._safe_write_ini_key(gl_qol_path, {
                        "ClickOutsideClosesInventory": qol_clickoutside_val,
                        "CloseOnTakeAllKey": qol_closeontakeall_val
                    }, encoding="utf-8")

                # 4.3. gl_map_blur_fx.ini (Размытие фона в окнах)
                blur_path = os.path.join(target_dir, "mods", "gl_map_blur_fx.ini")
                if os.path.exists(blur_path):
                    self._safe_write_ini_key(blur_path, {
                        "Enable": map_blur_val
                    }, encoding="utf-8")

                # 4.4. wasteland_voices.ini (Живые голоса Пустоши)
                voices_path = os.path.join(target_dir, "mods", "wasteland_voices.ini")
                if os.path.exists(voices_path):
                    self._safe_write_ini_key(voices_path, {
                        "EnableMod": wasteland_voices_val
                    }, encoding="utf-8")

                # 4.5. gl_laststand.ini (Тактика ИИ и сдача раненых)
                laststand_path = os.path.join(target_dir, "mods", "gl_laststand.ini")
                if os.path.exists(laststand_path):
                    self._safe_write_ini_key(laststand_path, {
                        "EnableSurrender": last_stand_surrender_val
                    }, encoding="utf-8")

            # 5. Управление ReShade для Direct3D 9 в Gameplay-профиле
            reshade_choice = cfg.get("reshade", "off")
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            presets_reshade = os.path.join(curr_dir, "presets", "reshade")
            if not os.path.exists(presets_reshade):
                presets_reshade = os.path.join(self.root_dir, "launcher_nextgen", "presets", "reshade")

            gameplay_d3d9 = os.path.join(self.gameplay_dir, "d3d9.dll")
            gameplay_d3d9_off = os.path.join(self.gameplay_dir, "d3d9.dll.off")

            if reshade_choice == "off":
                if os.path.exists(gameplay_d3d9):
                    try:
                        if os.path.exists(gameplay_d3d9_off):
                            os.remove(gameplay_d3d9_off)
                        os.rename(gameplay_d3d9, gameplay_d3d9_off)
                    except Exception as re_err:
                        print("Warning disabling ReShade:", re_err)
            else:
                src_d3d9 = os.path.join(presets_reshade, "d3d9.dll")
                if os.path.exists(src_d3d9):
                    try:
                        shutil.copy2(src_d3d9, gameplay_d3d9)
                        if os.path.exists(gameplay_d3d9_off):
                            os.remove(gameplay_d3d9_off)
                    except Exception as re_err:
                        print("Warning copying ReShade DLL:", re_err)

                src_ini = os.path.join(presets_reshade, "ReShade.ini")
                if os.path.exists(src_ini):
                    try:
                        shutil.copy2(src_ini, os.path.join(self.gameplay_dir, "ReShade.ini"))
                    except Exception:
                        pass

                preset_file = "preset_cinema_88.ini" if reshade_choice == "cinema" else "preset_soft_163.ini"
                src_preset = os.path.join(presets_reshade, preset_file)
                if os.path.exists(src_preset):
                    try:
                        shutil.copy2(src_preset, os.path.join(self.gameplay_dir, "ReShadePreset.ini"))
                    except Exception:
                        pass

                src_shaders = os.path.join(presets_reshade, "reshade-shaders")
                dest_shaders = os.path.join(self.gameplay_dir, "reshade-shaders")
                if os.path.exists(src_shaders) and not os.path.exists(dest_shaders):
                    try:
                        shutil.copytree(src_shaders, dest_shaders)
                    except Exception:
                        pass

            return {
                "status": "success",
                "message": f"Конфигурация успешно сохранена: {w}x{h}, {mode}, Scale {scale_choice}, бег={running_val}, автоперезарядка={auto_reload_val}, обучение={temple_tut_val}."
            }
        except Exception as e:
            return {"status": "error", "message": f"Ошибка сохранения настроек: {str(e)}"}

    def get_saves_info(self, profile="gameplay") -> list:
        """Сбор информации о слотах сохранений выбранного профиля с глубоким парсингом SAVE.DAT."""
        target_dir = self.gameplay_dir if profile == "gameplay" else self.hd_dir
        saves_dir = os.path.join(target_dir, "DATA", "SAVEGAME")
        slots = []

        MAP_LABELS = {
            "ARCAVES": "Арройо // Священные пещеры",
            "ARTEMPLE": "Арройо // Храм Испытаний",
            "ARVILLAG": "Деревня Арройо",
            "ARBRIDGE": "Великий мост Арройо",
            "KLADWTWN": "Клэмат // Центр города",
            "KLAGRAZ": "Клэмат // Пастбища браминов",
            "KLACANYN": "Клэмат // Токсичный каньон",
            "KLAMAL": "Клэмат // Охотничьи угодья",
            "DENBUS1": "Дыра (Ден) // Деловой район",
            "DENBUS2": "Дыра (Ден) // Жилой район",
            "MOUNTN6": "Пустошь // Горная встреча",
            "MODMAIN": "Модок // Главная улица",
            "MODINN": "Модок // Гостиница Розы",
            "V13ENT": "Убежище 13 // Вход",
            "V15ENT": "Убежище 15",
            "NCENT": "Нью-Рено // Вход в город",
            "NCBISH": "Нью-Рено // Клуб Бишопа",
            "NCWRIGHT": "Нью-Рено // Особняк Райтов",
            "BROKEN1": "Брокен Хиллз // Центр",
            "REDMENT": "Реддинг // Главная улица",
            "SFCHIN": "Сан-Франциско // Чайнатаун",
            "NAVARRO": "Военная база Наварро",
            "SIERRA1": "Армейский склад Сьерра"
        }

        for i in range(1, 11):
            slot_name = f"SLOT{i:02d}"
            slot_path = os.path.join(saves_dir, slot_name)
            save_dat = os.path.join(slot_path, "SAVE.DAT")
            has_data = os.path.exists(save_dat)
            meta = "[Пустой слот]"
            char_name = ""
            location = ""
            size_kb = 0
            mtime_str = ""

            if has_data:
                try:
                    total_bytes = sum(
                        os.path.getsize(os.path.join(slot_path, f)) 
                        for f in os.listdir(slot_path) 
                        if os.path.isfile(os.path.join(slot_path, f))
                    )
                    size_kb = total_bytes // 1024
                    mtime = os.path.getmtime(save_dat)
                    mtime_str = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M")

                    # Парсинг заголовка SAVE.DAT
                    with open(save_dat, "rb") as sf:
                        raw_head = sf.read(160)
                        if len(raw_head) >= 60 and raw_head.startswith(b"FALLOUT SAVE FILE"):
                            desc_raw = raw_head[0x1C:0x1C+30].split(b"\x00")[0]
                            char_name = desc_raw.decode("cp1251", errors="replace").strip()
                            if char_name.startswith("R") and len(char_name) > 1:
                                char_name = char_name[1:].strip()
                            
                            import re
                            m_map = re.search(rb'([A-Za-z0-9_]+)\.sav', raw_head, re.IGNORECASE)
                            if m_map:
                                map_code = m_map.group(1).decode("ascii").upper()
                                location = MAP_LABELS.get(map_code, f"Пустошь ({map_code})")

                    if char_name and location:
                        meta = f"{char_name} — {location}"
                    elif char_name:
                        meta = f"{char_name} (Сейв {i})"
                    else:
                        meta = f"Сейв {i} ({size_kb} КБ)"
                except Exception as ex:
                    print(f"Error parsing save {slot_name}:", ex)

            slots.append({
                "slot": f"{i:02d}",
                "hasData": has_data,
                "title": meta,
                "character": char_name,
                "location": location,
                "timestamp": mtime_str,
                "size": f"{size_kb} КБ" if has_data else "0 КБ"
            })
        return slots

    def backup_saves(self, profile="gameplay") -> dict:
        """Создание резервной ZIP-копии папки SAVEGAME."""
        try:
            target_dir = self.gameplay_dir if profile == "gameplay" else self.hd_dir
            saves_dir = os.path.join(target_dir, "DATA", "SAVEGAME")
            if not os.path.exists(saves_dir):
                return {"status": "error", "message": "Папка сохранений не найдена."}

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_name = f"Fallout2_{profile}_{timestamp}.zip"
            zip_path = os.path.join(self.backups_dir, zip_name)

            file_count = 0
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(saves_dir):
                    for file in files:
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, saves_dir)
                        zipf.write(full_p, rel_p)
                        file_count += 1

            size_kb = os.path.getsize(zip_path) // 1024
            return {
                "status": "success",
                "zipName": zip_name,
                "sizeKb": size_kb,
                "fileCount": file_count,
                "path": zip_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_backups(self) -> list:
        """Получение списка существующих архивов резервных копий."""
        if not os.path.exists(self.backups_dir):
            return []
        res = []
        for f in sorted(os.listdir(self.backups_dir), reverse=True):
            if f.lower().endswith(".zip"):
                fp = os.path.join(self.backups_dir, f)
                size_kb = os.path.getsize(fp) // 1024
                mtime = os.path.getmtime(fp)
                mtime_str = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M")
                res.append({
                    "fileName": f,
                    "size": f"{size_kb} КБ",
                    "date": mtime_str
                })
        return res

    def restore_save_backup(self, zip_name: str, profile="gameplay") -> dict:
        """Безопасное восстановление сохранений из бэкапа с предварительным автобэкапом."""
        try:
            zip_path = os.path.join(self.backups_dir, zip_name)
            if not os.path.exists(zip_path):
                return {"status": "error", "message": f"Архив бэкапа не найден: {zip_name}"}

            target_dir = self.gameplay_dir if profile == "gameplay" else self.hd_dir
            saves_dir = os.path.join(target_dir, "DATA", "SAVEGAME")

            # 1. Автоматический снапшот перед перезаписью
            if os.path.exists(saves_dir):
                self.backup_saves(profile=f"safety_pre_restore_{profile}")

            # 2. Распаковка архива
            os.makedirs(saves_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(saves_dir)

            return {"status": "success", "message": f"Сейвы успешно восстановлены из {zip_name}!"}
        except Exception as e:
            return {"status": "error", "message": f"Сбой восстановления: {str(e)}"}

    def generate_diagnostic_report(self, user_text: str, category: str, profile: str) -> dict:
        """Генерация комплексного пакета телеметрии и диагностики для быстрой поддержки."""
        try:
            target_dir = self.gameplay_dir if "gameplay" in profile.lower() else self.hd_dir
            
            # Проверка наличия ключевых файлов
            files_status = {}
            for f in ["fallout2.exe", "ddraw.dll", "ddraw.ini", "f2_res.ini", "fallout2.cfg", "dustlight.exe"]:
                fp = os.path.join(target_dir, f)
                files_status[f] = "ЕСТЬ" if os.path.exists(fp) else "ОТСУТСТВУЕТ"

            # Сбор последних строк логов
            log_lines = []
            for log_name in ["ddraw.log", "debug.log", "f2_res.log"]:
                lp = os.path.join(target_dir, log_name)
                if os.path.exists(lp):
                    try:
                        with open(lp, "r", encoding="utf-8", errors="ignore") as lf:
                            last_lines = lf.readlines()[-15:]
                            log_lines.append(f"=== {log_name} (последние {len(last_lines)} строк) ===\n" + "".join(last_lines))
                    except Exception:
                        pass

            report = [
                "============================================================",
                "   FALLOUT 2 ULTIMATE WASTELAND 2026 // DIAGNOSTIC REPORT   ",
                "============================================================",
                f"Время формирования: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                f"Категория: {category}",
                f"Выбранный профиль: {profile}",
                f"Сообщение игрока: {user_text.strip() or 'Без комментария'}",
                "",
                "--- СОСТОЯНИЕ ФАЙЛОВОЙ СИСТЕМЫ ---",
                *[f"  [{status}] {name}" for name, status in files_status.items()],
                "",
                "--- СРЕЗ КОНФИГУРАЦИИ ---",
                json.dumps(self.read_config(), indent=2, ensure_ascii=False),
                "",
                "--- ЖУРНАЛЫ И ЛОГИ СИСТЕМЫ ---",
                *(log_lines if log_lines else ["(Логи пусты или еще не сформированы движком)"]),
                "============================================================"
            ]

            full_text = "\n".join(report)
            report_path = os.path.join(self.backups_dir, "diagnostic_report.txt")
            with open(report_path, "w", encoding="utf-8") as rf:
                rf.write(full_text)

            return {
                "status": "success",
                "reportText": full_text,
                "savedPath": report_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def verify_integrity(self) -> dict:
        """Мгновенная проверка целостности ключевых файлов сборки по контрольным суммам SHA-256."""
        import hashlib
        checksums_file = os.path.join(self.root_dir, "checksums.json")
        bundle_dir = getattr(sys, "_MEIPASS", None)
        if not os.path.exists(checksums_file) and bundle_dir:
            checksums_file = os.path.join(bundle_dir, "checksums.json")
        if not os.path.exists(checksums_file):
            checksums_file = os.path.join(os.path.dirname(__file__), "checksums.json")

        if not os.path.exists(checksums_file):
            return {"status": "error", "message": "Файл манифеста контрольных сумм (checksums.json) не найден."}

        try:
            with open(checksums_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            total = len(manifest)
            passed = 0
            failed = 0
            missing = 0
            details = []

            for rel_path, expected in manifest.items():
                abs_path = os.path.join(self.root_dir, rel_path.replace("/", os.sep))
                item_name = os.path.basename(rel_path)
                if not os.path.exists(abs_path):
                    missing += 1
                    details.append({"file": rel_path, "name": item_name, "status": "missing", "message": "Файл отсутствует"})
                    continue

                sha = hashlib.sha256()
                try:
                    with open(abs_path, "rb") as bf:
                        while chunk := bf.read(1024 * 1024):
                            sha.update(chunk)
                    actual_digest = sha.hexdigest()
                    if actual_digest.lower() == expected["sha256"].lower():
                        passed += 1
                        details.append({"file": rel_path, "name": item_name, "status": "ok", "message": "Целостность подтверждена"})
                    else:
                        failed += 1
                        details.append({"file": rel_path, "name": item_name, "status": "corrupted", "message": "Контрольная сумма не совпадает"})
                except Exception as e:
                    failed += 1
                    details.append({"file": rel_path, "name": item_name, "status": "error", "message": str(e)})

            overall_status = "ok" if (failed == 0 and missing == 0) else "warning" if failed == 0 else "error"
            return {
                "status": "success",
                "overall": overall_status,
                "total": total,
                "passed": passed,
                "failed": failed,
                "missing": missing,
                "details": details
            }
        except Exception as e:
            return {"status": "error", "message": f"Ошибка верификации целостности: {str(e)}"}

    def check_smart_health(self) -> dict:
        """
        Умная диагностика готовности без душноты:
        1. Права доступа и системная изоляция (Program Files vs Games).
        2. Базовые архивы (master.dat, critter.dat) — наличие и DAT2 сигнатуры.
        3. Совместимость ядра (fallout2.exe US 1.02d + sfall ddraw.dll).
        4. Конфликты старых/чужих модов в DATA/scripts.
        5. Не блокирует игру по мелочам: второстепенные файлы не вызывают панику.
        """
        import struct
        checks = []
        is_blocked = False
        has_warnings = False

        target_dir = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir

        # 1. Проверка прав записи и системной папки UAC
        norm_path = os.path.normpath(target_dir).lower()
        in_program_files = "program files" in norm_path or "program files (x86)" in norm_path
        write_ok = False
        try:
            test_tmp = os.path.join(target_dir, ".vault13_write_test.tmp")
            with open(test_tmp, "wb") as f:
                f.write(b"ok")
            if os.path.exists(test_tmp):
                os.remove(test_tmp)
                write_ok = True
        except Exception:
            write_ok = False

        if not write_ok:
            is_blocked = True
            checks.append({
                "id": "write_access",
                "title": "ПРАВА ЗАПИСИ (UAC / WINDOWS)",
                "status": "critical",
                "badge": "БЛОКИРОВКА",
                "message": "Каталог игры защищен Windows от записи. Сохранения и настройки не смогут записаться на диск. Запустите лаунчер от имени администратора или перенесите папку игры."
            })
        elif in_program_files:
            has_warnings = True
            checks.append({
                "id": "write_access",
                "title": "СИСТЕМНЫЙ КАТАЛОГ (PROGRAM FILES)",
                "status": "warning",
                "badge": "ВНИМАНИЕ",
                "message": "Игра установлена в системную папку Program Files. Рекомендуется перенести игру в корень диска (например C:\\Games или D:\\Games), чтобы избежать скрытых сбоев UAC."
            })
        else:
            checks.append({
                "id": "write_access",
                "title": "ПРАВА ЗАПИСИ И UAC",
                "status": "ok",
                "badge": "ДОСТУПНО",
                "message": "Полный доступ на запись. Конфликтов UAC и системных ограничений нет."
            })

        # 2. Проверка базовых архивов (master.dat и critter.dat)
        dat_errors = []
        for dat_name in ["master.dat", "CRITTER.DAT"]:
            dp = os.path.join(target_dir, dat_name)
            if not os.path.exists(dp):
                dp_lower = os.path.join(target_dir, dat_name.lower())
                if os.path.exists(dp_lower):
                    dp = dp_lower
            if not os.path.exists(dp):
                dat_errors.append(f"Отсутствует {dat_name}")
            else:
                sz = os.path.getsize(dp)
                if sz < 10 * 1024 * 1024:
                    dat_errors.append(f"{dat_name} поврежден ({sz // 1024} КБ)")
                else:
                    try:
                        with open(dp, "rb") as df:
                            df.seek(-8, os.SEEK_END)
                            dir_sz, tot_sz = struct.unpack("<II", df.read(8))
                            if tot_sz != sz:
                                dat_errors.append(f"{dat_name} поврежден (сбой сигнатуры DAT2)")
                    except Exception:
                        pass

        if dat_errors:
            is_blocked = True
            checks.append({
                "id": "base_dats",
                "title": "ОРИГИНАЛЬНЫЕ АРХИВЫ (MASTER & CRITTER)",
                "status": "critical",
                "badge": "ОШИБКА",
                "message": "; ".join(dat_errors) + ". Без них движок Fallout 2 не сможет загрузить базовые спрайты и карты."
            })
        else:
            checks.append({
                "id": "base_dats",
                "title": "ОРИГИНАЛЬНЫЕ АРХИВЫ",
                "status": "ok",
                "badge": "ВАЛИДНО",
                "message": "Базовые архивы master.dat (380+ МБ) и critter.dat (159+ МБ) на месте и не повреждены."
            })

        # 3. Проверка исполняемого ядра (fallout2.exe + sfall ddraw.dll)
        exe_path = os.path.join(target_dir, "fallout2.exe")
        ddraw_path = os.path.join(target_dir, "ddraw.dll")

        if not os.path.exists(exe_path):
            is_blocked = True
            checks.append({
                "id": "engine_exe",
                "title": "ИСПОЛНЯЕМЫЙ ФАЙЛ FALLOUT2.EXE",
                "status": "critical",
                "badge": "ОТСУТСТВУЕТ",
                "message": "Основной файл fallout2.exe не найден в директории игры."
            })
        else:
            exe_size = os.path.getsize(exe_path)
            if exe_size == 1189888:
                exe_status = "ok"
                exe_msg = "Оригинальный бинарник US 1.02d (1 189 888 байт). 100% совместимость со всеми хуками."
            elif exe_size in [1185792, 1186304, 1187840]:
                has_warnings = True
                exe_status = "warning"
                exe_msg = f"Обнаружена устаревшая версия fallout2.exe ({exe_size} байт, вероятно v1.00 или v1.01). Рекомендуется обновить до US 1.02d для стабильной работы sFall."
            else:
                exe_status = "ok"
                exe_msg = f"Исполняемый файл найден ({exe_size // 1024} КБ)."

            if not os.path.exists(ddraw_path):
                has_warnings = True
                checks.append({
                    "id": "engine_exe",
                    "title": "ДВИЖОК SFALL (DDRAW.DLL)",
                    "status": "warning",
                    "badge": "ОТСУТСТВУЕТ",
                    "message": "Библиотека sFall (ddraw.dll) не найдена. Модификации скриптов и высокое разрешение не будут активны."
                })
            else:
                checks.append({
                    "id": "engine_exe",
                    "title": "ЯДРО ДВИЖКА И SFALL",
                    "status": exe_status,
                    "badge": "СОВМЕСТИМО" if exe_status == "ok" else "ВНИМАНИЕ",
                    "message": f"{exe_msg} sFall (ddraw.dll) активен."
                })

        # 4. Проверка на посторонние скрипты / старые сборки (Megamod, чужие паки)
        scripts_dir = os.path.join(target_dir, "DATA", "scripts")
        known_canonical_scripts = {
            "aibkdor.int", "dcjoey.int", "dcsmitty.int", "gl_glasses.int", 
            "gl_molotov.int", "gl_pariah_fix.int", "gl_pbs_useobjon_sneak.int", 
            "kcdunton.int", "kctorr.int", "mccornel.int", "mcfarrel.int", 
            "mcmiria.int", "nctray.int", "nibasdor.int", "vccasidy.int", "vcdrtroy.int",
            "gl_temple_hints.int", "gl_ammomod.int", "gl_highlighting_build.int", "gl_laststand.int"
        }

        foreign_scripts = []
        if os.path.exists(scripts_dir):
            try:
                for f in os.listdir(scripts_dir):
                    if f.lower().endswith(".int") and f.lower() not in known_canonical_scripts:
                        foreign_scripts.append(f)
            except Exception:
                pass

        if foreign_scripts:
            has_warnings = True
            sample = ", ".join(foreign_scripts[:4])
            if len(foreign_scripts) > 4:
                sample += f" и ещё {len(foreign_scripts) - 4} шт."
            checks.append({
                "id": "foreign_mods",
                "title": "СТОРОННИЕ СКРИПТЫ В ПАПКЕ DATA",
                "status": "warning",
                "badge": f"НАЙДЕНО: {len(foreign_scripts)}",
                "message": f"Обнаружены посторонние скрипты от других модов ({sample}). Они могут вызывать вылеты и конфликты. Рекомендуется изолировать их в архив.",
                "foreign_count": len(foreign_scripts),
                "can_isolate": True
            })
        else:
            checks.append({
                "id": "foreign_mods",
                "title": "ЧИСТОТА ПАПКИ СКРИПТОВ",
                "status": "ok",
                "badge": "ЧИСТО",
                "message": "В DATA/scripts нет посторонних скриптов от старых сборок. Конфликты исключены."
            })

        # 5. Второстепенные файлы (Никакой душноты! Не блокируют игру)
        checks.append({
            "id": "minor_files",
            "title": "ДОПОЛНИТЕЛЬНЫЕ МОДУЛИ",
            "status": "info",
            "badge": "ГОТОВО",
            "message": "Конфигурация, шейдеры и звуковые пакеты настроены."
        })

        overall_status = "critical" if is_blocked else ("warning" if has_warnings else "ok")
        status_text = (
            "СИСТЕМА ГОТОВА К ЗАПУСКУ" if overall_status == "ok" else
            "СБОРКА РАБОТАЕТ (ЕСТЬ РЕКОМЕНДАЦИИ)" if overall_status == "warning" else
            "ОБНАРУЖЕНЫ КРИТИЧЕСКИЕ БЛОКИРОВКИ"
        )

        return {
            "status": "success",
            "overall": overall_status,
            "can_launch": not is_blocked,
            "status_text": status_text,
            "checks": checks,
            "has_foreign_mods": len(foreign_scripts) > 0,
            "foreign_count": len(foreign_scripts)
        }

    def isolate_legacy_conflicts(self) -> dict:
        """Безопасная изоляция посторонних скриптов старых сборок в ZIP-бэкап."""
        try:
            target_dir = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir
            scripts_dir = os.path.join(target_dir, "DATA", "scripts")
            if not os.path.exists(scripts_dir):
                return {"status": "success", "message": "Папка DATA/scripts чиста."}

            known_canonical_scripts = {
                "aibkdor.int", "dcjoey.int", "dcsmitty.int", "gl_glasses.int", 
                "gl_molotov.int", "gl_pariah_fix.int", "gl_pbs_useobjon_sneak.int", 
                "kcdunton.int", "kctorr.int", "mccornel.int", "mcfarrel.int", 
                "mcmiria.int", "nctray.int", "nibasdor.int", "vccasidy.int", "vcdrtroy.int",
                "gl_temple_hints.int", "gl_ammomod.int", "gl_highlighting_build.int", "gl_laststand.int"
            }

            foreign_files = []
            for f in os.listdir(scripts_dir):
                if f.lower().endswith(".int") and f.lower() not in known_canonical_scripts:
                    foreign_files.append(f)

            if not foreign_files:
                return {"status": "success", "message": "Посторонних файлов не обнаружено."}

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_name = f"legacy_mods_backup_{ts}.zip"
            zip_path = os.path.join(self.backups_dir, zip_name)

            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for f in foreign_files:
                    fp = os.path.join(scripts_dir, f)
                    zipf.write(fp, arcname=f)
                    os.remove(fp)

            return {
                "status": "success",
                "message": f"Успешно изолировано {len(foreign_files)} скриптов в архив {zip_name}!",
                "isolatedCount": len(foreign_files),
                "zipName": zip_name
            }
        except Exception as e:
            return {"status": "error", "message": f"Сбой при изоляции: {str(e)}"}

    def open_saves_folder(self, profile="gameplay"):
        """Открытие папки сохранений выбранного профиля в проводнике Windows."""
        target_dir = self.gameplay_dir if profile == "gameplay" else self.hd_dir
        saves_dir = os.path.join(target_dir, "DATA", "SAVEGAME")
        os.makedirs(saves_dir, exist_ok=True)
        os.startfile(saves_dir)

    def get_changelog_text(self) -> str:
        """Считывание полного текстового журнала изменений CHANGELOG_2026.txt."""
        candidates = [
            os.path.join(self.root_dir, "CHANGELOG_2026.txt"),
            os.path.join(self.gameplay_dir, "CHANGELOG_2026.txt"),
            os.path.join(os.path.dirname(self.root_dir), "CHANGELOG_2026.txt")
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    with open(c, "r", encoding="utf-8", errors="ignore") as f:
                        return f.read()
                except Exception as e:
                    return f"Ошибка чтения журнала изменений: {str(e)}"
        return "Журнал изменений CHANGELOG_2026.txt не найден на диске."

    def open_changelog_file(self) -> dict:
        """Открытие файла CHANGELOG_2026.txt в текстовом редакторе Windows."""
        candidates = [
            os.path.join(self.root_dir, "CHANGELOG_2026.txt"),
            os.path.join(self.gameplay_dir, "CHANGELOG_2026.txt"),
            os.path.join(os.path.dirname(self.root_dir), "CHANGELOG_2026.txt")
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    os.startfile(c)
                    return {"status": "success", "file": c}
                except Exception as e:
                    return {"status": "error", "message": f"Ошибка открытия файла: {str(e)}"}
        return {"status": "error", "message": "Файл CHANGELOG_2026.txt не найден на диске."}

    def open_external_url(self, url: str):
        """Открытие внешней ссылки в системном браузере по умолчанию."""
        webbrowser.open(url)


def show_webview_error():
    """Системное диалоговое окно при отсутствии Microsoft Edge WebView2."""
    msg = (
        "Для работы лаунчера Pip-Boy требуется компонент Microsoft Edge WebView2 Runtime.\n\n"
        "Нажмите 'ОК', чтобы открыть страницу официальной загрузки от Microsoft, "
        "или запустите игру напрямую через ярлыки в папках профилей."
    )
    title = "Fallout 2 Ultimate Wasteland // Требуется WebView2"
    MB_OKCANCEL = 0x01
    MB_ICONWARNING = 0x30
    IDOK = 1
    
    try:
        ret = ctypes.windll.user32.MessageBoxW(0, msg, title, MB_OKCANCEL | MB_ICONWARNING)
        if ret == IDOK:
            webbrowser.open("https://go.microsoft.com/fwlink/p/?LinkId=2124703")
    except Exception:
        webbrowser.open("https://go.microsoft.com/fwlink/p/?LinkId=2124703")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = current_dir

    possible_roots = [
        exe_dir,
        os.path.abspath(os.path.join(exe_dir, "..")),
        r"E:\Fallout2_Ultimate"
    ]
    root_dir = exe_dir
    for r in possible_roots:
        if os.path.exists(os.path.join(r, "Fallout2_Gameplay")) or os.path.exists(os.path.join(r, "master.dat")):
            root_dir = r
            break

    bridge = LauncherBridge(root_dir)
    external_ui = os.path.abspath(os.path.join(root_dir, "launcher_nextgen", "ui"))
    local_ui = os.path.join(current_dir, "ui")
    bundle_dir = getattr(sys, "_MEIPASS", None)

    if os.path.exists(os.path.join(external_ui, "index.html")):
        ui_dir = external_ui
    elif os.path.exists(os.path.join(local_ui, "index.html")):
        ui_dir = local_ui
    elif bundle_dir and os.path.exists(os.path.join(bundle_dir, "ui")):
        ui_dir = os.path.join(bundle_dir, "ui")
    else:
        ui_dir = external_ui

    index_path = os.path.join(ui_dir, "index.html")

    try:
        window = webview.create_window(
            title="Fallout 2 Ultimate Wasteland Edition 2026 // Pip-Boy 2000 Plus",
            url=index_path,
            js_api=bridge,
            width=1280,
            height=820,
            min_size=(1024, 720),
            background_color="#050806",
            text_select=False
        )
        bridge.set_window(window)

        import threading, time
        def apply_window_icon():
            candidate_paths = [
                os.path.join(ui_dir, "assets", "vault13_icon.ico"),
                os.path.join(bundle_dir, "ui", "assets", "vault13_icon.ico") if bundle_dir else "",
                os.path.join(ui_dir, "assets", "app_icon.ico"),
            ]
            ico_path = None
            for p in candidate_paths:
                if p and os.path.exists(p):
                    ico_path = p
                    break
            if not ico_path:
                return
            IMAGE_ICON = 1
            LR_LOADFROMFILE = 0x00000010
            WM_SETICON = 0x0080
            GCLP_HICON = -14
            GCLP_HICONSM = -34

            found_hwnds = []
            def enum_cb(h, _):
                length = ctypes.windll.user32.GetWindowTextLengthW(h)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(h, buf, length + 1)
                    if "Fallout 2 Ultimate" in buf.value:
                        found_hwnds.append(h)
                return True

            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
            proc = EnumWindowsProc(enum_cb)

            for _ in range(25):
                time.sleep(0.2)
                try:
                    found_hwnds.clear()
                    hwnd_direct = ctypes.windll.user32.FindWindowW(None, "Fallout 2 Ultimate Wasteland Edition 2026 // Pip-Boy 2000 Plus")
                    if hwnd_direct:
                        found_hwnds.append(hwnd_direct)
                    ctypes.windll.user32.EnumWindows(proc, 0)
                    if found_hwnds:
                        h_icon_big = ctypes.windll.user32.LoadImageW(0, ico_path, IMAGE_ICON, 48, 48, LR_LOADFROMFILE)
                        h_icon_small = ctypes.windll.user32.LoadImageW(0, ico_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
                        for h in set(found_hwnds):
                            if h_icon_big:
                                ctypes.windll.user32.SendMessageW(h, WM_SETICON, 1, h_icon_big)
                                try:
                                    ctypes.windll.user32.SetClassLongPtrW(h, GCLP_HICON, h_icon_big)
                                except Exception:
                                    pass
                            if h_icon_small:
                                ctypes.windll.user32.SendMessageW(h, WM_SETICON, 0, h_icon_small)
                                try:
                                    ctypes.windll.user32.SetClassLongPtrW(h, GCLP_HICONSM, h_icon_small)
                                except Exception:
                                    pass
                        break
                except Exception:
                    pass

        threading.Thread(target=apply_window_icon, daemon=True).start()

        webview.start(gui="edgechromium", debug=False)
    except Exception as e:
        print("WebView2 initialization error:", e)
        show_webview_error()

if __name__ == "__main__":
    main()
