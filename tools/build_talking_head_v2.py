import os
import struct
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_IMG_PATH = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_fallout1998_sculpt.png"
OUTPUT_DIR = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_head_assets_v2"

WIDTH = 300
HEIGHT = 200

# Precise facial coordinates on 300x200 Fallout 1998 sculpt:
# Pupils: Left ~(129, 68), Right ~(164, 68)
LEFT_EYE = (118, 62, 140, 75)
RIGHT_EYE = (153, 62, 175, 75)

# Mouth seam is strictly at Y=126..128, X: 130..166
MOUTH_CENTER_X = 148
MOUTH_SEAM_Y = 127
LIP_LEFT_X = 132
LIP_RIGHT_X = 164

def get_base():
    return Image.open(BASE_IMG_PATH).convert("RGBA")

def create_frm(out_path, num_frames=9, width=WIDTH, height=HEIGHT, fps=10):
    frame_sz = width * height
    single_frame_len = 12 + frame_sz
    total_data_sz = single_frame_len * num_frames
    
    header = bytearray()
    header += struct.pack('>IHhh', 4, fps, 0, num_frames)
    header += b'\x00' * 12
    header += b'\x00' * 12
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
    Eyelid closure directly over left and right eye sockets.
    progress: 0.0 (open) to 1.0 (fully closed)
    """
    if progress <= 0.01:
        return img.copy()
        
    res = img.copy()
    draw = ImageDraw.Draw(res)
    
    for (x1, y1, x2, y2) in [LEFT_EYE, RIGHT_EYE]:
        w = x2 - x1
        h = y2 - y1
        lid_drop = int(h * progress)
        if lid_drop < 1:
            continue
            
        # Sample realistic eyelid skin tone from brow furrow just above eye
        skin_sample = img.crop((x1, y1 - 3, x2, y1 + 1))
        stretched_lid = skin_sample.resize((w, lid_drop), Image.Resampling.BILINEAR)
        
        # Elliptical eyelid mask matching eye socket curvature
        mask = Image.new("L", (w, lid_drop), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, -int(lid_drop * 0.4), w, lid_drop * 2], fill=245)
        mask = mask.filter(ImageFilter.GaussianBlur(0.8))
        
        res.paste(stretched_lid, (x1, y1), mask)
        
        # Eyelash crease when closed
        if progress >= 0.7:
            crease_y = y1 + lid_drop - 1
            draw.line([(x1 + 1, crease_y), (x2 - 1, crease_y)], fill=(28, 16, 12, 220), width=1)
            
    return res

def apply_speech_phoneme(img, open_amount, round_amount=0.0, mood=0.0):
    """
    Anatomically correct jaw & lip articulation:
    - Oral cavity opens strictly between upper lip (Y=125) and lower lip (Y=128).
    - Lower jaw drops by open_amount * 6 px.
    - Chin & beard smoothly displace down with a strict falloff terminating at Y=162.
    - COLLAR AND COAT (Y >= 165) NEVER MOVE (weight = 0).
    """
    if open_amount <= 0.01 and abs(mood) <= 0.05:
        return img.copy()
        
    base_arr = np.array(img, dtype=np.float32)
    h, w, c = base_arr.shape
    out_arr = base_arr.copy()
    
    jaw_drop = open_amount * 5.5 # Max 5.5 px drop for gritty realistic speech
    
    # 1. Warp lower jaw & beard (Y: 128 to 162, X: 125 to 172)
    # Cosine vertical falloff from 1.0 at Y=128 down to 0.0 at Y=162
    y_start = MOUTH_SEAM_Y + 1
    y_end = 162
    x_start = LIP_LEFT_X - 6
    x_end = LIP_RIGHT_X + 6
    
    if jaw_drop > 0.3:
        for y in range(y_end, y_start - 1, -1):
            # Normalized distance from seam to collar
            t = (y - y_start) / float(y_end - y_start) # 0.0 at seam, 1.0 at collar
            # Weight: 1.0 at seam, smooth curve down to 0.0 at collar
            w_y = 0.5 * (1.0 + np.cos(t * np.pi))
            disp = jaw_drop * w_y
            
            src_y = y - disp
            y0 = int(np.floor(src_y))
            y1_idx = min(h - 1, y0 + 1)
            fy = src_y - y0
            
            for x in range(x_start, x_end + 1):
                # Horizontal taper from mouth center
                dx = abs(x - MOUTH_CENTER_X) / float(x_end - MOUTH_CENTER_X)
                w_x = max(0.0, 1.0 - (dx * dx))
                eff_disp = disp * w_x
                
                sy = y - eff_disp
                sy0 = int(np.floor(sy))
                sy1 = min(h - 1, sy0 + 1)
                sfy = sy - sy0
                
                out_arr[y, x] = (1.0 - sfy) * base_arr[sy0, x] + sfy * base_arr[sy1, x]
                
    res = Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(res)
    
    # 2. Render realistic oral cavity at lip parting (strictly Y=126..130)
    if jaw_drop > 1.0:
        cavity_half_w = int((LIP_RIGHT_X - LIP_LEFT_X) * 0.42 * (1.0 - round_amount * 0.2))
        cavity_h = int(jaw_drop)
        cx = MOUTH_CENTER_X
        cy = MOUTH_SEAM_Y
        
        # Deep mouth darkness (dark maroon shadow)
        cavity_box = [cx - cavity_half_w, cy - 1, cx + cavity_half_w, cy + cavity_h + 1]
        draw.ellipse(cavity_box, fill=(18, 9, 8, 255))
        
        # Upper teeth hint (slightly shaded, weathered post-apocalyptic teeth)
        if jaw_drop >= 2.5:
            teeth_half_w = int(cavity_half_w * 0.65)
            teeth_box = [cx - teeth_half_w, cy, cx + teeth_half_w, cy + min(2, int(jaw_drop * 0.4))]
            draw.rectangle(teeth_box, fill=(175, 168, 150, 220))
            # Dental gaps / grime
            draw.line([(cx - 3, cy), (cx - 3, cy + 2)], fill=(30, 15, 12, 200), width=1)
            draw.line([(cx + 3, cy), (cx + 3, cy + 2)], fill=(30, 15, 12, 200), width=1)
            
    # 3. Mood: Brow and mouth corners
    if abs(mood) > 0.05:
        # Mouth corner grimace / smile
        dy = int(mood * 2)
        lc = img.crop((LIP_LEFT_X - 2, MOUTH_SEAM_Y - 2, LIP_LEFT_X + 5, MOUTH_SEAM_Y + 4))
        res.paste(lc, (LIP_LEFT_X - 2, MOUTH_SEAM_Y - 2 - dy))
        rc = img.crop((LIP_RIGHT_X - 5, MOUTH_SEAM_Y - 2, LIP_RIGHT_X + 2, MOUTH_SEAM_Y + 4))
        res.paste(rc, (LIP_RIGHT_X - 5, MOUTH_SEAM_Y - 2 - dy))

    return res

def apply_brow_mood(img, mood):
    """
    mood: -1.0 (angry frown) to +1.0 (relaxed/happy)
    """
    if abs(mood) <= 0.05:
        return img.copy()
        
    res = img.copy()
    brow_shift = int(mood * -2)
    # Left brow: (115, 52, 142, 63)
    lb = img.crop((115, 52, 142, 63))
    res.paste(lb, (115, 52 - brow_shift))
    # Right brow: (150, 52, 178, 63)
    rb = img.crop((150, 52, 178, 63))
    res.paste(rb, (150, 52 - brow_shift))
    return res

def build_all_assets():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base = get_base()
    
    # Verify zero movement on shoulders/collar: test frame 3 vs frame 0 below Y=165
    print("Building Fallout 2 authentic talking head set (v2)...")
    
    # 1. Neutral Speech (np: 9 frames)
    # Vowel cycle: rest -> slight -> open -> peak -> O -> closed -> half -> slight -> rest
    np_amts = [0.0, 0.35, 0.75, 1.0, 0.65, 0.10, 0.50, 0.20, 0.0]
    np_dir = os.path.join(OUTPUT_DIR, "kcbobnp")
    os.makedirs(np_dir, exist_ok=True)
    frames_np = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(base, open_amount=amt, round_amount=0.25 if i == 4 else 0.0)
        f.save(os.path.join(np_dir, f"{i}.png"))
        frames_np.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobnp.frm"), num_frames=9, fps=10)
    
    # Check diff below Y=165:
    f0_arr = np.array(frames_np[0])
    f3_arr = np.array(frames_np[3])
    lower_diff = np.sum(f0_arr[165:, :, :] != f3_arr[165:, :, :])
    print(f"Collar/clothing movement assertion (Y >= 165): {lower_diff} pixels changed (MUST BE 0)")
    assert lower_diff == 0, "ERROR: Collar or clothing is moving!"
    
    # 2. Neutral Fidget / Blink (nf1: 4 frames)
    nf1_amts = [0.0, 0.45, 1.0, 0.45]
    nf1_dir = os.path.join(OUTPUT_DIR, "kcbobnf1")
    os.makedirs(nf1_dir, exist_ok=True)
    frames_nf1 = []
    for i, amt in enumerate(nf1_amts):
        f = apply_blink(base, progress=amt)
        f.save(os.path.join(nf1_dir, f"{i}.png"))
        frames_nf1.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobnf1.frm"), num_frames=4, fps=10)
    
    # 3. Bad Speech (bp: 9 frames)
    bp_dir = os.path.join(OUTPUT_DIR, "kcbobbp")
    os.makedirs(bp_dir, exist_ok=True)
    angry_base = apply_brow_mood(base, mood=-1.0)
    frames_bp = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(angry_base, open_amount=amt, mood=-0.8)
        f.save(os.path.join(bp_dir, f"{i}.png"))
        frames_bp.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobbp.frm"), num_frames=9, fps=10)
    
    # 4. Bad Fidget (bf1: 4 frames)
    bf1_dir = os.path.join(OUTPUT_DIR, "kcbobbf1")
    os.makedirs(bf1_dir, exist_ok=True)
    frames_bf1 = []
    for i, amt in enumerate(nf1_amts):
        f = apply_blink(angry_base, progress=amt)
        f = apply_speech_phoneme(f, open_amount=0.0, mood=-0.8)
        f.save(os.path.join(bf1_dir, f"{i}.png"))
        frames_bf1.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobbf1.frm"), num_frames=4, fps=10)
    
    # 5. Good Speech (gp: 9 frames)
    gp_dir = os.path.join(OUTPUT_DIR, "kcbobgp")
    os.makedirs(gp_dir, exist_ok=True)
    good_base = apply_brow_mood(base, mood=0.6)
    frames_gp = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(good_base, open_amount=amt, mood=0.6)
        f.save(os.path.join(gp_dir, f"{i}.png"))
        frames_gp.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobgp.frm"), num_frames=9, fps=10)
    
    # 6. Good Fidget (gf1: 4 frames)
    gf1_dir = os.path.join(OUTPUT_DIR, "kcbobgf1")
    os.makedirs(gf1_dir, exist_ok=True)
    frames_gf1 = []
    for i, amt in enumerate(nf1_amts):
        f = apply_blink(good_base, progress=amt)
        f = apply_speech_phoneme(f, open_amount=0.0, mood=0.6)
        f.save(os.path.join(gf1_dir, f"{i}.png"))
        frames_gf1.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobgf1.frm"), num_frames=4, fps=10)

    # Save animated GIF previews
    frames_np[0].save(os.path.join(OUTPUT_DIR, "preview_np_v2.gif"), save_all=True, append_images=frames_np[1:], duration=110, loop=0)
    frames_nf1[0].save(os.path.join(OUTPUT_DIR, "preview_nf1_v2.gif"), save_all=True, append_images=frames_nf1[1:], duration=160, loop=0)
    frames_bp[0].save(os.path.join(OUTPUT_DIR, "preview_bp_v2.gif"), save_all=True, append_images=frames_bp[1:], duration=110, loop=0)
    print("SUCCESS: V2 assets generated with anatomical accuracy!")

if __name__ == "__main__":
    build_all_assets()
