#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FALLOUT 2 MOD COMPARATOR & DIFFERENTIAL EXTRACTION ENGINE (diff_engine.py)
-------------------------------------------------------------------------
Automated inspection, extraction, and comparison tool between
Foxx's Expansion Version (E:\\Games\\Fallout 2 (Expansion Version))
and Ultimate Wasteland Edition 2026 (E:\\Fallout2_Ultimate & E:\\FALLOUT Ult pjt).
Uses verified Big-Endian .PRO layout (Type fields start at 0x39 after SoundID u8@0x38)
and resolves VFS layers strictly via mods/mods_order.txt (top=lowest, bottom=highest).
"""

import argparse
import os
import re
import struct
import sys
import zlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_FOXX_ROOT = r"E:\Games\Fallout 2 (Expansion Version)"
DEFAULT_OUR_GP = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
DEFAULT_OUR_HD = r"E:\Fallout2_Ultimate\Fallout2_HD"
DEFAULT_OUR_PJT = r"E:\FALLOUT Ult pjt"


def list_dat2(dat_path):
    """Returns dict of {lowercase_inner_path: (real_size, packed_size, offset, is_compressed, name)}"""
    if not os.path.exists(dat_path) or os.path.isdir(dat_path):
        return {}
    with open(dat_path, "rb") as f:
        f.seek(-8, os.SEEK_END)
        tree_size, _file_size = struct.unpack("<II", f.read(8))
        f.seek(-tree_size - 8, os.SEEK_END)
        file_count = struct.unpack("<I", f.read(4))[0]
        files = {}
        for _ in range(file_count):
            name_len = struct.unpack("<I", f.read(4))[0]
            name = f.read(name_len).decode("ascii", errors="ignore")
            is_comp, r_sz, p_sz, offset = struct.unpack("<BIII", f.read(13))
            files[name.lower()] = (r_sz, p_sz, offset, is_comp, name)
        return files


def extract_dat2_file(dat_path, inner_path):
    """Extracts raw bytes of a file from DAT2 archive."""
    if not os.path.exists(dat_path) or os.path.isdir(dat_path):
        return None
    inner_norm = inner_path.replace("/", "\\").lower()
    with open(dat_path, "rb") as f:
        f.seek(-8, os.SEEK_END)
        tree_size, _file_size = struct.unpack("<II", f.read(8))
        f.seek(-tree_size - 8, os.SEEK_END)
        file_count = struct.unpack("<I", f.read(4))[0]
        for _ in range(file_count):
            name_len = struct.unpack("<I", f.read(4))[0]
            name = f.read(name_len).decode("ascii", errors="ignore")
            is_comp, _r_sz, p_sz, offset = struct.unpack("<BIII", f.read(13))
            if name.lower() == inner_norm:
                f.seek(offset)
                raw = f.read(p_sz)
                if is_comp == 1:
                    return zlib.decompress(raw)
                return raw
    return None


def get_foxx_file(inner_path, foxx_root=DEFAULT_FOXX_ROOT):
    """Resolves file from Foxx build: data/ override -> mods/ -> master.dat -> critter.dat."""
    inner_norm = inner_path.replace("/", "\\")
    direct_p = os.path.join(foxx_root, inner_norm)
    if os.path.exists(direct_p):
        with open(direct_p, "rb") as f:
            return f.read(), f"Direct: {direct_p}"

    data_p = os.path.join(foxx_root, "data", inner_norm)
    if os.path.exists(data_p):
        with open(data_p, "rb") as f:
            return f.read(), f"Data Override: {data_p}"

    mods_dir = os.path.join(foxx_root, "mods")
    if os.path.exists(mods_dir):
        for mod_entry in sorted(os.listdir(mods_dir), reverse=True):
            mp = os.path.join(mods_dir, mod_entry)
            if os.path.isdir(mp):
                candidate = os.path.join(mp, inner_norm)
                if os.path.exists(candidate):
                    with open(candidate, "rb") as f:
                        return f.read(), f"Mod Dir: {candidate}"
            elif mod_entry.lower().endswith(".dat"):
                raw = extract_dat2_file(mp, inner_norm)
                if raw is not None:
                    return raw, f"Mod DAT: {mod_entry}"

    master_p = os.path.join(foxx_root, "master.dat")
    raw = extract_dat2_file(master_p, inner_norm)
    if raw is not None:
        return raw, "master.dat"

    critter_p = os.path.join(foxx_root, "critter.dat")
    raw = extract_dat2_file(critter_p, inner_norm)
    if raw is not None:
        return raw, "critter.dat"

    if inner_norm.lower().startswith("text\\russian\\"):
        alt_inner = "text\\english\\" + inner_norm[len("text\\russian\\"):]
        raw = extract_dat2_file(master_p, alt_inner)
        if raw is not None:
            return raw, "master.dat (mapped text\\english)"

    return None, None


def get_our_mods_priority(our_root):
    """Reads mods/mods_order.txt top-to-bottom and returns entries reversed (highest override first)."""
    order_path = os.path.join(our_root, "mods", "mods_order.txt")
    mods = []
    if os.path.exists(order_path):
        with open(order_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith(";"):
                    mods.append(s)
    return list(reversed(mods))


def get_our_file(inner_path, our_root=DEFAULT_OUR_GP, our_pjt=DEFAULT_OUR_PJT):
    """Resolves file from our build strictly following DATA/ override -> mods/mods_order.txt (top override first) -> base DATs."""
    inner_norm = inner_path.replace("/", "\\")

    data_p = os.path.join(our_root, "DATA", inner_norm)
    if os.path.exists(data_p):
        with open(data_p, "rb") as f:
            return f.read(), f"Loose DATA: {data_p}"

    mods_dir = os.path.join(our_root, "mods")
    priority_dats = get_our_mods_priority(our_root)
    for dat_name in priority_dats:
        mp = os.path.join(mods_dir, dat_name)
        if not os.path.exists(mp):
            continue
        if os.path.isdir(mp):
            candidate = os.path.join(mp, inner_norm)
            if os.path.exists(candidate):
                with open(candidate, "rb") as f:
                    return f.read(), f"Our Mod Dir: {dat_name}"
        else:
            raw = extract_dat2_file(mp, inner_norm)
            if raw is not None:
                return raw, f"Our Mod DAT: {dat_name}"

    for base_dat in ["master.dat", "CRITTER.DAT"]:
        bp = os.path.join(our_root, base_dat)
        if os.path.exists(bp):
            raw = extract_dat2_file(bp, inner_norm)
            if raw is not None:
                return raw, f"Our Base: {base_dat}"

    pjt_candidate = os.path.join(our_pjt, inner_norm)
    if os.path.exists(pjt_candidate):
        with open(pjt_candidate, "rb") as f:
            return f.read(), f"Project Source: {pjt_candidate}"

    return None, None


def parse_msg(raw_bytes):
    """Parses .msg file into dict: {id: (sound_token, text)}."""
    if raw_bytes is None:
        return {}
    text = raw_bytes.decode("cp1251", errors="ignore")
    pattern = re.compile(r"\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}", re.DOTALL)
    entries = {}
    for match in pattern.finditer(text):
        msg_id = int(match.group(1))
        snd = match.group(2).strip()
        cnt = match.group(3).strip()
        entries[msg_id] = (snd, cnt)
    return entries


def diff_dialogue(msg_filename, our_root=DEFAULT_OUR_GP):
    """Performs deep dialogue line-by-line comparison for a given MSG filename."""
    if not msg_filename.lower().endswith(".msg"):
        msg_filename += ".msg"

    inner_rel = os.path.join("text", "russian", "dialog", msg_filename)
    foxx_raw, foxx_src = get_foxx_file(inner_rel)
    our_raw, our_src = get_our_file(inner_rel, our_root=our_root)

    print("=" * 80)
    print(f"DIALOGUE COMPARISON: {msg_filename}")
    print(f"Foxx Source: {foxx_src} (Raw: {len(foxx_raw) if foxx_raw else 0} bytes)")
    print(f"Our Source:  {our_src} (Raw: {len(our_raw) if our_raw else 0} bytes)")
    print("=" * 80)

    if not foxx_raw and not our_raw:
        print(f"[!] File {msg_filename} not found in either build.")
        return

    f_dict = parse_msg(foxx_raw)
    o_dict = parse_msg(our_raw)

    print(f"Total lines in Foxx: {len(f_dict)} | Total lines in Ours: {len(o_dict)}\n")

    only_foxx = sorted(set(f_dict.keys()) - set(o_dict.keys()))
    only_our = sorted(set(o_dict.keys()) - set(f_dict.keys()))
    both = sorted(set(f_dict.keys()) & set(o_dict.keys()))

    diff_lines = [mid for mid in both if f_dict[mid] != o_dict[mid]]

    if only_foxx:
        print(f"--- [LINES ONLY IN FOXX: {len(only_foxx)}] ---")
        for mid in only_foxx:
            snd, txt = f_dict[mid]
            snd_str = f"{{{snd}}}" if snd else "{}"
            print(f"+ FOXX {{{mid}}}{snd_str}{{{txt}}}")
        print()

    if only_our:
        print(f"--- [LINES ONLY IN OUR BUILD: {len(only_our)}] ---")
        for mid in only_our:
            snd, txt = o_dict[mid]
            snd_str = f"{{{snd}}}" if snd else "{}"
            print(f"- OUR  {{{mid}}}{snd_str}{{{txt}}}")
        print()

    if diff_lines:
        print(f"--- [MODIFIED / DIVERGENT LINES: {len(diff_lines)}] ---")
        for mid in diff_lines[:60]:
            f_snd, f_txt = f_dict[mid]
            o_snd, o_txt = o_dict[mid]
            print(f"Line {{{mid}}}:")
            print(f"  FOXX: {{{f_snd}}}{{{f_txt}}}")
            print(f"  OUR:  {{{o_snd}}}{{{o_txt}}}")
        if len(diff_lines) > 60:
            print(f"  ... ({len(diff_lines) - 60} more divergent lines omitted)")
        print()

    if not only_foxx and not only_our and not diff_lines:
        print("[=] Dialogue files are 100% IDENTICAL in texts, IDs, and tokens.")


def resolve_item_pro_filename(item_pid, raw_lst_bytes):
    """Maps 1-based item PID through items.lst to exact .pro filename."""
    pid_int = int(item_pid)
    if raw_lst_bytes:
        lines = [l.strip() for l in raw_lst_bytes.decode("latin-1", errors="ignore").splitlines() if l.strip()]
        if 1 <= pid_int <= len(lines):
            return lines[pid_int - 1].lower()
    return f"{pid_int:08d}.pro"


def parse_pro_item(raw_bytes):
    """
    Parses Fallout 2 binary item .pro (Big-Endian).
    Header: 0x00..0x24 (36 bytes)
    Common Item: 0x24..0x39 (21 bytes: MaterialID, Size, Weight, Cost, InvFID, SoundID u8@0x38)
    Type Data starts strictly at 0x39!
    """
    if not raw_bytes or len(raw_bytes) < 0x39:
        return None

    pid, text_id, _fid, _lr, _li, flags, _fext, sid, type_id = struct.unpack(">IIIIIIiIi", raw_bytes[:0x24])
    mat_id, size, weight, cost, inv_fid = struct.unpack(">IIIII", raw_bytes[0x24:0x38])
    sound_id = raw_bytes[0x38]

    types_map = {0: "Armor", 1: "Container", 2: "Drug", 3: "Weapon", 4: "Ammo", 5: "Misc", 6: "Key"}
    info = {
        "PID": pid,
        "TextID": text_id,
        "SID": sid,
        "Flags": f"0x{flags:08X}",
        "Type": types_map.get(type_id, f"Unknown ({type_id})"),
        "MaterialID": mat_id,
        "Size": size,
        "Weight": weight,
        "Cost": cost,
        "InvFID": inv_fid,
        "SoundID": sound_id,
        "RawLength": len(raw_bytes),
    }

    if type_id == 3 and len(raw_bytes) >= 0x79:
        (
            w_anim, min_dmg, max_dmg, dmg_type, max_range1, max_range2,
            proj_pid, min_st, ap1, ap2, crit_fail, perk, burst, cal, ammo_pid, max_ammo
        ) = struct.unpack(">IIIIIIiIIIIiIIiI", raw_bytes[0x39:0x79])
        info.update({
            "AnimCode": w_anim,
            "MinDmg": min_dmg,
            "MaxDmg": max_dmg,
            "DmgType": dmg_type,
            "RangePrimary": max_range1,
            "RangeSecondary": max_range2,
            "ProjPID": proj_pid,
            "MinST": min_st,
            "AP_Primary": ap1,
            "AP_Secondary": ap2,
            "CritFailTable": crit_fail,
            "Perk": perk,
            "BurstSize": burst,
            "Caliber": cal,
            "AmmoPID": ammo_pid,
            "MaxAmmo": max_ammo,
        })
    elif type_id == 0 and len(raw_bytes) >= 0x81:
        ac = struct.unpack(">i", raw_bytes[0x39:0x3D])[0]
        dr = struct.unpack(">7i", raw_bytes[0x3D:0x59])
        dt = struct.unpack(">7i", raw_bytes[0x59:0x75])
        perk, mfid, ffid = struct.unpack(">iII", raw_bytes[0x75:0x81])
        info.update({
            "AC": ac,
            "DR": dr,
            "DT": dt,
            "Perk": perk,
            "MaleFID": mfid,
            "FemaleFID": ffid,
        })
    elif type_id == 4 and len(raw_bytes) >= 0x51:
        cal, qty, ac_mod, dr_mod, dmg_mult, dmg_div = struct.unpack(">IIiiII", raw_bytes[0x39:0x51])
        info.update({
            "Caliber": cal,
            "PackQty": qty,
            "AC_Mod": ac_mod,
            "DR_Mod": dr_mod,
            "DmgMult": dmg_mult,
            "DmgDiv": dmg_div,
        })

    return info


def diff_proto(item_pid, our_root=DEFAULT_OUR_GP):
    """Compares binary PRO files between Foxx and Ours resolving via items.lst."""
    our_lst, _ = get_our_file(os.path.join("proto", "items", "items.lst"), our_root=our_root)
    foxx_lst, _ = get_foxx_file(os.path.join("proto", "items", "items.lst"))

    our_pro_fn = resolve_item_pro_filename(item_pid, our_lst)
    foxx_pro_fn = resolve_item_pro_filename(item_pid, foxx_lst)

    foxx_raw, foxx_src = get_foxx_file(os.path.join("proto", "items", foxx_pro_fn))
    our_raw, our_src = get_our_file(os.path.join("proto", "items", our_pro_fn), our_root=our_root)

    print("=" * 80)
    print(f"ITEM PROTO COMPARISON: PID {item_pid} (Foxx={foxx_pro_fn}, Our={our_pro_fn})")
    print(f"Foxx Source: {foxx_src}")
    print(f"Our Source:  {our_src}")
    print("=" * 80)

    if not foxx_raw and not our_raw:
        print(f"[!] Proto for PID {item_pid} not found in either build.")
        return

    f_info = parse_pro_item(foxx_raw)
    o_info = parse_pro_item(our_raw)

    print(f"{'Field':20} {'Foxx':30} {'Our Build':30}")
    print("-" * 80)
    all_keys = sorted(set((f_info or {}).keys()) | set((o_info or {}).keys()))
    for k in all_keys:
        fv = (f_info or {}).get(k, "N/A")
        ov = (o_info or {}).get(k, "N/A")
        diff_mark = "  " if fv == ov else "* "
        print(f"{diff_mark}{k:18} {str(fv):30} {str(ov):30}")


def search_text_foxx(query, foxx_root=DEFAULT_FOXX_ROOT):
    """Searches string in all MSG files inside Foxx master.dat."""
    master_p = os.path.join(foxx_root, "master.dat")
    files = list_dat2(master_p)
    print(f"Searching for '{query}' across Foxx master.dat ({len(files)} files)...")
    matches = []
    for k in files.keys():
        if k.endswith(".msg"):
            raw = extract_dat2_file(master_p, k)
            if raw:
                text = raw.decode("cp1251", errors="ignore")
                if query.lower() in text.lower():
                    matches.append(k)
    print(f"Found {len(matches)} files matching query:")
    for m in matches[:25]:
        print(f"  {m}")


def main():
    parser = argparse.ArgumentParser(description="Fallout 2 Mod & Build Comparator")
    subparsers = parser.add_subparsers(dest="command")

    msg_parser = subparsers.add_parser("msg", help="Compare dialogue .msg file")
    msg_parser.add_argument("filename", help="MSG file name (e.g. vccasidy, dcsmitty)")

    pro_parser = subparsers.add_parser("pro", help="Compare item .pro file")
    pro_parser.add_argument("pid", help="Item PID (1-based index in items.lst, e.g. 8, 455)")

    search_parser = subparsers.add_parser("search", help="Search text in Foxx master.dat")
    search_parser.add_argument("query", help="Text search query")

    args = parser.parse_args()

    if args.command == "msg":
        diff_dialogue(args.filename)
    elif args.command == "pro":
        diff_proto(args.pid)
    elif args.command == "search":
        search_text_foxx(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
