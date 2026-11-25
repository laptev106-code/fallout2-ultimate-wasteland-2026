import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_poster = r"E:\FALLOUT Ult pjt\launcher_nextgen\ui\assets\posters\community_fixes.png"
out_poster = r"E:\FALLOUT Ult pjt\launcher_nextgen\ui\assets\posters\master_patch.png"

img = Image.open(base_poster).convert("RGBA")
W, H = img.size

# Create a sleek dark overlay for the poster
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Add Pip-Boy CRT grid lines and dark tint at the bottom
for y in range(0, H, 4):
    draw.line([(0, y), (W, y)], fill=(0, 20, 10, 15))

# Dark vignette / panel at the bottom
draw.rectangle([(0, H - 240), (W, H)], fill=(10, 20, 15, 230))
draw.line([(0, H - 240), (W, H - 240)], fill=(0, 255, 128, 200), width=3)
draw.line([(0, H - 235), (W, H - 235)], fill=(0, 255, 128, 80), width=1)

# Badge: TOP PRIORITY CUMULATIVE VFS LAYER
draw.rectangle([(40, H - 220), (460, H - 180)], fill=(0, 80, 40, 220), outline=(0, 255, 128, 255), width=2)

try:
    font_badge = ImageFont.truetype("arialbd.ttf", 22)
    font_title = ImageFont.truetype("arialbd.ttf", 46)
    font_sub = ImageFont.truetype("arial.ttf", 24)
except:
    font_badge = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

draw.text((55, H - 213), "MASTER PATCH ARCHITECTURE // 2026", fill=(0, 255, 128, 255), font=font_badge)
draw.text((40, H - 165), "ULTIMATE WASTELAND CUMULATIVE PATCH", fill=(255, 255, 255, 255), font=font_title)
draw.text((40, H - 105), "Единый монолитный пакет: Скрипты, Диалоги, Баланс, Двуязычный лог, Плавный UI", fill=(0, 230, 140, 255), font=font_sub)
draw.text((40, H - 70), "Автоматический монтаж в наивысший приоритет VFS (mods/rpu_russian_uncensored.dat)", fill=(160, 180, 170, 255), font=font_sub)

final_img = Image.alpha_composite(img, overlay)
final_img.save(out_poster, "PNG")
print("SUCCESS: Created", out_poster)
