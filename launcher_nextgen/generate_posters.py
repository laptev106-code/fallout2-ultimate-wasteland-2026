"""
Generator of 15 cinema-grade widescreen posters for Fallout 2 Ultimate Wasteland 2026 Launcher.
Format: 1200x675 (16:9), PNG format.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

POSTER_DIR = os.path.join(os.path.dirname(__file__), "ui", "assets", "posters")
os.makedirs(POSTER_DIR, exist_ok=True)

MODS_DATA = [
    {
        "id": "rpu",
        "title": "RESTORATION PROJECT UPDATED",
        "category": "КВЕСТЫ И ЛОКАЦИИ",
        "badge": "КОНТЕНТ МИРА",
        "version": "v28.0 DIRECTORS CUT",
        "author": "killap, Burn, Darek, RPU Team",
        "theme": "green",
        "tagline": "Восстановление вырезанного контента 1998 года: Аббатство, EPA, Деревня Дикарей, Лагерь Работорговцев",
        "specs": ["LOCATIONS: +6 MAJOR", "QUESTS: +45 UNLOCKED", "CUT CHARACTERS: 80+", "VOICE LINES: RESTORED"],
        "icon_type": "worldmap"
    },
    {
        "id": "upu",
        "title": "UNOFFICIAL PATCH UPDATED",
        "category": "СТАБИЛЬНОСТЬ",
        "badge": "1000+ ФИКСОВ",
        "version": "v28.0 ENGINE STABLE",
        "author": "killap, UPU Team",
        "theme": "blue",
        "tagline": "Фундамент стабильности: устранение всех критических багов, утечек памяти, зависаний и софтлоков",
        "specs": ["BUG FIXES: 1200+", "SCRIPT ERRORS: 0", "CRASH PROTECTION: ACTIVE", "SAVE CORRUPTION: IMMUNE"],
        "icon_type": "shield"
    },
    {
        "id": "sfall",
        "title": "SFALL v4.4.8 ADVANCED ENGINE",
        "category": "ДВИЖОК",
        "badge": "DIRECTX 9 & 144HZ",
        "version": "v4.4.8 MASTER BUILD",
        "author": "Timeslip, Crafty, Mr.Stalin",
        "theme": "green",
        "tagline": "Полный рендеринг через DirectX 9, частота обновления до 144-240 Гц, аппаратный скроллинг мыши",
        "specs": ["RENDERER: DIRECT3D 9", "MAX FPS: 144/240 HZ", "MOUSE: SUBPIXEL RAW INPUT", "SCRIPT EXTENDER: ACTIVE"],
        "icon_type": "engine"
    },
    {
        "id": "weapons",
        "title": "COMBAT & WEAPON ANIMATIONS",
        "category": "ВИЗУАЛ И БОЙ",
        "badge": "ОРУЖИЕ",
        "version": "v2.6 EXPANDED",
        "author": "RPU Animation Team, Continuum",
        "theme": "amber",
        "tagline": "Сотни новых кадров анимаций: охотничьи винтовки, мечи вакидзаси, тяжелый огнемет, дульная вспышка",
        "specs": ["WEAPONS: 18 NEW SPRITES", "DIRECTIONS: 8-WAY ISOMETRIC", "RELOAD ANIMS: EXPANDED", "FRAME RATE: 100% SYNC"],
        "icon_type": "crosshair"
    },
    {
        "id": "armor",
        "title": "NPC ARMOR VISUAL EVOLUTION",
        "category": "СПУТНИКИ",
        "badge": "БРОНЯ НАПАРНИКОВ",
        "version": "v3.1 VISUAL SPRITES",
        "author": "Continuum, Skynet, RPU Team",
        "theme": "cyan",
        "tagline": "Напарники меняют внешний вид при смене брони: Сулик, Вик, Мирия и Дэвин в кожаных куртках и силовой броне",
        "specs": ["SULIK: ALL ARMOR TIERS", "VIC: FULL SPRITE SET", "MIRIA/DAVIN: COMBAT ARMOR", "POWER ARMOR: COMPATIBLE"],
        "icon_type": "armor"
    },
    {
        "id": "marcus",
        "title": "MARCUS ARMOR & DOGMEAT KEVLAR",
        "category": "СПУТНИКИ",
        "badge": "ТЯЖЕЛЫЙ ЭКИП",
        "version": "v1.8 HARDENED",
        "author": "RPU Team, Continuum",
        "theme": "amber",
        "tagline": "Тяжелая броня супермутантов для Маркуса и кевларовый бронежилет для Псины — защита в финальной фазе игры",
        "specs": ["MARCUS HP BOOST: +40%", "PLASMA RESIST: 50%", "DOGMEAT KEVLAR: 35% DT", "LATE GAME VIABILITY: S-TIER"],
        "icon_type": "mutant"
    },
    {
        "id": "cassidy",
        "title": "JOHN CASSIDY TALKING HEAD",
        "category": "ОЗВУЧКА И ДИАЛОГИ",
        "badge": "3D-ГОЛОВА",
        "version": "v2.0 STUDIO VOICED",
        "author": "Joey Bracken, RPU Team",
        "theme": "green",
        "tagline": "Живая анимированная 3D-голова бармена Джона Кэссиди из Города Убежища со студийной актерской озвучкой",
        "specs": ["HEAD MODEL: 3D PRERENDER", "LIP SYNC: AUTOMATED", "ACTOR: JOEY BRACKEN", "SOUND QUALITY: 44.1 KHZ"],
        "icon_type": "head"
    },
    {
        "id": "music",
        "title": "MARK MORGAN LOSSLESS REMASTER",
        "category": "САУНДТРЕК",
        "badge": "ЗВУК 1 ГБ",
        "version": "44.1 KHZ LOSSLESS STEREO",
        "author": "Mark Morgan, BGforge Net",
        "theme": "green",
        "tagline": "Отреставрированный студийный саундтрек: замена глухого моно 22 кГц 1998 года на кристальный стереозвук",
        "specs": ["TRACKS: 31 COMPOSITIONS", "AUDIO FORMAT: LOSSLESS ACM", "BITRATE: 1411 KBPS", "DYNAMIC RANGE: FULL"],
        "icon_type": "wave"
    },
    {
        "id": "doors",
        "title": "AUTODOORS & LOOT PROTECTION",
        "category": "ИНТЕРФЕЙС И QOL",
        "badge": "QOL ТВЕРДО",
        "version": "v2.4 FO2TWEAKS",
        "author": "BGforge Net, sfall contributors",
        "theme": "cyan",
        "tagline": "Автоматическое открытие дверей перед бегущим героем и сохранение лута при лазерной дезинтеграции",
        "specs": ["DOOR CLICKS: ELIMINATED", "DEINTEGRATION LOSS: 0%", "INVENTORY DROP: PILE LOCKED", "LATENCY: 0 MS"],
        "icon_type": "door"
    },
    {
        "id": "inventory",
        "title": "ADVANCED INVENTORY & SORTING",
        "category": "УПРАВЛЕНИЕ",
        "badge": "БЫСТРЫЙ ИНВЕНТАРЬ",
        "version": "v4.2 SMART UI",
        "author": "sfall team, Mr.Stalin",
        "theme": "green",
        "tagline": "Колесо мыши для прокрутки лута, быстрые горячие клавиши, фильтрация по типам предметов и авто-перезарядка",
        "specs": ["WHEEL SCROLL: NATIVE", "CONTAINER FOCUS: AUTO", "QUICK BARTER: 4 SLOTS", "TAKE ALL: 1-CLICK"],
        "icon_type": "inventory"
    },
    {
        "id": "miria",
        "title": "MIRIA COMPANION REWORK",
        "category": "СПУТНИКИ И КВЕСТЫ",
        "badge": "ПОЛНЫЙ КОМПАНЬОН",
        "version": "v2.0 EXPANDED",
        "author": "RPU Team, killap",
        "theme": "magenta",
        "tagline": "Превращение жены/мужа из Модока в полноценного боевого напарника с прокачкой, экипировкой и командой 'Жди здесь'",
        "specs": ["WAIT COMMAND: ENABLED", "LEVEL PROGRESSION: 1-6", "INVENTORY TRADE: OPEN", "DIVORCE QUEST: EXPANDED"],
        "icon_type": "heart"
    },
    {
        "id": "damage",
        "title": "YAAM & GLOVZ BALLISTICS REWORK",
        "category": "БАЛАНС БОЯ",
        "badge": "БАЛАНС УРОНА",
        "version": "v1.5 REBALANCED",
        "author": "Glovz, YAAM, sfall team",
        "theme": "amber",
        "tagline": "Исправление сломанной формулы бронебойных пуль оригинала: AP-патроны теперь пробивают тяжелую броню Анклава",
        "specs": ["AP FORMULA: FIXED", "JHP BULLETS: FLESH DAMAGE", "ARMOR PIERCING: VIABLE", "BURST MULTIPLIER: BALANCED"],
        "icon_type": "bullet"
    },
    {
        "id": "worldmap",
        "title": "ENHANCED WORLDMAP & ENCOUNTERS",
        "category": "ГЛОБАЛЬНАЯ КАРТА",
        "badge": "ГЛОБАЛЬНАЯ КАРТА",
        "version": "v3.0 EXPANDED",
        "author": "RPU Team, Mash",
        "theme": "blue",
        "tagline": "Широкоформатная карта мира с честным масштабированием и устранением аномальной частоты случайных встреч",
        "specs": ["MAP RESOLUTION: 890x720+", "ENCOUNTER RATES: NORMALIZED", "CAR TRUNK ACCESS: FIXED", "SPECIAL TILES: 100% WORKING"],
        "icon_type": "map"
    },
    {
        "id": "graphics",
        "title": "NATIVE 2560x1440 32-BIT ARGB",
        "category": "ВИЗУАЛ",
        "badge": "2K / 4K NATIVE",
        "version": "v4.1.8 HI-RES MASTER",
        "author": "Mash, sfall team",
        "theme": "cyan",
        "tagline": "Аппаратное сглаживание текстур на GPU, нативное разрешение 2K QHD без дробного масштабирования и лесенок",
        "specs": ["TARGET RES: 2560x1440", "COLOR DEPTH: 32-BIT ARGB", "FILTERING: BILINEAR GPU", "SCALE MODE: 2X INTEGRAL"],
        "icon_type": "display"
    },
    {
        "id": "dustlight",
        "title": "DUSTLIGHT VOLUMETRIC LIGHTING",
        "category": "ГРАФИКА HD",
        "badge": "ЛУЧЕВОЙ СВЕТ",
        "version": "v1.4 COMM. EDITION",
        "author": "Dustlight Team, Community Edition",
        "theme": "amber",
        "tagline": "Объемное лучевое освещение, атмосферный туман войны, мягкие тени факелов и динамические источники света",
        "specs": ["LIGHTING: VOLUMETRIC RAYMARCH", "FOG OF WAR: DYNAMIC", "ENGINE: SDL2 COMPATIBLE", "PROFILE: HD VISUAL ONLY"],
        "icon_type": "sun"
    },
    {
        "id": "crafting",
        "title": "WASTELAND CRAFT & PIPE WEAPONS",
        "category": "КУСТАРНОЕ ОРУЖИЕ",
        "badge": "САМОПАЛЫ И КРАФТ",
        "version": "v2.0 EXPANDED",
        "author": "phobos2077, EcCo Team",
        "theme": "amber",
        "tagline": "Трубчатые самопалы (Pipe Rifle), кустарные гранаты, арбалеты и капканы у рейдеров и бродяг (Храм и Арройо не затронуты)",
        "specs": ["PIPE WEAPONS: VIABLE EARLY GAME", "TRAPS: EPA SPIKES & BEAR TRAPS", "WORLD DISTRIBUTION: LORE COMPLIANT", "ARROYO/TEMPLE: 100% CANON"],
        "icon_type": "crosshair"
    },
    {
        "id": "hunting",
        "title": "HUNTING, HARVESTING & FIELD SURVIVAL",
        "category": "ОХОТА И ВЫЖИВАНИЕ",
        "badge": "РАЗДЕЛКА ДИЧИ",
        "version": "v2.0 SURVIVAL",
        "author": "EcCo Team, RPU",
        "theme": "green",
        "tagline": "Свежевание ножом: шкуры гекконов, мясо, хвосты скорпионов для противоядий и жарка мяса на кострах деревни",
        "specs": ["HARVESTING: MEAT, SKINS, TAILS", "CAMPFIRE COOKING: RESTORES HP", "SKILL SCALING: OUTDOORSMAN", "EARLY SURVIVAL: IMMERSIVE"],
        "icon_type": "shield"
    },
    {
        "id": "highwayman",
        "title": "HIGHWAYMAN OVERHAUL & TRUNK FIX",
        "category": "ТРАНСПОРТ",
        "badge": "АВТО ХАЙВЕЙМЕН",
        "version": "v3.2 OVERHAUL",
        "author": "phobos2077, sfall team",
        "theme": "cyan",
        "tagline": "Защита багажника от исчезновения вещей, оптимизация расхода ядерных батарей и тюнинг нагнетателя у Смитти",
        "specs": ["TRUNK BUG: COMPLETELY ELIMINATED", "FUEL CONSUMPTION: -30% REGULATOR", "SPEED BOOST: SMITTY BLOWER", "SAVE INTEGRITY: PROTECTED"],
        "icon_type": "engine"
    },
    {
        "id": "encounters",
        "title": "CURATED ENCOUNTERS & WORLD ENGINE",
        "category": "ГЛОБАЛЬНАЯ КАРТА",
        "badge": "БАЛАНС ВСТРЕЧ",
        "version": "v4.4.8 ENGINE FIX",
        "author": "Ray, sfall team, RPU",
        "theme": "blue",
        "tagline": "Полное устранение спама случайных встреч на современных процессорах: редкие, атмосферные встречи вместо засад каждые 2 секунды",
        "specs": ["ENCOUNTER SPAM: ELIMINATED (FIX=1)", "SPACING: CALIBRATED (RATE=7)", "OUTDOORSMAN CHECK: FULL CONTROL", "EXPANDED MAP: 890x720 NATIVE"],
        "icon_type": "worldmap"
    }
]

PALETTES = {
    "green": {
        "bg_top": (10, 22, 14),
        "bg_bot": (5, 12, 8),
        "accent": (0, 255, 102),
        "accent_dim": (20, 140, 60),
        "text_main": (230, 255, 235),
        "grid": (15, 45, 25)
    },
    "blue": {
        "bg_top": (8, 18, 28),
        "bg_bot": (4, 10, 16),
        "accent": (40, 190, 255),
        "accent_dim": (20, 100, 150),
        "text_main": (225, 245, 255),
        "grid": (15, 35, 55)
    },
    "amber": {
        "bg_top": (26, 18, 8),
        "bg_bot": (14, 9, 4),
        "accent": (255, 175, 40),
        "accent_dim": (150, 95, 20),
        "text_main": (255, 242, 220),
        "grid": (50, 35, 15)
    },
    "cyan": {
        "bg_top": (8, 24, 24),
        "bg_bot": (4, 12, 14),
        "accent": (0, 230, 210),
        "accent_dim": (15, 120, 110),
        "text_main": (220, 255, 250),
        "grid": (15, 45, 45)
    },
    "magenta": {
        "bg_top": (24, 10, 20),
        "bg_bot": (12, 5, 10),
        "accent": (255, 80, 170),
        "accent_dim": (140, 35, 90),
        "text_main": (255, 230, 245),
        "grid": (45, 18, 38)
    }
}

def draw_schematic_icon(draw, icon_type, cx, cy, size, color):
    """Draw technical isometric blueprint icon."""
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], outline=color, width=1)
    
    # Crosshairs
    draw.line([cx - r - 15, cy, cx + r + 15, cy], fill=color, width=1)
    draw.line([cx, cy - r - 15, cx, cy + r + 15], fill=color, width=1)
    
    if icon_type == "crosshair":
        draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], outline=color, width=2)
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=color, width=2)
    elif icon_type == "shield":
        points = [
            (cx, cy - 35),
            (cx + 30, cy - 20),
            (cx + 25, cy + 15),
            (cx, cy + 40),
            (cx - 25, cy + 15),
            (cx - 30, cy - 20),
        ]
        draw.polygon(points, outline=color, width=2)
        draw.line([cx, cy - 25, cx, cy + 30], fill=color, width=2)
    elif icon_type == "engine":
        for a in range(0, 360, 45):
            rad = math.radians(a)
            x1 = cx + math.cos(rad) * 20
            y1 = cy + math.sin(rad) * 20
            x2 = cx + math.cos(rad) * 45
            y2 = cy + math.sin(rad) * 45
            draw.line([x1, y1, x2, y2], fill=color, width=2)
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=color, width=3)
    elif icon_type == "display":
        draw.rectangle([cx - 40, cy - 28, cx + 40, cy + 22], outline=color, width=2)
        draw.line([cx - 15, cy + 22, cx - 25, cy + 38], fill=color, width=2)
        draw.line([cx + 15, cy + 22, cx + 25, cy + 38], fill=color, width=2)
        draw.line([cx - 30, cy + 38, cx + 30, cy + 38], fill=color, width=2)
    elif icon_type == "wave":
        for x in range(cx - 40, cx + 41, 5):
            h = int(math.sin((x - cx) * 0.15) * 25)
            draw.line([x, cy - h, x, cy + h], fill=color, width=2)
    else:
        draw.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], outline=color, width=2)
        draw.rectangle([cx - 18, cy - 18, cx + 18, cy + 18], outline=color, width=1)

def generate_poster(mod):
    w, h = 1200, 675
    pal = PALETTES.get(mod["theme"], PALETTES["green"])
    
    img = Image.new("RGB", (w, h), pal["bg_bot"])
    draw = ImageDraw.Draw(img)
    
    # 1. Background vertical gradient
    for y in range(h):
        t = y / float(h)
        r = int(pal["bg_top"][0] * (1 - t) + pal["bg_bot"][0] * t)
        g = int(pal["bg_top"][1] * (1 - t) + pal["bg_bot"][1] * t)
        b = int(pal["bg_top"][2] * (1 - t) + pal["bg_bot"][2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # 2. Isometric technical grid
    grid_col = pal["grid"]
    grid_size = 45
    for x in range(0, w, grid_size):
        draw.line([(x, 0), (x, h)], fill=grid_col, width=1)
    for y in range(0, h, grid_size):
        draw.line([(0, y), (w, y)], fill=grid_col, width=1)
        
    # 3. Outer viewport tech frame
    margin = 25
    draw.rectangle([margin, margin, w - margin, h - margin], outline=pal["accent_dim"], width=2)
    draw.rectangle([margin + 6, margin + 6, w - margin - 6, h - margin - 6], outline=pal["grid"], width=1)
    
    # Corner brackets (RobCo tactical display)
    corner_len = 35
    accent = pal["accent"]
    for (cx, cy, dx, dy) in [
        (margin, margin, 1, 1),
        (w - margin, margin, -1, 1),
        (margin, h - margin, 1, -1),
        (w - margin, h - margin, -1, -1)
    ]:
        draw.line([cx, cy, cx + dx * corner_len, cy], fill=accent, width=4)
        draw.line([cx, cy, cx, cy + dy * corner_len], fill=accent, width=4)
        
    # 4. Header Bar
    draw.rectangle([margin + 12, margin + 12, w - margin - 12, margin + 46], fill=(0, 0, 0, 180), outline=pal["accent_dim"], width=1)
    draw.text((margin + 24, margin + 18), "ROBCO INDUSTRIES (TM) // MODULE ARCHIVE SPECIFICATION", fill=accent)
    draw.text((w - margin - 260, margin + 18), f"REV. 2026 // {mod['version']}", fill=accent)
    
    # 5. Mod Badge & Category
    badge_x = margin + 30
    badge_y = margin + 70
    draw.rectangle([badge_x, badge_y, badge_x + 190, badge_y + 32], fill=accent)
    draw.text((badge_x + 12, badge_y + 8), f"● {mod['badge']}", fill=(10, 15, 10))
    
    draw.text((badge_x + 210, badge_y + 8), f"КАТЕГОРИЯ: {mod['category']}  |  АВТОР: {mod['author']}", fill=pal["accent_dim"])
    
    # 6. Main Title (Huge & Clean)
    title_y = badge_y + 46
    draw.text((badge_x, title_y), mod["title"], fill=pal["text_main"])
    draw.line([badge_x, title_y + 48, badge_x + 750, title_y + 48], fill=accent, width=2)
    
    # 7. Tagline description
    tagline_y = title_y + 65
    draw.text((badge_x, tagline_y), mod["tagline"], fill=(190, 215, 200))
    
    # 8. Technical Blueprint Box (Left bottom)
    box_x = badge_x
    box_y = tagline_y + 65
    box_w = 680
    box_h = 240
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=(0, 0, 0, 190), outline=pal["accent_dim"], width=1)
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 32], fill=(pal["bg_top"][0], pal["bg_top"][1], pal["bg_top"][2]))
    draw.text((box_x + 16, box_y + 8), "АРХИТЕКТУРНЫЕ ХАРАКТЕРИСТИКИ И ТЕЛЕМЕТРИЯ", fill=accent)
    
    spec_y = box_y + 46
    for i, spec in enumerate(mod["specs"]):
        draw.text((box_x + 24, spec_y + i * 40), f"[0{i+1}] {spec}", fill=pal["text_main"])
        draw.line([box_x + 24, spec_y + i * 40 + 24, box_x + box_w - 24, spec_y + i * 40 + 24], fill=pal["grid"], width=1)
        
    # 9. Right Blueprint Diagram Area
    diag_cx = w - margin - 230
    diag_cy = h // 2 + 30
    draw_schematic_icon(draw, mod["icon_type"], diag_cx, diag_cy, 220, accent)
    
    # Circular radar rings around diagram
    for rad_offset in [130, 150, 170]:
        draw.arc([diag_cx - rad_offset, diag_cy - rad_offset, diag_cx + rad_offset, diag_cy + rad_offset], 45, 135, fill=pal["accent_dim"], width=1)
        draw.arc([diag_cx - rad_offset, diag_cy - rad_offset, diag_cx + rad_offset, diag_cy + rad_offset], 225, 315, fill=pal["accent_dim"], width=1)
        
    draw.text((diag_cx - 95, diag_cy + 190), "DIAGNOSTIC TELEMETRY: PASS", fill=accent)
    draw.text((diag_cx - 75, diag_cy + 210), "VAULT-TEC SECURE SYSTEM", fill=pal["accent_dim"])
    
    # 10. Bottom Status Bar
    draw.rectangle([margin + 12, h - margin - 40, w - margin - 12, h - margin - 12], fill=(0, 0, 0, 210), outline=pal["accent_dim"], width=1)
    draw.text((margin + 24, h - margin - 32), "STATUS: VERIFIED OPTIMAL  |  INTEGRATION: 100% CLEAN  |  DIRECTOR'S CUT COMPLIANT", fill=accent)
    draw.text((w - margin - 220, h - margin - 32), "FALLOUT 2 ULTIMATE 2026", fill=pal["accent_dim"])
    
    # 11. Subtle Scanline overlay
    scanlines = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scanlines)
    for y in range(0, h, 3):
        sdraw.line([(0, y), (w, y)], fill=(0, 0, 0, 40))
        
    final_img = Image.alpha_composite(img.convert("RGBA"), scanlines)
    
    out_path = os.path.join(POSTER_DIR, f"{mod['id']}.png")
    final_img.save(out_path, "PNG")
    print(f"Generated poster: {out_path}")

def main():
    print(f"Generating {len(MODS_DATA)} cinema posters in {POSTER_DIR}...")
    for mod in MODS_DATA:
        generate_poster(mod)
    print("All 15 posters successfully created!")

if __name__ == "__main__":
    main()
