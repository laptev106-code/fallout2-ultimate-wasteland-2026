import subprocess
import os
import shutil

TOOLS_DIR = r"e:\FALLOUT Ult pjt\tools"
COMPILER = os.path.join(TOOLS_DIR, "compile.exe")

GP_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
HD_DIR = r"E:\Fallout2_Ultimate\Fallout2_HD"
REPO_DIR = r"e:\FALLOUT Ult pjt"

# -------------------------------------------------------------
# 1. gl_highlighting.ssl
# -------------------------------------------------------------
ssl_highlighting = """/*
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
*/

#pragma sce
#define SCRIPT_REALNAME "gl_highlighting"
#include "headers/define.h"
#include "headers/sfall/sfall.h"
#include "headers/sfall/define_extra.h"

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

variable persistent_active := 0;
variable shift_hold_active := 0;
variable last_dude_tile    := -1;

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
   // Single clean display refresh only upon turning off
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
               if (obj_is_locked(obj)) then
                  set_outline(obj, COLOR_LOCKED);
               else if (IS_EMPTY(obj)) then
                  set_outline(obj, COLOR_CONTAINER_EMPTY);
               else
                  set_outline(obj, COLOR_CONTAINERS);
            end else begin
               set_outline(obj, COLOR_ITEMS);
            end
         end
      end
   end

   // 2. Dead Bodies (yellow if holding items, gray if empty)
   foreach obj in list_as_array(LIST_CRITTERS) begin
      if (obj and obj != dude_obj) then begin
         if (elevation(obj) == dude_elev) then begin
            isCorpse := (critter_state(obj) == 1);
            if (isCorpse and not NO_STEAL(obj)) then begin
               if (not IS_EMPTY(obj)) then
                  set_outline(obj, COLOR_CORPSES);
               else
                  set_outline(obj, COLOR_CORPSE_EMPTY);
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
               if (obj_is_locked(obj) and not obj_is_open(obj)) then
                  set_outline(obj, COLOR_LOCKED);
               else
                  set_outline(obj, COLOR_INTERACTIVE_SCENERY);
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
      set_sfall_global("GL_PERM_HIGH", persistent_active);
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

procedure start begin
   variable gmode;
   if game_loaded then begin
      if (sfall_ver_major < 4) then return;
      persistent_active := get_sfall_global_int("GL_PERM_HIGH");

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
"""

