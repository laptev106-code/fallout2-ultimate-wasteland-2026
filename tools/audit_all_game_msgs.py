import sys
sys.path.insert(0, '.')
import tools.engine_full_audit as efa
import os, re

vfs, collisions, order, stats = efa.build_profile_vfs(r'E:\Fallout2_Ultimate\Fallout2_Gameplay')
ecco_files = efa.read_dat2_directory(r'E:\Fallout2_Ultimate\Fallout2_Gameplay\mods\rpu_y_ecco.dat')

game_msgs = [k for k in vfs if k.startswith('text\\russian\\game\\') and k.endswith('.msg')]

print(f"Auditing {len(game_msgs)} game message files...")

# Ignored Latin tokens (proper nouns, technical IDs, format tokens, standard acronyms)
ALLOWED_LATIN = {
    'UNUSED', 'USED ART', 'spare', 'NONE', 'None', 'none', 'error', 'Error', 'ERROR',
    'PID', 'FID', 'SID', 'ACM', 'FRM', 'DAT', 'INI', 'EXE', 'DLL',
    'FN', 'FAL', 'HPFA', 'BMG', 'JHP', 'AP', 'FMJ', 'G11', 'G11E', 'HK', 'P90', 'P90c',
    'XL70E3', 'CAWS', 'L30', 'M60', 'M3A1', 'PPK', 'Desert', 'Eagle', 'Magnum', 'Colt',
    'Browning', 'Auto', 'Remington', 'Winchester', 'Glock', 'Sig', 'Sauer', 'Mauser',
    'Bozar', 'Vindicator', 'Avenger', 'Solar', 'Scorcher', 'Phazer', 'Alien', 'Blaster',
    'Robo', 'Rocket', 'Launcher', 'Flamer', 'Plasma', 'Rifle', 'Pistol', 'Laser', 'Gatling',
    'Red', 'Ryder', 'LE', 'BB', 'Gun', 'Spitfire', 'Turbo', 'Super', 'Sledge', 'Ripper',
    'Wakizashi', 'Combat', 'Knife', 'Power', 'Armor', 'Tesla', 'Bridge', 'Keeper',
    'Pip-Boy', 'PipBoy', 'Vault-Tec', 'Poseidon', 'Oil', 'Enclave', 'NCR', 'Brotherhood', 'Steel'
}

for k in sorted(game_msgs):
    info = vfs[k]
    txt, enc = efa.read_vfs_text(info)
    if not txt:
        print(f"[FAIL] Cannot read {k}")
        continue

    # 1. Syntax check: all braces match
    pattern = re.compile(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}')
    matches = list(pattern.finditer(txt))
    
    # Check for unmatched braces
    open_count = txt.count('{')
    close_count = txt.count('}')
    if open_count != close_count or open_count != len(matches) * 3:
        # Check if difference is just comments or real syntax error
        # Let's inspect
        raw_lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith(';')]
        print(f"  [CHECK BRACES] {k}: opens={open_count}, closes={close_count}, matched_entries={len(matches)}")

    # 2. Linguistic check: English leaks
    leaks = []
    for m in matches:
        num = int(m.group(1))
        val = m.group(3).strip()
        has_cyr = bool(re.search(r'[А-Яа-яЁё]', val))
        has_lat = bool(re.search(r'[a-zA-Z]{3,}', val))
        if has_lat and not has_cyr:
            # Check individual words
            words = re.findall(r'[a-zA-Z]+', val)
            unallowed = [w for w in words if w not in ALLOWED_LATIN]
            if unallowed and len(unallowed) > 1:
                leaks.append((num, val))

    if leaks:
        print(f"  [ENGLISH LEAKS] {k}: {len(leaks)} lines with unallowed Latin text:")
        for num, val in leaks[:8]:
            print(f"    [{num}] {val}")

    # 3. EcCo comparison: if file exists in EcCo DAT, verify no lines are missing
    if k in ecco_files:
        e_txt = efa.extract_dat2_file(ecco_files[k]).decode('cp1251', errors='ignore')
        e_entries = {int(m.group(1)): m.group(3) for m in pattern.finditer(e_txt)}
        v_entries = {int(m.group(1)): m.group(3) for m in matches}
        missing_from_ecco = set(e_entries.keys()) - set(v_entries.keys())
        if missing_from_ecco:
            print(f"  [ECCO PARITY FAIL] {k}: {len(missing_from_ecco)} missing lines from EcCo: {sorted(list(missing_from_ecco))[:10]}")
        else:
            print(f"  [ECCO PARITY OK] {k}: 100% lines present ({len(e_entries)} entries)")
