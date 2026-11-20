import os
import struct
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_IMG_PATH = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_base_300x200.png"
OUTPUT_DIR = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_head_assets"

# Target resolution
WIDTH = 300
HEIGHT = 200

# Landmark approximations on 300x200 image
LEFT_EYE_BOX = (112, 64, 136, 78)   # (x1, y1, x2, y2)
RIGHT_EYE_BOX = (144, 64, 168, 78)
MOUTH_BOX = (126, 120, 168, 146)
MOUTH_LINE_Y = 126

def get_base():
    return Image.open(BASE_IMG_PATH).convert("RGBA")

def create_frm(out_path, num_frames=9, width=WIDTH, height=HEIGHT, fps=10):
    frame_sz = width * height
    single_frame_len = 12 + frame_sz
    total_data_sz = single_frame_len * num_frames
    
    header = bytearray()
    header += struct.pack('>IHhh', 4, fps, 0, num_frames)
    header += b'\x00' * 12 # shift_x (6 * 2)
    header += b'\x00' * 12 # shift_y (6 * 2)
    header += struct.pack('>IIIIII', 62, 0, 0, 0, 0, 0)
    header += struct.pack('>I', total_data_sz)
    
    with open(out_path, 'wb') as f:
        f.write(header)
        for i in range(num_frames):
            frame_hdr = struct.pack('>HHIhh', width, height, frame_sz, 0, 0)
            f.write(frame_hdr)
            f.write(b'\x00' * frame_sz)

def apply_blink(img, progress):
    """
    progress: 0.0 (open) to 1.0 (fully closed)
    """
    if progress <= 0.01:
        return img.copy()
    
    res = img.copy()
    draw = ImageDraw.Draw(res)
    
    # Process both eyes
    for box in [LEFT_EYE_BOX, RIGHT_EYE_BOX]:
        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        
        # Upper eyelid descends
        lid_drop = int(h * progress)
        if lid_drop < 1:
            continue
            
        # Sample eyelid skin tone from just above the eye
        skin_sample = img.crop((x1, max(0, y1 - 4), x2, y1 + 1))
        # Stretch skin tone downward
        stretched_skin = skin_sample.resize((w, lid_drop), Image.Resampling.BILINEAR)
        
        # Soft mask for eyelid
        mask = Image.new("L", (w, lid_drop), 0)
        mask_draw = ImageDraw.Draw(mask)
        # Elliptical eyelid shape
        mask_draw.ellipse([0, -int(lid_drop*0.5), w, lid_drop * 2], fill=240)
        mask = mask.filter(ImageFilter.GaussianBlur(1.0))
        
        res.paste(stretched_skin, (x1, y1), mask)
        
        # If nearly closed, draw lash line
        if progress >= 0.7:
            lash_y = y1 + lid_drop
            draw.line([(x1 + 1, lash_y), (x2 - 1, lash_y)], fill=(35, 20, 15, 200), width=1)
            
    return res

