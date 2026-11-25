import subprocess
import os
import shutil
import struct

TOOLS_DIR = r"e:\FALLOUT Ult pjt\tools"
COMPILER = os.path.join(TOOLS_DIR, "compile.exe")

GP_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
HD_DIR = r"E:\Fallout2_Ultimate\Fallout2_HD"
REPO_DIR = r"e:\FALLOUT Ult pjt"

ssl_source = """/*
   Fallout 2 Ultimate Wasteland Edition 2026
   Clean Zero-Flicker Highlighting & Object Radar (sFall 4.5.1 / D3D9)
   - Left / Right Shift (Hold): Temporary item & container illumination
   - Caps Lock (Press): Persistent toggle on/off with on-screen status
   - Color coding:
       * Bright Yellow (16): Ground loot and corpses with items
       * Glowing Green (8): Containers with loot
       * Red (2): Locked doors and locked containers
       * Purple (64): Interactive terminals, computers, bulletin boards
       * Subtle Gray (4): Empty looted containers and corpses
   - Floor-Aware: Only illuminates objects on player's current elevation
   - Zero-Flicker: Updates on hex movement, no continuous screen invalidation
   - sFall 4.5.1 strict compliance: 8-char global variable 'GL_PHIGH'
*/

#pragma sce
#define SCRIPT_REALNAME "gl_highlighting"
#include "headers/define.h"
#include "headers/sfall/sfall.h"
#include "headers/sfall/define_extra.h"

#define INI_FILE                    "mods\\gl_highlighting.ini"
#define SFALL_GLOBAL_VAR            "GL_PHIGH"

#define COLOR_ITEMS                 (16) // Bright yellow for loot on ground
#define COLOR_CORPSES               (16) // Bright yellow for corpses with loot
#define COLOR_CORPSE_EMPTY          (4)  // Subtle gray for empty corpses
#define COLOR_CONTAINERS            (8)  // Glowing green for containers with loot
#define COLOR_CONTAINER_EMPTY       (4)  // Subtle gray for empty looted containers
#define COLOR_LOCKED                (2)  // Red for locked doors & locked containers
#define COLOR_INTERACTIVE_SCENERY   (64) // Purple for bulletin boards, terminals, computers, generators

#define NO_HIGHLIGHT(obj)           (get_flags(obj) bwand FLAG_NOHIGHLIGHT)
#define NO_STEAL(obj)               (get_proto_data(obj_pid(obj), PROTO_CR_FLAGS) bwand CFLG_NOSTEAL)
#define IS_EMPTY(obj)               (inven_ptr(obj, 0) == 0)

procedure start;
procedure LoadHighlightConfig;
procedure ClearAllOutlines;
procedure ApplyOutlines;
procedure ShowStatusMsg(variable is_on);
procedure KeyPressHandler;
procedure GameModeChangeHandler;
procedure InventoryMoveHandler;

variable persistent_active := 0;
variable shift_hold_active := 0;
variable last_dude_tile    := -1;

variable cfg_items         := 1;
variable cfg_containers    := 1;
variable cfg_empty_cont    := 1;
variable cfg_corpses       := 1;
variable cfg_empty_corp    := 1;
variable cfg_scenery       := 1;
variable cfg_doors         := 1;

procedure start begin
   variable gmode;
   if game_loaded then begin
      if (sfall_ver_major < 4) then return;
      call LoadHighlightConfig;
      persistent_active := get_sfall_global_int(SFALL_GLOBAL_VAR);

      register_hook_proc(HOOK_KEYPRESS, KeyPressHandler);
      register_hook_proc(HOOK_GAMEMODECHANGE, GameModeChangeHandler);
      register_hook_proc(HOOK_INVENTORYMOVE, InventoryMoveHandler);

      set_global_script_type(1);
      // Run repeat tick every 20 frames (~3 times per second)
      set_global_script_repeat(20);

      if persistent_active then call ApplyOutlines;
   end else begin
      // Repeat tick: update ONLY if player moved to a new tile
      if (persistent_active or shift_hold_active) then begin
         gmode := get_game_mode;
         if ((gmode bwand (WORLDMAP bwor DIALOG bwor ESCMENU bwor SAVEGAME bwor LOADGAME bwor OPTIONS bwor HELP bwor CHARSCREEN bwor PIPBOY bwor AUTOMAP bwor BARTER)) == 0) then begin
            if (tile_num(dude_obj) != last_dude_tile) then begin
               last_dude_tile := tile_num(dude_obj);
               call ApplyOutlines;
            end
         end
      end
   end
end

procedure LoadHighlightConfig begin
   variable val;
   val := get_ini_setting(INI_FILE + "|Highlighting|Items");
   if (val >= 0) then cfg_items := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|Containers");
   if (val >= 0) then cfg_containers := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|EmptyContainers");
   if (val >= 0) then cfg_empty_cont := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|Corpses");
   if (val >= 0) then cfg_corpses := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|EmptyCorpses");
   if (val >= 0) then cfg_empty_corp := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|Scenery");
   if (val >= 0) then cfg_scenery := val;
   val := get_ini_setting(INI_FILE + "|Highlighting|Doors");
   if (val >= 0) then cfg_doors := val;
end

procedure ClearAllOutlines begin
   variable obj;
   foreach obj in list_as_array(LIST_GROUNDITEMS) begin
      if obj then set_outline(obj, 0);
   end
   foreach obj in list_as_array(LIST_CRITTERS) begin
      if obj then set_outline(obj, 0);
   end
   foreach obj in list_as_array(LIST_SCENERY) begin
      if obj then set_outline(obj, 0);
   end
   tile_refresh_display;
end

procedure ApplyOutlines begin
   variable obj, isCorpse, sid, dude_elev;

   dude_elev := elevation(dude_obj);

   // 1. Ground Items & Containers
   foreach obj in list_as_array(LIST_GROUNDITEMS) begin
      if (obj and obj != outlined_object and not NO_HIGHLIGHT(obj)) then begin
         if (elevation(obj) == dude_elev) then begin
            if (obj_item_subtype(obj) == item_type_container) then begin
               if (cfg_containers) then begin
                  if (obj_is_locked(obj)) then begin
                     if (cfg_doors) then set_outline(obj, COLOR_LOCKED);
                  end else if (IS_EMPTY(obj)) then begin
                     if (cfg_empty_cont) then set_outline(obj, COLOR_CONTAINER_EMPTY);
                  end else begin
                     set_outline(obj, COLOR_CONTAINERS);
                  end
               end
            end else begin
               if (cfg_items) then set_outline(obj, COLOR_ITEMS);
            end
         end
      end
   end

   // 2. Dead Bodies (yellow if holding items, gray if empty)
   if (cfg_corpses) then begin
      foreach obj in list_as_array(LIST_CRITTERS) begin
         if (obj and obj != dude_obj) then begin
            if (elevation(obj) == dude_elev) then begin
               isCorpse := (critter_state(obj) == 1);
               if (isCorpse and not NO_STEAL(obj)) then begin
                  if (not IS_EMPTY(obj)) then begin
                     set_outline(obj, COLOR_CORPSES);
                  end else if (cfg_empty_corp) then begin
                     set_outline(obj, COLOR_CORPSE_EMPTY);
                  end
               end
            end
         end
      end
   end

   // 3. Interactive Props with attached scripts (Bulletin boards, Terminals, Computers, Locked doors)
   foreach obj in list_as_array(LIST_SCENERY) begin
      if obj then begin
         if (elevation(obj) == dude_elev) then begin
            sid := get_object_data(obj, OBJ_DATA_SID);
            if (sid != -1 and not NO_HIGHLIGHT(obj)) then begin
               if (obj_is_locked(obj) and not obj_is_open(obj)) then begin
                  if (cfg_doors) then set_outline(obj, COLOR_LOCKED);
               end else if (cfg_scenery) then begin
                  set_outline(obj, COLOR_INTERACTIVE_SCENERY);
               end
            end
         end
      end
   end
   tile_refresh_display;
end

procedure ShowStatusMsg(variable is_on) begin
   variable lang;
   lang := get_ini_string("fallout2.cfg|system|language");
   if (lang == "english") then begin
      if is_on then
         display_msg("Highlighting: ON");
      else
         display_msg("Highlighting: OFF");
   end else begin
      if is_on then
         display_msg("Подсветка: ВКЛ");
      else
         display_msg("Подсветка: ВЫКЛ");
   end
end

procedure KeyPressHandler begin
   variable pressed  := get_sfall_arg;
   variable scanCode := get_sfall_arg;
   variable gmode;

   // Block keypress during modal blocking screens
   gmode := get_game_mode;
   if (gmode bwand (WORLDMAP bwor DIALOG bwor ESCMENU bwor SAVEGAME bwor LOADGAME bwor OPTIONS bwor HELP bwor CHARSCREEN bwor PIPBOY bwor AUTOMAP bwor BARTER)) then return;

   // Caps Lock (key 58) -> Persistent Toggle
   if (scanCode == 58 and pressed) then begin
      persistent_active := not persistent_active;
      set_sfall_global(SFALL_GLOBAL_VAR, persistent_active);
      if persistent_active then begin
         call ApplyOutlines;
         call ShowStatusMsg(1);
      end else begin
         call ClearAllOutlines;
         call ShowStatusMsg(0);
      end
      return;
   end

   // Left Shift (42) or Right Shift (54) -> Temporary Hold
   if (scanCode == 42 or scanCode == 54) then begin
      if (pressed and not shift_hold_active) then begin
         shift_hold_active := 1;
         call ApplyOutlines;
      end else if (not pressed and shift_hold_active) then begin
         shift_hold_active := 0;
         if (not persistent_active) then call ClearAllOutlines;
      end
   end
end

procedure GameModeChangeHandler begin
   variable gmode;
   gmode := get_game_mode;
   // When returning from menus/inventory back to the game map
   if (persistent_active or shift_hold_active) then begin
      if ((gmode bwand (WORLDMAP bwor DIALOG bwor ESCMENU bwor SAVEGAME bwor LOADGAME bwor OPTIONS bwor HELP bwor CHARSCREEN bwor PIPBOY bwor AUTOMAP bwor BARTER)) == 0) then begin
         call ApplyOutlines;
      end
   end
end

procedure InventoryMoveHandler begin
   // Clear outline when an item is picked up (slot 7 = ground pickup)
   if ((persistent_active or shift_hold_active) and get_sfall_arg == 7) then begin
      set_outline(get_sfall_arg, 0);
   end
end
"""