# -------------------------------------------------------------
# 2. gl_qol_interface.ssl
# -------------------------------------------------------------
ssl_qol = """/*
   Fallout 2 Ultimate Wasteland Edition 2026
   Quality of Life Interface Enhancements (gl_qol_interface.ssl)
   - Click outside inventory/container to close (Fast Exit)
   - STRICTLY EXCLUDES BARTER (SHOP), DIALOGUE, AND COMBAT to allow
     mouse quantity selection and trade confirmation without interference!
   - Fully aware of dual-column inventory (ExpandInventory=1: 570px/673px)
   - Fully aware of InventoryFilter category tabs (left & right side panels)
   - Expanded Done / ГОТОВО clickable hit-box for inventory
   - Optional Auto-Close on Take All / Empty Container
*/

#pragma sce
#define SCRIPT_REALNAME "gl_qol_interface"

#include "headers/define.h"
#include "headers/sfall/sfall.h"
#include "headers/sfall/define_extra.h"

#define INI_FILE "mods\\\\gl_qol_interface.ini"
#define WINTYPE_INV (0)

variable cfg_loaded := 0;
variable cfg_click_outside := 1;
variable cfg_expanded_done := 1;
variable cfg_auto_close_empty := 0;
variable cfg_take_all_close := 1;

procedure start;
procedure load_config;
procedure mouseclick_handler;
procedure keypress_handler;
procedure invenmove_handler;

procedure load_config begin
   variable val;
   if (cfg_loaded) then return;

   val := get_ini_setting(INI_FILE + "|Settings|ClickOutsideClosesInventory");
   if (val >= 0) then cfg_click_outside := val; else cfg_click_outside := 1;

   val := get_ini_setting(INI_FILE + "|Settings|ExpandedDoneButtonArea");
   if (val >= 0) then cfg_expanded_done := val; else cfg_expanded_done := 1;

   val := get_ini_setting(INI_FILE + "|Settings|AutoCloseEmptyContainers");
   if (val >= 0) then cfg_auto_close_empty := val; else cfg_auto_close_empty := 0;

   val := get_ini_setting(INI_FILE + "|Settings|CloseOnTakeAllKey");
   if (val >= 0) then cfg_take_all_close := val; else cfg_take_all_close := 1;

   cfg_loaded := 1;
end

procedure start begin
   if game_loaded then begin
      if (sfall_ver_major < 4) then return;
      call load_config;
      register_hook_proc(HOOK_MOUSECLICK, mouseclick_handler);
      register_hook_proc(HOOK_KEYPRESS, keypress_handler);
      register_hook_proc(HOOK_INVENTORYMOVE, invenmove_handler);
   end
end

procedure mouseclick_handler begin
   variable pressed, button, mx, my, wx, wy, ww, wh, gmode;
   variable eff_ww, eff_wh, min_safe_x, max_safe_x, min_safe_y, max_safe_y;

   pressed := get_sfall_arg;
   button  := get_sfall_arg;

   // Trigger only on left mouse click press (button 0, pressed 1)
   if (pressed != 1 or button != 0) then return;

   gmode := get_game_mode;

   // 1. ABSOLUTE EXCLUSIONS: Never intercept clicks during Barter (Store), Dialogue, or Combat!
   // In Barter, the player is buying/selling items and using the quantity selection slider/dialog.
   if (gmode bwand (BARTER bwor DIALOG bwor COMBAT bwor PCOMBAT)) then return;

   // 2. Only operate during standard Inventory or Container Loot screens
   if ((gmode bwand (INVENTORY bwor INTFACELOOT)) == 0) then return;
   if (not intface_is_shown(WINTYPE_INV)) then return;

   call load_config;

   wx := get_interface_x(WINTYPE_INV);
   wy := get_interface_y(WINTYPE_INV);
   ww := get_interface_width(WINTYPE_INV);
   wh := get_interface_height(WINTYPE_INV);

   mx := get_mouse_x;
   my := get_mouse_y;

   // Calculate effective dimensions taking into account dual-column inventory (ExpandInventory=1)
   // INVBOX2.frm = 570x377, LOOT2.frm = 673x376
   eff_ww := ww;
   if (eff_ww < 570) then eff_ww := 570;
   if ((gmode bwand INTFACELOOT) and (eff_ww < 673)) then eff_ww := 673;

   eff_wh := wh;
   if (eff_wh < 376) then eff_wh := 376;

   // 1. Click outside the inventory/loot window bounds -> Close immediately
   // Safe margins protect:
   // - Left side category filter tabs (Weapons, Ammo, Armor, Drugs, Tools, Misc, Caps): wx - 75 .. wx
   // - Right side container filter tabs: wx + eff_ww .. wx + eff_ww + 75
   // - Top swap party/container bar: wy - 45 .. wy
   // - Bottom drop-all/take-all panel: wy + eff_wh .. wy + eff_wh + 50
   if (cfg_click_outside) then begin
      min_safe_x := wx - 75;
      max_safe_x := wx + eff_ww + 75;
      min_safe_y := wy - 45;
      max_safe_y := wy + eff_wh + 50;

      // Only close when click is strictly OUTSIDE the interface and all its tabs/panels
      if (mx < min_safe_x or mx > max_safe_x or my < min_safe_y or my > max_safe_y) then begin
         tap_key(1); // Simulate ESC
         set_sfall_return(0);
         return;
      end
   end

   // 2. Click in the expanded Done / ГОТОВО text area (bottom-right plate, left of the red button)
   // Native red button (wx + eff_ww - 35 .. wx + eff_ww - 5) is handled by the engine.
   if (cfg_expanded_done) then begin
      if (mx >= (wx + eff_ww - 140) and mx <= (wx + eff_ww - 36) and my >= (wy + eff_wh - 48) and my <= (wy + eff_wh - 6)) then begin
         tap_key(1); // Simulate ESC / Done
         set_sfall_return(0);
         return;
      end
   end
end

procedure keypress_handler begin
   variable pressed, scancode, gmode;
   pressed  := get_sfall_arg;
   scancode := get_sfall_arg;

   if (not cfg_take_all_close or pressed != 1) then return;

   // Key 'D' (scancode 32) is standard Take All key in InventoryFilter
   if (scancode == 32) then begin
      gmode := get_game_mode;
      if (gmode bwand INTFACELOOT) then begin
         if (cfg_auto_close_empty) then begin
            tap_key(1);
         end
      end
   end
end

procedure invenmove_handler begin
   variable source, item, slot, gmode, l_obj;
   source := get_sfall_arg;
   item   := get_sfall_arg;
   slot   := get_sfall_arg;

   if (not cfg_auto_close_empty) then return;

   gmode := get_game_mode;
   if (gmode bwand INTFACELOOT) then begin
      l_obj := loot_obj;
      if (l_obj != 0) then begin
         if (inven_ptr(l_obj, 0) == 0) then begin
            tap_key(1);
         end
      end
   end
end
"""

