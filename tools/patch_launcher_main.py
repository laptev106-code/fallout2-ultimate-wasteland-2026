import os

main_py = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\main.py"
with open(main_py, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Replace read_config resolution mapping
old_read = """                cfg["resolution"] = f"{w}x{h}"
                if win_val == 1 and win_fs == 1:
                    cfg["mode"] = "borderless"
                elif win_val == 1:
                    cfg["mode"] = "windowed"
                else:
                    cfg["mode"] = "fullscreen"
            except Exception as e:
                print("Error reading f2_res.ini:", e)"""

new_read = """                if w == 1280 and h == 720:
                    cfg["resolution"] = "2560x1440"
                    cfg["scale"] = "2x"
                else:
                    cfg["resolution"] = f"{w}x{h}"
                if win_val == 1 and win_fs == 1:
                    cfg["mode"] = "borderless"
                elif win_val == 1:
                    cfg["mode"] = "windowed"
                else:
                    cfg["mode"] = "fullscreen"
            except Exception as e:
                print("Error reading f2_res.ini:", e)"""

if old_read in content:
    content = content.replace(old_read, new_read)
    print("Replaced read_config")
else:
    print("Could not find old_read")

# Replace save_config resolution logic
target_start = "            if scale_choice == \"4x\" or (w >= 3200 and scale_choice == \"2x\"):"
target_end = "            for target_dir in target_dirs:\n                # 1. f2_res.ini"

new_save_block = """            if scale_choice == "2x" or scale_choice == "4x":
                # В Fallout 2 связка SCR_WIDTH=1280 и SCR_HEIGHT=720 с SCALE_2X=1
                # и sfall Mode=6 (DirectX 9 Borderless Fullscreen) масштабируется видеокартой
                # на весь экран монитора (1440p / 1080p / 4K) с идеальными крупными пропорциями UI,
                # крупным инвентарем и четкими шрифтами без микроскопических элементов.
                f2_w = 1280
                f2_h = 720
                f2_scale_2x = 1
                ddraw_gw = 0
                ddraw_gh = 0
                ce_scale = 2 if scale_choice == "2x" else 3
            else: # 1x (Оригинальный мелкий интерфейс / максимальный обзор)
                f2_w = w
                f2_h = h
                f2_scale_2x = 0
                ddraw_gw = 0
                ddraw_gh = 0
                ce_scale = 1

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
                    "GraphicsWidth": ddraw_gw,
                    "GraphicsHeight": ddraw_gh,
                    "TextureFilter": filter_val,
                    "WindowData": 0,
                    "BackgroundKeyboard": 1,
                    "BackgroundMouse": 1,
                    "SpeedInventoryPCRotation": 600,
                    "CombatPanelAnimDelay": 90,
                    "WorldMapEncounterRate": 14,
                    "SkipCompatModeCheck": 1
                }, encoding="cp1251")

                # 3. fallout2.cfg
                fallout_cfg = os.path.join(target_dir, "fallout2.cfg")
                self._safe_write_ini_key(fallout_cfg, {
                    "music_volume": music_vol,
                    "sndfx_volume": sfx_vol,
                    "speech_volume": sfx_vol,
                    "combat_speed": 85,
                    "resolution_x": w,
                    "resolution_y": h,
                    "scale": ce_scale,
                    "windowed": cfg_windowed
                }, encoding="utf-8")

                # 4. fo2tweaks.ini (отключение дерганного авто-релоада после боя)
                fo2tweaks_path = os.path.join(target_dir, "mods", "fo2tweaks.ini")
                if os.path.exists(fo2tweaks_path):
                    self._safe_write_ini_key(fo2tweaks_path, {"auto_reload": 0}, encoding="utf-8")

                # 5. sfall-mods.ini (отключение 10-кадрового цикла сканирования криттеров)
                sfall_mods_path = os.path.join(target_dir, "mods", "sfall-mods.ini")
                if os.path.exists(sfall_mods_path):
                    self._safe_write_ini_key(sfall_mods_path, {"Critters": 0, "CheckLOS": 0}, encoding="utf-8")
"""

# Find and replace the save section
idx_start = content.find(target_start)
idx_end = content.find("            return {\n                \"status\": \"success\",\n                \"message\": f\"")

if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + new_save_block + "\n" + content[idx_end:]
    print("Replaced save_config block")
else:
    print(f"Indices: {idx_start}, {idx_end}")

with open(main_py, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved main.py")
