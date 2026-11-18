"""
Fallout 2 Ultimate Wasteland Edition 2026 - Master Installer GUI
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict

# Добавляем корень проекта в путь импорта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.manifest import COMPONENTS
from core.engine_detector import autodetect_clean_fallout, check_fallout_dir
from core.compatibility_engine import CompatibilityEngine
from core.installer import InstallationEngine

class FalloutMasterInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fallout 2 Ultimate 2026 - Master Installer & Pipeline")
        self.geometry("820x720")
        self.minsize(780, 680)
        self.configure(bg="#121511")
        
        self.cache_dir = os.path.join(PROJECT_ROOT, "cache")
        self.engine = InstallationEngine(self.cache_dir)
        
        self.source_dir = tk.StringVar()
        self.target_dir = tk.StringVar()
        self.selected_preset = tk.StringVar(value="gameplay_ultimate")
        self.component_vars: Dict[str, tk.BooleanVar] = {}
        
        # Автодетекция при старте
        detected = autodetect_clean_fallout()
        if detected:
            self.source_dir.set(detected)
            self.target_dir.set(os.path.join(os.path.dirname(detected), "Fallout2_Ultimate"))
        else:
            self.source_dir.set("")
            self.target_dir.set(r"C:\Games\Fallout2_Ultimate")
            
        self.setup_styles()
        self.setup_ui()
        self.apply_preset_selection()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        self.style.configure(".", background="#121511", foreground="#e0e0e0")
        self.style.configure("TLabel", background="#121511", foreground="#ddffdd", font=("Segoe UI", 9))
        self.style.configure("TFrame", background="#121511")
        self.style.configure("Header.TLabel", font=("Terminal", 16, "bold"), foreground="#44ff44", background="#1a2118")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#88cc88", background="#1a2118")
        self.style.configure("Error.TLabel", foreground="#ff5555", font=("Segoe UI", 9, "bold"))
        self.style.configure("Success.TLabel", foreground="#55ff55", font=("Segoe UI", 9, "bold"))
        self.style.configure("TLabelframe", background="#121511", foreground="#66bb66")
        self.style.configure("TLabelframe.Label", background="#121511", foreground="#66bb66", font=("Segoe UI", 10, "bold"))

    def setup_ui(self):
        # Header banner
        header = tk.Frame(self, bg="#1a2118", pady=12)
        header.pack(fill="x")
        
        tk.Label(header, text="FALLOUT 2: ULTIMATE WASTELAND 2026", font=("Segoe UI", 16, "bold"), fg="#44ff44", bg="#1a2118").pack()
        tk.Label(header, text="Единый мастер-инсталлятор и верификатор совместимости", font=("Segoe UI", 9), fg="#99dd99", bg="#1a2118").pack()

        main_frame = tk.Frame(self, bg="#121511", padx=16, pady=10)
        main_frame.pack(fill="both", expand=True)

        # 1. Секция путей (Источник и Назначение)
        path_box = ttk.LabelFrame(main_frame, text=" 1. Директории игры ", padding=10)
        path_box.pack(fill="x", pady=4)

        # Source
        f_src = tk.Frame(path_box, bg="#121511")
        f_src.pack(fill="x", pady=2)
        tk.Label(f_src, text="Чистая Fallout 2 (Steam / GOG):", width=28, anchor="w", fg="#cccccc", bg="#121511").pack(side="left")
        tk.Entry(f_src, textvariable=self.source_dir, bg="#1e221d", fg="#ffffff", insertbackground="#44ff44").pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(f_src, text="Обзор...", bg="#252c23", fg="#ffffff", command=self.browse_source).pack(side="right")

        # Target
        f_tgt = tk.Frame(path_box, bg="#121511")
        f_tgt.pack(fill="x", pady=2)
        tk.Label(f_tgt, text="Куда установить Ultimate сборку:", width=28, anchor="w", fg="#cccccc", bg="#121511").pack(side="left")
        tk.Entry(f_tgt, textvariable=self.target_dir, bg="#1e221d", fg="#ffffff", insertbackground="#44ff44").pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(f_tgt, text="Обзор...", bg="#252c23", fg="#ffffff", command=self.browse_target).pack(side="right")

        # 2. Выбор профиля установки
        preset_box = ttk.LabelFrame(main_frame, text=" 2. Выбор режима сборки ", padding=8)
        preset_box.pack(fill="x", pady=4)

        p_frame = tk.Frame(preset_box, bg="#121511")
        p_frame.pack(fill="x")

        tk.Radiobutton(
            p_frame, text="★ Gameplay Ultimate (Рекомендовано: RPU + EcCo + MiniRework + FO2Tweaks + Lossless Music + sfall 4.5.1)",
            variable=self.selected_preset, value="gameplay_ultimate",
            command=self.apply_preset_selection,
            bg="#121511", fg="#44ff44", selectcolor="#1c2b1c", activebackground="#121511", activeforeground="#44ff44", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=2)

        tk.Radiobutton(
            p_frame, text="🎨 HD Visual Ultimate (Dustlight 0.9.2 HD + AI 2x/3x + Community Edition Engine)",
            variable=self.selected_preset, value="hd_ultimate",
            command=self.apply_preset_selection,
            bg="#121511", fg="#88ccff", selectcolor="#182333", activebackground="#121511", activeforeground="#88ccff", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=2)

        tk.Radiobutton(
            p_frame, text="⚡ Dual Profile (Оба режима параллельно в две изолированные папки)",
            variable=self.selected_preset, value="dual_profile",
            command=self.apply_preset_selection,
            bg="#121511", fg="#ffcc44", selectcolor="#2b2618", activebackground="#121511", activeforeground="#ffcc44", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=2)

        tk.Radiobutton(
            p_frame, text="🛠 Пользовательский режим (Выбор галочками вручную)",
            variable=self.selected_preset, value="custom",
            command=self.apply_preset_selection,
            bg="#121511", fg="#cccccc", selectcolor="#222222", activebackground="#121511", activeforeground="#ffffff"
        ).pack(anchor="w", pady=2)

        # 3. Список компонентов и чекбоксы
        comp_box = ttk.LabelFrame(main_frame, text=" 3. Компоненты сборки (Валидация на лету) ", padding=8)
        comp_box.pack(fill="both", expand=True, pady=4)

        canvas = tk.Canvas(comp_box, bg="#121511", highlightthickness=0)
        scrollbar = ttk.Scrollbar(comp_box, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#121511")

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Создаем чекбоксы компонентов
        for cid, mod in COMPONENTS.items():
            var = tk.BooleanVar(value=mod.default_enabled_gameplay)
            self.component_vars[cid] = var
            
            f_row = tk.Frame(self.scroll_frame, bg="#121511", pady=2)
            f_row.pack(fill="x", anchor="w")
            
            cb = tk.Checkbutton(
                f_row, text=f"{mod.name} (v{mod.version})",
                variable=var, command=self.on_checkbox_change,
                bg="#121511", fg="#ffffff", selectcolor="#1c2b1c",
                activebackground="#121511", activeforeground="#44ff44",
                font=("Segoe UI", 9)
            )
            cb.pack(side="left")
            
            lbl_desc = tk.Label(f_row, text=f"— {mod.description}", fg="#777777", bg="#121511", font=("Segoe UI", 8))
            lbl_desc.pack(side="left", padx=5)

        # Индикатор валидации
        self.lbl_validation = tk.Label(main_frame, text="", bg="#121511", wraplength=760, justify="left")
        self.lbl_validation.pack(fill="x", pady=4)

        # 4. Прогресс и лог
        self.progress_bar = ttk.Progressbar(main_frame, mode="determinate")
        self.progress_bar.pack(fill="x", pady=4)

        self.lbl_status = tk.Label(main_frame, text="Готов к установке", fg="#88cc88", bg="#121511", anchor="w")
        self.lbl_status.pack(fill="x")

        # Кнопка установки
        btn_frame = tk.Frame(main_frame, bg="#121511", pady=6)
        btn_frame.pack(fill="x")

        self.btn_install = tk.Button(
            btn_frame, text="⚡ СОБРАТЬ И УСТАНОВИТЬ СБОРКУ",
            font=("Segoe UI", 12, "bold"),
            bg="#225522", fg="#ffffff", activebackground="#338833", activeforeground="#ffffff",
            relief="raised", bd=3, pady=6, command=self.start_installation
        )
        self.btn_install.pack(fill="x")

    def browse_source(self):
        d = filedialog.askdirectory(title="Выберите директорию с чистой Fallout 2")
        if d:
            self.source_dir.set(d)
            self.validate_environment()

    def browse_target(self):
        d = filedialog.askdirectory(title="Выберите папку назначения для сборки")
        if d:
            self.target_dir.set(d)

    def apply_preset_selection(self):
        preset = self.selected_preset.get()
        if preset == "gameplay_ultimate":
            for cid, var in self.component_vars.items():
                var.set(COMPONENTS[cid].default_enabled_gameplay)
        elif preset == "hd_ultimate":
            for cid, var in self.component_vars.items():
                var.set(COMPONENTS[cid].default_enabled_hd)
        elif preset == "dual_profile":
            # При дуал-профиле активируем все
            for cid, var in self.component_vars.items():
                var.set(True)
        self.validate_environment()

    def on_checkbox_change(self):
        self.selected_preset.set("custom")
        self.validate_environment()

    def validate_environment(self) -> bool:
        src = self.source_dir.get().strip()
        chk = check_fallout_dir(src)
        
        selected_ids = [cid for cid, var in self.component_vars.items() if var.get()]
        preset = self.selected_preset.get()
        
        target_profile = "custom"
        if preset == "gameplay_ultimate":
            target_profile = "gameplay"
        elif preset == "hd_ultimate":
            target_profile = "hd"
            
        if preset != "dual_profile":
            is_valid, errors, warnings = CompatibilityEngine.validate_selection(selected_ids, target_profile)
        else:
            is_valid = True
            errors = []
            warnings = ["Будут созданы две независимые изолированные папки: Fallout2_Gameplay и Fallout2_HD."]

        if not chk.get("valid"):
            self.lbl_validation.config(text=f"⚠ Исходная папка: {chk.get('reason')}", fg="#ff5555")
            self.btn_install.config(state="disabled")
            return False
            
        if not is_valid and errors:
            self.lbl_validation.config(text=f"❌ Ошибка совместимости: {errors[0]}", fg="#ff4444")
            self.btn_install.config(state="disabled")
            return False
            
        msg = "✔ Конфигурация полностью совместима и готова к развертыванию!"
        if warnings:
            msg += f" ({warnings[0]})"
        self.lbl_validation.config(text=msg, fg="#55ff55")
        self.btn_install.config(state="normal")
        return True

    def start_installation(self):
        if not self.validate_environment():
            return
            
        self.btn_install.config(state="disabled")
        threading.Thread(target=self._run_install_thread, daemon=True).start()

    def _run_install_thread(self):
        src = self.source_dir.get().strip()
        tgt = self.target_dir.get().strip()
        preset = self.selected_preset.get()
        
        try:
            if preset == "dual_profile":
                # Установка двух профилей параллельно
                p1_dir = os.path.join(tgt, "Fallout2_Gameplay")
                p1_mods = CompatibilityEngine.get_preset_components("gameplay_ultimate")
                self.engine.install_profile(
                    src, p1_dir, p1_mods, "Gameplay Ultimate",
                    progress_callback=self._update_progress,
                    log_callback=self._log
                )
                
                p2_dir = os.path.join(tgt, "Fallout2_HD")
                p2_mods = CompatibilityEngine.get_preset_components("hd_ultimate")
                self.engine.install_profile(
                    src, p2_dir, p2_mods, "HD Visual Dustlight",
                    progress_callback=self._update_progress,
                    log_callback=self._log
                )
                
                # Копируем мастер-лаунчер в корень и создаем Run_Launcher.bat
                shutil.copy2(os.path.join(PROJECT_ROOT, "core", "launcher.py"), os.path.join(tgt, "launcher.py"))
                launcher_bat = os.path.join(tgt, "Run_Launcher.bat")
                with open(launcher_bat, "w", encoding="utf-8") as f:
                    f.write("@echo off\nstart \"\" py -3 \"%~dp0launcher.py\"\n")
            else:
                selected_ids = [cid for cid, var in self.component_vars.items() if var.get()]
                self.engine.install_profile(
                    src, tgt, selected_ids, preset,
                    progress_callback=self._update_progress,
                    log_callback=self._log
                )
                shutil.copy2(os.path.join(PROJECT_ROOT, "core", "launcher.py"), os.path.join(tgt, "launcher.py"))
                launcher_bat = os.path.join(tgt, "Run_Launcher.bat")
                with open(launcher_bat, "w", encoding="utf-8") as f:
                    f.write("@echo off\nstart \"\" py -3 \"%~dp0launcher.py\"\n")

            self._log("🎉 ВСЕ ОПЕРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ!")
            self._update_progress(100, 100, "Установка завершена на 100%")
            messagebox.showinfo("Успех", f"Сборка Fallout 2 Ultimate 2026 успешно установлена в:\n{tgt}\n\nДля запуска используйте launcher.py!")
        except Exception as e:
            self._log(f"ОШИБКА: {e}")
            messagebox.showerror("Ошибка установки", str(e))
        finally:
            self.btn_install.config(state="normal")

    def _update_progress(self, current: int, total: int, text: str):
        self.after(0, lambda: self._apply_progress(current, total, text))

    def _apply_progress(self, current: int, total: int, text: str):
        self.progress_bar["value"] = current
        self.lbl_status.config(text=text)

    def _log(self, msg: str):
        self.after(0, lambda: self.lbl_status.config(text=msg))

if __name__ == "__main__":
    app = FalloutMasterInstaller()
    app.mainloop()
