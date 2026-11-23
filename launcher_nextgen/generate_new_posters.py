import os
import math
from PIL import Image, ImageDraw, ImageFont

POSTER_DIR = os.path.join(os.path.dirname(__file__), "ui", "assets", "posters")
os.makedirs(POSTER_DIR, exist_ok=True)

PALETTES = {
    "green": {
        "bg_top": (10, 22, 14), "bg_bot": (5, 12, 8),
        "accent": (0, 255, 102), "accent_dim": (20, 140, 60),
        "text_main": (230, 255, 235), "grid": (15, 45, 25)
    },
    "blue": {
        "bg_top": (8, 18, 28), "bg_bot": (4, 10, 16),
        "accent": (40, 190, 255), "accent_dim": (20, 100, 150),
        "text_main": (225, 245, 255), "grid": (15, 35, 55)
    },
    "amber": {
        "bg_top": (26, 18, 8), "bg_bot": (14, 9, 4),
        "accent": (255, 175, 40), "accent_dim": (150, 95, 20),
        "text_main": (255, 242, 220), "grid": (50, 35, 15)
    },
    "cyan": {
        "bg_top": (8, 24, 24), "bg_bot": (4, 12, 14),
        "accent": (0, 230, 210), "accent_dim": (15, 120, 110),
        "text_main": (220, 255, 250), "grid": (15, 45, 45)
    },
    "magenta": {
        "bg_top": (24, 10, 20), "bg_bot": (12, 5, 10),
        "accent": (255, 80, 170), "accent_dim": (140, 35, 90),
        "text_main": (255, 230, 245), "grid": (45, 18, 38)
    }
}

def draw_schematic_icon(draw, icon_type, cx, cy, size, color):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], outline=color, width=1)
    draw.line([cx - r - 15, cy, cx + r + 15, cy], fill=color, width=1)
    draw.line([cx, cy - r - 15, cx, cy + r + 15], fill=color, width=1)
    
    if icon_type == "shield":
        points = [(cx, cy - 35), (cx + 30, cy - 20), (cx + 25, cy + 15), (cx, cy + 40), (cx - 25, cy + 15), (cx - 30, cy - 20)]
        draw.polygon(points, outline=color, width=2)
        draw.line([cx, cy - 25, cx, cy + 30], fill=color, width=2)
    elif icon_type == "wave":
        for x in range(cx - 40, cx + 41, 5):
            h = int(math.sin((x - cx) * 0.15) * 25)
            draw.line([x, cy - h, x, cy + h], fill=color, width=2)
    elif icon_type == "eye":
        draw.arc([cx - 40, cy - 20, cx + 40, cy + 20], 0, 180, fill=color, width=2)
        draw.arc([cx - 40, cy - 20, cx + 40, cy + 20], 180, 360, fill=color, width=2)
        draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=color, width=2)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
    elif icon_type == "display":
        draw.rectangle([cx - 40, cy - 28, cx + 40, cy + 22], outline=color, width=2)
        draw.line([cx - 15, cy + 22, cx - 25, cy + 38], fill=color, width=2)
        draw.line([cx + 15, cy + 22, cx + 25, cy + 38], fill=color, width=2)
        draw.line([cx - 30, cy + 38, cx + 30, cy + 38], fill=color, width=2)
    elif icon_type == "inventory":
        draw.rectangle([cx - 35, cy - 25, cx + 35, cy + 25], outline=color, width=2)
        draw.line([cx - 35, cy, cx + 35, cy], fill=color, width=1)
        draw.line([cx, cy - 25, cx, cy + 25], fill=color, width=1)
    elif icon_type == "crosshair":
        draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], outline=color, width=2)
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=color, width=2)
    elif icon_type == "flashlight":
        # Searchlight/Highlighter icon
        draw.polygon([(cx - 25, cy - 15), (cx + 25, cy - 35), (cx + 25, cy + 35), (cx - 25, cy + 15)], outline=color, width=2)
        draw.line([cx - 35, cy - 8, cx - 25, cy - 8], fill=color, width=3)
        draw.line([cx - 35, cy + 8, cx - 25, cy + 8], fill=color, width=3)
        draw.line([cx + 25, cy - 20, cx + 45, cy - 30], fill=color, width=1)
        draw.line([cx + 25, cy, cx + 50, cy], fill=color, width=1)
        draw.line([cx + 25, cy + 20, cx + 45, cy + 30], fill=color, width=1)
    else:
        draw.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], outline=color, width=2)

