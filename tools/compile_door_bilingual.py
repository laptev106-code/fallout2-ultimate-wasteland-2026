import subprocess, os
from build_dual_language_pack import write_dual

tools_dir = r"d:\AG games mods\fallout2-ultimate-wasteland-2026\tools"
compiler = os.path.join(tools_dir, "compile.exe")

ssl_code = """/*
    Fallout 2 Ultimate Wasteland 2026 - Anti-Softlock Temple Door Fix & Subtle Hints
    Script: AIBKDOR.SSL
    Bilingual: English & Russian
*/

#define SCRIPT_REALNAME "aibkdor"
#include "define.h"
#define NAME 35
#include "command.h"
#include "sfall.h"

procedure start;
procedure damage_p_proc;
procedure use_p_proc;
procedure use_skill_on_p_proc;
procedure use_obj_on_p_proc;
procedure look_at_p_proc;
procedure description_p_proc;

procedure start begin
end

procedure damage_p_proc begin
   variable Door;
   if (metarule(49, target_obj) == 6) then begin
      Door := create_object_sid(33555365, tile_num(self_obj), elevation(self_obj), -1);
      destroy_object(self_obj);
   end
end

procedure use_p_proc begin
   variable Door, lang;
   lang := get_ini_string("fallout2.cfg|system|language");
   script_overrides;

   if (get_critter_stat(dude_obj, 0) >= 8) then begin
      if (lang == "english") then
         display_msg("Straining with all your might, you smash the jammed door open!");
      else
         display_msg("Напрягши все силы, вы мощным ударом высаживаете заклинившую дверь!");
      give_exp_points(50);
      Door := create_object_sid(33555365, tile_num(self_obj), elevation(self_obj), -1);
      destroy_object(self_obj);
   end else begin
      if (lang == "english") then
         display_msg("The door is jammed shut without a handle. Try lockpicking, prying with a spear, or an explosive charge.");
      else
         display_msg("Дверь заклинило без ручки. Попробуйте взломать засов, применить копье как рычаг или взорвать.");
   end
end

procedure use_skill_on_p_proc begin
   variable skill, Door, lang;
   lang := get_ini_string("fallout2.cfg|system|language");
   skill := action_being_used;
   script_overrides;

   if (skill == 9) then begin
      if ((has_skill(dude_obj, 9) >= 25) or (is_success(roll_vs_skill(dude_obj, 9, 0)))) then begin
         if (lang == "english") then
            display_msg("You successfully locate and slide back the hidden stone bolt!");
         else
            display_msg("Вам удается нащупать и отжать скрытый каменный засов двери!");
         give_exp_points(50);
         Door := create_object_sid(33555365, tile_num(self_obj), elevation(self_obj), -1);
         destroy_object(self_obj);
      end else begin
         if (lang == "english") then
            display_msg("You fail to pick the jammed door bolt.");
         else
            display_msg("Вам не удается вскрыть заклинивший засов двери.");
      end
   end else begin
      if (lang == "english") then
         display_msg("That skill is useless here.");
      else
         display_msg("Этот навык здесь бесполезен.");
   end
end

procedure use_obj_on_p_proc begin
   variable tool, Door, lang;
   lang := get_ini_string("fallout2.cfg|system|language");
   tool := obj_pid(obj_being_used_with);
   script_overrides;

   // 7 = Spear, 280 = Sharpened Spear, 20 = Crowbar
   if ((tool == 7) or (tool == 280) or (tool == 20)) then begin
      if (get_critter_stat(dude_obj, 0) >= 6) then begin
         if (lang == "english") then
            display_msg("Using the shaft as a lever, you pry open the heavy stone door!");
         else
            display_msg("Используя древко как рычаг, вы выламываете заклинившую дверь!");
         give_exp_points(50);
         Door := create_object_sid(33555365, tile_num(self_obj), elevation(self_obj), -1);
         destroy_object(self_obj);
      end else begin
         if (lang == "english") then
            display_msg("You lack the strength (need 6+) to pry this heavy door open.");
         else
            display_msg("Вам не хватает силы (нужно 6+), чтобы выломать эту тяжелую дверь рычагом.");
      end
   end else if ((tool == 85) or (tool == 51)) then begin
      if (lang == "english") then
         display_msg("Set the timer on the explosives in your inventory and place it next to the door.");
      else
         display_msg("Установите таймер на взрывчатке в инвентаре и положите ее на пол рядом с дверью.");
   end else begin
      if (lang == "english") then
         display_msg("That item does not fit the door.");
      else
         display_msg("Этот предмет не подходит для открытия двери.");
   end
end

procedure look_at_p_proc begin
   script_overrides;
   display_msg(message_str(13, 101));
end

procedure description_p_proc begin
   script_overrides;
   display_msg(message_str(130, 900));
end
"""

ssl_file = os.path.join(tools_dir, "aibkdor.ssl")
with open(ssl_file, "w", encoding="cp1251") as f:
    f.write(ssl_code)

out_int = "AIBKDOR.INT"
cmd = [
    compiler,
    "-p",
    "-q",
    "-s",
    "-Iheaders",
    "-O2",
    "aibkdor.ssl",
    "-o", out_int
]

print("Compiling bilingual AIBKDOR...")
res = subprocess.run(cmd, cwd=tools_dir, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Return code:", res.returncode)

int_path = os.path.join(tools_dir, out_int)
if os.path.exists(int_path):
    print("SUCCESS! Compiled:", int_path, "Size:", os.path.getsize(int_path))
    with open(int_path, "rb") as f:
        write_dual(r"scripts\AIBKDOR.INT", f.read())
else:
    print("FAILED!")
