#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, struct

sys.path.append(r"e:\FALLOUT Ult pjt\tools")
from diff_engine import get_foxx_file, get_our_file

raw_lst, _ = get_foxx_file("proto\\items\\items.lst")
items_lst = [l.strip() for l in raw_lst.decode("ascii", errors="ignore").splitlines() if l.strip()]

def get_weapon_data(pid, get_fn):
    pro_fn = items_lst[pid - 1]
    raw, src = get_fn(f"proto\\items\\{pro_fn}")
    if not raw or len(raw) < 0x75: return None
    cost = int.from_bytes(raw[0x2c:0x34], "big")
    min_d = raw[0x3c]
    max_d = raw[0x44]
    rng = raw[0x4c]
    min_st = raw[0x58]
    ap = raw[0x5c]
    burst = raw[0x60]
    cap = raw[0x70]
    ammo_pid = raw[0x74]
    return {
        "Cost": cost, "MinD": min_d, "MaxD": max_d, "Range": rng,
        "AP": ap, "Burst": burst, "Cap": cap, "AmmoPID": ammo_pid, "Src": src
    }

def get_armor_data(pid, get_fn):
    pro_fn = items_lst[pid - 1]
    raw, src = get_fn(f"proto\\items\\{pro_fn}")
    if not raw or len(raw) < 0x60: return None
    cost = int.from_bytes(raw[0x2c:0x34], "big")
    ac = int.from_bytes(raw[0x24:0x28], "big", signed=True)
    dr_norm = int.from_bytes(raw[0x28:0x2c], "big", signed=True)
    dr_laser = int.from_bytes(raw[0x2c:0x30], "big", signed=True)
    dr_plasma = int.from_bytes(raw[0x34:0x38], "big", signed=True)
    dr_expl = int.from_bytes(raw[0x40:0x44], "big", signed=True)
    dt_norm = int.from_bytes(raw[0x44:0x48], "big", signed=True)
    dt_laser = int.from_bytes(raw[0x48:0x4c], "big", signed=True)
    dt_plasma = int.from_bytes(raw[0x50:0x54], "big", signed=True)
    dt_expl = int.from_bytes(raw[0x5c:0x60], "big", signed=True)
    return {
        "Cost": cost, "AC": ac, "DR_N": dr_norm, "DT_N": dt_norm,
        "DR_L": dr_laser, "DT_L": dt_laser, "DR_P": dr_plasma, "DT_P": dt_plasma, "Src": src
    }

def get_ammo_data(pid, get_fn):
    pro_fn = items_lst[pid - 1]
    raw, src = get_fn(f"proto\\items\\{pro_fn}")
    if not raw or len(raw) < 0x3c: return None
    cost = int.from_bytes(raw[0x2c:0x34], "big")
    cal = int.from_bytes(raw[0x24:0x28], "big")
    qty = int.from_bytes(raw[0x28:0x2c], "big")
    ac_mod = int.from_bytes(raw[0x2c:0x30], "big", signed=True)
    dr_mod = int.from_bytes(raw[0x30:0x34], "big", signed=True)
    dmg_mult = int.from_bytes(raw[0x34:0x38], "big", signed=True)
    dmg_div = int.from_bytes(raw[0x38:0x3c], "big", signed=True)
    return {
        "Cost": cost, "Cal": cal, "Qty": qty, "AC_Mod": ac_mod,
        "DR_Mod": dr_mod, "Mult": dmg_mult, "Div": dmg_div, "Src": src
    }

print("="*95)
print("1. ОРУЖИЕ (WEAPONS)")
print(f"{'Weapon':20} | {'Foxx (Vanilla RPU)':32} | {'Our Build (EcCo Overhaul)':32}")
print("="*95)
weapons = [
    (8, "10mm Pistol"), (10, "Hunting Rifle"), (23, "Assault Rifle"),
    (242, "Combat Shotgun"), (15, "Plasma Rifle"), (16, "Laser Rifle"),
    (115, "Super Sledge"), (12, "Minigun"), (28, "Sniper Rifle"),
    (299, "Gauss Rifle"), (388, "Pipe Rifle")
]
for pid, name in weapons:
    f = get_weapon_data(pid, get_foxx_file)
    o = get_weapon_data(pid, get_our_file)
    f_s = f"Dmg:{f['MinD']}-{f['MaxD']} Rng:{f['Range']} AP:{f['AP']} B:{f['Burst']} C:{f['Cap']}"
    o_s = f"Dmg:{o['MinD']}-{o['MaxD']} Rng:{o['Range']} AP:{o['AP']} B:{o['Burst']} C:{o['Cap']}"
    diff = "  " if f_s == o_s else "* "
    print(f"{diff}{name:18} | {f_s:32} | {o_s:32}")

print("\n" + "="*95)
print("2. БРОНЯ (ARMOR)")
print(f"{'Armor':20} | {'Foxx (AC / DR-Norm / DT-Norm)':32} | {'Our Build (EcCo Overhaul)':32}")
print("="*95)
armors = [
    (1, "Leather Armor"), (2, "Metal Armor"), (17, "Combat Armor"),
    (3, "Power Armor"), (232, "Hardened Power Armor"), (348, "Adv Power Armor")
]
for pid, name in armors:
    f = get_armor_data(pid, get_foxx_file)
    o = get_armor_data(pid, get_our_file)
    f_s = f"AC:{f['AC']:2d} | DR:{f['DR_N']:2d}% | DT:{f['DT_N']:2d}"
    o_s = f"AC:{o['AC']:2d} | DR:{o['DR_N']:2d}% | DT:{o['DT_N']:2d}"
    diff = "  " if f_s == o_s else "* "
    print(f"{diff}{name:18} | {f_s:32} | {o_s:32}")

print("\n" + "="*95)
print("3. БОЕПРИПАСЫ (AMMO MODIFIERS)")
print(f"{'Ammo':20} | {'Foxx (DR-Mod / AC-Mod / Mult:Div)':32} | {'Our Build (EcCo Overhaul)':32}")
print("="*95)
ammos = [
    (29, "10mm JHP"), (30, "10mm AP"), (35, "5mm JHP"), (36, "5mm AP"),
    (95, "Small Energy Cell"), (38, "Micro Fusion Cell"), (14, "Shotgun Shells")
]
for pid, name in ammos:
    f = get_ammo_data(pid, get_foxx_file)
    o = get_ammo_data(pid, get_our_file)
    f_s = f"DR:{f['DR_Mod']:3d}% | AC:{f['AC_Mod']:2d} | {f['Mult']}/{f['Div']}"
    o_s = f"DR:{o['DR_Mod']:3d}% | AC:{o['AC_Mod']:2d} | {o['Mult']}/{o['Div']}"
    diff = "  " if f_s == o_s else "* "
    print(f"{diff}{name:18} | {f_s:32} | {o_s:32}")
