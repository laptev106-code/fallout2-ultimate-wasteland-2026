import subprocess, os
from build_dual_language_pack import write_dual

tools_dir = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\tools"
compiler = os.path.join(tools_dir, "compile.exe")

ssl_code = """/*
    Temple of Trials Atmospheric Hints for Beginners
    Script: gl_temple_hints.ssl
    Bilingual: English & Russian
*/

#pragma sce
#define SCRIPT_REALNAME "gl_temple_hints"
#include "define.h"
#include "sfall.h"

#define MAP_ARROYO_TEMPLE (126)
#define SGVAR_TEMPLE_HINTS "SGVAR_TEMPLE_HINT_SEEN"

procedure start;
procedure map_enter_p_proc;

procedure start begin
end

procedure map_enter_p_proc begin
   variable seen, lang;
   if (cur_map_index == MAP_ARROYO_TEMPLE) then begin
      seen := get_sfall_global_int(SGVAR_TEMPLE_HINTS);
      if (seen == 0) then begin
         set_sfall_global(SGVAR_TEMPLE_HINTS, 1);
         lang := get_ini_string("fallout2.cfg|system|language");
         if (lang == "english") then begin
            display_msg("The sanctuary is shrouded in darkness. Hint: TAB highlights objects, F1 opens controls.");
            display_msg("Tribal lore: Ancestors often concealed useful supplies inside clay urns and pots.");
         end else begin
            display_msg("Святилище погружено во тьму. Совет: Клавиша TAB подсвечивает предметы, F1 открывает справку.");
            display_msg("Предания племени: Предки нередко оставляли полезные припасы в глиняных урнах и сосудах.");
         end
      end
   end
end
"""

ssl_file = os.path.join(tools_dir, "gl_temple_hints.ssl")
with open(ssl_file, "w", encoding="cp1251") as f:
    f.write(ssl_code)

out_int = "gl_temple_hints.int"
cmd = [
    compiler,
    "-p",
    "-q",
    "-s",
    "-Iheaders",
    "-O2",
    "gl_temple_hints.ssl",
    "-o", out_int
]

print("Compiling gl_temple_hints...")
res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Return code:", res.returncode)

int_path = os.path.join(tools_dir, out_int)
if os.path.exists(int_path):
    print("SUCCESS! Compiled:", int_path, "Size:", os.path.getsize(int_path))
    with open(int_path, "rb") as f:
        write_dual(r"scripts\gl_temple_hints.int", f.read())
else:
    print("FAILED!")
