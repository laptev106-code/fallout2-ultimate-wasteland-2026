import sys, re, os

GAME_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
DDRAW_PATH = os.path.join(GAME_DIR, "ddraw.ini")
F2RES_PATH = os.path.join(GAME_DIR, "f2_res.ini")

def set_config(mode_type="window_lossless_720", sharpness=2):
    with open(DDRAW_PATH, "r", encoding="latin1") as f:
        ddraw = f.read()

    # Sharpness: 0 = Pixel Retro, 1 = Balanced, 2 = Smooth DX9
    ddraw = re.sub(r"(?m)^TextureFilter=\d+", f"TextureFilter={sharpness}", ddraw)

    # Window Mode: Mode=5 (DX9 Windowed), Mode=6 (DX9 Borderless Fullscreen)
    if "window" in mode_type:
        ddraw = re.sub(r"(?m)^Mode=\d+", "Mode=5", ddraw)
    else:
        ddraw = re.sub(r"(?m)^Mode=\d+", "Mode=6", ddraw)

    with open(DDRAW_PATH, "w", encoding="latin1") as f:
        f.write(ddraw)

    with open(F2RES_PATH, "r", encoding="latin1") as f:
        f2res = f.read()

    if mode_type == "window_lossless_720":
        f2res = re.sub(r"(?m)^SCR_WIDTH=\d+", "SCR_WIDTH=1280", f2res)
        f2res = re.sub(r"(?m)^SCR_HEIGHT=\d+", "SCR_HEIGHT=720", f2res)
        f2res = re.sub(r"(?m)^SCALE_2X=\d+", "SCALE_2X=0", f2res)
        f2res = re.sub(r"(?m)^WINDOWED=\d+", "WINDOWED=1", f2res)
        f2res = re.sub(r"(?m)^WINDOWED_FULLSCREEN=\d+", "WINDOWED_FULLSCREEN=0", f2res)
    elif mode_type == "window_lossless_1080":
        f2res = re.sub(r"(?m)^SCR_WIDTH=\d+", "SCR_WIDTH=1920", f2res)
        f2res = re.sub(r"(?m)^SCR_HEIGHT=\d+", "SCR_HEIGHT=1080", f2res)
        f2res = re.sub(r"(?m)^SCALE_2X=\d+", "SCALE_2X=1", f2res)
        f2res = re.sub(r"(?m)^WINDOWED=\d+", "WINDOWED=1", f2res)
        f2res = re.sub(r"(?m)^WINDOWED_FULLSCREEN=\d+", "WINDOWED_FULLSCREEN=0", f2res)
    elif mode_type == "borderless_2k":
        f2res = re.sub(r"(?m)^SCR_WIDTH=\d+", "SCR_WIDTH=1920", f2res)
        f2res = re.sub(r"(?m)^SCR_HEIGHT=\d+", "SCR_HEIGHT=1080", f2res)
        f2res = re.sub(r"(?m)^SCALE_2X=\d+", "SCALE_2X=1", f2res)
        f2res = re.sub(r"(?m)^WINDOWED=\d+", "WINDOWED=1", f2res)
        f2res = re.sub(r"(?m)^WINDOWED_FULLSCREEN=\d+", "WINDOWED_FULLSCREEN=1", f2res)

    with open(F2RES_PATH, "w", encoding="latin1") as f:
        f.write(f2res)

    print(f"Applied: mode={mode_type}, sharpness={sharpness}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "window_lossless_720"
    sharp = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    set_config(mode, sharp)
