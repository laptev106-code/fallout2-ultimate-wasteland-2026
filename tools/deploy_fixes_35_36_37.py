"""
Deploy FIX-35, FIX-36, and FIX-37:
- FIX-35: Full EcCo dialogue expansion, dynamic barter format strings, and unified scripts (Fung, John, Connar).
- FIX-36: Full Russian translation of scenery objects in text/russian/game/pro_scen.msg.
- FIX-37: Party Orders hotkey deconfliction (PickUpKey=20+29, isolating Town Map 'T').
"""

import os
import sys
import re

sys.path.insert(0, '.')
import tools.engine_full_audit as efa

GAMEPLAY_DIR = r"E:\Fallout2_Ultimate\Fallout2_Gameplay"
HD_DIR = r"E:\Fallout2_Ultimate\Fallout2_HD"
WORKSPACE_DIR = r"E:\FALLOUT Ult pjt"

ECCO_DAT = os.path.join(GAMEPLAY_DIR, "mods", "rpu_y_ecco.dat")
TARGET_DAT_FOLDER = "rpu_russian_uncensored.dat"

def parse_msg_entries(text):
    entries = {}
    order = []
    pattern = re.compile(r'\{(\d+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}')
    for m in pattern.finditer(text):
        num = int(m.group(1))
        sound = m.group(2)
        val = m.group(3)
        entries[num] = (sound, val)
        order.append(num)
    return entries, order

def serialize_msg(entries, order):
    lines = []
    # Ensure all keys in entries are represented in order
    seen = set()
    full_order = []
    for k in order:
        if k in entries and k not in seen:
            full_order.append(k)
            seen.add(k)
    for k in sorted(entries.keys()):
        if k not in seen:
            full_order.append(k)
            seen.add(k)

    for k in full_order:
        sound, val = entries[k]
        lines.append(f"{{{k}}}{{{sound}}}{{{val}}}")
    return "\r\n".join(lines) + "\r\n"

def deploy_to_profiles_and_workspace(rel_path, data_bytes):
    targets = [
        os.path.join(GAMEPLAY_DIR, "mods", TARGET_DAT_FOLDER, rel_path),
        os.path.join(HD_DIR, "mods", TARGET_DAT_FOLDER, rel_path),
        os.path.join(WORKSPACE_DIR, rel_path)
    ]
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        with open(t, "wb") as f:
            f.write(data_bytes)
    print(f"  [DEPLOYED] {rel_path} ({len(data_bytes)} bytes) -> Gameplay, HD, Workspace")

def execute_fix_35():
    print("\n--- Executing FIX-35: EcCo Dialogue & Script Unification ---")
    ecco_files = efa.read_dat2_directory(ECCO_DAT)
    vfs, collisions, order, stats = efa.build_profile_vfs(GAMEPLAY_DIR)

    # 1. Deploy the 3 EcCo scripts to rpu_russian_uncensored.dat/scripts/
    for script_name in ['fcdrfung.int', 'rcdrjohn.int', 'vcconnar.int']:
        rel_int = os.path.join("scripts", script_name)
        dat_key = rel_int.lower().replace('/', '\\')
        if dat_key in ecco_files:
            int_bytes = efa.extract_dat2_file(ecco_files[dat_key])
            deploy_to_profiles_and_workspace(rel_int, int_bytes)
        else:
            print(f"  [ERROR] {dat_key} not in EcCo DAT!")

    # 2. Update dialogue files:
    # List of files to update with missing lines and dynamic price format strings
    dialog_files_to_merge = [
        'bscomp1.msg', 'ecbandit.msg', 'epai7.msg', 'fccrocke.msg', 'fclaocho.msg',
        'kcmaida.msg', 'kctrapr.msg', 'ncalgern.msg', 'rcascort.msg', 'scdocjub.msg',
        'sckarl.msg', 'scsherif.msg', 'slvcc1.msg', 'vcconnar.msg', 'vcdrtroy.msg',
        'vcdwnbar.msg', 'vckohl.msg', 'vcmainwk.msg', 'vcmclure.msg', 'vcoldjoe.msg',
        'vcstark.msg', 'zidcegrl.msg'
    ]

    for df in dialog_files_to_merge:
        rel_msg = os.path.join("text", "russian", "dialog", df)
        dat_key = rel_msg.lower().replace('/', '\\')
        
        # Read current VFS version (preserves translated lines, 7700+ lines, and lip-sync tags)
        v_info = vfs.get(dat_key)
        if not v_info:
            print(f"  [WARN] {dat_key} not found in VFS!")
            continue
        v_text, v_enc = efa.read_vfs_text(v_info)
        v_entries, v_order = parse_msg_entries(v_text)

        # Read EcCo version
        if dat_key not in ecco_files:
            print(f"  [WARN] {dat_key} not in EcCo DAT!")
            continue
        e_text = efa.extract_dat2_file(ecco_files[dat_key]).decode('cp1251', errors='ignore')
        e_entries, e_order = parse_msg_entries(e_text)

        added_count = 0
        updated_count = 0

        # Step A: Add missing lines from EcCo
        for num in e_order:
            if num not in v_entries:
                v_entries[num] = e_entries[num]
                v_order.append(num)
                added_count += 1

        # Step B: Update dynamic format specifier lines (%d) where EcCo has %d and VFS has hardcoded $
        # But NEVER overwrite 7700+ lines with English!
        for num, (e_snd, e_val) in e_entries.items():
            if num in v_entries and num < 7000:
                v_snd, v_val = v_entries[num]
                if '%d' in e_val and '%d' not in v_val:
                    # Update to EcCo's dynamic format string
                    # Preserve any lip-sync sound tags if VFS had one
                    final_snd = v_snd if v_snd else e_snd
                    v_entries[num] = (final_snd, e_val)
                    updated_count += 1

        # Step C: Special handling for Valerie (vcmainwk.msg) lines 7703 and 7704:
        # Keep Russian text but insert %d for the dynamic price
        if df == 'vcmainwk.msg':
            if 7703 in v_entries:
                snd = v_entries[7703][0]
                v_entries[7703] = (snd, "Я могу поставить ускоритель перезарядки на ваш Магнум за $%d. Хмммм. Этот ваш Дезерт Игл... Если хотите, я могу поставить увеличенный магазин. Это будет стоить $%d.")
                updated_count += 1
            if 7704 in v_entries:
                snd = v_entries[7704][0]
                v_entries[7704] = (snd, "Эта ваша штурмовая винтовка... Я могу поставить увеличенный магазин за $%d. Хмммм. У меня есть прибор ночного видения, который я могу установить на ваш FN FAL за $%d.")
                updated_count += 1

        # Step D: Special typo fix in zidcegrl.msg line 219
        if df == 'zidcegrl.msg' and 219 in v_entries:
            snd = v_entries[219][0]
            v_entries[219] = (snd, "Добро пожаловать в казино,")

        # Serialize and deploy
        merged_text = serialize_msg(v_entries, v_order)
        merged_bytes = merged_text.encode('cp1251', errors='replace')
        deploy_to_profiles_and_workspace(rel_msg, merged_bytes)
        print(f"    -> Merged {df}: +{added_count} missing lines, {updated_count} dynamic price updates.")

