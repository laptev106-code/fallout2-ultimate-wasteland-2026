"""
Fallout 2 Ultimate Wasteland 2026 // Next-Gen Desktop Launcher
Powered by pywebview (Microsoft Edge WebView2 Hardware-Accelerated Core).
"""
import os
import sys
import json
import zipfile
import subprocess
import webbrowser
import shutil
import ctypes
from datetime import datetime
import webview

class LauncherBridge:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.gameplay_dir = os.path.join(self.root_dir, "Fallout2_Gameplay")
        self.hd_dir = os.path.join(self.root_dir, "Fallout2_HD")
        self.backups_dir = os.path.join(self.root_dir, "Backups")
        self.config_file = os.path.join(self.root_dir, "launcher_config.json")
        os.makedirs(self.backups_dir, exist_ok=True)
        self._window = None

    def set_window(self, window):
        self._window = window

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

            # 3. Запуск дочернего процесса
            subprocess.Popen([target_exe], cwd=target_cwd)
            return {"status": "success", "profile": profile, "exe": os.path.basename(target_exe)}
        except Exception as e:
            return {"status": "error", "message": f"Критический сбой запуска: {str(e)}"}

    def read_config(self) -> dict:
        """Считывание сохраненных настроек из launcher_config.json с синхронизацией из INI при первом запуске."""
        default_cfg = {
            "resolution": "1920x1080",
            "mode": "fullscreen",
            "scale": "2x",
            "filtering": "bilinear",
            "musicVol": 80,
            "sfxVol": 80,
            "alwaysRun": True,
            "autoReload": True,
            "templeTutorial": True
        }

        # 1. Если уже сохранен launcher_config.json, загружаем его как эталон
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
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
            except Exception:
                pass

        # ddraw.ini (TempleTutorial)
        ddraw_cfg = os.path.join(self.gameplay_dir, "ddraw.ini")
        if os.path.exists(ddraw_cfg):
            try:
                with open(ddraw_cfg, "r", encoding="cp1251", errors="ignore") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("TempleTutorial=") or line_s.startswith("TempleTutorial ="):
                            val = line_s.split("=")[1].strip()
                            cfg["templeTutorial"] = (val == "1")
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

        with open(file_path, "w", encoding=encoding, errors="ignore") as f:
            f.writelines(new_lines)

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

            if mode == "borderless":
                f2_windowed = 0
                f2_borderless = 0
                ddraw_mode = 6
                cfg_windowed = 2
            elif mode == "windowed":
                f2_windowed = 1
                f2_borderless = 0
                ddraw_mode = 5
                cfg_windowed = 1
            else:  # fullscreen
                f2_windowed = 0
                f2_borderless = 0
                ddraw_mode = 6
                cfg_windowed = 0

            filter_val = 2 if cfg.get("filtering") == "bilinear" else 0
            music_vol = int((cfg.get("musicVol", 80) / 100.0) * 32767)
            sfx_vol = int((cfg.get("sfxVol", 80) / 100.0) * 32767)

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

            auto_reload_val = 1 if cfg.get("autoReload", False) else 0
            running_val = 1 if cfg.get("alwaysRun", True) else 0
            temple_tut_val = 1 if cfg.get("templeTutorial", True) else 0

            target_dirs = [self.gameplay_dir]
            if os.path.exists(self.hd_dir):
                target_dirs.append(self.hd_dir)

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
                    "EXTRA_WIN_MSG_CHECKS": 0
                }, encoding="cp1251")

                # 2. ddraw.ini
                ddraw_path = os.path.join(target_dir, "ddraw.ini")
                self._safe_write_ini_key(ddraw_path, {
                    "Mode": ddraw_mode,
                    "GraphicsWidth": 0,
                    "GraphicsHeight": 0,
                    "TextureFilter": filter_val,
                    "WindowData": 0,
                    "BackgroundKeyboard": 1,
                    "BackgroundMouse": 1,
                    "SpeedInventoryPCRotation": 300,
                    "CombatPanelAnimDelay": 90,
                    "WorldMapEncounterRate": 14,
                    "SkipCompatModeCheck": 1,
                    "ExtraCRC": "0xf18aa577,0xe1680293",
                    "TempleTutorial": temple_tut_val
                }, encoding="cp1251")

                # 3. fallout2.cfg
                fallout_cfg = os.path.join(target_dir, "fallout2.cfg")
                self._safe_write_ini_key(fallout_cfg, {
                    "music_volume": music_vol,
                    "sndfx_volume": sfx_vol,
                    "speech_volume": sfx_vol,
                    "combat_speed": 85,
                    "running": running_val,
                    "resolution_x": w,
                    "resolution_y": h,
                    "scale": ce_scale,
                    "windowed": cfg_windowed
                }, encoding="utf-8")

                # 4. fo2tweaks.ini
                fo2tweaks_path = os.path.join(target_dir, "mods", "fo2tweaks.ini")
                if os.path.exists(fo2tweaks_path):
                    self._safe_write_ini_key(fo2tweaks_path, {"auto_reload": auto_reload_val}, encoding="utf-8")

            return {
                "status": "success",
                "message": f"Конфигурация успешно сохранена: {w}x{h}, {mode}, Scale {scale_choice}, бег={running_val}, автоперезарядка={auto_reload_val}, обучение={temple_tut_val}."
            }
        except Exception as e:
            return {"status": "error", "message": f"Ошибка сохранения настроек: {str(e)}"}

    def get_saves_info(self, profile="gameplay") -> list:
        """Сбор информации о слотах сохранений выбранного профиля."""
        target_dir = self.gameplay_dir if profile == "gameplay" else self.hd_dir
        saves_dir = os.path.join(target_dir, "DATA", "SAVEGAME")
        slots = []

        for i in range(1, 11):
            slot_name = f"SLOT{i:02d}"
            slot_path = os.path.join(saves_dir, slot_name)
            has_data = os.path.exists(slot_path) and len(os.listdir(slot_path)) > 0
            meta = "Пустой слот"
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
                    save_dat = os.path.join(slot_path, "SAVE.DAT")
                    mtime = os.path.getmtime(save_dat if os.path.exists(save_dat) else slot_path)
                    mtime_str = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M")
                    meta = f"Сейв {i} ({size_kb} КБ)"
                except Exception:
                    pass

            slots.append({
                "slot": f"{i:02d}",
                "hasData": has_data,
                "title": meta,
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

    def open_saves_folder(self):
        """Открытие папки сохранений в проводнике Windows."""
        saves_dir = os.path.join(self.gameplay_dir, "DATA", "SAVEGAME")
        os.makedirs(saves_dir, exist_ok=True)
        os.startfile(saves_dir)

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
    possible_roots = [
        r"E:\Fallout2_Ultimate",
        os.path.abspath(os.path.join(current_dir, "..", "..", "Fallout2_Ultimate")),
        os.path.abspath(os.path.join(current_dir, ".."))
    ]
    root_dir = r"E:\Fallout2_Ultimate"
    for r in possible_roots:
        if os.path.exists(os.path.join(r, "Fallout2_Gameplay")):
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
            title="Fallout 2 Ultimate Wasteland Edition 2026 // Pip-Boy 3000 Mk IV",
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
            time.sleep(0.6)
            try:
                hwnd = ctypes.windll.user32.FindWindowW(None, "Fallout 2 Ultimate Wasteland Edition 2026 // Pip-Boy 3000 Mk IV")
                if hwnd:
                    ico_path = os.path.join(ui_dir, "assets", "vault13_icon.ico")
                    if os.path.exists(ico_path):
                        IMAGE_ICON = 1
                        LR_LOADFROMFILE = 0x00000010
                        h_icon_big = ctypes.windll.user32.LoadImageW(0, ico_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE)
                        h_icon_small = ctypes.windll.user32.LoadImageW(0, ico_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
                        WM_SETICON = 0x0080
                        if h_icon_big:
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, 1, h_icon_big)
                        if h_icon_small:
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, 0, h_icon_small)
            except Exception:
                pass

        threading.Thread(target=apply_window_icon, daemon=True).start()

        webview.start(gui="edgechromium", debug=False)
    except Exception as e:
        print("WebView2 initialization error:", e)
        show_webview_error()

if __name__ == "__main__":
    main()
