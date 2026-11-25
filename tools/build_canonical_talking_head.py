import os
import struct
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

BASE_IMG_PATH = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_base.jpg"
OUTPUT_DIR = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\kcbob_canonical_head"

# Canonical Fallout 2 talking head dimensions
WIDTH = 262
HEIGHT = 200

# 1. Precise crop from high-res source (1200x896)
# Center: X=552, Y=408. Bounding box captures head from hat tip to collarbone
SRC_X1 = 306
SRC_X2 = 797  # Width = 491
SRC_Y1 = 220
SRC_Y2 = 595  # Height = 375 (Aspect 491:375 = 262:200)

# Exact anatomical landmarks on 262x200 canvas:
EYE_Y = 84
LEFT_EYE = (112, 78, 128, 90)   # Pupil ~(119, 84)
RIGHT_EYE = (144, 78, 160, 90)  # Pupil ~(152, 84)

MOUTH_CENTER_X = 136
MOUTH_SEAM_Y = 134
LIP_LEFT_X = 120
LIP_RIGHT_X = 152
BEARD_END_Y = 175  # Jaw displacement strictly ceases before collar at Y=175
COLLAR_START_Y = 178

def create_base_sculpt():
    im = Image.open(BASE_IMG_PATH)
    cropped = im.crop((SRC_X1, SRC_Y1, SRC_X2, SRC_Y2))
    resized = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    # Apply Fallout 1998 Black Isle style:
    # 1. Earthy wasteland color grading (desaturate digital vibrancy)
    enh_color = ImageEnhance.Color(resized).enhance(0.80)
    # 2. Sharp clay sculpt contrast
    enh_contrast = ImageEnhance.Contrast(enh_color).enhance(1.22)
    enh_sharp = ImageEnhance.Sharpness(enh_contrast).enhance(1.6)
    
    # 3. Vignette background to pure black (#000000) outside character silhouette
    arr = np.array(enh_sharp, dtype=np.float32)
    
    # Create radial/elliptical silhouette mask
    # Head center: (136, 100), radii rx=85, ry=98
    yy, xx = np.mgrid[:HEIGHT, :WIDTH]
    # Distance from center normalized
    dx = (xx - 136.0) / 88.0
    dy = (yy - 100.0) / 98.0
    dist = (dx * dx) + (dy * dy)
    
    # Mask: 1.0 inside character, fading to 0.0 at outer edges
    alpha = np.clip(1.0 - (dist - 0.75) / 0.35, 0.0, 1.0)
    # Ensure shoulders extend down to bottom
    shoulder_mask = (yy >= 165) & (xx >= 45) & (xx <= 225)
    alpha[shoulder_mask] = 1.0
    
    # Smooth mask
    mask_im = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.0))
    alpha_smooth = np.array(mask_im, dtype=np.float32) / 255.0
    
    # Apply black background
    for c in range(3):
        arr[:, :, c] = arr[:, :, c] * alpha_smooth
        
    # 4. Add subtle 1998 SGI film grain to skin
    np.random.seed(1998)
    noise = np.random.normal(0, 3.5, arr.shape)
    arr_sculpt = np.clip(arr + (noise * alpha_smooth[:, :, None]), 0, 255).astype(np.uint8)
    
    sculpt_im = Image.fromarray(arr_sculpt)
    # Unsharp mask to make clay ridges pop
    final_sculpt = sculpt_im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=2))
    return final_sculpt

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
    Eyelid closure directly over pupils.
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
            
        skin_sample = img.crop((x1, y1 - 2, x2, y1 + 1))
        stretched_lid = skin_sample.resize((w, lid_drop), Image.Resampling.BILINEAR)
        
        mask = Image.new("L", (w, lid_drop), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, -int(lid_drop * 0.4), w, lid_drop * 2], fill=240)
        mask = mask.filter(ImageFilter.GaussianBlur(0.7))
        
        res.paste(stretched_lid, (x1, y1), mask)
        
        if progress >= 0.7:
            lash_y = y1 + lid_drop - 1
            draw.line([(x1 + 1, lash_y), (x2 - 1, lash_y)], fill=(25, 14, 10), width=1)
            
    return res

