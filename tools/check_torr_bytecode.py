from audit_maps_quests import extract_file, base
import os

patch_torr = extract_file(os.path.join(base, "talking_heads_that_rpu_map_update_patch.dat"), "scripts/kctorr.int")
th_torr = extract_file(os.path.join(base, "talking_heads.dat"), "scripts/kctorr.int")
uncens_torr = open(r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_russian_uncensored.dat\scripts\kctorr.int", "rb").read()

print("Patch Torr size:", len(patch_torr) if patch_torr else "None")
print("TH Torr size:", len(th_torr) if th_torr else "None")
print("Uncensored Torr size:", len(uncens_torr))

# Find opcode 0x808C (start_gdialog) or strings in binary
# In SSLC bytecode start_gdialog has an opcode or export
import struct

def find_gdialog_args(bytecode):
    # Opcode for start_gdialog in Fallout engine bytecode
    # Let's search for HEAD constant or background constant
    # Or check if HEAD_TORR exists in headers
    pass
