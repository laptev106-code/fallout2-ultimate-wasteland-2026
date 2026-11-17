"""
Fallout 2: Ultimate Mega Rework 2026
Manifest & Component Registry
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ModComponent:
    id: str
    name: str
    version: str
    category: str  # 'core', 'gameplay', 'tactics', 'qol', 'audio_visual', 'expansion', 'graphics_ce'
    description: str
    download_url: str
    archive_name: str
    conflicts_with: List[str] = field(default_factory=list)
    requires: List[str] = field(default_factory=list)
    default_enabled_gameplay: bool = True
    default_enabled_hd: bool = False
    is_ce_only: bool = False
    is_sfall_only: bool = False

# Реестр компонентов
COMPONENTS: Dict[str, ModComponent] = {
    "rpu": ModComponent(
        id="rpu",
        name="Restoration Project Updated (RPU)",
        version="2.4.34",
        category="core",
        description="Фундамент сборки: восстановленные локации (EPA, Abbey, Primitive Tribe), квесты, NPC, Unofficial Patch, High Res Patch и анимации.",
        download_url="https://github.com/BGforgeNet/Fallout2_Restoration_Project/releases/download/v2.4.34/rpu_v2.4.34.zip",
        archive_name="rpu_v2.4.34.zip",
        default_enabled_gameplay=True,
        default_enabled_hd=True
    ),
    "rpu_ru": ModComponent(
        id="rpu_ru",
        name="RPU Russian Translation (Локализация)",
        version="2.4.34",
        category="core",
        description="Полная русская локализация текстов и диалогов RPU.",
        download_url="https://github.com/BGforgeNet/Fallout2_Restoration_Project/releases/download/v2.4.34/rpu_v2.4.34_translations.zip",
        archive_name="rpu_v2.4.34_translations.zip",
        requires=["rpu"],
        default_enabled_gameplay=True,
        default_enabled_hd=True
    ),
    "ecco": ModComponent(
        id="ecco",
        name="EcCo Gameplay Overhaul",
        version="1.0.0",
        category="gameplay",
        description="Главная переработка баланса: характеристики оружия, брони, формулы урона, экономика, крафт, ловушки и рецепты.",
        download_url="https://github.com/phobos2077/fo2_ecco/releases/download/v1.0.0/pbs_fo2rpu_ecco_mod_v1-0-0.zip",
        archive_name="pbs_fo2rpu_ecco_mod_v1-0-0.zip",
        requires=["rpu"],
        conflicts_with=["dustlight", "fallout2_ce"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "ecco_hf1": ModComponent(
        id="ecco_hf1",
        name="EcCo Hotfix 1.0.0 hf1",
        version="1.0.0-hf1",
        category="gameplay",
        description="Обязательный хотфикс формул и скриптов для EcCo 1.0.0.",
        download_url="https://github.com/phobos2077/fo2_ecco/releases/download/v1.0.0/pbs_fo2rpu_ecco_patch_1-0-0-hf1.zip",
        archive_name="pbs_fo2rpu_ecco_patch_1-0-0-hf1.zip",
        requires=["ecco"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "ecco_that_patch": ModComponent(
        id="ecco_that_patch",
        name="THAT + EcCo RPU 2.4.34 Compatibility Patch",
        version="v2",
        category="audio_visual",
        description="Официальный патч совместимости диалогов EcCo и говорящих голов THAT под RPU 2.4.34.",
        download_url="https://github.com/phobos2077/fo2_ecco/releases/download/v1.0.0/THAT_rpu_v2.4.34_compatibility_patch_v2.zip",
        archive_name="THAT_rpu_v2.4.34_compatibility_patch_v2.zip",
        requires=["ecco"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "minirework": ModComponent(
        id="minirework",
        name="Fallout Mechanics MiniRework",
        version="2.0.4.3",
        category="tactics",
        description="Альтернативные режимы стрельбы, яды, скрытность, книги напарников, исправление критических ударов.",
        download_url="https://github.com/dekrus/Fallout2MechanicsMiniRework/releases/download/2.0.4.3/F2MechanicsMiniRework_v2.0.4.3.zip",
        archive_name="F2MechanicsMiniRework_v2.0.4.3.zip",
        requires=["rpu"],
        conflicts_with=["dustlight", "fallout2_ce"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "minirework_ru": ModComponent(
        id="minirework_ru",
        name="MiniRework Russian Translation",
        version="2.0.4.3",
        category="tactics",
        description="Русские описания перков и боевых механик MiniRework.",
        download_url="https://github.com/dekrus/Fallout2MechanicsMiniRework/releases/download/2.0.4.3/F2MechanicsMiniRework_v2.0.4.3_RUS.zip",
        archive_name="F2MechanicsMiniRework_v2.0.4.3_RUS.zip",
        requires=["minirework"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "fo2tweaks": ModComponent(
        id="fo2tweaks",
        name="FO2Tweaks (Quality of Life)",
        version="15.0",
        category="qol",
        description="Удобный инвентарь, авто-двери, подсветка контейнеров, авто-перезарядка без читов и конфликтов с EcCo.",
        download_url="https://github.com/BGforgeNet/FO2tweaks/releases/download/v15.0/fo2tweaks_v15.0.zip",
        archive_name="fo2tweaks_v15.0.zip",
        requires=["rpu"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "vock": ModComponent(
        id="vock",
        name="V.O.C.K. Full Voice Acting Mod",
        version="1.15",
        category="audio_visual",
        description="Полная авторская озвучка диалогов NPC, голоса напарников, уникальные реплики и Talking Head Священной Головы.",
        download_url="https://github.com/dweltvauller/vock-fo2/archive/refs/tags/v1.15.zip",
        archive_name="vock_fo2_v1.15.zip",
        requires=["rpu"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "bunker21": ModComponent(
        id="bunker21",
        name="Bunker 21 & Truck Locations",
        version="1.00",
        category="expansion",
        description="Самостоятельное расширение карты RPU: возвращение уникального Бункера 21 и грузовиков.",
        download_url="https://github.com/BGforgeNet/Fallout2_Restoration_Project/releases/download/v2.4.34/rpu_v2.4.34.zip", # fallback mirror
        archive_name="bunker21_truck_locations_1.00.zip",
        requires=["rpu"],
        is_sfall_only=True,
        default_enabled_gameplay=True,
        default_enabled_hd=False
    ),
    "fallout2_ce": ModComponent(
        id="fallout2_ce",
        name="Fallout 2 Community Edition (SDL2 Engine)",
        version="1.3.0",
        category="graphics_ce",
        description="Кроссплатформенный порт движка Fallout 2 с нативной поддержкой современных ОС и шейдеров.",
        download_url="https://github.com/alexbatalov/fallout2-ce/releases/download/v1.3.0/fallout2-ce-windows-x64.zip",
        archive_name="fallout2-ce-windows-x64.zip",
        requires=["rpu"],
        conflicts_with=["ecco", "minirework", "fo2tweaks", "bunker21", "vock"],
        is_ce_only=True,
        default_enabled_gameplay=False,
        default_enabled_hd=True
    ),
    "dustlight": ModComponent(
        id="dustlight",
        name="Dustlight HD Graphics & Dynamic Lighting",
        version="0.9.4-beta",
        category="graphics_ce",
        description="HD апскейл спрайтов (Scale2x/AI), цветное освещение, мягкие тени и атмосферная тьма ночей.",
        download_url="https://github.com/mrdushidush/dustlight/releases/download/v0.9.4-beta/Dustlight-0.9.4-beta-engine.zip",
        archive_name="Dustlight-0.9.4-beta-engine.zip",
        requires=["fallout2_ce", "rpu"],
        conflicts_with=["ecco", "minirework", "fo2tweaks", "bunker21", "vock"],
        is_ce_only=True,
        default_enabled_gameplay=False,
        default_enabled_hd=True
    )
}
