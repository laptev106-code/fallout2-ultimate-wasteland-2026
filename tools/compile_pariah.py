import subprocess
import os

tools_dir = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools"
compiler = os.path.join(tools_dir, "compile.exe")

ssl_code = """/*
   Pariah Dog Fix for Fallout 2 (Ultimate Wasteland Edition 2026)
   Fixes bug where killing Pariah Dog via party members / indirect damage
   leaves the Jinxed Perk on the player forever.
*/

#pragma sce
#define SCRIPT_REALNAME "gl_pariah_fix"
#include "define.h"
#include "sfall.h"

#define PID_PARIAH_DOG (16777600)
#define SCRIPT_ECPARIAH (1098)

procedure start;
procedure death_handler;

procedure start begin
   if game_loaded then begin
      register_hook_proc(HOOK_ONDEATH, death_handler);
   end
end

procedure death_handler begin
   variable dead_critter;
   dead_critter := get_sfall_arg;

   if (dead_critter != 0) then begin
      if (obj_pid(dead_critter) == PID_PARIAH_DOG) then begin
         if (has_trait(TRAIT_PERK, dude_obj, PERK_jinxed_perk)) then begin
            critter_rm_trait(dude_obj, TRAIT_PERK, PERK_jinxed_perk, 1);
            display_msg(message_str(SCRIPT_ECPARIAH, 104));
         end
      end
   end
end
"""

ssl_file = os.path.join(tools_dir, "gl_pariah_fix.ssl")
with open(ssl_file, "w", encoding="cp1251") as f:
    f.write(ssl_code)

out_int = "gl_pariah_fix.int"
cmd = [
    compiler,
    "-q",
    "-s",
    "-Iheaders",
    "-O2",
    "gl_pariah_fix.ssl",
    "-o", out_int
]

print("Compiling gl_pariah_fix...")
res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Return code:", res.returncode)

int_path = os.path.join(tools_dir, out_int)
if os.path.exists(int_path):
    print("SUCCESS! Compiled:", int_path, "Size:", os.path.getsize(int_path))
else:
    print("FAILED! File not created")
