# -*- coding: utf-8 -*-
import os
import sys

BASE_DIR = r"E:\FALLOUT Ult pjt"
WV_DIR = os.path.join(BASE_DIR, "standalone_mods", "wasteland_voices")
SCRIPTS_DIR = os.path.join(WV_DIR, "scripts")

CORE_SSL = os.path.join(SCRIPTS_DIR, "gl_wv_core.ssl")
EXT_SSL = os.path.join(SCRIPTS_DIR, "gl_wv_extended.ssl")

NEW_CORE_CODE = """/*
   Wasteland Voices // Живые Голоса Пустоши (v1.0.0)
   КОНТУР 1: Core RPU Content & Companion Combat Shouts
   Standalone Narrative Mod for Fallout 2 (RPU / Definitive Edition)
   Стандарт Black Isle Studios 1998
*/

#pragma sce
#define SCRIPT_REALNAME "gl_wv_core"

#include "headers/define.h"
#include "headers/command.h"
#include "headers/sfall/sfall.h"
#include "headers/sfall/define_extra.h"
#include "headers/sfall/lib.arrays.h"
#include "headers/maps.h"
#include "headers/party.h"
#include "headers/aipacket.h"
#include "headers/itempid.h"
#include "headers/global.h"

#define INI_FILE "mods\\\\wasteland_voices.ini"

#define dude_has_heavy_weapon (\\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_AVENGER_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_VINDICATOR_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_BOZAR) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_FLAMER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_IMPROVED_FLAMETHROWER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_ROCKET_LAUNCHER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_AVENGER_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_VINDICATOR_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_BOZAR) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_FLAMER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_IMPROVED_FLAMETHROWER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_ROCKET_LAUNCHER))

variable cfg_loaded;
variable cfg_enabled;
variable cfg_core_rpu;
variable cfg_cooldown;
variable cfg_rng_chance;
variable cfg_show_init;
variable cfg_react_pa;
variable cfg_react_hw;
variable cfg_react_comp;
variable cfg_react_iq;

variable last_shout_time;

procedure start;
procedure load_config;
procedure stdprocedure_handler;
procedure combatdamage_handler;
procedure is_generic_citizen(variable cr);
procedure get_freak_companion;
procedure get_player_react_line;
procedure get_quest_line;
procedure get_small_talk_line;
procedure get_town_line_id;
procedure get_nearby_alive_companion;
procedure get_companion_shout_hurt(variable comp_obj);
procedure get_companion_shout_crit(variable comp_obj);

procedure load_config begin
   variable val;
   if (cfg_loaded) then return;

   val := get_ini_setting(INI_FILE + "|General|EnableMod");
   if (val >= 0) then cfg_enabled := val; else cfg_enabled := 1;

   val := get_ini_setting(INI_FILE + "|Modules|EnableCoreRPU");
   if (val >= 0) then cfg_core_rpu := val; else cfg_core_rpu := 1;

   val := get_ini_setting(INI_FILE + "|General|MinCooldownSeconds");
   if (val > 0) then cfg_cooldown := val; else cfg_cooldown := 90;

   val := get_ini_setting(INI_FILE + "|General|RNGChance");
   if (val > 0) then cfg_rng_chance := val; else cfg_rng_chance := 20;

   val := get_ini_setting(INI_FILE + "|General|ShowInitMessage");
   if (val >= 0) then cfg_show_init := val; else cfg_show_init := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToPowerArmor");
   if (val >= 0) then cfg_react_pa := val; else cfg_react_pa := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToHeavyWeapons");
   if (val >= 0) then cfg_react_hw := val; else cfg_react_hw := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToCompanions");
   if (val >= 0) then cfg_react_comp := val; else cfg_react_comp := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToLowIQ");
   if (val >= 0) then cfg_react_iq := val; else cfg_react_iq := 1;

   cfg_loaded := 1;
end

procedure is_generic_citizen(variable cr) begin
   variable ai, pid;
   if (cr == 0 or cr == dude_obj) then return false;
   if (is_critter_dead(cr)) then return false;

   pid := obj_pid(cr);
   if (party_member_obj(pid) != 0) then return false;
   if (pid == PID_SULIK or pid == PID_VIC or pid == PID_MYRON or pid == PID_JOHN_MACRAE) then return false;
   if (pid == PID_MARCUS or pid == PID_LENNY or pid == PID_GORIS or pid == PID_MIRIA) then return false;
   if (pid == PID_DAVIN or pid == PID_ROBOBRAIN or pid == PID_CYBERDOG or pid == PID_DOGMEAT) then return false;

   ai := has_trait(TRAIT_OBJECT, cr, OBJECT_AI_PACKET);

   if (ai == AI_PEASANT or ai == AI_WIMPY_PEASANT or ai == AI_TOUGH_CITIZEN) then return true;
   if (ai == AI_LONER_CITIZEN or ai == AI_PEASANT_NO_MOVE) then return true;
   if (ai == AI_PRIMITIVE_COWARD or ai == AI_PRIMITIVE_KAMAKAZI) then return true;
   if (ai == AI_SLAVE or ai == AI_ADDICT or ai == AI_CRAZY_ADDICT) then return true;
   if (ai == AI_REDDING_MINER or ai == AI_VAULT_DEATHCLAW) then return true;

   return false;
end

procedure get_freak_companion begin
   if (party_member_obj(PID_MARCUS) != 0) then return 1;
   if (party_member_obj(PID_LENNY) != 0) then return 2;
   if (party_member_obj(PID_GORIS) != 0) then return 3;
   return 0;
end

procedure get_player_react_line begin
   variable roll, comp;
   roll := random(1, 100);

   if (cfg_react_iq and dude_is_stupid) then begin
      if (roll <= 40) then return random(5880, 5886);
   end else if (cfg_react_pa and dude_wearing_power_armor) then begin
      if (roll <= 35) then return random(5800, 5809);
   end else if (cfg_react_hw and dude_has_heavy_weapon) then begin
      if (roll <= 35) then return random(5830, 5835);
   end else if (cfg_react_comp) then begin
      comp := get_freak_companion;
      if (comp > 0 and roll <= 35) then begin
         if (comp == 1) then return random(5850, 5852);
         else if (comp == 2) then return random(5853, 5854);
         else if (comp == 3) then return random(5855, 5856);
         else return 5857;
      end
   end

   return 0;
end

procedure get_quest_line begin
   variable t, line;
   t := cur_town;
   line := 0;

   if (t == AREA_ARROYO) then begin
      if (global_var(GVAR_FALLOUT_2) == 8) then return random(5500, 5502);
      if (global_var(GVAR_ARROYO_DOG) == 1) then return random(5503, 5505);
      if (global_var(GVAR_ARROYO_DOG) == 2) then return random(5506, 5508);
      if (global_var(GVAR_KILL_EVIL_PLANTS) == 2) then return random(5509, 5511);
   end else if (t == AREA_KLAMATH) then begin
      if (global_var(GVAR_STILL_STATUS) == 1) then return random(5512, 5514);
      if (global_var(GVAR_TORR_GUARD_STATUS) == 1) then return random(5515, 5517);
      if (global_var(GVAR_SMILEY_STATUS) == 1) then return random(5518, 5521);
   end else if (t == AREA_DEN) then begin
      if (global_var(GVAR_DEN_VIC_STATUS) == 1) then return random(5530, 5532);
      if (global_var(GVAR_DEN_GANGWAR) == 1) then return random(5533, 5535);
      if (global_var(GVAR_DEN_MAGGIE_STILL) == 1) then return random(5536, 5538);
      if (global_var(GVAR_DEN_FRED_STATUS) == 1) then return random(5539, 5542);
      if (global_var(GVAR_DEN_FLAG_1) == 1) then return random(5543, 5545);
   end else if (t == AREA_MODOC) then begin
      if (global_var(GVAR_MODOC_GHOST_FARM_SEED) == 1) then return random(5550, 5552);
      if (global_var(GVAR_MODOC_KARL_SEED) == 1) then return random(5553, 5555);
      if (global_var(GVAR_MODOC_FAMILY_FEUD_SEED_ONE) == 1) then return random(5556, 5558);
      if (global_var(GVAR_MODOC_JONNY_HOME) == 1) then return random(5559, 5561);
   end else if (t == AREA_VAULT_CITY) then begin
      if (global_var(GVAR_VAULT_CITIZEN) == 1) then return random(5570, 5572);
      if (global_var(GVAR_VAULT_CITY_VENT) == 1) then return random(5573, 5575);
      if (global_var(GVAR_VAULT_GECKO_PLANT) == 1) then return random(5576, 5578);
      if (global_var(GVAR_VAULT_RAIDERS) == 1) then return random(5579, 5581);
   end else if (t == AREA_GECKO) then begin
      if (global_var(GVAR_GECKO_ECON_DISK) == 1) then return random(5600, 5602);
      if (global_var(GVAR_GECKO_REQ_FORM) == 1) then return random(5603, 5605);
      if (global_var(GVAR_GECKO_SKEETER_PART) == 1) then return random(5606, 5608);
      if (global_var(GVAR_GECKO_BRAIN_FRIEND) == 1) then return random(5609, 5611);
   end else if (t == AREA_BROKEN_HILLS) then begin
      if (global_var(GVAR_BH_MINE) == 1) then return random(5620, 5622);
      if (global_var(GVAR_BH_CONSPIRACY) == 1) then return random(5623, 5625);
      if (global_var(GVAR_BH_JAIL) == 1) then return random(5626, 5628);
      if (global_var(GVAR_BH_POWER) == 1) then return random(5629, 5631);
   end else if (t == AREA_NEW_RENO) then begin
      if (global_var(GVAR_NEW_RENO_FLAG_1) == 1) then return random(5640, 5642);
      if (global_var(GVAR_NEW_RENO_FLAG_2) == 1) then return random(5643, 5645);
      if (global_var(GVAR_NEW_RENO_FLAG_3) == 1) then return random(5646, 5648);
      if (global_var(GVAR_NEW_RENO_FLAG_4) == 1) then return random(5649, 5651);
      if (global_var(GVAR_MADE_MAN_SALVATORE) == 1) then return random(5652, 5654);
      if (global_var(GVAR_MADE_MAN_BISHOP) == 1) then return random(5655, 5657);
      if (global_var(GVAR_MADE_MAN_MORDINO) == 1) then return random(5658, 5661);
      if (global_var(GVAR_MADE_MAN_WRIGHT) == 1) then return random(5662, 5665);
   end else if (t == AREA_REDDING) then begin
      if (global_var(GVAR_REDDING_EXCAVATOR_CHIP) == 1) then return random(5670, 5672);
      if (global_var(GVAR_REDDING_JOHNSON_STATUS) == 1) then return random(5673, 5675);
      if (global_var(GVAR_REDDING_SHERIFF) == 1) then return random(5676, 5678);
      if (global_var(GVAR_WANAMINGO_OCCUPADO) == 1) then return random(5679, 5682);
   end else if (t == AREA_NCR) then begin
      if (global_var(GVAR_NCR_TANDI_WORK) == 1) then return random(5690, 5692);
      if (global_var(GVAR_NCR_V15_DARION_DEAD) == 1) then return random(5693, 5695);
      if (global_var(GVAR_NCR_SPY_KNOWN) == 1) then return random(5696, 5698);
      if (global_var(GVAR_NCR_WESTIN_SEED) == 1) then return random(5699, 5701);
   end else if (t == AREA_VAULT_15) then begin
      if (global_var(GVAR_V15_SEED_STATUS) == 1) then return random(5710, 5712);
      if (global_var(GVAR_NCR_V15_DARION_DEAD) == 1) then return random(5713, 5716);
   end

   return line;
end

procedure get_small_talk_line begin
   variable t, line;
   t := cur_town;
   line := 0;

   if (t == AREA_ARROYO) then line := random(5010, 5025);
   else if (t == AREA_DEN) then line := random(5030, 5045);
   else if (t == AREA_KLAMATH) then line := random(5050, 5065);
   else if (t == AREA_MODOC) then line := random(5070, 5085);
   else if (t == AREA_VAULT_CITY) then line := random(5090, 5105);
   else if (t == AREA_GECKO) then line := random(5130, 5145);
   else if (t == AREA_BROKEN_HILLS) then line := random(5150, 5169);
   else if (t == AREA_NEW_RENO) then line := random(5170, 5185);
   else if (t == AREA_VAULT_15) then line := random(5210, 5225);
   else if (t == AREA_NCR) then line := random(5190, 5209);
   else if (t == AREA_VAULT_13) then line := random(5230, 5245);
   else if (t == AREA_REDDING) then line := random(5110, 5125);
   else if (t == AREA_SAN_FRANCISCO) then line := random(5250, 5275);
   else if (t == AREA_NAVARRO) then line := random(5280, 5299);
   else if (t == AREA_THE_ENCLAVE) then line := random(5300, 5315);

   return line;
end

procedure get_town_line_id begin
   variable line;
   line := get_player_react_line;
   if (line > 0) then return line;

   if (random(1, 100) <= 50) then begin
      line := get_quest_line;
      if (line > 0) then return line;
   end

   return get_small_talk_line;
end

procedure stdprocedure_handler begin
   variable proc_id, self, source, is_end, line_id;
   proc_id := get_sfall_arg;
   self    := get_sfall_arg;
   source  := get_sfall_arg;
   is_end  := get_sfall_arg;

   if (proc_id != 11 or is_end != 0) then return;
   if (source != dude_obj) then return;
   if (combat_is_initialized) then return;

   call load_config;
   if (not cfg_enabled or not cfg_core_rpu) then return;

   if (is_generic_citizen(self)) then begin
      line_id := get_town_line_id;
      if (line_id > 0) then begin
         float_msg(self, mstr_custom(line_id), FLOAT_MSG_NORMAL);
         set_sfall_return(-1);
         return;
      end
   end
end

procedure get_nearby_alive_companion begin
   variable c;
   c := party_member_obj(PID_SULIK);
   if (c != 0 and not is_critter_dead(c) and tile_distance_objs(dude_obj, c) <= 12) then return c;
   c := party_member_obj(PID_VIC);
   if (c != 0 and not is_critter_dead(c) and tile_distance_objs(dude_obj, c) <= 12) then return c;
   c := party_member_obj(PID_JOHN_MACRAE);
   if (c != 0 and not is_critter_dead(c) and tile_distance_objs(dude_obj, c) <= 12) then return c;
   c := party_member_obj(PID_MIRIA);
   if (c != 0 and not is_critter_dead(c) and tile_distance_objs(dude_obj, c) <= 12) then return c;
   c := party_member_obj(PID_MARCUS);
   if (c != 0 and not is_critter_dead(c) and tile_distance_objs(dude_obj, c) <= 12) then return c;
   return 0;
end

procedure get_companion_shout_hurt(variable comp_obj) begin
   variable pid;
   pid := obj_pid(comp_obj);
   if (pid == PID_SULIK) then return random(5950, 5952);
   else if (pid == PID_VIC) then return random(5953, 5955);
   else if (pid == PID_JOHN_MACRAE) then return random(5956, 5958);
   else if (pid == PID_MIRIA) then return random(5959, 5961);
   else if (pid == PID_MARCUS) then return random(5962, 5964);
   return 0;
end

procedure get_companion_shout_crit(variable comp_obj) begin
   variable pid;
   pid := obj_pid(comp_obj);
   if (pid == PID_SULIK) then return random(5970, 5972);
   else if (pid == PID_VIC) then return random(5973, 5975);
   else if (pid == PID_JOHN_MACRAE) then return random(5976, 5978);
   else if (pid == PID_MIRIA) then return random(5979, 5981);
   else if (pid == PID_MARCUS) then return random(5982, 5984);
   return 0;
end

procedure combatdamage_handler begin
   variable target, attacker, damage, flags, comp, shout_id;
   target   := get_sfall_arg;
   attacker := get_sfall_arg;
   damage   := get_sfall_arg;
   flags    := get_sfall_arg;

   if (target == 0 or attacker == 0) then return;

   // Защита от спама: не чаще 1 выкрика за 40 тиков (4 секунды)
   if (game_time - last_shout_time < 40) then return;

   // 1. Избранный тяжело ранен (здоровье упало ниже 25%)
   if (target == dude_obj and damage >= 12) then begin
      if ((get_critter_stat(dude_obj, STAT_current_hp) - damage) <= (get_critter_stat(dude_obj, STAT_max_hp) / 4)) then begin
         comp := get_nearby_alive_companion;
         if (comp != 0) then begin
            shout_id := get_companion_shout_hurt(comp);
            if (shout_id > 0) then begin
               float_msg(comp, mstr_custom(shout_id), FLOAT_MSG_RED);
               last_shout_time := game_time;
               return;
            end
         end
      end
   end

   // 2. Спутник совершил сокрушительный критический удар
   if (party_member_obj(obj_pid(attacker)) != 0 and damage >= 25 and (flags bwand DAM_CRITICAL)) then begin
      if (random(1, 100) <= 45) then begin
         shout_id := get_companion_shout_crit(attacker);
         if (shout_id > 0) then begin
            float_msg(attacker, mstr_custom(shout_id), FLOAT_MSG_NORMAL);
            last_shout_time := game_time;
            return;
         end
      end
   end
end

procedure start begin
   if game_loaded then begin
      call load_config;
      if (cfg_enabled and cfg_core_rpu) then begin
         register_hook_proc(HOOK_STDPROCEDURE, stdprocedure_handler);
         register_hook_proc(HOOK_COMBATDAMAGE, combatdamage_handler);
         if (cfg_show_init) then begin
            display_msg(mstr_custom(5000));
            display_msg(mstr_custom(5001));
         end
      end
   end
end
"""

