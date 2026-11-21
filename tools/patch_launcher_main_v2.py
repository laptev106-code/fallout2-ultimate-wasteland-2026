import os

main_py = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\main.py"
with open(main_py, "r", encoding="utf-8") as f:
    text = f.read()

s = text.find('    def read_config(self) -> dict:')
e = text.find('    def get_saves_info')

new_block = '''    def read_config(self) -> dict:
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
                    new_lines.append(f"{k}={v}\\n")
                    if k in unhandled_keys:
                        unhandled_keys.remove(k)
                    replaced = True
                    break
            if not replaced:
                new_lines.append(line)

        if unhandled_keys:
            new_lines.append("\\n; Added by Fallout 2 Next-Gen Launcher\\n")
            for k in unhandled_keys:
                new_lines.append(f"{k}={key_values[k]}\\n")

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

'''

updated_text = text[:s] + new_block + text[e:]
with open(main_py, "w", encoding="utf-8") as f:
    f.write(updated_text)

print("Updated main.py successfully! Total length:", len(updated_text))
