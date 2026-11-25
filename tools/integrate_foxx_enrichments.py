import os
import sys
import shutil

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file
from tools.build_foxx_tribute_pack import pack_to_dat2

FOXX_DIR = r"E:\Games\Fallout 2 (Expansion Version)"
FOXX_MASTER = os.path.join(FOXX_DIR, "master.dat")
FOXX_CASSIDY = os.path.join(FOXX_DIR, "mods", "DB_Cassidy_Voice.dat")

TRIBUTE_DATA_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\data"
TRIBUTE_DAT_PATH = r"E:\FALLOUT Ult pjt\standalone_mods\foxx_rebuild_tribute\foxx_rebuild_tribute.dat"

SPEECH_STAGING_DIR = r"E:\FALLOUT Ult pjt\standalone_mods\armored_speech_staging"
SPEECH_DAT_PATH = r"E:\FALLOUT Ult pjt\mods\armored_talking_heads_speech.dat"

PROFILES = [
    r"E:\FALLOUT Ult pjt",
    r"E:\Fallout2_Ultimate\Fallout2_Gameplay",
    r"E:\Fallout2_Ultimate\Fallout2_HD"
]

def step4_deploy_speech():
    print("\n[*] Step 4: Deploying Armored Companion Speech to target profiles...")
    if not os.path.exists(SPEECH_DAT_PATH):
        print("[*] Packing armored_talking_heads_speech.dat...")
        pack_to_dat2(SPEECH_STAGING_DIR, SPEECH_DAT_PATH)
    
    sz = os.path.getsize(SPEECH_DAT_PATH)
    print(f"  [✔] Ready armored_talking_heads_speech.dat: {sz:,} bytes")

    for prof in PROFILES:
        mods_dir = os.path.join(prof, "mods")
        if os.path.exists(mods_dir):
            target_dat = os.path.join(mods_dir, "armored_talking_heads_speech.dat")
            if os.path.abspath(SPEECH_DAT_PATH) != os.path.abspath(target_dat):
                shutil.copy2(SPEECH_DAT_PATH, target_dat)
                print(f"    -> Deployed to {target_dat}")
            else:
                print(f"    -> Already in master {target_dat}")

            # Register in mods_order.txt right after talking_heads.dat
            mo_path = os.path.join(mods_dir, "mods_order.txt")
            if os.path.exists(mo_path):
                with open(mo_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                if "armored_talking_heads_speech.dat" not in lines:
                    new_lines = []
                    inserted = False
                    for line in lines:
                        new_lines.append(line)
                        if "talking_heads" in line.lower() and not inserted and not line.startswith(";"):
                            new_lines.append("armored_talking_heads_speech.dat")
                            inserted = True
                    if not inserted:
                        new_lines.append("armored_talking_heads_speech.dat")
                    with open(mo_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(new_lines) + "\n")
                    print(f"    -> Registered in {mo_path}")

def step5_docs():
    print("\n[*] Step 5: Copying valuable guide docs to Docs/...")
    docs_dir = os.path.join(FOXX_DIR, "!docs")
    dest_docs = r"E:\FALLOUT Ult pjt\Docs"
    os.makedirs(dest_docs, exist_ok=True)
    for doc in ["RP_Walkthrough_(RU).pdf", "Fallout_Bible.pdf", "Fallout2_Manual.pdf"]:
        src = os.path.join(docs_dir, doc)
        if os.path.exists(src):
            dst = os.path.join(dest_docs, doc)
            shutil.copy2(src, dst)
            print(f"  [✔] Copied {doc} ({os.path.getsize(dst):,} bytes)")

def main():
    step4_deploy_speech()
    step5_docs()
    print("\n[✔] ALL ENRICHMENTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