NEW_EXT_CODE = """/*
   Wasteland Voices // Живые Голоса Пустоши (v1.0.0)
   КОНТУР 2: Extended Wasteland Content & Miria Travel Reactivity
   Standalone Narrative Mod for Fallout 2 (RPU / Definitive Edition)
   Стандарт Black Isle Studios 1998
*/

#pragma sce
#define SCRIPT_REALNAME "gl_wv_ext"

#include "headers/define.h"
#include "headers/command.h"
#include "headers/sfall/sfall.h"
#include "headers/sfall/define_extra.h"
#include "headers/sfall/lib.arrays.h"
#include "headers/maps.h"
#include "headers/party.h"
#include "headers/aipacket.h"
#include "headers/itempid.h"
#include "headers/global.h"

#define INI_FILE "mods\\\\wasteland_voices.ini"

#define dude_has_heavy_weapon (\\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_AVENGER_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_VINDICATOR_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_BOZAR) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_FLAMER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_IMPROVED_FLAMETHROWER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_RIGHT_HAND)) == PID_ROCKET_LAUNCHER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_AVENGER_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_VINDICATOR_MINIGUN) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_BOZAR) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_FLAMER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_IMPROVED_FLAMETHROWER) or \\
   (obj_pid(critter_inven_obj(dude_obj,INVEN_TYPE_LEFT_HAND)) == PID_ROCKET_LAUNCHER))

variable cfg_loaded;
variable cfg_enabled;
variable cfg_extended;
variable cfg_cooldown;
variable cfg_rng_chance;
variable cfg_show_init;
variable cfg_react_pa;
variable cfg_react_hw;
variable cfg_react_comp;
variable cfg_react_iq;

variable last_miria_town;

procedure start;
procedure load_config;
procedure map_enter_p_proc;
procedure ext_stdprocedure_handler;
procedure is_generic_ext_critter(variable cr);
procedure get_freak_companion;
procedure get_player_react_line;
procedure get_extended_quest_line;
procedure get_extended_line_id;
procedure get_miria_city_line(variable town_id);

procedure load_config begin
   variable val;
   if (cfg_loaded) then return;

   val := get_ini_setting(INI_FILE + "|General|EnableMod");
   if (val >= 0) then cfg_enabled := val; else cfg_enabled := 1;

   val := get_ini_setting(INI_FILE + "|Modules|EnableExtendedMods");
   if (val >= 0) then cfg_extended := val; else cfg_extended := 1;

   val := get_ini_setting(INI_FILE + "|General|MinCooldownSeconds");
   if (val > 0) then cfg_cooldown := val; else cfg_cooldown := 90;

   val := get_ini_setting(INI_FILE + "|General|RNGChance");
   if (val > 0) then cfg_rng_chance := val; else cfg_rng_chance := 20;

   val := get_ini_setting(INI_FILE + "|General|ShowInitMessage");
   if (val >= 0) then cfg_show_init := val; else cfg_show_init := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToPowerArmor");
   if (val >= 0) then cfg_react_pa := val; else cfg_react_pa := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToHeavyWeapons");
   if (val >= 0) then cfg_react_hw := val; else cfg_react_hw := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToCompanions");
   if (val >= 0) then cfg_react_comp := val; else cfg_react_comp := 1;

   val := get_ini_setting(INI_FILE + "|Reactivity|ReactToLowIQ");
   if (val >= 0) then cfg_react_iq := val; else cfg_react_iq := 1;

   cfg_loaded := 1;
end

procedure is_generic_ext_critter(variable cr) begin
   variable ai, pid;
   if (cr == 0 or cr == dude_obj) then return false;
   if (is_critter_dead(cr)) then return false;

   pid := obj_pid(cr);
   if (party_member_obj(pid) != 0) then return false;
   if (pid == PID_SULIK or pid == PID_VIC or pid == PID_MYRON or pid == PID_JOHN_MACRAE) then return false;
   if (pid == PID_MARCUS or pid == PID_LENNY or pid == PID_GORIS or pid == PID_MIRIA) then return false;
   if (pid == PID_DAVIN or pid == PID_ROBOBRAIN or pid == PID_CYBERDOG or pid == PID_DOGMEAT) then return false;

   ai := has_trait(TRAIT_OBJECT, cr, OBJECT_AI_PACKET);

   if (ai == AI_PEASANT or ai == AI_WIMPY_PEASANT or ai == AI_TOUGH_CITIZEN) then return true;
   if (ai == AI_LONER_CITIZEN or ai == AI_PEASANT_NO_MOVE) then return true;
   if (ai == AI_PRIMITIVE_COWARD or ai == AI_PRIMITIVE_KAMAKAZI) then return true;
   if (ai == AI_SLAVE or ai == AI_ADDICT or ai == AI_CRAZY_ADDICT) then return true;
   if (ai == AI_NCR_RANGERS or ai == AI_SLAVER) then return true;

   return false;
end

procedure get_freak_companion begin
   if (party_member_obj(PID_MARCUS) != 0) then return 1;
   if (party_member_obj(PID_LENNY) != 0) then return 2;
   if (party_member_obj(PID_GORIS) != 0) then return 3;
   return 0;
end

procedure get_player_react_line begin
   variable roll, comp;
   roll := random(1, 100);

   if (cfg_react_iq and dude_is_stupid) then begin
      if (roll <= 40) then return random(5880, 5886);
   end else if (cfg_react_pa and dude_wearing_power_armor) then begin
      if (roll <= 35) then return random(5800, 5809);
   end else if (cfg_react_hw and dude_has_heavy_weapon) then begin
      if (roll <= 35) then return random(5830, 5835);
   end else if (cfg_react_comp) then begin
      comp := get_freak_companion;
      if (comp > 0 and roll <= 35) then begin
         if (comp == 1) then return random(5850, 5852);
         else if (comp == 2) then return random(5853, 5854);
         else if (comp == 3) then return random(5855, 5856);
         else return 5857;
      end
   end

   return 0;
end

procedure get_extended_quest_line begin
   variable t, line;
   t := cur_town;
   line := 0;

   if (t == AREA_ABBEY) then begin
      if (global_var(GVAR_ABBEY_PUMP) == 2 and random(1, 100) <= 60) then return random(5730, 5732);
      if (global_var(GVAR_ABBEY_BEAST) == 2 and random(1, 100) <= 60) then return random(5733, 5735);
      if (global_var(GVAR_ABBEY_PART) == 2 and random(1, 100) <= 60) then return random(5736, 5738);
   end else if (t == AREA_PRIMITIVE_TRIBE) then begin
      if (global_var(GVAR_FIXTRIBE_WELL) == 2 and random(1, 100) <= 60) then return random(5740, 5742);
      if (global_var(GVAR_SULIK_SISTER) == 2 and random(1, 100) <= 60) then return random(5743, 5745);
      if (global_var(GVAR_TRIBE_WEAPONS) == 2 and random(1, 100) <= 60) then return random(5746, 5748);
   end else if (t == AREA_EPA) then begin
      if (global_var(GVAR_KILL_EPAPLANTS) == 2 and random(1, 100) <= 60) then return random(5750, 5752);
      if (global_var(GVAR_FREE_EPASLAVES) == 2 and random(1, 100) <= 60) then return random(5753, 5755);
   end else if (t == AREA_VAULT_VILLAGE) then begin
      if ((global_var(GVAR_QUEST_VAULT_VILLAGE) == 2 or (global_var(GVAR_VAULT_VILLAGE_FLAGS) bwand 2)) and random(1, 100) <= 60) then return random(5760, 5763);
   end else if (t == AREA_SLAVER_CAMP) then begin
      if (global_var(GVAR_WIPED_OUT_SLAVER_CAMP) == 1 and random(1, 100) <= 70) then return random(5770, 5773);
   end else if (t == AREA_RANGER_SAFE1 or t == AREA_RANGER_SAFE2 or t == AREA_RANGER_SAFE3) then begin
      if (random(1, 100) <= 50) then return random(5775, 5778);
   end

   return line;
end

procedure get_extended_line_id begin
   variable t, line;
   t := cur_town;
   line := 0;

   // 1. Реакция на игрока
   line := get_player_react_line;
   if (line > 0) then return line;

   // 2. С вероятностью 50% квестовая реплика расширенных локаций
   if (random(1, 100) <= 50) then begin
      line := get_extended_quest_line;
      if (line > 0) then return line;
   end

   // 3. Фоновый срез локаций расширенных модов
   if (t == AREA_ABBEY) then begin
      line := random(5320, 5339);
   end else if (t == AREA_PRIMITIVE_TRIBE) then begin
      line := random(5340, 5359);
   end else if (t == AREA_EPA) then begin
      line := random(5360, 5375);
   end else if (t == AREA_VAULT_VILLAGE) then begin
      line := random(5380, 5395);
   end else if (t == AREA_RENO_STABLES) then begin
      line := random(5400, 5415);
   end else if (t == AREA_SLAVER_CAMP) then begin
      line := random(5420, 5435);
   end else if (t == AREA_RANGER_SAFE1 or t == AREA_RANGER_SAFE2 or t == AREA_RANGER_SAFE3) then begin
      line := random(5440, 5455);
   end else if (t == AREA_SAN_FRAN_SUB) then begin
      line := random(5460, 5475);
   end

   return line;
end

procedure ext_stdprocedure_handler begin
   variable proc_id, self, source, is_end, line_id;
   proc_id := get_sfall_arg;
   self    := get_sfall_arg;
   source  := get_sfall_arg;
   is_end  := get_sfall_arg;

   if (proc_id != 11 or is_end != 0) then return;
   if (source != dude_obj) then return;
   if (combat_is_initialized) then return;

   call load_config;
   if (not cfg_enabled or not cfg_extended) then return;

   if (is_generic_ext_critter(self)) then begin
      line_id := get_extended_line_id;
      if (line_id > 0) then begin
         float_msg(self, mstr_custom(line_id), FLOAT_MSG_NORMAL);
         set_sfall_return(-1);
         return;
      end
   end
end

procedure get_miria_city_line(variable town_id) begin
   if (town_id == AREA_NEW_RENO) then return random(5900, 5903);
   else if (town_id == AREA_VAULT_CITY) then return random(5904, 5907);
   else if (town_id == AREA_DEN) then return random(5908, 5911);
   else if (town_id == AREA_MODOC) then return random(5912, 5915);
   else if (town_id == AREA_KLAMATH) then return random(5916, 5919);
   else if (town_id == AREA_SAN_FRANCISCO) then return random(5920, 5923);
   else if (town_id == AREA_BROKEN_HILLS) then return random(5924, 5927);
   else if (town_id == AREA_REDDING) then return random(5928, 5931);
   else if (town_id == AREA_ABBEY) then return random(5932, 5934);
   else if (town_id == AREA_EPA) then return random(5935, 5937);
   else if (town_id == AREA_PRIMITIVE_TRIBE) then return random(5938, 5940);
   return random(5941, 5945);
end

procedure map_enter_p_proc begin
   variable miria_obj, t, line_id;

   call load_config;
   if (not cfg_enabled or not cfg_extended) then return;

   miria_obj := party_member_obj(PID_MIRIA);
   if (miria_obj == 0) then return;
   if (is_critter_dead(miria_obj)) then return;

   t := cur_town;
   if (t != 0 and t != last_miria_town) then begin
      last_miria_town := t;
      line_id := get_miria_city_line(t);
      if (line_id > 0) then begin
         float_msg(miria_obj, mstr_custom(line_id), FLOAT_MSG_YELLOW);
      end
   end
end

procedure start begin
   if game_loaded then begin
      call load_config;
      if (cfg_enabled and cfg_extended) then begin
         register_hook_proc(HOOK_STDPROCEDURE, ext_stdprocedure_handler);
      end
   end
end
"""

def update_scripts():
    print("[2/3] Обновление скриптов gl_wv_core.ssl и gl_wv_extended.ssl...")
    with open(CORE_SSL, "w", encoding="cp1251", errors="replace") as f:
        f.write(NEW_CORE_CODE.strip() + "\n")
    print(f"[OK] Обновлен {CORE_SSL}")

    with open(EXT_SSL, "w", encoding="cp1251", errors="replace") as f:
        f.write(NEW_EXT_CODE.strip() + "\n")
    print(f"[OK] Обновлен {EXT_SSL}")
    return True

if __name__ == "__main__":
    if update_scripts():
        print("Скрипты успешно обновлены.")
    else:
        sys.exit(1)