def execute_fix_36():
    print("\n--- Executing FIX-36: Scenery Descriptions Russian Translation in pro_scen.msg ---")
    vfs, collisions, order, stats = efa.build_profile_vfs(GAMEPLAY_DIR)
    scen_key = "text\\russian\\game\\pro_scen.msg"
    info = vfs.get(scen_key)
    if not info:
        print(f"  [ERROR] {scen_key} not in VFS!")
        return

    text, enc = efa.read_vfs_text(info)
    entries, order_list = parse_msg_entries(text)

    # Scenery translations map
    scenery_translations = {
        230300: "Пылающая жаровня",
        230301: "Эта чадящая масляная жаровня служит неплохим источником света. От едкого дыма невольно слезятся глаза и жжет в носу.",
        230400: "Шины",
        230401: "Старые резиновые покрышки, брошенные среди сорняков.",
        230700: "Осколки стекла",
        230701: "Осколки разбитого стекла, усеивающие землю.",
        230800: "Ржавеющий остов",
        230801: "Песок медленно поглощает этот брошенный автомобиль.",
        231900: "Книги",
        231901: "Разнообразные книги и журналы.",
        232000: "Ящики и мешки",
        232001: "Разнокалиберные ящики и мешки с припасами.",
        232100: "Металлические детали",
        232101: "Разнообразные металлические обломки и детали.",
        232200: "Книги",
        232201: "Разнообразные книги и журналы.",
        232300: "Ящики и мешки",
        232301: "Разнокалиберные ящики и мешки с припасами.",
        232400: "Металлические детали",
        232401: "Разнообразные металлические обломки и детали.",
        232501: "Бочка, доверху набитая вонючими мясными обрезками.",
        232601: "Бочка, доверху набитая вонючими мясными обрезками.",
        232701: "Бочка, доверху набитая вонючими мясными обрезками.",
        232801: "Бочка, доверху набитая вонючими мясными обрезками.",
        232900: "Мухи",
        233000: "Мухи"
    }

    translated_count = 0
    for num, rus_val in scenery_translations.items():
        snd = entries.get(num, ("", ""))[0]
        entries[num] = (snd, rus_val)
        if num not in order_list:
            order_list.append(num)
        translated_count += 1

    merged_text = serialize_msg(entries, order_list)
    merged_bytes = merged_text.encode('cp1251', errors='replace')
    deploy_to_profiles_and_workspace(os.path.join("text", "russian", "game", "pro_scen.msg"), merged_bytes)
    print(f"  [SUCCESS] Translated {translated_count} scenery entries in pro_scen.msg.")

def execute_fix_37():
    print("\n--- Executing FIX-37: Party Orders Hotkey Deconfliction ---")
    ini_paths = [
        os.path.join(GAMEPLAY_DIR, "mods", "party_orders.ini"),
        os.path.join(HD_DIR, "mods", "party_orders.ini")
    ]
    for p in ini_paths:
        if not os.path.exists(p):
            print(f"  [WARN] {p} not found!")
            continue
        with open(p, "r", encoding="cp1251", errors="ignore") as f:
            content = f.read()

        # Replace PickUpKey=20 with PickUpKey=20+29
        # And ensure description clarifies Ctrl+T
        new_content = re.sub(r'(?i)PickUpKey\s*=\s*20\b', 'PickUpKey=20+29', content)
        if new_content != content:
            with open(p, "w", encoding="cp1251") as f:
                f.write(new_content)
            print(f"  [SUCCESS] Updated {p}: PickUpKey=20+29 (Ctrl+T deconflicted from Town Map T).")
        else:
            print(f"  [INFO] {p} already has PickUpKey deconflicted.")

if __name__ == '__main__':
    execute_fix_35()
    execute_fix_36()
    execute_fix_37()
    print("\nAll 3 fixes applied successfully!")
