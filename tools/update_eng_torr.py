import os
from build_dual_language_pack import get_msg_from_dat, write_dual, RPU_ENG_DAT

eng_torr = get_msg_from_dat(RPU_ENG_DAT, "text/english/dialog/kctorr.msg").decode('latin1')
if "{900}" not in eng_torr:
    eng_torr += """
# --- Torr Combat & Dunton Encounter Additions ---
{247}{}{Torr, the Dunton brothers by the campfire want to steal your brahmin. Let's go teach them a lesson!}
{248}{}{Torr! Bad Dunton men want steal moo-moo! We go beat Duntons!}
{256}{}{Torr protect moo-moo! Torr break Dunton faces! Let's go!}
{257}{}{Argh! Duntons bad! Steal Torr's moo-moos?! Torr smash Dunton!}
{900}{}{Torr smash mean bugmen! For moo-moos!}
{901}{}{No touch friend of Torr! Torr hit you with stick!}
{902}{}{Bad men! Torr protect moo-moos!}
{903}{}{Torr strong! Torr smash!}
"""
write_dual(r"text\english\dialog\kctorr.msg", eng_torr.encode('latin1'))
print("Updated English kctorr.msg successfully across all targets!")
