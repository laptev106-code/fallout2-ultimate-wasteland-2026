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
from datetime import datetime
import webview

class LauncherBridge:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.gameplay_dir = os.path.join(self.root_dir, "Fallout2_Gameplay")
        self.hd_dir = os.path.join(self.root_dir, "Fallout2_HD")
        self.backups_dir = os.path.join(self.root_dir, "Backups")
        os.makedirs(self.backups_dir, exist_ok=True)
        self._window = None

    def set_window(self, window):
        self._window = window

    def launch_profile(self, profile: str) -> dict:
        """Запуск выбранного игрового профиля с проверкой фоновых процессов."""
        try:
            # Проверка, не запущена ли уже игра
            try:
                tasklist = subprocess.check_output('tasklist /FI "IMAGENAME eq fallout2.exe"', shell=True, text=True)
                if "fallout2.exe" in tasklist.lower():
                    return {"status": "error", "message": "Процесс fallout2.exe уже запущен в системе."}
            except Exception:
                pass

            if profile == "gameplay":
                target_exe = os.path.join(self.gameplay_dir, "fallout2.exe")
                target_cwd = self.gameplay_dir
            else:
                ce_exe = os.path.join(self.hd_dir, "fallout2-ce.exe")
                dust_exe = os.path.join(self.hd_dir, "dustlight.exe")
                target_exe = dust_exe if os.path.exists(dust_exe) else ce_exe
                target_cwd = self.hd_dir

            if not os.path.exists(target_exe):
                return {"status": "error", "message": f"Исполняемый файл не найден: {target_exe}"}

            subprocess.Popen([target_exe], cwd=target_cwd)
            return {"status": "success", "profile": profile}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_config(self) -> dict:
        """Считывание текущих настроек f2_res.ini, ddraw.ini и fallout2.cfg."""
        cfg = {
            "resolution": "2560x1440",
            "mode": "fullscreen",
            "scale": "2x",
            "filtering": "bilinear",
            "musicVol": 80,
            "sfxVol": 80
        }

        # 1. f2_res.ini
        ini_path = os.path.join(self.gameplay_dir, "f2_res.ini")
        if os.path.exists(ini_path):
            try:
                with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                w = 2560
                h = 1440
                win_val = 0
                win_fs = 0
                for line in content.splitlines():
                    line_s = line.strip()
                    if line_s.startswith("SCR_WIDTH="):
                        w = int(line_s.split("=")[1].strip())
                    elif line_s.startswith("SCR_HEIGHT="):
                        h = int(line_s.split("=")[1].strip())
                    elif line_s.startswith("SCALE_2X=0"):
                        cfg["scale"] = "1x"
                    elif line_s.startswith("SCALE_2X=1"):
                        cfg["scale"] = "2x"
                    elif line_s.startswith("WINDOWED="):
                        win_val = int(line_s.split("=")[1].strip())
                    elif line_s.startswith("WINDOWED_FULLSCREEN="):
                        win_fs = int(line_s.split("=")[1].strip())

                cfg["resolution"] = f"{w}x{h}"
                if win_val == 1 and win_fs == 1:
                    cfg["mode"] = "borderless"
                elif win_val == 1:
                    cfg["mode"] = "windowed"
                else:
                    cfg["mode"] = "fullscreen"
            except Exception as e:
                print("Error reading f2_res.ini:", e)

        # 2. ddraw.ini
        ddraw_path = os.path.join(self.gameplay_dir, "ddraw.ini")
        if os.path.exists(ddraw_path):
            try:
                with open(ddraw_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip().startswith("TextureFilter="):
                            val = line.strip().split("=")[1].strip()
                            cfg["filtering"] = "bilinear" if val == "2" else "point"
            except Exception:
                pass

        # 3. fallout2.cfg
        fallout_cfg = os.path.join(self.gameplay_dir, "fallout2.cfg")
        if os.path.exists(fallout_cfg):
            try:
                with open(fallout_cfg, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("music_volume="):
                            vol = int(line.split("=")[1].strip())
                            cfg["musicVol"] = int((vol / 32767.0) * 100)
                        elif line.startswith("sndfx_volume="):
                            vol = int(line.split("=")[1].strip())
                            cfg["sfxVol"] = int((vol / 32767.0) * 100)
            except Exception:
                pass

        return cfg

    def save_config(self, cfg: dict) -> dict:
        """Хирургическая запись настроек в f2_res.ini, ddraw.ini и fallout2.cfg."""
        try:
            res_val = cfg.get("resolution", "2560x1440")
            w, h = res_val.split("x")
            w, h = int(w), int(h)

            scale_2x = 1 if cfg.get("scale") == "2x" else 0
            mode = cfg.get("mode", "fullscreen")
            if mode == "borderless":
                windowed = 1
                borderless = 1
            elif mode == "windowed":
                windowed = 1
                borderless = 0
            else:
                windowed = 0
                borderless = 0

            filter_val = 2 if cfg.get("filtering") == "bilinear" else 0

            # 1. Update f2_res.ini
            ini_path = os.path.join(self.gameplay_dir, "f2_res.ini")
            if os.path.exists(ini_path):
                with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                new_lines = []
                for line in lines:
                    if line.startswith("SCR_WIDTH="):
                        new_lines.append(f"SCR_WIDTH={w}\n")
                    elif line.startswith("SCR_HEIGHT="):
                        new_lines.append(f"SCR_HEIGHT={h}\n")
                    elif line.startswith("SCALE_2X="):
                        new_lines.append(f"SCALE_2X={scale_2x}\n")
                    elif line.startswith("WINDOWED="):
                        new_lines.append(f"WINDOWED={windowed}\n")
                    elif line.startswith("WINDOWED_FULLSCREEN="):
                        new_lines.append(f"WINDOWED_FULLSCREEN={borderless}\n")
                    elif line.startswith("COLOUR_BITS="):
                        new_lines.append("COLOUR_BITS=32\n")
                    else:
                        new_lines.append(line)

                with open(ini_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

            # 2. Update ddraw.ini
            ddraw_path = os.path.join(self.gameplay_dir, "ddraw.ini")
            if os.path.exists(ddraw_path):
                with open(ddraw_path, "r", encoding="utf-8", errors="ignore") as f:
                    dlines = f.readlines()

                new_dlines = []
                for line in dlines:
                    if line.strip().startswith("TextureFilter="):
                        new_dlines.append(f"TextureFilter={filter_val}\n")
                    else:
                        new_dlines.append(line)

                with open(ddraw_path, "w", encoding="utf-8") as f:
                    f.writelines(new_dlines)

            # 3. Update fallout2.cfg
            cfg_path = os.path.join(self.gameplay_dir, "fallout2.cfg")
            if os.path.exists(cfg_path):
                music_vol = int((cfg.get("musicVol", 80) / 100.0) * 32767)
                sfx_vol = int((cfg.get("sfxVol", 80) / 100.0) * 32767)

                with open(cfg_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                new_lines = []
                for line in lines:
                    if line.startswith("music_volume="):
                        new_lines.append(f"music_volume={music_vol}\n")
                    elif line.startswith("sndfx_volume="):
                        new_lines.append(f"sndfx_volume={sfx_vol}\n")
                    elif line.startswith("speech_volume="):
                        new_lines.append(f"speech_volume={sfx_vol}\n")
                    else:
                        new_lines.append(line)

                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_saves_info(self) -> list:
        """Сбор информации о слотах сохранений."""
        saves_dir = os.path.join(self.gameplay_dir, "DATA", "SAVEGAME")
        slots = []
        for i in range(1, 11):
            slot_name = f"SLOT{i:02d}"
            slot_path = os.path.join(saves_dir, slot_name)
            has_data = os.path.exists(slot_path) and len(os.listdir(slot_path)) > 0
            meta = "Пусто"
            size_kb = 0
            mtime_str = ""

            if has_data:
                try:
                    total_bytes = sum(os.path.getsize(os.path.join(slot_path, f)) for f in os.listdir(slot_path) if os.path.isfile(os.path.join(slot_path, f)))
                    size_kb = total_bytes // 1024
                    save_dat = os.path.join(slot_path, "SAVE.DAT")
                    mtime = os.path.getmtime(save_dat if os.path.exists(save_dat) else slot_path)
                    mtime_str = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y %H:%M")
                    meta = f"Слот {i} (Активен)"
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

    def backup_saves(self) -> str:
        """Создание резервной ZIP-копии папки SAVEGAME."""
        saves_dir = os.path.join(self.gameplay_dir, "DATA", "SAVEGAME")
        if not os.path.exists(saves_dir):
            raise Exception("Папка сохранений не найдена.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"Fallout2_Saves_Backup_{timestamp}.zip"
        zip_path = os.path.join(self.backups_dir, zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(saves_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, saves_dir)
                    zipf.write(full_p, rel_p)

        return zip_name

    def open_saves_folder(self):
        """Открытие папки сохранений в проводнике Windows."""
        saves_dir = os.path.join(self.gameplay_dir, "DATA", "SAVEGAME")
        os.makedirs(saves_dir, exist_ok=True)
        os.startfile(saves_dir)

    def open_external_url(self, url: str):
        """Открытие внешней ссылки в системном браузере по умолчанию."""
        webbrowser.open(url)


def main():
    # Находим базовую директорию сборки
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Если запущен из launcher_nextgen, root - родительская папка или E:\Fallout2_Ultimate
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
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir and os.path.exists(os.path.join(bundle_dir, "ui")):
        ui_dir = os.path.join(bundle_dir, "ui")
    elif os.path.exists(os.path.join(current_dir, "ui")):
        ui_dir = os.path.join(current_dir, "ui")
    else:
        ui_dir = os.path.abspath(os.path.join(root_dir, "launcher_nextgen", "ui"))

    index_path = os.path.join(ui_dir, "index.html")

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

    # Запуск WebView2 с аппаратным ускорением GPU
    webview.start(gui="edgechromium", debug=False)

if __name__ == "__main__":
    main()
