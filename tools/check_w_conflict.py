import subprocess

p = subprocess.run("git -C \"D:/AG games mods/fallout2-ultimate-wasteland-2026\" show 7fc7cf0", shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
for line in p.stdout.splitlines():
    if any(k in line.lower() for k in ["hotkey", "conflict", "key", "ddraw", "fo2tweaks"]):
        print(line)
