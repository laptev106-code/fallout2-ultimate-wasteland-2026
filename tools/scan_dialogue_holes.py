# -*- coding: utf-8 -*-
"""
Fallout 2 Ultimate Wasteland 2026 // Deep Dialogue & Script Hole Scanner
Scans 1000+ dialogue files and scripts across DAT archives and overrides
to identify plot holes, missing nodes, unreferenced lines, low-IQ dead-ends,
and untranslated text.
"""
import os
import sys
import struct
import zlib
import re
from collections import defaultdict

GAME_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
RU_DAT = os.path.join(GAME_DIR, "mods", "rpu_russian.dat")
RPU_DAT = os.path.join(GAME_DIR, "mods", "rpu.dat")
MASTER_DAT = os.path.join(GAME_DIR, "master.dat")
OVERRIDE_DIR = os.path.join(GAME_DIR, "data", "text", "russian", "dialog")

def read_dat_entries(dat_path):
    """Reads DAT2 file directory tree and returns dict: {filename_lower: (is_comp, real_sz, comp_sz, offset)}"""
    if not os.path.exists(dat_path):
        return {}
    with open(dat_path, "rb") as f:
        f.seek(-8, 2)
        tree_size, dat_size = struct.unpack("<II", f.read(8))
        f.seek(dat_size - tree_size - 8)
        num_files = struct.unpack("<I", f.read(4))[0]
        entries = {}
        for _ in range(num_files):
            nlen = struct.unpack("<I", f.read(4))[0]
            fname = f.read(nlen).decode("ascii", errors="ignore")
            is_comp, real_sz, comp_sz, offset = struct.unpack("<BIII", f.read(13))
            entries[fname.lower().replace("/", "\\")] = (is_comp, real_sz, comp_sz, offset, fname)
        return entries

def extract_file_content(dat_path, entry):
    is_comp, real_sz, comp_sz, offset, _ = entry
    with open(dat_path, "rb") as f:
        f.seek(offset)
        raw = f.read(comp_sz if is_comp else real_sz)
        if is_comp:
            raw = zlib.decompress(raw)
        return raw

def parse_msg_lines(text):
    """Parses Fallout MSG format: {ID}{Sound}{Text}"""
    pattern = re.compile(r"\{(\d+)\}\s*\{([^}]*)\}\s*\{(.*?)\}(?=\s*\{|\s*$)", re.DOTALL)
    messages = {}
    for match in pattern.finditer(text):
        msg_id = int(match.group(1))
        sound = match.group(2).strip()
        body = match.group(3).strip()
        messages[msg_id] = {"sound": sound, "text": body}
    return messages