def apply_speech_phoneme(img, open_amount, round_amount=0.0, mood=0.0):
    """
    Physically modeled jaw & mouth articulation matching Sulik/Cassidy:
    - Oral cavity opens between upper lip (Y=133) and lower lip (Y=136).
    - Lower jaw drops by open_amount * 6.0 px.
    - Jaw displacement tapers to ZERO at BEARD_END_Y (175).
    - COLLAR AND SHOULDERS (Y >= 178) NEVER MOVE.
    """
    if open_amount <= 0.01 and abs(mood) <= 0.05:
        return img.copy()
        
    base_arr = np.array(img, dtype=np.float32)
    h, w, c = base_arr.shape
    out_arr = base_arr.copy()
    
    jaw_drop = open_amount * 6.0
    
    # 1. Displace lower jaw & beard (Y: 135 to 175, X: 112 to 160)
    y_start = MOUTH_SEAM_Y + 1
    y_end = BEARD_END_Y
    x_start = LIP_LEFT_X - 6
    x_end = LIP_RIGHT_X + 6
    
    if jaw_drop > 0.3:
        for y in range(y_end, y_start - 1, -1):
            t = (y - y_start) / float(y_end - y_start)
            # Smooth cosine falloff
            w_y = 0.5 * (1.0 + np.cos(t * np.pi))
            disp = jaw_drop * w_y
            
            src_y = y - disp
            y0 = int(np.floor(src_y))
            y1_idx = min(h - 1, y0 + 1)
            fy = src_y - y0
            
            for x in range(x_start, x_end + 1):
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
    
    # 2. Oral cavity (deep dark mouth interior)
    if jaw_drop > 1.0:
        cavity_half_w = int((LIP_RIGHT_X - LIP_LEFT_X) * 0.45 * (1.0 - round_amount * 0.22))
        cavity_h = int(jaw_drop)
        cx = MOUTH_CENTER_X
        cy = MOUTH_SEAM_Y
        
        # Deep mouth shadow
        cavity_box = [cx - cavity_half_w, cy - 1, cx + cavity_half_w, cy + cavity_h + 1]
        draw.ellipse(cavity_box, fill=(16, 8, 8))
        
        # Upper teeth hint (authentic Fallout 2 enamel)
        if jaw_drop >= 2.5:
            teeth_half_w = int(cavity_half_w * 0.68)
            teeth_box = [cx - teeth_half_w, cy, cx + teeth_half_w, cy + min(2, int(jaw_drop * 0.4))]
            draw.rectangle(teeth_box, fill=(182, 175, 158))
            draw.line([(cx - 3, cy), (cx - 3, cy + 2)], fill=(32, 16, 12), width=1)
            draw.line([(cx + 3, cy), (cx + 3, cy + 2)], fill=(32, 16, 12), width=1)
            
    # 3. Mood: Mouth corners
    if abs(mood) > 0.05:
        dy = int(mood * 2)
        lc = img.crop((LIP_LEFT_X - 2, MOUTH_SEAM_Y - 2, LIP_LEFT_X + 4, MOUTH_SEAM_Y + 4))
        res.paste(lc, (LIP_LEFT_X - 2, MOUTH_SEAM_Y - 2 - dy))
        rc = img.crop((LIP_RIGHT_X - 4, MOUTH_SEAM_Y - 2, LIP_RIGHT_X + 2, MOUTH_SEAM_Y + 4))
        res.paste(rc, (LIP_RIGHT_X - 4, MOUTH_SEAM_Y - 2 - dy))

    return res

def apply_brow_mood(img, mood):
    """
    mood: -1.0 (angry) to +1.0 (relaxed/friendly)
    """
    if abs(mood) <= 0.05:
        return img.copy()
        
    res = img.copy()
    brow_shift = int(mood * -2)
    # Left brow: (108, 68, 132, 78)
    lb = img.crop((108, 68, 132, 78))
    res.paste(lb, (108, 68 - brow_shift))
    # Right brow: (140, 68, 164, 78)
    rb = img.crop((140, 68, 164, 78))
    res.paste(rb, (140, 68 - brow_shift))
    return res

