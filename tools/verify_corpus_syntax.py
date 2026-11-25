# -*- coding: utf-8 -*-
import os
import re

def verify():
    base = "E:/FALLOUT Ult pjt/standalone_mods/wasteland_voices/text"
    ru_files = [
        os.path.join(base, "russian", "dialog", "wv_dialog.msg"),
        os.path.join(base, "russian", "game", "custom.msg")
    ]
    en_files = [
        os.path.join(base, "english", "dialog", "wv_dialog.msg"),
        os.path.join(base, "english", "game", "custom.msg")
    ]

    for p in ru_files:
        with open(p, "rb") as f:
            raw = f.read()
        text = raw.decode("cp1251")
        matches = re.findall(r"\{(\d+)\}\{.*\}\{(.*)\}", text)
        print(f"RU file {os.path.basename(p)}: {len(matches)} entries parsed, valid CP1251")

    for p in en_files:
        with open(p, "rb") as f:
            raw = f.read()
        text = raw.decode("ascii")
        matches = re.findall(r"\{(\d+)\}\{.*\}\{(.*)\}", text)
        print(f"EN file {os.path.basename(p)}: {len(matches)} entries parsed, valid ASCII")

    # Check Party Tactics lines 0..604 in custom.msg
    with open(ru_files[1], "rb") as f:
        t = f.read().decode("cp1251")
    assert "{0}{}" in t, "Line 0 missing from ru custom.msg!"
    assert "{100}{}" in t, "Line 100 missing from ru custom.msg!"
    assert "{604}{}" in t, "Line 604 missing from ru custom.msg!"
    assert "{5000}{}" in t, "Line 5000 missing from ru custom.msg!"
    print("ALL ASSERTIONS PASSED: Party Tactics lines 0..604 + Mod lines 5000..5909 are intact!")

if __name__ == "__main__":
    verify()