def build_highlighting():
    ssl_path = os.path.join(TOOLS_DIR, "gl_highlighting.ssl")
    int_path = os.path.join(TOOLS_DIR, "gl_highlighting.int")
    with open(ssl_path, "w", encoding="cp1251") as f:
        f.write(ssl_source)

    cmd = [COMPILER, "-p", "-q", "-s", "-Iheaders", "-O2", "gl_highlighting.ssl", "-o", "gl_highlighting.int"]
    res = subprocess.run(cmd, cwd=TOOLS_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print("Compile ERROR:")
        print(res.stderr)
        raise RuntimeError("Failed to compile gl_highlighting.ssl")
    print(f"SUCCESS: gl_highlighting.int compiled ({os.path.getsize(int_path)} bytes)")
    return int_path

# 1. Compile gl_highlighting.int
hl_int = build_highlighting()

# 2. Deploy to VFS Layer 1 (mods/rpu_russian_uncensored.dat/scripts/)
targets_scripts = [
    os.path.join(REPO_DIR, "mods", "rpu_russian_uncensored.dat", "scripts"),
    os.path.join(GP_DIR, "mods", "rpu_russian_uncensored.dat", "scripts"),
    os.path.join(HD_DIR, "mods", "rpu_russian_uncensored.dat", "scripts")
]

for d in targets_scripts:
    os.makedirs(d, exist_ok=True)
    shutil.copy2(hl_int, os.path.join(d, "gl_highlighting.int"))
    print(f"Deployed gl_highlighting.int -> {d}")

# 3. Ensure fo2tweaks.ini has highlighting=0 across all locations
ini_paths = [
    os.path.join(REPO_DIR, "mods", "fo2tweaks.ini"),
    os.path.join(GP_DIR, "mods", "fo2tweaks.ini"),
    os.path.join(HD_DIR, "mods", "fo2tweaks.ini")
]
for p in ini_paths:
    if os.path.exists(p):
        with open(p, "r", encoding="cp1251", errors="ignore") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.strip().startswith("highlighting="):
                new_lines.append("highlighting=0\n")
            else:
                new_lines.append(line)
        with open(p, "w", encoding="cp1251") as f:
            f.writelines(new_lines)
        print(f"Verified highlighting=0 in {p}")

# 4. Comment out DB_MapBlurFX.dat in mods_order.txt across all locations
mods_order_paths = [
    os.path.join(REPO_DIR, "mods", "mods_order.txt"),
    os.path.join(GP_DIR, "mods", "mods_order.txt"),
    os.path.join(HD_DIR, "mods", "mods_order.txt")
]
for mop in mods_order_paths:
    if os.path.exists(mop):
        with open(mop, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.strip() == "DB_MapBlurFX.dat":
                new_lines.append("; DB_MapBlurFX.dat\n")
            else:
                new_lines.append(line)
        with open(mop, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Disabled DB_MapBlurFX.dat in {mop}")

# 5. Restore clean original gl_keyshelp.int from Foxx into KeysHelp.dat
foxx_keyshelp_int = r"E:\Games\Fallout 2 (Expansion Version)\mods\KeysHelp.dat\scripts\gl_keyshelp.int"
if os.path.exists(foxx_keyshelp_int):
    import sys
    sys.path.insert(0, REPO_DIR)
    from tools.build_foxx_tribute_pack import pack_to_dat2
    kh_staging = os.path.join(REPO_DIR, "standalone_mods", "foxx_rebuild_tribute", "keyshelp_staging")
    kh_scripts = os.path.join(kh_staging, "scripts")
    os.makedirs(kh_scripts, exist_ok=True)
    shutil.copy2(foxx_keyshelp_int, os.path.join(kh_scripts, "gl_keyshelp.int"))
    
    # Re-pack KeysHelp.dat
    kh_dat_out = os.path.join(REPO_DIR, "mods", "KeysHelp.dat")
    pack_to_dat2(kh_staging, kh_dat_out)
    shutil.copy2(kh_dat_out, os.path.join(GP_DIR, "mods", "KeysHelp.dat"))
    shutil.copy2(kh_dat_out, os.path.join(HD_DIR, "mods", "KeysHelp.dat"))
    print("Re-packed and restored clean KeysHelp.dat across all profiles!")

# 6. Add missing {48901} description in pro_item.msg
pro_item_paths = [
    os.path.join(REPO_DIR, "mods", "rpu_russian_uncensored.dat", "text", "russian", "game", "pro_item.msg"),
    os.path.join(GP_DIR, "mods", "rpu_russian_uncensored.dat", "text", "russian", "game", "pro_item.msg"),
    os.path.join(HD_DIR, "mods", "rpu_russian_uncensored.dat", "text", "russian", "game", "pro_item.msg")
]
desc_line = "{48901}{}{Специальное оружие, используемое боксером на ринге Нью-Рино.}\n"
for pip in pro_item_paths:
    if os.path.exists(pip):
        with open(pip, "r", encoding="cp1251", errors="ignore") as f:
            content = f.read()
        if "{48901}" not in content:
            idx = content.find("{48900}")
            if idx != -1:
                end_line_idx = content.find("\n", idx)
                content = content[:end_line_idx+1] + desc_line + content[end_line_idx+1:]
                with open(pip, "w", encoding="cp1251") as f:
                    f.write(content)
                print(f"Added PID 489 description into {pip}")

print("ALL STEP-BY-STEP FIXES PROCESSED SUCCESSFULLY!")
