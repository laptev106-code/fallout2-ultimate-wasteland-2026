import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

def create_remaster_icon():
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2
    
    # 1. Outer Vault Gear (Шестеренка Убежища Волт-Тек)
    gear_outer_r = 236
    gear_inner_r = 205
    teeth_count = 12
    
    gear_points = []
    for i in range(teeth_count):
        angle_base = i * (2 * math.pi / teeth_count)
        a1 = angle_base - (math.pi / (teeth_count * 3))
        a2 = angle_base + (math.pi / (teeth_count * 3))
        a3 = angle_base + (2 * math.pi / (teeth_count * 2)) - (math.pi / (teeth_count * 3))
        a4 = angle_base + (2 * math.pi / (teeth_count * 2)) + (math.pi / (teeth_count * 3))
        
        gear_points.append((center + gear_outer_r * math.cos(a1), center + gear_outer_r * math.sin(a1)))
        gear_points.append((center + gear_outer_r * math.cos(a2), center + gear_outer_r * math.sin(a2)))
        gear_points.append((center + gear_inner_r * math.cos(a3), center + gear_inner_r * math.sin(a3)))
        gear_points.append((center + gear_inner_r * math.cos(a4), center + gear_inner_r * math.sin(a4)))
        
    # Drop shadow
    shadow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_points = [(x + 4, y + 8) for x, y in gear_points]
    s_draw.polygon(s_points, fill=(0, 0, 0, 180))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(shadow_img)
    
    # Dark titanium gear body
    draw.polygon(gear_points, fill=(20, 26, 23, 255), outline=(50, 65, 58, 255))
    
    # Dual-Engine neon halo on gear edges:
    # Left: emerald green (sfall Gameplay), Right: amber gold (Dustlight HD)
    for p1, p2 in zip(gear_points, gear_points[1:] + [gear_points[0]]):
        mid_x = (p1[0] + p2[0]) / 2
        edge_col = (0, 240, 110, 230) if mid_x < center else (255, 180, 20, 230)
        draw.line([p1, p2], fill=edge_col, width=3)
        
    # Inner circular bezel
    inner_bezel_r = 192
    draw.ellipse([center - inner_bezel_r, center - inner_bezel_r, center + inner_bezel_r, center + inner_bezel_r], 
                 fill=(12, 16, 14, 255), outline=(190, 160, 50, 255), width=4)
                 
    # Brass rivets
    for i in range(teeth_count):
        a = i * (2 * math.pi / teeth_count)
        rx = center + 184 * math.cos(a)
        ry = center + 184 * math.sin(a)
        draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=(220, 185, 75, 255), outline=(40, 30, 10, 255))

    # 2. CRT Screen Interior
    screen_r = 175
    screen_mask = Image.new("L", (size, size), 0)
    sm_draw = ImageDraw.Draw(screen_mask)
    sm_draw.ellipse([center - screen_r, center - screen_r, center + screen_r, center + screen_r], fill=255)
    
    crt_bg = Image.new("RGBA", (size, size), (4, 10, 6, 255))
    crt_draw = ImageDraw.Draw(crt_bg)
    
    # Dual radial glow (green left, amber right)
    for r in range(screen_r, 0, -6):
        intensity = int(85 * (1.0 - (r / screen_r)))
        crt_draw.ellipse([center - r, center - r, center + r, center + r], 
                         fill=(0, int(intensity * 1.6), int(intensity * 0.9), int(intensity * 1.3)))
                         
    # Scanlines
    for y in range(center - screen_r, center + screen_r, 3):
        crt_draw.line([(center - screen_r, y), (center + screen_r, y)], fill=(0, 255, 120, 20), width=1)
        
    img.paste(crt_bg, (0, 0), screen_mask)

    # 3. Vault Boy Figure
    vb_crop_path = "tools/test_vb_crop.png"
    if os.path.exists(vb_crop_path):
        vb = Image.open(vb_crop_path).convert("RGBA")
        
        target_h = int(screen_r * 1.88)
        scale_fac = target_h / vb.height
        target_w = int(vb.width * scale_fac)
        vb_scaled = vb.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        vx = center - target_w // 2 - 4
        vy = center - target_h // 2 + 12
        
        r, g, b, a = vb_scaled.split()
        g_enh = ImageEnhance.Brightness(g).enhance(1.25)
        vb_colored = Image.merge("RGBA", (r, g_enh, b, a))
        
        # Emerald glow
        glow_mask = a.filter(ImageFilter.GaussianBlur(10))
        glow_layer = Image.new("RGBA", (target_w, target_h), (0, 255, 130, 190))
        img.paste(glow_layer, (vx, vy), glow_mask)
        
        # Paste Vault Boy
        img.alpha_composite(vb_colored, (vx, vy))
        
        # 4. Precision Badass Aviator Sunglasses
        # Eyes in original crop are at x=345..440, y=160..195
        # Scale to placed coordinates:
        fx = vx + int(target_w * (390 / 667)) # center of face
        fy = vy + int(target_h * (182 / 657)) # eye line
        
        glass_w = int(target_w * 0.28) # total width
        glass_h = int(target_h * 0.11) # height
        
        glass_overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glass_overlay)
        
        lens_w = glass_w // 2 - 2
        # Left Lens (viewer's left eye)
        lx1 = fx - glass_w // 2
        ly1 = fy - glass_h // 2
        lx2 = lx1 + lens_w
        ly2 = ly1 + glass_h
        
        # Right Lens (viewer's right eye)
        rx1 = fx + 3
        ry1 = fy - glass_h // 2
        rx2 = rx1 + lens_w
        ry2 = ry1 + glass_h
        
        # Draw curved aviator lenses with gold trim
        g_draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=8, fill=(10, 16, 12, 250), outline=(220, 185, 60, 255), width=2)
        g_draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=8, fill=(10, 16, 12, 250), outline=(220, 185, 60, 255), width=2)
        
        # Bridge connecting lenses
        g_draw.line([(lx2, fy - 3), (rx1, fy - 3)], fill=(240, 200, 70, 255), width=3)
        g_draw.line([(lx2, fy + 3), (rx1, fy + 3)], fill=(200, 160, 50, 255), width=2)
        
        # HUD reflection on sunglasses: green Pip-Boy telemetry
        g_draw.line([(lx1 + 4, fy), (lx2 - 4, fy)], fill=(0, 255, 140, 210), width=1)
        g_draw.line([(rx1 + 4, fy), (rx2 - 4, fy)], fill=(0, 255, 140, 210), width=1)
        # Tactical targeting reticle dots
        g_draw.ellipse([lx1 + lens_w//2 - 2, fy - 2, lx1 + lens_w//2 + 2, fy + 2], fill=(0, 255, 220, 255))
        g_draw.ellipse([rx1 + lens_w//2 - 2, fy - 2, rx1 + lens_w//2 + 2, fy + 2], fill=(0, 255, 220, 255))
        
        # Lens specular shine
        g_draw.line([(lx1 + 6, ly1 + 3), (lx1 + 16, ly1 + 3)], fill=(255, 255, 255, 120), width=1)
        g_draw.line([(rx1 + 6, ry1 + 3), (rx1 + 16, ry1 + 3)], fill=(255, 255, 255, 120), width=1)
        
        img.alpha_composite(glass_overlay)

    # 5. Bottom Vault-Tec Badge: "FALLOUT 2.5 // DEFINITIVE EDITION"
    badge_w = 200
    badge_h = 44
    badge_x = center - badge_w // 2
    badge_y = size - 72
    
    badge_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge_img)
    # Shadow
    b_draw.rounded_rectangle([badge_x + 2, badge_y + 3, badge_x + badge_w + 2, badge_y + badge_h + 3], radius=6, fill=(0, 0, 0, 180))
    # Plate
    b_draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=6, fill=(16, 22, 18, 255), outline=(220, 180, 50, 255), width=2)
    
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arialbd.ttf", 10)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    b_draw.text((center, badge_y + 14), "FALLOUT 2.5", fill=(0, 255, 130, 255), font=font_main, anchor="mm")
    b_draw.text((center, badge_y + 31), "DEFINITIVE EDITION", fill=(255, 195, 45, 255), font=font_sub, anchor="mm")
    
    img.alpha_composite(badge_img)

    # 6. Save outputs
    out_png = "launcher_nextgen/ui/assets/app_icon.png"
    out_ico = "launcher_nextgen/ui/assets/app_icon.ico"
    
    img.save(out_png, "PNG")
    print(f"Saved PNG icon: {out_png}")
    
    ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(out_ico, format="ICO", sizes=ico_sizes)
    print(f"Saved Windows ICO: {out_ico}")
    
    # Copy to assets root
    os.makedirs("assets", exist_ok=True)
    img.save("assets/app_icon.ico", format="ICO", sizes=ico_sizes)
    img.save("assets/app_icon.png", "PNG")
    
    # Copy to artifact folder for immediate visual preview
    art_path = r"C:\Users\Геннадий\.gemini\antigravity\brain\a3e3fb8b-370c-4ec1-90c9-bd8542c080cd\app_icon_remaster.png"
    shutil.copy2(out_png, art_path)
    print("Copied to artifact dir")

if __name__ == "__main__":
    create_remaster_icon()