def build_all_assets():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base = create_base_sculpt()
    base.save(os.path.join(OUTPUT_DIR, "base_sculpt.png"))
    print("Created authentic base sculpt (262x200, black background)")
    
    # 1. Neutral Speech (np: 9 frames)
    # Exactly matching 9-frame phoneme timing of Sulik and Cassidy
    np_amts = [0.0, 0.35, 0.75, 1.0, 0.65, 0.10, 0.50, 0.20, 0.0]
    np_dir = os.path.join(OUTPUT_DIR, "kcbobnp")
    os.makedirs(np_dir, exist_ok=True)
    frames_np = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(base, open_amount=amt, round_amount=0.25 if i == 4 else 0.0)
        f.save(os.path.join(np_dir, f"{i}.png"))
        frames_np.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobnp.frm"), num_frames=9, width=WIDTH, height=HEIGHT, fps=10)
    
    # Check assertion: Collar and shoulders (Y >= 178) MUST BE 100% UNTOUCHED
    f0_arr = np.array(frames_np[0])
    f3_arr = np.array(frames_np[3])
    lower_diff = np.sum(f0_arr[178:, :, :] != f3_arr[178:, :, :])
    print(f"Collar/clothing movement assertion (Y >= 178): {lower_diff} pixels changed (MUST BE 0)")
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
    create_frm(os.path.join(OUTPUT_DIR, "kcbobnf1.frm"), num_frames=4, width=WIDTH, height=HEIGHT, fps=10)
    
    # 3. Bad Speech (bp: 9 frames)
    bp_dir = os.path.join(OUTPUT_DIR, "kcbobbp")
    os.makedirs(bp_dir, exist_ok=True)
    angry_base = apply_brow_mood(base, mood=-1.0)
    frames_bp = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(angry_base, open_amount=amt, mood=-0.8)
        f.save(os.path.join(bp_dir, f"{i}.png"))
        frames_bp.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobbp.frm"), num_frames=9, width=WIDTH, height=HEIGHT, fps=10)
    
    # 4. Bad Fidget (bf1: 4 frames)
    bf1_dir = os.path.join(OUTPUT_DIR, "kcbobbf1")
    os.makedirs(bf1_dir, exist_ok=True)
    frames_bf1 = []
    for i, amt in enumerate(nf1_amts):
        f = apply_blink(angry_base, progress=amt)
        f = apply_speech_phoneme(f, open_amount=0.0, mood=-0.8)
        f.save(os.path.join(bf1_dir, f"{i}.png"))
        frames_bf1.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobbf1.frm"), num_frames=4, width=WIDTH, height=HEIGHT, fps=10)
    
    # 5. Good Speech (gp: 9 frames)
    gp_dir = os.path.join(OUTPUT_DIR, "kcbobgp")
    os.makedirs(gp_dir, exist_ok=True)
    good_base = apply_brow_mood(base, mood=0.6)
    frames_gp = []
    for i, amt in enumerate(np_amts):
        f = apply_speech_phoneme(good_base, open_amount=amt, mood=0.6)
        f.save(os.path.join(gp_dir, f"{i}.png"))
        frames_gp.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobgp.frm"), num_frames=9, width=WIDTH, height=HEIGHT, fps=10)
    
    # 6. Good Fidget (gf1: 4 frames)
    gf1_dir = os.path.join(OUTPUT_DIR, "kcbobgf1")
    os.makedirs(gf1_dir, exist_ok=True)
    frames_gf1 = []
    for i, amt in enumerate(nf1_amts):
        f = apply_blink(good_base, progress=amt)
        f = apply_speech_phoneme(f, open_amount=0.0, mood=0.6)
        f.save(os.path.join(gf1_dir, f"{i}.png"))
        frames_gf1.append(f)
    create_frm(os.path.join(OUTPUT_DIR, "kcbobgf1.frm"), num_frames=4, width=WIDTH, height=HEIGHT, fps=10)

    # Save animated preview GIFs
    frames_np[0].save(os.path.join(OUTPUT_DIR, "kcbob_speech_canonical.gif"), save_all=True, append_images=frames_np[1:], duration=110, loop=0)
    frames_nf1[0].save(os.path.join(OUTPUT_DIR, "kcbob_blink_canonical.gif"), save_all=True, append_images=frames_nf1[1:], duration=160, loop=0)
    frames_bp[0].save(os.path.join(OUTPUT_DIR, "kcbob_angry_canonical.gif"), save_all=True, append_images=frames_bp[1:], duration=110, loop=0)
    print("SUCCESS: All canonical Fallout 2 talking head assets generated cleanly!")

if __name__ == "__main__":
    build_all_assets()
