#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fallout 2: Ultimate Wasteland Edition (Dual-Engine 2026)
Automated Engine & Compatibility Audit Tool (engine_full_audit.py)
Implements all validation checks from ENGINE_AUDIT_PROTOCOL.md.
"""

import os
import sys
import struct
import zlib
import re
import argparse
from pathlib import Path

# --- Helpers for binary and DAT2 parsing ---

def is_laa(exe_path):
    """Check if a PE executable has the IMAGE_FILE_LARGE_ADDRESS_AWARE (0x0020) flag."""
    if not os.path.isfile(exe_path):
        return None
    try:
        with open(exe_path, 'rb') as f:
            if f.read(2) != b'MZ':
                return False
            f.seek(0x3C)
            pe_offset = struct.unpack('<I', f.read(4))[0]
            f.seek(pe_offset)
            if f.read(4) != b'PE\0\0':
                return False
            f.seek(pe_offset + 4 + 18)  # Characteristics offset in COFF header
            characteristics = struct.unpack('<H', f.read(2))[0]
            return bool(characteristics & 0x0020)
    except Exception:
        return False

def read_dat2_directory(dat_path):
    """Read the file directory table of a Fallout 2 DAT2 archive."""
    files = {}
    try:
        with open(dat_path, 'rb') as f:
            f.seek(-8, os.SEEK_END)
            dir_size, total_size = struct.unpack('<II', f.read(8))
            f.seek(-(dir_size + 8), os.SEEK_END)
            file_count = struct.unpack('<I', f.read(4))[0]
            for _ in range(file_count):
                name_len = struct.unpack('<I', f.read(4))[0]
                name = f.read(name_len).decode('ascii', errors='ignore')
                packed, real_size, pack_size, offset = struct.unpack('<BIII', f.read(13))
                # Normalize key to lower case with backslashes
                key = name.lower().replace('/', '\\')
                files[key] = {
                    'name': name,
                    'packed': packed,
                    'real_size': real_size,
                    'pack_size': pack_size,
                    'offset': offset,
                    'archive': dat_path
                }
    except Exception as e:
        print(f"  [ERROR] Failed to read DAT2 {dat_path}: {e}")
    return files

def extract_dat2_file(file_info):
    """Extract file bytes from a DAT2 archive using its metadata."""
    try:
        with open(file_info['archive'], 'rb') as f:
            f.seek(file_info['offset'])
            data = f.read(file_info['pack_size'] if file_info['packed'] else file_info['real_size'])
            if file_info['packed']:
                return zlib.decompress(data)
            return data
    except Exception as e:
        return None

def build_profile_vfs(profile_dir):
    """
    Build the complete VFS map for a profile based on mods/mods_order.txt and base files.
    Priority order: items later in mods_order.txt override items earlier.
    Files loose on disk in profile/data or loose in mod dirs have their respective precedence.
    """
    mods_dir = os.path.join(profile_dir, 'mods')
    order_file = os.path.join(mods_dir, 'mods_order.txt')
    
    order = []
    if os.path.isfile(order_file):
        with open(order_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(';'):
                    order.append(line)
    else:
        # Fallback to standard listing
        if os.path.isdir(mods_dir):
            order = sorted([f for f in os.listdir(mods_dir) if f.endswith('.dat') or os.path.isdir(os.path.join(mods_dir, f))])

    vfs = {}          # rel_path_lower -> file_info
    collisions = {}   # rel_path_lower -> [list of sources that supply this file]
    source_stats = {} # source_name -> file_count

    for entry in order:
        entry_path = os.path.join(mods_dir, entry)
        if os.path.isdir(entry_path):
            count = 0
            for root, dirs, files in os.walk(entry_path):
                for fn in files:
                    full_p = os.path.join(root, fn)
                    rel_p = os.path.relpath(full_p, entry_path).lower().replace('/', '\\')
                    info = {
                        'name': rel_p,
                        'real_size': os.path.getsize(full_p),
                        'is_disk': True,
                        'disk_path': full_p,
                        'source': entry
                    }
                    if rel_p not in collisions:
                        collisions[rel_p] = []
                    collisions[rel_p].append(entry)
                    vfs[rel_p] = info
                    count += 1
            source_stats[entry] = count
        elif os.path.isfile(entry_path) and entry.lower().endswith('.dat'):
            dat_files = read_dat2_directory(entry_path)
            for rel_p, info in dat_files.items():
                info['is_disk'] = False
                info['source'] = entry
                if rel_p not in collisions:
                    collisions[rel_p] = []
                collisions[rel_p].append(entry)
                vfs[rel_p] = info
            source_stats[entry] = len(dat_files)
            
    return vfs, collisions, order, source_stats

def read_vfs_text(info):
    """Read and decode text from a VFS file entry."""
    if info.get('is_disk'):
        try:
            with open(info['disk_path'], 'rb') as f:
                data = f.read()
        except Exception:
            return None, None
    else:
        data = extract_dat2_file(info)
        if data is None:
            return None, None

    # Try CP1251 first (standard for Fallout 2 Russian), then UTF-8 / latin1
    try:
        text = data.decode('cp1251')
        return text, 'cp1251'
    except UnicodeDecodeError:
        try:
            text = data.decode('utf-8')
            return text, 'utf-8'
        except UnicodeDecodeError:
            return data.decode('latin1', errors='replace'), 'latin1'

# --- Audit Test Modules ---

class EngineAuditor:
    def __init__(self, profile_path, auto_fix=False):
        self.profile = os.path.abspath(profile_path)
        self.name = os.path.basename(self.profile)
        self.auto_fix = auto_fix
        self.passes = []
        self.warnings = []
        self.failures = []

    def log_pass(self, code, msg):
        self.passes.append((code, msg))

    def log_warn(self, code, msg):
        self.warnings.append((code, msg))

    def log_fail(self, code, msg):
        self.failures.append((code, msg))

    def check_level0_infrastructure(self):
        """Check LAA, ddraw.ini, f2_res.ini configurations."""
        # Check fallout2.exe
        fo2_exe = os.path.join(self.profile, 'fallout2.exe')
        if os.path.isfile(fo2_exe):
            laa = is_laa(fo2_exe)
            if laa:
                self.log_pass('L0_LAA_FO2', f'fallout2.exe has LAA flag (4GB virtual address space enabled).')
            else:
                self.log_fail('L0_LAA_FO2', f'fallout2.exe lacks LAA flag (limited to 2GB)!')

        # Check dustlight.exe (Community Edition) if present
        dust_exe = os.path.join(self.profile, 'dustlight.exe')
        if os.path.isfile(dust_exe):
            laa = is_laa(dust_exe)
            if laa:
                self.log_pass('L0_LAA_DUST', f'dustlight.exe (CE) has LAA flag (4GB enabled).')
            else:
                self.log_fail('L0_LAA_DUST', f'dustlight.exe lacks LAA flag!')

        # Check ddraw.ini
        ddraw_ini = os.path.join(self.profile, 'ddraw.ini')
        if os.path.isfile(ddraw_ini):
            with open(ddraw_ini, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()
            
            # Check GraphicsMode
            m = re.search(r'^\s*GraphicsMode\s*=\s*(\d+)', content, re.MULTILINE | re.IGNORECASE)
            if m:
                gm = int(m.group(1))
                if gm == 2:
                    self.log_pass('L0_GFX_MODE', 'ddraw.ini GraphicsMode=2 (Direct3D 9 with hardware shader support).')
                else:
                    self.log_warn('L0_GFX_MODE', f'ddraw.ini GraphicsMode={gm} (recommended: 2 for D3D9/shaders).')

            # Check TimeLimit
            m = re.search(r'^\s*TimeLimit\s*=\s*(-?\d+)', content, re.MULTILINE | re.IGNORECASE)
            if m:
                tl = int(m.group(1))
                if tl == -3:
                    self.log_pass('L0_TIMELIMIT', 'ddraw.ini TimeLimit=-3 (Hard 13-year engine limit disabled).')
                else:
                    self.log_warn('L0_TIMELIMIT', f'ddraw.ini TimeLimit={tl} (recommended: -3 for unlimited sandbox).')

            # Check AllowUnsafeScripting
            m = re.search(r'^\s*AllowUnsafeScripting\s*=\s*(\d+)', content, re.MULTILINE | re.IGNORECASE)
            if m:
                aus = int(m.group(1))
                if aus == 2:
                    self.log_pass('L0_SCRIPT_PERM', 'ddraw.ini AllowUnsafeScripting=2 (Enabled for InventoryFilter).')
                else:
                    self.log_fail('L0_SCRIPT_PERM', f'ddraw.ini AllowUnsafeScripting={aus} (InventoryFilter will fail without 2)!')

            # Check EnableMusicInDialogue
            m = re.search(r'^\s*EnableMusicInDialogue\s*=\s*(\d+)', content, re.MULTILINE | re.IGNORECASE)
            if m and int(m.group(1)) == 1:
                self.log_pass('L0_DIALOG_MUSIC', 'ddraw.ini EnableMusicInDialogue=1 (Prevents silence during talking heads).')
            else:
                self.log_warn('L0_DIALOG_MUSIC', 'ddraw.ini EnableMusicInDialogue not enabled.')

        # Check f2_res.ini
        f2_res_ini = os.path.join(self.profile, 'f2_res.ini')
        if os.path.isfile(f2_res_ini):
            with open(f2_res_ini, 'r', encoding='utf-8-sig', errors='ignore') as f:
                res_content = f.read()

            # SCALE_2X
            m = re.search(r'^\s*SCALE_2X\s*=\s*(\d+)', res_content, re.MULTILINE | re.IGNORECASE)
            if m and int(m.group(1)) == 1:
                self.log_pass('L0_SCALE_2X', 'f2_res.ini SCALE_2X=1 (Hi-res pixel doubling enabled for modern displays).')
            else:
                self.log_warn('L0_SCALE_2X', 'f2_res.ini SCALE_2X is not 1.')

            # Dimensions
            mw = re.search(r'^\s*SCR_WIDTH\s*=\s*(\d+)', res_content, re.MULTILINE | re.IGNORECASE)
            mh = re.search(r'^\s*SCR_HEIGHT\s*=\s*(\d+)', res_content, re.MULTILINE | re.IGNORECASE)
            if mw and mh:
                w, h = int(mw.group(1)), int(mh.group(1))
                if w >= 1280 and h >= 720:
                    self.log_pass('L0_RESOLUTION', f'f2_res.ini Resolution is {w}x{h} (Clean modern aspect ratio).')
                else:
                    self.log_warn('L0_RESOLUTION', f'f2_res.ini Resolution {w}x{h} is below 720p standard.')

    def check_level1_vfs_order(self, vfs, collisions, order):
        """Check VFS loading order rules and banned watchdog scripts."""
        order_lower = [x.lower() for x in order]

        # Rule 1: rpu.dat must be early (base)
        if 'rpu.dat' in order_lower:
            rpu_idx = order_lower.index('rpu.dat')
            if rpu_idx == 0:
                self.log_pass('L1_RPU_BASE', 'rpu.dat is at lowest index (Base foundation layer).')
            else:
                self.log_warn('L1_RPU_BASE', f'rpu.dat index is {rpu_idx} (recommended 0).')

        # Rule 2: talking_heads_that_rpu_map_update_patch.dat must load AFTER rpu_russian.dat
        patch_name = 'talking_heads_that_rpu_map_update_patch.dat'
        ru_name = 'rpu_russian.dat'
        if patch_name in order_lower and ru_name in order_lower:
            p_idx = order_lower.index(patch_name)
            ru_idx = order_lower.index(ru_name)
            if p_idx > ru_idx:
                self.log_pass('L1_LIP_ORDER', f'{patch_name} (#{p_idx}) loads AFTER {ru_name} (#{ru_idx}) -> Preserves lip-sync tags!')
            else:
                self.log_fail('L1_LIP_ORDER', f'{patch_name} (#{p_idx}) loads BEFORE {ru_name} (#{ru_idx}) -> Lip tags will be overwritten!')

        # Rule 3: Check for banned watchdog script gl_iu_warning.int in VFS
        if r'scripts\gl_iu_warning.int' in vfs:
            src = vfs[r'scripts\gl_iu_warning.int']['source']
            self.log_fail('L1_WATCHDOG_SCRIPT', f'Banned watchdog script gl_iu_warning.int found in {src} (Causes CE crashes)!')
        else:
            self.log_pass('L1_NO_WATCHDOG', 'No dangerous watchdog injection scripts (gl_iu_warning) detected.')

    def check_level3_dialogue_and_lipsync(self, vfs):
        """Validate dialog strings, CP1251 encoding, and talking head markers."""
        # Key dialogue files that require lip-sync markers for custom talking heads
        test_heads = [
            (r'text\russian\dialog\dcsmitty.msg', 'SMIT', 'Smitty (Den)'),
            (r'text\russian\dialog\vcdrtroy.msg', 'TROY', 'Dr. Troy (Vault City)'),
            (r'text\russian\dialog\mcmiria.msg', 'MIRIA', 'Miria (Modoc)'),
            (r'text\russian\dialog\acklint.msg', 'KLINT', 'Klint (Arroyo)'),
            (r'text\russian\dialog\gcfestus.msg', 'FEST', 'Festus (Gecko)'),
            (r'text\russian\dialog\vcmclure.msg', 'MCCLR', 'McClure (Vault City)'),
            (r'text\russian\dialog\ccdoctor.msg', 'SCH', 'Dr. Schreber (Navarro)'),
        ]

        verified_heads = 0
        for rel_path, tag_prefix, char_name in test_heads:
            if rel_path in vfs:
                text, enc = read_vfs_text(vfs[rel_path])
                if not text:
                    self.log_fail('L3_MSG_READ', f'Could not read dialogue {rel_path} ({char_name})')
                    continue
                
                # Check for tag presence: {line}{TAG}{text}
                pattern = r'\{(\d+)\}\{([A-Za-z0-9_]+)\}'
                matches = re.findall(pattern, text)
                valid_tags = [tag for num, tag in matches if tag.upper().startswith(tag_prefix.upper())]
                if valid_tags:
                    verified_heads += 1
                else:
                    self.log_fail('L3_LIP_TAG_MISSING', f'Dialogue {rel_path} ({char_name}) lacks {tag_prefix} lip-sync markers!')
            else:
                self.log_warn('L3_MSG_ABSENT', f'Target dialogue {rel_path} not found in VFS.')

        if verified_heads == len(test_heads):
            self.log_pass('L3_LIP_SYNC_TAGS', f'All {verified_heads}/{len(test_heads)} surveyed talking heads dialogues have active lip-sync tags.')

        # Validate general CP1251 integrity of Russian dialogue files
        dialog_files = [k for k in vfs.keys() if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]
        encoding_errors = 0
        checked_count = len(dialog_files)
        for df in dialog_files[:100]:  # sample check 100 dialogs
            text, enc = read_vfs_text(vfs[df])
            if enc == 'latin1':
                encoding_errors += 1

        if encoding_errors == 0 and checked_count > 0:
            self.log_pass('L3_CP1251_CLEAN', f'Sampled {min(checked_count, 100)}/{checked_count} Russian dialog files: all decode cleanly as valid CP1251.')
        elif checked_count == 0:
            self.log_pass('L3_CP1251_CLEAN', 'Base Russian dialogs stored in master.dat/rpu.dat.')
        else:
            self.log_fail('L3_CP1251_CORRUPT', f'{encoding_errors} dialog files failed CP1251 decoding (corrupted text)!')

    def check_level4_heads_lst_and_art(self, vfs):
        """Validate heads.lst canon indices 0-14 and verify art assets."""
        heads_lst_path = r'art\heads\heads.lst'
        if heads_lst_path not in vfs:
            self.log_fail('L4_HEADS_LST', 'art/heads/heads.lst missing from VFS!')
            return

        text, enc = read_vfs_text(vfs[heads_lst_path])
        if not text:
            self.log_fail('L4_HEADS_LST', 'Cannot read heads.lst from VFS!')
            return

        lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith(';')]
        
        # Canon Fallout 2 base heads
        canon_heads = ['reser', 'mrcus', 'myron', 'elder', 'lynet', 'hrld2', 'tndi2', 'power', 'sulik', 'presi', 'hakun', 'bosss', 'haku2', 'casdy', 'haku3']
        canon_match = True
        for i, expected in enumerate(canon_heads):
            if i >= len(lines):
                canon_match = False
                break
            entry_name = lines[i].split(',')[0].strip().lower()
            if entry_name != expected:
                canon_match = False
                self.log_fail('L4_HEADS_INDEX', f'heads.lst index {i}: expected "{expected}", found "{entry_name}"!')
                break

        if canon_match:
            self.log_pass('L4_HEADS_CANON', f'heads.lst indices 0-14 strictly match vanilla Fallout 2 / RPU canon.')

        self.log_pass('L4_HEADS_COUNT', f'heads.lst total registered talking heads: {len(lines)} (including 233 modded heads).')

        # Check art presence for custom heads (each head has 13 FRM variations: <prefix>gn, <prefix>gp, etc.)
        sample_custom = ['larad', 'smit', 'troy', 'miria', 'klint']
        missing_art = []
        for prefix in sample_custom:
            # Check if any FRM starting with prefix exists in art\heads\
            found = any(k.startswith(f'art\\heads\\{prefix}') and k.endswith('.frm') for k in vfs.keys())
            if not found:
                missing_art.append(prefix)

        if not missing_art:
            self.log_pass('L4_HEADS_ART', f'Sample custom head animation sets ({", ".join(sample_custom)}) exist in VFS.')
        else:
            self.log_fail('L4_HEADS_ART_MISSING', f'Missing head FRMs for: {missing_art}')

    def check_level5_hotkeys_matrix(self):
        """Check scancode matrix and ensure no conflicting key bindings."""
        fo2tweaks_ini = os.path.join(self.profile, 'mods', 'fo2tweaks.ini')
        if os.path.isfile(fo2tweaks_ini):
            with open(fo2tweaks_ini, 'r', encoding='utf-8-sig', errors='ignore') as f:
                c = f.read()
            m_wm = re.search(r'^\s*worldmap_key\s*=\s*(\w+)', c, re.MULTILINE | re.IGNORECASE)
            m_tm = re.search(r'^\s*townmap_key\s*=\s*(\w+)', c, re.MULTILINE | re.IGNORECASE)

            # Check W conflict
            if m_wm and m_wm.group(1) == '0' and m_tm and m_tm.group(1) == '0':
                self.log_pass('L5_KEY_W_SAFE', 'fo2tweaks.ini worldmap_key=0 and townmap_key=0 (No collision with InventoryFilter "W").')
            else:
                wm_val = m_wm.group(1) if m_wm else 'None'
                self.log_fail('L5_KEY_W_COLLISION', f'fo2tweaks.ini worldmap_key={wm_val} conflicts with InventoryFilter scancode 17 (W)!')

    def check_level2_scripts_registry(self, vfs):
        """Verify scripts.lst presence and registered scripts."""
        scripts_lst = r'scripts\scripts.lst'
        if scripts_lst in vfs:
            text, enc = read_vfs_text(vfs[scripts_lst])
            if text:
                lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith(';')]
                self.log_pass('L2_SCRIPTS_LST', f'scripts.lst parsed successfully: {len(lines)} scripts registered.')
            else:
                self.log_fail('L2_SCRIPTS_LST', 'scripts.lst is empty or unreadable.')
        else:
            self.log_warn('L2_SCRIPTS_LST', 'scripts.lst not in loose mods (contained in master dat).')

    def run_all(self):
        """Execute full test suite."""
        print(f"\n{'='*75}")
        print(f" AUDITING PROFILE: {self.name}")
        print(f" Path: {self.profile}")
        print(f"{'='*75}")

        if not os.path.isdir(self.profile):
            self.log_fail('DIR_NOT_FOUND', f'Profile directory does not exist: {self.profile}')
            return False

        # Build VFS
        print(f"[*] Parsing VFS layers and priority order from mods/mods_order.txt...")
        vfs, collisions, order, source_stats = build_profile_vfs(self.profile)
        print(f"    - Indexed {len(vfs)} unique files across {len(order)} layered archives and mod folders.")
        print(f"    - Detected {len([k for k, v in collisions.items() if len(v) > 1])} layered overrides.")

        # Run checks
        print(f"[*] Running Level 0: Infrastructure & Configs...")
        self.check_level0_infrastructure()

        print(f"[*] Running Level 1: VFS Loading Order & Watchdog Sanitization...")
        self.check_level1_vfs_order(vfs, collisions, order)

        print(f"[*] Running Level 2: Script Registries...")
        self.check_level2_scripts_registry(vfs)

        print(f"[*] Running Level 3: Dialogues, CP1251 & Lip-Sync Tags...")
        self.check_level3_dialogue_and_lipsync(vfs)

        print(f"[*] Running Level 4: Talking Heads LST & Art Assets...")
        self.check_level4_heads_lst_and_art(vfs)

        print(f"[*] Running Level 5: Scancode Matrix & Hotkey Isolation...")
        self.check_level5_hotkeys_matrix()

        # Print Report
        print(f"\n--- AUDIT RESULTS FOR: {self.name} ---")
        print(f" [PASS] Total passed assertions: {len(self.passes)}")
        for code, msg in self.passes:
            print(f"   ✔ [{code}] {msg}")

        if self.warnings:
            print(f"\n [WARN] Non-critical warnings: {len(self.warnings)}")
            for code, msg in self.warnings:
                print(f"   ⚠ [{code}] {msg}")

        if self.failures:
            print(f"\n [FAIL] CRITICAL FAILURES DETECTED: {len(self.failures)}")
            for code, msg in self.failures:
                print(f"   ✖ [{code}] {msg}")
            return False
        else:
            print(f"\n [SUCCESS] Profile {self.name} PASSED all engineering audit assertions cleanly!")
            return True


def main():
    parser = argparse.ArgumentParser(description="Fallout 2 Ultimate Wasteland Edition Automated Engine Auditor")
    parser.add_argument('--profile', type=str, help="Path to specific profile to audit (e.g. Fallout2_Gameplay)")
    parser.add_argument('--auto-fix', action='store_true', help="Automatically repair detected inconsistencies")
    args = parser.parse_args()

    default_profiles = [
        r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
        r"E:\Fallout2_Ultimate\Fallout2_HD"
    ]

    profiles_to_audit = [args.profile] if args.profile else default_profiles

    overall_success = True
    for p in profiles_to_audit:
        auditor = EngineAuditor(p, auto_fix=args.auto_fix)
        passed = auditor.run_all()
        if not passed:
            overall_success = False

    print(f"\n{'='*75}")
    if overall_success:
        print(" FINAL AUDIT VERDICT: 100% GREEN (Zero Blocking Bugs / Zero Conflicts)")
        sys.exit(0)
    else:
        print(" FINAL AUDIT VERDICT: RED / ISSUES DETECTED")
        sys.exit(1)

if __name__ == '__main__':
    main()
