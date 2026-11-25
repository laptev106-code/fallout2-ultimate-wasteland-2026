import subprocess

def run_git(cmd):
    p = subprocess.run(f"git -C \"D:/AG games mods/fallout2-ultimate-wasteland-2026\" {cmd}", shell=True, capture_output=True, text=True)
    return p.stdout

print("=== GIT LOG FOR INI FILES ===")
print(run_git("log --oneline -n 20 -- mods/fo2tweaks.ini ddraw.ini"))

print("=== GIT LOG FOR ANY COMMITS MENTIONING fo2tweaks OR keys OR control ===")
print(run_git("log --oneline --grep=\"fo2tweaks\" --grep=\"key\" --grep=\"control\" --grep=\"управлен\""))