NEW_POSTERS = [
    {
        "id": "foxx_pack",
        "title": "FOXX REBUILD COMMUNITY PACK",
        "category": "КОМЬЮНИТИ",
        "badge": "ПАКЕТ ФОКСА",
        "version": "v19.03.26 ADAPT",
        "author": "Foxx (ReBuild) & genix106 Adapt",
        "theme": "amber",
        "tagline": "Комплекс проверенных фиксов из ReBuild: монтировка AleSiS, навигация EPA, 359 женских диалогов, анимации HMR01",
        "specs": ["GENDER DIALOGUES: 359 FILES", "CROWBAR FIX: 00000455.PRO", "EPA NAVMESH: CELL LINK FIXED", "HMR01 HERO: FULL ANIMATIONS"],
        "icon_type": "shield"
    },
    {
        "id": "wasteland_voices",
        "title": "WASTELAND VOICES // ГОЛОСА ПУСТОШИ",
        "category": "АТМОСФЕРА",
        "badge": "690+ РЕПЛИК",
        "version": "v1.0.0 STANDALONE",
        "author": "genix106 & Antigravity Lead Team",
        "theme": "green",
        "tagline": "Фоновый живой диалог во всех 23 поселениях Пустошей, реактивность на Силовую Броню, мутантов и низкий интеллект",
        "specs": ["SETTLEMENTS: ALL 23 CITIES", "REACTIVE CORPUS: 692 LINES", "POWER ARMOR & MUTANTS: REACTIVE", "MIRIA TRAVEL BANTER: 46 QUOTES"],
        "icon_type": "wave"
    },
    {
        "id": "dynamic_theft",
        "title": "DYNAMIC THEFT & WITNESS SYSTEM",
        "category": "В РАЗРАБОТКЕ",
        "badge": "ТЕСТ / R&D",
        "version": "v1.2.0 [ТЕСТИРОВАНИЕ]",
        "author": "genix106 & Antigravity Lead Team",
        "theme": "cyan",
        "tagline": "[В РАЗРАБОТКЕ] Fail-Forward стелс: 4 фазы тревоги вместо мгновенного агра города, спас-бросок Удачи 6+ и секторы обзора",
        "specs": ["STATUS: ISOLATED TESTING", "ALERT PHASES: 4 ESCALATION STEPS", "LUCK SAVE: LK 6+ DICE ROLL", "VISION CONE: 120 / 180 / 360 DEG"],
        "icon_type": "eye"
    },
    {
        "id": "resurrection_ui",
        "title": "DARK METAL HUD & WIDESCREEN WINGS",
        "category": "ВИЗУАЛ",
        "badge": "МЕТАЛЛ ИНТЕРФЕЙС",
        "version": "v2.0 WIDESCREEN",
        "author": "Resurrection Team, genix106 Adapt",
        "theme": "cyan",
        "tagline": "Стиль вороненой стали из Fallout Resurrection: 54 текстуры темного металла, 7 стилей широкоформатных крыльев 1080p-4K",
        "specs": ["DARK METAL HUD: 54 HD FRMS", "WIDESCREEN WINGS: 7 PRESETS", "SCALING: 1080P / 1440P / 4K", "PICTURE-PERFECT: ZERO GAPS"],
        "icon_type": "display"
    },
    {
        "id": "qol_interface",
        "title": "CONTAINER CLICK-OUT & HITBOX",
        "category": "В РАЗРАБОТКЕ",
        "badge": "ТЕСТ / QOL",
        "version": "v1.2 [ТЕСТИРОВАНИЕ]",
        "author": "genix106 & Antigravity Lead Team",
        "theme": "green",
        "tagline": "[В РАЗРАБОТКЕ] Закрытие сундуков кликом вне окна, хитбокс ГОТОВО на всю плашку, быстрый сбор пачек патронов и автозакрытие",
        "specs": ["STATUS: ТЕСТИРОВАНИЕ МЕХАНИКИ", "CLICK OUTSIDE: CLOSES WINDOW", "DONE HITBOX: 100% TEXT EXPANDED", "AUTO-CLOSE EMPTY: OPTIONAL"],
        "icon_type": "inventory"
    },
    {
        "id": "tactical_highlight",
        "title": "TACTICAL HIGHLIGHT & LOOT SCANNER",
        "category": "В РАЗРАБОТКЕ",
        "badge": "ТЕСТ / ПОДСВЕТКА",
        "version": "v1.0 [ТЕСТИРОВАНИЕ]",
        "author": "genix106 & Antigravity Lead Team",
        "theme": "amber",
        "tagline": "[В РАЗРАБОТКЕ] Настройка подсветки предметов, контейнеров и врагов: устранение статтеров, прямая видимость CheckLOS",
        "specs": ["STATUS: ТЕСТИРОВАНИЕ РЕЖИМОВ", "TARGET HIGHLIGHT: COMBAT TARGETS", "LOOT HIGHLIGHT: SHIFT HOTKEY", "LINE OF SIGHT: CHECKLOS NO-XRAY"],
        "icon_type": "flashlight"
    },
    {
        "id": "party_orders",
        "title": "PARTY ORDERS // ПРИКАЗЫ СПУТНИКАМ",
        "category": "СПУТНИКИ",
        "badge": "ГОРЯЧИЕ КЛАВИШИ",
        "version": "v1.4 ENHANCED",
        "author": "phobos2077, genix106 Config",
        "theme": "amber",
        "tagline": "Горячие клавиши для спутников: сбор разбросанного лута по Ctrl+T, смена калибра AP/JHP по Ctrl+B и быстрый хил",
        "specs": ["COLLECT LOOT: CTRL+T (T ISOLATED)", "AMMO SWAP: CTRL+B AP/JHP", "QUICK HEAL: INSTANT STIMPACKS", "COMBAT STANCES: DYNAMIC DISTANCE"],
        "icon_type": "crosshair"
    }
]

