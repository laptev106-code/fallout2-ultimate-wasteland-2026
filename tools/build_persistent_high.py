import subprocess
import os
import shutil

repo_dir = r"D:\AG games mods\fallout2-ultimate-wasteland-2026"
tools_dir = os.path.join(repo_dir, "tools")
compiler = os.path.join(tools_dir, "compile.exe")

ssl_utf8 = os.path.join(tools_dir, "gl_highlighting_v2.ssl")
ssl_cp1251 = os.path.join(tools_dir, "gl_highlighting_build.ssl")

with open(ssl_utf8, "r", encoding="utf-8") as f:
    text = f.read()

with open(ssl_cp1251, "w", encoding="cp1251", errors="replace") as f:
    f.write(text)

out_int = "gl_highlighting.int"
cmd = [compiler, "-p", "-q", "-s", "-Iheaders", "-O2", "gl_highlighting_build.ssl", "-o", out_int]

print("Compiling gl_highlighting...")
res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Return code:", res.returncode)

compiled_int = os.path.join(tools_dir, out_int)
if res.returncode == 0 and os.path.exists(compiled_int):
    sz = os.path.getsize(compiled_int)
    print(f"SUCCESS! Compiled {compiled_int} ({sz} bytes)")
    
    # Target destinations
    targets = [
        r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\scripts\gl_highlighting.int",
        r"E:\Fallout2_Ultimate\Fallout2_HD\DATA\scripts\gl_highlighting.int",
        r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\scripts\gl_highlighting.int",
        r"E:\Fallout2_Ultimate\Fallout2_HD\mods\rpu_russian_uncensored.dat\scripts\gl_highlighting.int"
    ]
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copy2(compiled_int, t)
        print(f"Deployed to: {t}")
    print("All deployments completed cleanly!")
else:
    print("FAILED TO COMPILE!")
