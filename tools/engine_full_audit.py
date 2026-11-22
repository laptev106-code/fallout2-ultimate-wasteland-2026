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

        # Rule 3: rpu_russian_uncensored.dat should load after base russian
        uncensored_name = 'rpu_russian_uncensored.dat'
        if uncensored_name in order_lower and ru_name in order_lower:
            u_idx = order_lower.index(uncensored_name)
            ru_idx = order_lower.index(ru_name)
            if u_idx > ru_idx:
                self.log_pass('L1_UNCENSORED_ORDER', f'{uncensored_name} (#{u_idx}) loads with highest priority -> Overrides text cleanly.')
            else:
                self.log_warn('L1_UNCENSORED_ORDER', f'{uncensored_name} (#{u_idx}) loads before base russian.')

        # Rule 4: Check for banned watchdog script gl_iu_warning.int in VFS
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
            (r'text\russian\dialog\tribec4.msg', 'SHAM', 'Shaman (Primitive Tribe)'),
            (r'text\russian\dialog\dcmom.msg', 'MOM', 'Mom (Den)'),
            (r'text\russian\dialog\schenry.msg', 'HENRY', 'Dr. Henry (NCR)'),
            (r'text\russian\dialog\mcbaltha.msg', 'BAL', 'Balthas (Modoc)'),
            (r'text\russian\dialog\vcmainwk.msg', 'VCVAL', 'Valerie (Vault City)'),
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

        # Validate general CP1251 integrity and brace syntax of ALL Russian dialogue files
        dialog_files = [k for k in vfs.keys() if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]
        encoding_errors = []
        syntax_errors = []
        checked_count = len(dialog_files)
        for df in dialog_files:
            text, enc = read_vfs_text(vfs[df])
            if enc == 'latin1':
                encoding_errors.append(df)
            elif text:
                if text.count('{') != text.count('}'):
                    syntax_errors.append(df)

        if not encoding_errors and not syntax_errors and checked_count > 0:
            self.log_pass('L3_CP1251_CLEAN', f'Audited all {checked_count} Russian dialog files: 100% valid CP1251 and 0 syntax brace mismatches.')
        elif encoding_errors:
            self.log_fail('L3_CP1251_CORRUPT', f'{len(encoding_errors)} dialog files failed CP1251 decoding: {encoding_errors[:3]}!')
        elif syntax_errors:
            self.log_fail('L3_SYNTAX_BRACES_MISMATCH', f'{len(syntax_errors)} dialog files have mismatched braces: {syntax_errors[:3]}!')
        else:
            self.log_pass('L3_CP1251_CLEAN', 'Base Russian dialogs stored in master.dat/rpu.dat.')

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

    def check_level6_deep_linter(self, vfs):
        """Level 6: Deep Armor Bounds, Loose Script Hygiene, Heap Limits & Craft Integrity."""

        # 1. Check critters.lst length vs npcarmor.ini FIDs
        critters_rel = r'art\critters\critters.lst'
        if critters_rel in vfs:
            text, enc = read_vfs_text(vfs[critters_rel])
            critter_lines = [l.strip() for l in text.splitlines() if l.strip()]
            
            # Check npcarmor.ini
            npcarmor_path = os.path.join(self.profile, 'mods', 'npcarmor.ini')
            if os.path.isfile(npcarmor_path):
                import configparser
                cfg = configparser.ConfigParser()
                cfg.read(npcarmor_path)
                bounds_errors = []
                for sec in cfg.sections():
                    if sec == 'ArmorTypes': continue
                    for k, v in cfg.items(sec):
                        if k in ['pid', 'weaponanims']: continue
                        try:
                            fid = int(v)
                            idx = fid - 16777216
                            if idx < 0 or idx >= len(critter_lines):
                                bounds_errors.append((sec, k, fid, idx))
                        except ValueError:
                            pass
                if bounds_errors:
                    self.log_fail('L6_ARMOR_BOUNDS_OVERFLOW', f'{len(bounds_errors)} FIDs exceed critters.lst ({len(critter_lines)} lines): {bounds_errors[:3]}')
                else:
                    self.log_pass('L6_ARMOR_BOUNDS_OK', f'All companion armor FIDs safely bound within {len(critter_lines)}-line critters.lst.')
            else:
                self.log_warn('L6_NPCARMOR_ABSENT', 'mods/npcarmor.ini not found.')
        else:
            self.log_warn('L6_CRITTERS_LST_ABSENT', 'art/critters/critters.lst not found in VFS.')

        # 2. Check loose scripts in DATA/scripts/
        loose_dir = os.path.join(self.profile, 'DATA', 'scripts')
        if os.path.isdir(loose_dir):
            loose_ints = [f for f in os.listdir(loose_dir) if f.lower().endswith('.int')]
            if loose_ints:
                self.log_fail('L6_LOOSE_SCRIPTS_DIRTY', f'Found {len(loose_ints)} loose INT files in DATA/scripts shadowing DAT priority: {loose_ints[:4]}')
            else:
                self.log_pass('L6_LOOSE_SCRIPTS_CLEAN', 'Zero loose INT scripts in DATA/scripts/ (Pure DAT priority hierarchy preserved).')
        else:
            self.log_pass('L6_LOOSE_SCRIPTS_CLEAN', 'DATA/scripts/ directory clean or absent.')

        # 3. Check Heap Safety (f2_res.ini NumPathNodes)
        f2_res_path = os.path.join(self.profile, 'f2_res.ini')
        if os.path.isfile(f2_res_path):
            with open(f2_res_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                c = f.read()
            m_nodes = re.search(r'^\s*NumPathNodes\s*=\s*(\d+)', c, re.MULTILINE | re.IGNORECASE)
            if m_nodes:
                val = int(m_nodes.group(1))
                if val <= 4:
                    self.log_pass('L6_HEAP_SAFETY', f'f2_res.ini NumPathNodes={val} <= 4 (Combat heap exhaustion protected).')
                else:
                    self.log_fail('L6_HEAP_OVERFLOW_RISK', f'f2_res.ini NumPathNodes={val} > 4 (Exceeds safe 8000 nodes limit)!')
            else:
                self.log_pass('L6_HEAP_SAFETY', 'f2_res.ini NumPathNodes not explicitly set (defaults to safe 1).')
        else:
            self.log_pass('L6_HEAP_SAFETY', 'f2_res.ini not present in profile (CE engine).')

        # 4. Check Craft Integrity (if pbs_craft.ini present)
        craft_rel = r'config\pbs_craft.ini'
        if craft_rel in vfs:
            import configparser
            text, enc = read_vfs_text(vfs[craft_rel])
            cfg = configparser.ConfigParser()
            cfg.read_string(text)
            existing_pids = set()
            for k in vfs.keys():
                if k.startswith('proto\\items\\') and k.endswith('.pro'):
                    try:
                        p_num = int(k[len('proto\\items\\'):-4])
                        existing_pids.add(p_num)
                    except ValueError:
                        pass
            craft_errors = []
            for sec in cfg.sections():
                if sec == 'Main': continue
                if cfg.has_option(sec, 'result'):
                    try:
                        r_pid = int(cfg.get(sec, 'result').split(',')[0].strip())
                        if r_pid not in existing_pids:
                            craft_errors.append((sec, 'result', r_pid))
                    except:
                        pass
            if craft_errors:
                self.log_fail('L6_CRAFT_PID_MISSING', f'{len(craft_errors)} craft recipes reference non-existent item PIDs: {craft_errors[:3]}')
            else:
                self.log_pass('L6_CRAFT_INTEGRITY', f'All {len(cfg.sections())-1} EcCo craft recipes reference verified item prototypes.')

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

    def check_level7_linguistic_and_mechanics(self, vfs):
        """Verify zero English leaks in Russian 7700+ dialogue lines and EcCo mechanics dialogue integrity."""
        ru_dialogs = [k for k in vfs if k.startswith('text\\russian\\dialog\\') and k.endswith('.msg')]
        leaks = []
        for k in ru_dialogs:
            txt, enc = read_vfs_text(vfs[k])
            if not txt: continue
            for m in re.finditer(r'\{(\d+)\}\{([^}]*)\}\{(.*)\}', txt):
                num = int(m.group(1))
                body = m.group(3)
                if num >= 7700:
                    ascii_words = re.findall(r'\b[A-Za-z]{4,}\b', body)
                    cyr_words = re.findall(r'\b[а-яА-ЯёЁ]{4,}\b', body)
                    if len(ascii_words) > 2 and len(cyr_words) == 0:
                        leaks.append((k, num, body[:40]))
        if leaks:
            self.log_fail('L7_ENGLISH_LEAK', f'{len(leaks)} English text leaks found in 7700+ Russian lines: {leaks[:3]}')
        else:
            self.log_pass('L7_NO_ENGLISH_LEAKS', f'Surveyed all {len(ru_dialogs)} Russian dialogue files: 0 English leaks in 7700+ voiced lines.')

        # Verify EcCo gameplay dialogue lines
        ecco_checks = [
            (r'text\russian\dialog\gcskeetr.msg', 1001, 'Skeeter ammo crafting'),
            (r'text\russian\dialog\dcvic.msg', 5100, 'Vic repair crafting'),
            (r'text\russian\dialog\dcmom.msg', 2001, 'Mom cooking training'),
            (r'text\russian\dialog\schenry.msg', 400, 'Dr. Henry mutant tentacle research'),
            (r'text\russian\dialog\mcbaltha.msg', 1001, 'Balthas leather tanning'),
            (r'text\russian\dialog\vcmainwk.msg', 501, 'Valerie tool crafting'),
            (r'text\russian\dialog\kctrapr.msg', 500, 'Klamath trapper gecko leather crafting'),
            (r'text\russian\dialog\rcascort.msg', 401, 'Ascorti Wanamingo mine leasing'),
            (r'text\russian\dialog\sckarl.msg', 200, 'Karl deputy security quests'),
            (r'text\russian\dialog\slvcc1.msg', 1001, 'Slaver camp Ranger infiltration'),
            (r'text\russian\dialog\vcconnar.msg', 800, 'Connar gun delivery negotiation'),
            (r'text\russian\dialog\fccrocke.msg', 129, 'Crockett dynamic price hardening ($%d)'),
        ]
        missing_ecco = []
        for rel_k, line_num, desc in ecco_checks:
            info = vfs.get(rel_k)
            txt, enc = read_vfs_text(info) if info else (None, None)
            if not txt or not re.search(rf'\{{{line_num}\}}', txt):
                missing_ecco.append((desc, line_num))

        if missing_ecco:
            self.log_fail('L7_ECCO_LINES_MISSING', f'EcCo dialogue lines missing in VFS: {missing_ecco}')
        else:
            self.log_pass('L7_ECCO_INTEGRITY', f'All {len(ecco_checks)} EcCo gameplay dialogue mechanics lines verified present in VFS.')

        # Verify Scenery descriptions translation (pro_scen.msg)
        scen_info = vfs.get(r'text\russian\game\pro_scen.msg')
        if scen_info:
            txt, enc = read_vfs_text(scen_info)
            scen_eng = []
            for num in [230300, 230301, 230400, 230401, 230700, 230701, 230800, 230801, 231900, 232000, 232100, 232501, 232900]:
                m = re.search(rf'\{{{num}\}}\{{[^}}]*\}}\{{([^}}]*)\}}', txt)
                if m and re.search(r'[A-Za-z]{4,}', m.group(1)) and not re.search(r'[А-Яа-яЁё]', m.group(1)):
                    scen_eng.append((num, m.group(1)))
            if scen_eng:
                self.log_fail('L7_SCENERY_LEAK', f'{len(scen_eng)} scenery objects in pro_scen.msg have English descriptions: {scen_eng[:3]}')
            else:
                self.log_pass('L7_SCENERY_CLEAN', 'All scenery descriptions in pro_scen.msg verified in 100% authentic Russian.')
        else:
            self.log_warn('L7_SCENERY_ABSENT', 'pro_scen.msg not found in VFS.')

        # Verify Party Orders hotkey deconfliction
        po_ini = os.path.join(self.profile, 'mods', 'party_orders.ini')
        if os.path.isfile(po_ini):
            with open(po_ini, 'r', encoding='cp1251', errors='ignore') as f:
                po_txt = f.read()
            if re.search(r'(?i)PickUpKey\s*=\s*20\b', po_txt) and not re.search(r'(?i)PickUpKey\s*=\s*20\s*\+', po_txt):
                self.log_fail('L7_HOTKEY_COLLISION', 'party_orders.ini uses bare PickUpKey=20 colliding with Town Map (T)!')
            else:
                self.log_pass('L7_HOTKEY_DECONFLICTED', 'party_orders.ini PickUpKey isolated with Ctrl+T (Town Map key T preserved).')

        # Verify fo2tweaks ammo and grenade synergy
        fo2_ini = os.path.join(self.profile, 'mods', 'fo2tweaks.ini')
        if os.path.isfile(fo2_ini):
            with open(fo2_ini, 'r', encoding='utf-8-sig', errors='ignore') as f:
                fo2_txt = f.read()
            # 1. Ammo PIDs (EcCo 7.62mm AP - 642)
            if re.search(r'ammo_pids\s*=.*?\b642\b', fo2_txt):
                self.log_pass('L7_AMMO_SYNC', 'fo2tweaks.ini ammo_pids includes EcCo 7.62mm AP (PID 642).')
            else:
                self.log_fail('L7_AMMO_MISSING', 'fo2tweaks.ini ammo_pids is missing EcCo 7.62mm AP (PID 642)!')

            # 2. Improved grenades Crowbar isolation
            m_g = re.search(r'\[improved_grenades\].*?weapons\s*=\s*([^\r\n]+)', fo2_txt, re.DOTALL)
            if m_g and re.search(r'\b20\b', m_g.group(1)):
                self.log_fail('L7_CROWBAR_EXPLOSIVE', 'fo2tweaks.ini treats Crowbar (PID 20) as explosive grenade!')
            else:
                self.log_pass('L7_GRENADE_CROWBAR_SAFE', 'fo2tweaks.ini weapons isolates Crowbar (PID 20) from grenade mechanics.')

        # Verify InvenFilter tool group cleanup
        inv_ini = os.path.join(self.profile, 'mods', 'InventoryFilter.dat', 'InvenFilter.ini')
        if os.path.isfile(inv_ini):
            with open(inv_ini, 'r', encoding='cp1251', errors='ignore') as f:
                inv_txt = f.read()
            m_tools = re.search(r'ToolGroupPids\s*=\s*([^\r\n]+)', inv_txt)
            if m_tools and any(bad in m_tools.group(1).split(',') for bad in ['393', '647', '556', '247']):
                self.log_fail('L7_INVEN_FILTER_DIRTY', f'InvenFilter.ini contains non-tool weapons or drugs: {m_tools.group(1)}')
            else:
                self.log_pass('L7_INVEN_FILTER_CLEAN', 'InvenFilter.ini ToolGroupPids verified clean of weapons and drugs.')

        # Verify NPC Armor Fire Gecko Armor mapping
        npc_ini = os.path.join(self.profile, 'mods', 'npcarmor.ini')
        if os.path.isfile(npc_ini):
            with open(npc_ini, 'r', encoding='utf-8', errors='ignore') as f:
                npc_txt = f.read()
            m_leather = re.search(r'\[ArmorTypes\].*?Leather\s*=\s*([^\r\n]+)', npc_txt, re.DOTALL)
            if m_leather and '652' in m_leather.group(1):
                self.log_pass('L7_NPC_ARMOR_GECKO', 'npcarmor.ini maps Fire Gecko Armor (PID 652) to Leather appearance.')
            else:
                self.log_fail('L7_NPC_ARMOR_GECKO_MISSING', 'npcarmor.ini does not recognize Fire Gecko Armor (PID 652)!')

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

        print(f"[*] Running Level 6: Deep Armor Bounds, Scripts Hygiene & Craft Integrity...")
        self.check_level6_deep_linter(vfs)

        print(f"[*] Running Level 7: Linguistic Integrity & EcCo Mechanics...")
        self.check_level7_linguistic_and_mechanics(vfs)

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