w, h = 1200, 675
for mod in NEW_POSTERS:
    pal = PALETTES.get(mod["theme"], PALETTES["green"])
    img = Image.new("RGB", (w, h), pal["bg_bot"])
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    for y in range(h):
        t = y / float(h)
        r = int(pal["bg_top"][0] * (1 - t) + pal["bg_bot"][0] * t)
        g = int(pal["bg_top"][1] * (1 - t) + pal["bg_bot"][1] * t)
        b = int(pal["bg_top"][2] * (1 - t) + pal["bg_bot"][2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Grid
    grid_col = pal["grid"]
    for x in range(0, w, 45):
        draw.line([(x, 0), (x, h)], fill=grid_col, width=1)
    for y in range(0, h, 45):
        draw.line([(0, y), (w, y)], fill=grid_col, width=1)
        
    # Outer frame
    margin = 25
    draw.rectangle([margin, margin, w - margin, h - margin], outline=pal["accent_dim"], width=2)
    draw.rectangle([margin + 6, margin + 6, w - margin - 6, h - margin - 6], outline=pal["grid"], width=1)
    
    accent = pal["accent"]
    for (cx, cy, dx, dy) in [(margin, margin, 1, 1), (w - margin, margin, -1, 1), (margin, h - margin, 1, -1), (w - margin, h - margin, -1, -1)]:
        draw.line([cx, cy, cx + dx * 35, cy], fill=accent, width=4)
        draw.line([cx, cy, cx, cy + dy * 35], fill=accent, width=4)
        
    # Header bar
    draw.rectangle([margin + 12, margin + 12, w - margin - 12, margin + 46], fill=(0, 0, 0, 180), outline=pal["accent_dim"], width=1)
    draw.text((margin + 24, margin + 18), "ROBCO INDUSTRIES (TM) // MODULE ARCHIVE SPECIFICATION", fill=accent)
    draw.text((w - margin - 260, margin + 18), f"REV. 2026 // {mod['version']}", fill=accent)
    
    # Badge
    badge_x = margin + 30
    badge_y = margin + 70
    draw.rectangle([badge_x, badge_y, badge_x + 190, badge_y + 32], fill=accent)
    draw.text((badge_x + 12, badge_y + 8), f"● {mod['badge']}", fill=(10, 15, 10))
    draw.text((badge_x + 210, badge_y + 8), f"КАТЕГОРИЯ: {mod['category']}  |  АВТОР: {mod['author']}", fill=pal["accent_dim"])
    
    # Title
    title_y = badge_y + 46
    draw.text((badge_x, title_y), mod["title"], fill=pal["text_main"])
    draw.line([badge_x, title_y + 48, badge_x + 750, title_y + 48], fill=accent, width=2)
    
    # Tagline
    tagline_y = title_y + 65
    draw.text((badge_x, tagline_y), mod["tagline"], fill=(190, 215, 200))
    
    # Specs Box
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
        
    # Schematic Icon
    diag_cx = w - margin - 230
    diag_cy = h // 2 + 30
    draw_schematic_icon(draw, mod["icon_type"], diag_cx, diag_cy, 220, accent)
    
    for rad_offset in [130, 150, 170]:
        draw.arc([diag_cx - rad_offset, diag_cy - rad_offset, diag_cx + rad_offset, diag_cy + rad_offset], 45, 135, fill=pal["accent_dim"], width=1)
        draw.arc([diag_cx - rad_offset, diag_cy - rad_offset, diag_cx + rad_offset, diag_cy + rad_offset], 225, 315, fill=pal["accent_dim"], width=1)
        
    draw.text((diag_cx - 95, diag_cy + 190), "DIAGNOSTIC TELEMETRY: PASS", fill=accent)
    draw.text((diag_cx - 75, diag_cy + 210), "VAULT-TEC SECURE SYSTEM", fill=pal["accent_dim"])
    
    # Bottom Status Bar
    draw.rectangle([margin + 12, h - margin - 40, w - margin - 12, h - margin - 12], fill=(0, 0, 0, 210), outline=pal["accent_dim"], width=1)
    draw.text((margin + 24, h - margin - 32), "STATUS: VERIFIED OPTIMAL  |  INTEGRATION: 100% CLEAN  |  DIRECTOR'S CUT COMPLIANT", fill=accent)
    draw.text((w - margin - 220, h - margin - 32), "FALLOUT 2 ULTIMATE 2026", fill=pal["accent_dim"])
    
    # Scanline overlay
    scanlines = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scanlines)
    for y in range(0, h, 3):
        sdraw.line([(0, y), (w, y)], fill=(0, 0, 0, 40))
        
    final_img = Image.alpha_composite(img.convert("RGBA"), scanlines)
    out_path = os.path.join(POSTER_DIR, f"{mod['id']}.png")
    final_img.save(out_path, "PNG")
    print("Generated:", out_path)

print("All new posters generated successfully!")
