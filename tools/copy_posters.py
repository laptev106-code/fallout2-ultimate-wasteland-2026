import shutil
import os
from PIL import Image

src_map = {
    "talking_heads.png": r"C:\Users\Геннадий\.gemini\antigravity\brain\b493567c-8e9b-4eb1-944d-57cf26997e1e\fallout2_lynette_talking_head_poster_png_1795104666187.jpg",
    "pip_timers.png": r"C:\Users\Геннадий\.gemini\antigravity\brain\b493567c-8e9b-4eb1-944d-57cf26997e1e\pipboy_quest_timers_poster_1795104670844.jpg",
    "angela.png": r"C:\Users\Геннадий\.gemini\antigravity\brain\b493567c-8e9b-4eb1-944d-57cf26997e1e\angela_bishop_companion_poster_1795104673655.jpg",
    "mapblur.png": r"C:\Users\Геннадий\.gemini\antigravity\brain\b493567c-8e9b-4eb1-944d-57cf26997e1e\fallout2_interface_mapblur_poster_1795104683006.jpg",
    "audio_unlocked.png": r"C:\Users\Геннадий\.gemini\antigravity\brain\b493567c-8e9b-4eb1-944d-57cf26997e1e\fallout2_sound_variations_clean_poster_1795104699978.jpg"
}

dst_dirs = [
    r"D:\AG games mods\fallout2-ultimate-wasteland-2026\launcher_nextgen\ui\assets\posters",
    r"E:\Fallout2_Ultimate\launcher_nextgen\ui\assets\posters"
]

for name, src in src_map.items():
    if not os.path.exists(src):
        print("Missing source:", src)
        continue
    img = Image.open(src)
    for d in dst_dirs:
        os.makedirs(d, exist_ok=True)
        out_path = os.path.join(d, name)
        img.save(out_path, "PNG")
        sz = os.path.getsize(out_path)
        print(f"Saved {name} -> {out_path} ({sz} bytes)")