def apply_mouth_phoneme(img, open_amount, round_amount=0.0, mood=0.0):
    """
    open_amount: 0.0 (closed) to 1.0 (wide open)
    round_amount: 0.0 to 1.0 (corners pulled inward for 'O')
    mood: -1.0 (angry grimace) to +1.0 (smile)
    """
    if open_amount <= 0.01 and abs(mood) <= 0.05:
        return img.copy()
        
    res = img.copy()
    x1, y1, x2, y2 = MOUTH_BOX
    w = x2 - x1
    h = y2 - y1
    
    # 1. Lower jaw displacement
    jaw_drop = int(open_amount * 8) # Max 8px drop for realistic dialogue
    
    if jaw_drop > 0:
        # Lower lip and chin patch
        chin_top = MOUTH_LINE_Y
        chin_h = y2 - chin_top
        chin_patch = img.crop((x1, chin_top, x2, y2 + 10))
        
        # Inner mouth cavity
        mouth_cx = (x1 + x2) // 2
        mouth_cy = MOUTH_LINE_Y + (jaw_drop // 2)
        cavity_w = int((w * 0.6) * (1.0 - round_amount * 0.25))
        cavity_h = max(2, jaw_drop + 2)
        
        # Draw dark oral cavity behind
        cavity_rect = [
            mouth_cx - cavity_w // 2,
            MOUTH_LINE_Y,
            mouth_cx + cavity_w // 2,
            MOUTH_LINE_Y + jaw_drop + 3
        ]
        draw = ImageDraw.Draw(res)
        # Deep mouth shadow
        draw.ellipse(cavity_rect, fill=(18, 8, 8, 255))
        
        # Teeth hint if open sufficiently
        if jaw_drop >= 3:
            teeth_w = int(cavity_w * 0.7)
            teeth_rect = [
                mouth_cx - teeth_w // 2,
                MOUTH_LINE_Y,
                mouth_cx + teeth_w // 2,
                MOUTH_LINE_Y + min(3, jaw_drop // 2)
            ]
            draw.rectangle(teeth_rect, fill=(190, 185, 175, 220))
            # Shading between teeth
            draw.line([(mouth_cx, MOUTH_LINE_Y), (mouth_cx, MOUTH_LINE_Y + 2)], fill=(40, 20, 20, 180), width=1)
            
        # Paste displaced lower lip and chin with feathered alpha mask
        chin_mask = Image.new("L", (w, chin_h + 10), 255)
        chin_draw = ImageDraw.Draw(chin_mask)
        chin_draw.rectangle([0, 0, w, 2], fill=0)
        chin_mask = chin_mask.filter(ImageFilter.GaussianBlur(1.2))
        
        res.paste(chin_patch, (x1, chin_top + jaw_drop), chin_mask)
        
    # Mood adjustments (smile / frown on mouth corners)
    if abs(mood) > 0.05:
        corner_dy = int(mood * 2) # +2 for smile, -2 for grimace
        # Left corner
        lc = img.crop((x1 - 2, MOUTH_LINE_Y - 2, x1 + 6, MOUTH_LINE_Y + 4))
        res.paste(lc, (x1 - 2, MOUTH_LINE_Y - 2 - corner_dy))
        # Right corner
        rc = img.crop((x2 - 6, MOUTH_LINE_Y - 2, x2 + 2, MOUTH_LINE_Y + 4))
        res.paste(rc, (x2 - 6, MOUTH_LINE_Y - 2 - corner_dy))

    return res

def apply_eyebrow_mood(img, mood):
    """
    mood: -1.0 (angry frown) to +1.0 (relaxed/happy)
    """
    if abs(mood) <= 0.05:
        return img.copy()
        
    res = img.copy()
    # Eyebrow vertical shifts
    brow_y_shift = int(mood * -2) # Angry = brows drop 2px
    
    # Left brow patch
    lb = img.crop((110, 56, 138, 66))
    res.paste(lb, (110, 56 - brow_y_shift))
    
    # Right brow patch
    rb = img.crop((142, 56, 170, 66))
    res.paste(rb, (142, 56 - brow_y_shift))
    
    return res

def generate_talking_head_set(base_img, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    states = {
        # name: (folder_name, num_frames, generator_func)
        "np": ("kcbobnp", 9),
        "nf1": ("kcbobnf1", 4),
        "bp": ("kcbobbp", 9),
        "bf1": ("kcbobbf1", 4),
        "gp": ("kcbobgp", 9),
        "gf1": ("kcbobgf1", 4),
    }
    
    # 1. Neutral Speech Loop (np: 9 frames)
    # Phoneme curve: 0 -> 0.3 -> 0.7 -> 1.0 -> 0.6 -> 0.1 -> 0.5 -> 0.2 -> 0
    np_amounts = [0.0, 0.35, 0.75, 1.0, 0.60, 0.10, 0.50, 0.20, 0.0]
    np_dir = os.path.join(out_dir, "kcbobnp")
    os.makedirs(np_dir, exist_ok=True)
    frames_np = []
    for i, amt in enumerate(np_amounts):
        f = apply_mouth_phoneme(base_img, open_amount=amt, round_amount=0.2 if i == 4 else 0.0, mood=0.0)
        f.save(os.path.join(np_dir, f"{i}.png"))
        frames_np.append(f)
    create_frm(os.path.join(out_dir, "kcbobnp.frm"), num_frames=9, fps=10)
    
    # 2. Neutral Fidget / Blink (nf1: 4 frames)
    # Blink curve: open -> half -> closed -> half
    nf1_amounts = [0.0, 0.45, 1.0, 0.45]
    nf1_dir = os.path.join(out_dir, "kcbobnf1")
    os.makedirs(nf1_dir, exist_ok=True)
    frames_nf1 = []
    for i, amt in enumerate(nf1_amounts):
        f = apply_blink(base_img, progress=amt)
        f.save(os.path.join(nf1_dir, f"{i}.png"))
        frames_nf1.append(f)
    create_frm(os.path.join(out_dir, "kcbobnf1.frm"), num_frames=4, fps=10)
    
    # 3. Bad Speech Loop (bp: 9 frames)
    bp_dir = os.path.join(out_dir, "kcbobbp")
    os.makedirs(bp_dir, exist_ok=True)
    angry_base = apply_eyebrow_mood(base_img, mood=-1.0)
    frames_bp = []
    for i, amt in enumerate(np_amounts):
        f = apply_mouth_phoneme(angry_base, open_amount=amt, mood=-0.8)
        f.save(os.path.join(bp_dir, f"{i}.png"))
        frames_bp.append(f)
    create_frm(os.path.join(out_dir, "kcbobbp.frm"), num_frames=9, fps=10)
    
    # 4. Bad Fidget / Blink (bf1: 4 frames)
    bf1_dir = os.path.join(out_dir, "kcbobbf1")
    os.makedirs(bf1_dir, exist_ok=True)
    frames_bf1 = []
    for i, amt in enumerate(nf1_amounts):
        f = apply_blink(angry_base, progress=amt)
        f = apply_mouth_phoneme(f, open_amount=0.0, mood=-0.8)
        f.save(os.path.join(bf1_dir, f"{i}.png"))
        frames_bf1.append(f)
    create_frm(os.path.join(out_dir, "kcbobbf1.frm"), num_frames=4, fps=10)
    
    # 5. Good Speech Loop (gp: 9 frames)
    gp_dir = os.path.join(out_dir, "kcbobgp")
    os.makedirs(gp_dir, exist_ok=True)
    good_base = apply_eyebrow_mood(base_img, mood=0.6)
    frames_gp = []
    for i, amt in enumerate(np_amounts):
        f = apply_mouth_phoneme(good_base, open_amount=amt, mood=0.6)
        f.save(os.path.join(gp_dir, f"{i}.png"))
        frames_gp.append(f)
    create_frm(os.path.join(out_dir, "kcbobgp.frm"), num_frames=9, fps=10)
    
    # 6. Good Fidget / Blink (gf1: 4 frames)
    gf1_dir = os.path.join(out_dir, "kcbobgf1")
    os.makedirs(gf1_dir, exist_ok=True)
    frames_gf1 = []
    for i, amt in enumerate(nf1_amounts):
        f = apply_blink(good_base, progress=amt)
        f = apply_mouth_phoneme(f, open_amount=0.0, mood=0.6)
        f.save(os.path.join(gf1_dir, f"{i}.png"))
        frames_gf1.append(f)
    create_frm(os.path.join(out_dir, "kcbobgf1.frm"), num_frames=4, fps=10)

    # Save animated preview GIFs for quick visual verification
    frames_np[0].save(os.path.join(out_dir, "preview_np.gif"), save_all=True, append_images=frames_np[1:], duration=100, loop=0)
    frames_nf1[0].save(os.path.join(out_dir, "preview_nf1.gif"), save_all=True, append_images=frames_nf1[1:], duration=150, loop=0)
    frames_bp[0].save(os.path.join(out_dir, "preview_bp.gif"), save_all=True, append_images=frames_bp[1:], duration=100, loop=0)
    print("All 6 animation sets and FRM containers generated successfully in:", out_dir)

if __name__ == "__main__":
    base = get_base()
    generate_talking_head_set(base, OUTPUT_DIR)
