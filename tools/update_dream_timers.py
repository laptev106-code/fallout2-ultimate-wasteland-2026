import os

targets = [
    r"E:\FALLOUT Ult pjt\ddraw.ini",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay\ddraw.ini",
    r"E:\Fallout2_Ultimate\Fallout2_HD\ddraw.ini"
]

replacement_block = """;Uncomment these lines to change the timers of how many days after the game starts Hakunin dream sequences will occur
;Set to -1 to disable the game event
MovieTimer_artimer1=120
MovieTimer_artimer2=235
MovieTimer_artimer3=350
MovieTimer_artimer4=470
"""

for path in targets:
    if not os.path.exists(path):
        print(f"Skipping missing: {path}")
        continue
    with open(path, "r", encoding="latin-1", errors="ignore") as f:
        content = f.read()
    
    # Locate the dream section
    import re
    pattern = r";Uncomment these lines to change the timers of how many days after the game starts Hakunin dream sequences will occur.*?(?=\n\n|\r\n\r\n)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content[:match.start()] + replacement_block.rstrip() + content[match.end():]
        with open(path, "w", encoding="latin-1") as f:
            f.write(new_content)
        print(f"Updated dream timers in: {path}")
    else:
        print(f"Pattern not found in: {path}")
