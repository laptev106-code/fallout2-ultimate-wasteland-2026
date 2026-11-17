"""
Fallout 2 Ultimate Wasteland Edition 2026 - Master Launcher
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class MasterLauncher(tk.Tk):
    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.title("Fallout 2: Ultimate Wasteland Edition 2026 - Launcher")
        self.geometry("640x480")
        self.resizable(False, False)
        self.configure(bg="#121511")
        
        self.gameplay_dir = os.path.join(root_dir, "Fallout2_Gameplay")
        self.hd_dir = os.path.join(root_dir, "Fallout2_HD")
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg="#1a2118", pady=15)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="FALLOUT 2: ULTIMATE EDITION",
            font=("Terminal", 18, "bold"),
            fg="#44ff44",
            bg="#1a2118"
        )
        title_label.pack()
        
        sub_label = tk.Label(
            header_frame,
            text="Dual-Profile Engine & Mod Manager 2026",
            font=("Segoe UI", 9),
            fg="#88cc88",
            bg="#1a2118"
        )
        sub_label.pack()

        # Content Area
        content = tk.Frame(self, bg="#121511", padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # Profile 1: Gameplay Ultimate
        btn_gameplay = tk.Button(
            content,
            text="▶ ЗАПУСК: GAMEPLAY ULTIMATE\n(RPU 2.4.34 + EcCo 1.0.0 + MiniRework + FO2Tweaks + Lossless Music + sfall 4.5.1)",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#1f441f",
            activebackground="#2d662d",
            activeforeground="#ffffff",
            relief="raised",
            bd=3,
            pady=8,
            command=self.launch_gameplay
        )
        btn_gameplay.pack(fill="x", pady=8)

        # Profile 2: HD Visual Ultimate
        btn_hd = tk.Button(
            content,
            text="▶ ЗАПУСК: HD VISUAL DUSTLIGHT\n(Fallout 2 Community Edition + AI HD 2x/3x + Dynamic Lights)",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#2a3f5f",
            activebackground="#3b5984",
            activeforeground="#ffffff",
            relief="raised",
            bd=3,
            pady=8,
            command=self.launch_hd
        )
        btn_hd.pack(fill="x", pady=8)

        # Utility Buttons
        util_frame = tk.Frame(content, bg="#121511", pady=15)
        util_frame.pack(fill="x")

        btn_saves = tk.Button(
            util_frame,
            text="📁 Папка сохранений",
            font=("Segoe UI", 9),
            fg="#cccccc",
            bg="#252825",
            command=self.open_saves
        )
        btn_saves.pack(side="left", expand=True, fill="x", padx=4)

        btn_config = tk.Button(
            util_frame,
            text="⚙ Настройки f2_res.ini",
            font=("Segoe UI", 9),
            fg="#cccccc",
            bg="#252825",
            command=self.open_res_config
        )
        btn_config.pack(side="right", expand=True, fill="x", padx=4)

        # Status footer
        self.status_var = tk.StringVar(value="Система готова к запуску.")
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            fg="#66aa66",
            bg="#0e110d",
            anchor="w",
            padx=10,
            pady=4
        )
        status_bar.pack(side="bottom", fill="x")

    def launch_gameplay(self):
        exe = os.path.join(self.gameplay_dir, "fallout2.exe")
        if not os.path.exists(exe):
            # Проверяем в текущей папке
            exe = os.path.join(self.root_dir, "fallout2.exe")
            
        if os.path.exists(exe):
            self.status_var.set("Запуск Gameplay Ultimate...")
            subprocess.Popen([exe], cwd=os.path.dirname(exe))
        else:
            messagebox.showerror("Ошибка", f"Файл не найден:\n{exe}\nУстановите профиль через Инсталлятор!")

    def launch_hd(self):
        exe = os.path.join(self.hd_dir, "fallout2-ce.exe")
        if not os.path.exists(exe):
            exe = os.path.join(self.root_dir, "fallout2-ce.exe")
            
        if os.path.exists(exe):
            self.status_var.set("Запуск HD Dustlight...")
            subprocess.Popen([exe], cwd=os.path.dirname(exe))
        else:
            messagebox.showerror("Ошибка", f"Файл не найден:\n{exe}\nУстановите HD-профиль через Инсталлятор!")

    def open_saves(self):
        target = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir
        saves_dir = os.path.join(target, "DATA", "SAVEGAME")
        os.makedirs(saves_dir, exist_ok=True)
        os.startfile(saves_dir)

    def open_res_config(self):
        target = self.gameplay_dir if os.path.exists(self.gameplay_dir) else self.root_dir
        cfg = os.path.join(target, "f2_res.ini")
        if os.path.exists(cfg):
            os.startfile(cfg)
        else:
            messagebox.showinfo("Инфо", f"Конфиг {cfg} будет создан после первого запуска игры.")

if __name__ == "__main__":
    app = MasterLauncher(os.path.dirname(os.path.abspath(__file__)))
    app.mainloop()
