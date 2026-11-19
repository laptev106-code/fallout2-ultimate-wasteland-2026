import re
import html

with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/wall_10479.html', 'rb') as f:
    raw = f.read()

txt = raw.decode('windows-1251', errors='ignore')

# Match og:description
match = re.search(r'property="og:description"\s+content="(.*?)"', txt, re.DOTALL)
if match:
    desc = match.group(1)
    # unescape html entities like &#127385; &lt; &gt;
    clean = html.unescape(desc)
    clean = clean.replace('<br>', '\n').replace('&lt;br&gt;', '\n')
    print("=== FULL WALL POST DESCRIPTION ===")
    print(clean)
    with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/foxx_wall_post.txt', 'w', encoding='utf-8') as out:
        out.write(clean)
