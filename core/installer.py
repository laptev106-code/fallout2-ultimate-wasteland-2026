"""
Deployment Pipeline & Installation Engine
"""

import os
import shutil
import zipfile
import urllib.request
from typing import List, Callable, Optional
from core.manifest import COMPONENTS
from core.configurator import Configurator
from core.patcher import Patcher

class InstallationEngine:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def download_file(self, url: str, target_path: str, progress_callback: Optional[Callable[[int, int, str], None]] = None) -> bool:
        """Скачивает файл с прогрессом."""
        if os.path.exists(target_path) and os.path.getsize(target_path) > 1024:
            if progress_callback:
                progress_callback(100, 100, f"Кэш найден: {os.path.basename(target_path)}")
            return True
            
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as response, open(target_path, "wb") as out_file:
                total_size = int(response.info().get("Content-Length", 0))
                downloaded = 0
                block_size = 65536
                
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    out_file.write(buffer)
                    if progress_callback and total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        progress_callback(percent, 100, f"Загрузка {os.path.basename(target_path)}: {percent}%")
            return True
        except Exception as e:
            if os.path.exists(target_path):
                os.remove(target_path)
            raise RuntimeError(f"Ошибка загрузки {url}: {e}")

    def extract_zip(self, zip_path: str, dest_dir: str, progress_callback: Optional[Callable[[int, int, str], None]] = None):
        """Безопасно распаковывает архив с защитой от перезаписи sfall 4.5.1 и маршрутизацией dat-модов."""
        with zipfile.ZipFile(zip_path, "r") as zf:
            infolist = zf.infolist()
            total = len(infolist)
            for i, member in enumerate(infolist):
                member_name = member.filename
                
                # Защита sfall 4.5.1: если ddraw.dll уже существует в целевой папке (от RPU),
                # не позволяем сторонним модам (например, FO2tweaks) перезаписывать его версией sfall 5
                if member_name.lower() == "ddraw.dll" and os.path.exists(os.path.join(dest_dir, "ddraw.dll")):
                    continue
                
                # Фильтр локализации RPU: извлекаем строго русскую локализацию и звук,
                # пропуская остальные языки (испанский, французский, польский и т.д.)
                if "translation" in os.path.basename(zip_path).lower():
                    if member_name.lower().endswith(".dat") and "russian" not in member_name.lower():
                        continue
                
                # Если одиночный .dat файл находится в корне архива (например, патч THAT или Bunker 21),
                # направляем его в папку mods/, чтобы sfall корректно загрузил его
                if member_name.lower().endswith(".dat") and "/" not in member_name and "\\" not in member_name:
                    target_mods_dir = os.path.join(dest_dir, "mods")
                    os.makedirs(target_mods_dir, exist_ok=True)
                    out_path = os.path.join(target_mods_dir, member_name)
                    with zf.open(member) as src_f, open(out_path, "wb") as dst_f:
                        shutil.copyfileobj(src_f, dst_f)
                else:
                    zf.extract(member, dest_dir)
                    
                if progress_callback and i % 50 == 0:
                    percent = int((i / total) * 100)
                    progress_callback(percent, 100, f"Распаковка {os.path.basename(zip_path)}: {percent}%")

    def copy_clean_base(self, source_dir: str, target_dir: str, log_callback: Optional[Callable[[str], None]] = None):
        """Копирует ключевые файлы оригинальной Fallout 2 в чистую целевую папку."""
        os.makedirs(target_dir, exist_ok=True)
        if log_callback:
            log_callback(f"Копирование базовых архивов из {source_dir} в {target_dir}...")
            
        # Обязательные базовые файлы: master.dat, critter.dat, sound.dat, fallout2.exe, fallout2.cfg, data
        allowed_files = ["master.dat", "critter.dat", "sound.dat", "fallout2.exe", "fallout2.cfg", "data"]
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(target_dir, item)
            item_lower = item.lower()
            
            if item_lower in allowed_files:
                if os.path.isdir(s):
                    if not os.path.exists(d):
                        shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

    def install_profile(
        self,
        clean_source_dir: str,
        target_dir: str,
        component_ids: List[str],
        profile_name: str,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ):
        """Полный цикл установки выбранного профиля."""
        if log_callback:
            log_callback(f"Начало сборки профиля: {profile_name}")
            
        # 1. Подготовка целевой директории
        self.copy_clean_base(clean_source_dir, target_dir, log_callback)
        
        # 2. Скачивание и распаковка компонентов по порядку
        for cid in component_ids:
            mod = COMPONENTS.get(cid)
            if not mod:
                continue
                
            archive_path = os.path.join(self.cache_dir, mod.archive_name)
            if log_callback:
                log_callback(f"Подготовка компонента: {mod.name} ({mod.version})")
                
            if not os.path.exists(archive_path):
                if not mod.download_url:
                    if log_callback:
                        log_callback(f"Пропуск {mod.name}: архив {mod.archive_name} не найден в cache/ (требуется ручная загрузка с Nexus Mods).")
                    continue
                self.download_file(mod.download_url, archive_path, progress_callback)
            
            if os.path.exists(archive_path):
                if log_callback:
                    log_callback(f"Интеграция: {mod.name}...")
                self.extract_zip(archive_path, target_dir, progress_callback)
            
        # 3. Тонкая настройка конфигураций и устранение кракозябр
        if log_callback:
            log_callback("Применение инженерных параметров совместимости (INI tuning & CodePage)...")
            
        Patcher.ensure_fallout_cfg(target_dir)
        Patcher.apply_codepage_fix(target_dir)

        ddraw_ini = os.path.join(target_dir, "ddraw.ini")
        Configurator.tune_ddraw_ini(ddraw_ini)
        
        f2_res_ini = os.path.join(target_dir, "f2_res.ini")
        Configurator.tune_f2_res_ini(f2_res_ini)
        
        Configurator.tune_minirework_ini(target_dir)
        Configurator.tune_fo2tweaks_ini(target_dir)
        
        mods_dir = os.path.join(target_dir, "mods")
        Configurator.write_mods_order(mods_dir)
            
        # 4. Бинарный патчинг LAA 4GB
        exe_path = os.path.join(target_dir, "fallout2.exe")
        if os.path.exists(exe_path):
            if log_callback:
                log_callback("Патчинг fallout2.exe: Large Address Aware (4GB Virtual Memory)...")
            Patcher.apply_4gb_laa_patch(exe_path)
            
        # 5. Генерация батника быстрого запуска
        bat_path = os.path.join(target_dir, "Play_Fallout2.bat")
        try:
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write("@echo off\nstart \"\" \"%~dp0fallout2.exe\"\n")
        except Exception:
            pass

        if log_callback:
            log_callback(f"Профиль '{profile_name}' успешно собран и готов к запуску!")
