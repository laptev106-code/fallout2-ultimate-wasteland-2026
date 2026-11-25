import os
import sys
import re
sys.path.insert(0, os.path.abspath("."))
import tools.engine_full_audit as efa

gp = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
vfs_gp, col_gp, order_gp, stats_gp = efa.build_profile_vfs(gp)

game_msgs = [k for k in vfs_gp if k.startswith("text\\russian\\game\\") and k.endswith(".msg")]
print(f"Total game message files to audit: {len(game_msgs)}")

all_leaks = {}
for gm in sorted(game_msgs):
    info = vfs_gp[gm]
    txt, enc = efa.read_vfs_text(info)
    if not txt:
        continue
    file_leaks = []
    for m in re.finditer(r"\{(\d+)\}\{([^}]*)\}\{(.*)\}", txt):
        num = int(m.group(1))
        body = m.group(3).strip()
        if not body:
            continue
        # Ignore technical markers
        if re.match(r"^[\d\s\.,;:!?\-_=\+\*\#\$\%\^\&\|\/\\\'\"\(\)\[\]]+$", body):
            continue
        ascii_words = re.findall(r"\b[A-Za-z]{3,}\b", body)
        cyr_words = re.findall(r"\b[а-яА-ЯёЁ]{3,}\b", body)
        ignored = {"vault", "fallout", "sfall", "directx", "shader", "vertex", "blitting", "pipboy", "stimpak", "laser", "plasma"}
        filtered_ascii = [w for w in ascii_words if w.lower() not in ignored]
        if len(filtered_ascii) >= 2 and len(cyr_words) == 0:
            file_leaks.append((num, body))
    if file_leaks:
        all_leaks[gm] = file_leaks

print(f"Files with potential English leaks: {len(all_leaks)}")
for fn, leaks in all_leaks.items():
    print(f"=== {fn} ({len(leaks)} leaks) ===")
    for num, b in leaks[:15]:
        print(f"  {{{num}}}: {b}")