def compile_script(ssl_text, ssl_name, int_name):
    ssl_path = os.path.join(TOOLS_DIR, ssl_name)
    int_path = os.path.join(TOOLS_DIR, int_name)
    with open(ssl_path, "w", encoding="cp1251") as f:
        f.write(ssl_text)

    cmd = [COMPILER, "-p", "-q", "-s", "-Iheaders", "-O2", ssl_name, "-o", int_name]
    res = subprocess.run(cmd, cwd=TOOLS_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR compiling {ssl_name}:")
        print(res.stderr)
        raise RuntimeError(f"Compilation failed for {ssl_name}")
    print(f"SUCCESS: {int_name} compiled ({os.path.getsize(int_path)} bytes)")
    return int_path

# Compile both scripts
hl_int = compile_script(ssl_highlighting, "gl_highlighting.ssl", "gl_highlighting.int")
qol_int = compile_script(ssl_qol, "gl_qol_interface.ssl", "gl_qol_interface.int")

# Deploy to VFS layer 1 (mods/rpu_russian_uncensored.dat/scripts/)
targets_scripts = [
    os.path.join(REPO_DIR, "mods", "rpu_russian_uncensored.dat", "scripts"),
    os.path.join(GP_DIR, "mods", "rpu_russian_uncensored.dat", "scripts"),
    os.path.join(HD_DIR, "mods", "rpu_russian_uncensored.dat", "scripts")
]

for d in targets_scripts:
    os.makedirs(d, exist_ok=True)
    shutil.copy2(hl_int, os.path.join(d, "gl_highlighting.int"))
    shutil.copy2(qol_int, os.path.join(d, "gl_qol_interface.int"))
    print(f"Deployed gl_highlighting.int & gl_qol_interface.int -> {d}")

# Clean up obsolete loose scripts to protect VFS
obsolete = [
    os.path.join(GP_DIR, "mods", "gl_highlighting.int"),
    os.path.join(HD_DIR, "mods", "gl_highlighting.int"),
    os.path.join(GP_DIR, "DATA", "scripts_disabled", "gl_highlighting.int"),
    os.path.join(HD_DIR, "DATA", "scripts_disabled", "gl_highlighting.int"),
    os.path.join(GP_DIR, "DATA", "scripts", "gl_highlighting.int"),
    os.path.join(HD_DIR, "DATA", "scripts", "gl_highlighting.int"),
    os.path.join(GP_DIR, "DATA", "scripts", "gl_qol_interface.int"),
    os.path.join(HD_DIR, "DATA", "scripts", "gl_qol_interface.int")
]
for obs in obsolete:
    if os.path.exists(obs):
        os.remove(obs)
        print(f"Cleaned up obsolete script: {obs}")

print("ALL DEPLOYMENTS AND CLEANUPS COMPLETED SUCCESSFULLY!")