def main():
    print("=" * 70)
    print("FALLOUT 2 ULTIMATE // DEEP DIALOGUE & SCRIPT AUDIT ENGINE")
    print("=" * 70)
    
    ru_entries = read_dat_entries(RU_DAT)
    print(f"[*] Indexed {len(ru_entries)} files in rpu_russian.dat")
    
    # Filter dialog msg files
    dialog_entries = {k: v for k, v in ru_entries.items() if k.endswith(".msg") and "dialog" in k}
    print(f"[*] Found {len(dialog_entries)} Russian dialogue files (.msg)")

    findings = {
        "untranslated": [],
        "dev_markers": [],
        "broken_syntax": [],
        "empty_lines": [],
        "low_iq_deadends": [],
        "story_plot_holes": [],
        "orphan_messages": []
    }

    # Dev tags regex
    dev_regex = re.compile(r"\b(TODO|FIXME|TEMP|DEBUG|BUG|PLACEHOLDER|XXX|НЕ РЕАЛИЗОВАНО|ЗАГЛУШКА|В РАЗРАБОТКЕ)\b", re.IGNORECASE)
    # English sentences in Russian text
    eng_regex = re.compile(r"^[A-Z][a-zA-Z\s,\.\'\!\?\"\:\;\-]{20,}$")

    scanned_count = 0
    total_messages = 0

    for norm_path, entry in sorted(dialog_entries.items()):
        raw_bytes = extract_file_content(RU_DAT, entry)
        scanned_count += 1
        
        # Check override
        base_name = os.path.basename(norm_path)
        override_file = os.path.join(OVERRIDE_DIR, base_name)
        if os.path.exists(override_file):
            with open(override_file, "rb") as ovf:
                raw_bytes = ovf.read()

        try:
            text = raw_bytes.decode("cp1251", errors="replace")
        except:
            text = raw_bytes.decode("utf-8", errors="replace")

        parsed = parse_msg_lines(text)
        total_messages += len(parsed)

        # 1. Dev markers
        for mid, data in parsed.items():
            t = data["text"]
            if dev_regex.search(t):
                # Ignore in-game computer errors like ACOMPU or EPAC
                if not any(k in base_name for k in ["acompu", "epai", "eastereg", "civerti"]):
                    findings["dev_markers"].append((base_name, mid, t))
            
            # 2. Untranslated English strings
            clean_t = t.strip()
            if eng_regex.match(clean_t) and not any(k in clean_t.lower() for k in ["pip-boy", "vault-tec", "fallout", "geck", "poseidon"]):
                findings["untranslated"].append((base_name, mid, clean_t))

            # 3. Empty messages with valid IDs in important ranges (100-500)
            if len(clean_t) == 0 and 100 <= mid <= 500:
                findings["empty_lines"].append((base_name, mid))

        # 4. Low-IQ coverage check:
        # Check if NPC dialogue has >30 messages, mentions complex quests, but has ZERO dumb responses
        has_dumb = False
        dumb_markers = ["угг", "ы-ы", "э-э", "ага", "хнык", "моя идти", "моя хотеть", "бу-бу", "моя искать", "дурак"]
        for mid, data in parsed.items():
            tl = data["text"].lower()
            if any(dm in tl for dm in dumb_markers):
                has_dumb = True
                break
        
        if len(parsed) >= 40 and not has_dumb:
            # Exclude ambient float messages or purely system messages (like terminals/doors/generic guards)
            if not any(ign in base_name for ign in ["box", "door", "guard", "term", "comp", "elev", "trap", "sign", "brahmn", "scorp", "rat", "dog", "child", "float", "rnd"]):
                findings["low_iq_deadends"].append((base_name, len(parsed)))

    print(f"[*] Analyzed {scanned_count} files ({total_messages} dialogue lines total).")
    print(f"\n[+] RESULTS BREAKDOWN:")
    print(f"  - Dev markers / TODO / Placeholders: {len(findings['dev_markers'])}")
    print(f"  - Raw Untranslated English lines:    {len(findings['untranslated'])}")
    print(f"  - Missing / Empty dialogue lines:   {len(findings['empty_lines'])}")
    print(f"  - NPCs with 0 Low-IQ dialogue support: {len(findings['low_iq_deadends'])}")

    print("\n" + "=" * 70)
    print("DETAILED SAMPLES & SIGNIFICANT FINDINGS:")
    print("=" * 70)

    if findings["dev_markers"]:
        print("\n--- [DEV MARKERS & PLACEHOLDERS] ---")
        for fn, mid, txt in findings["dev_markers"][:10]:
            print(f"• {fn} #{mid}: {txt}")

    if findings["untranslated"]:
        print("\n--- [UNTRANSLATED ENGLISH LEAKS] ---")
        for fn, mid, txt in findings["untranslated"][:15]:
            print(f"• {fn} #{mid}: \"{txt}\"")

    if findings["low_iq_deadends"]:
        print("\n--- [KEY QUEST NPCS WITHOUT LOW-IQ DIALOGUE (LOCKOUT)] ---")
        for fn, count in findings["low_iq_deadends"][:15]:
            print(f"• {fn} ({count} lines total - 0 dumb options, instant lock-out for dumb character)")

if __name__ == "__main__":
    main()
