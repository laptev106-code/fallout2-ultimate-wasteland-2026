import os
import sys

sys.path.insert(0, r"E:\FALLOUT Ult pjt")
from tools.engine_full_audit import read_dat2_directory, extract_dat2_file

FOXX_DIR = r"E:\Games\Fallout 2 (Expansion Version)"
MASTER_DAT = os.path.join(FOXX_DIR, "master.dat")

def main():
    print("=" * 70)
    print("  SCANNING FOXX MASTER.DAT FOR HISTORICAL CHANGELOG FIXES")
    print("=" * 70)
    
    foxx_files = read_dat2_directory(MASTER_DAT)
    print(f"Total files in Foxx master.dat: {len(foxx_files)}")

    patterns = [
        "vilrat.msg", "ectravlr.msg", "tribe02.map", "raiders", "epautdoc",
        "giskeetc", "gcsktr", "scduppo", "kisafe", "kislvdor", "tribec",
        "marley", "00000543.pro", "00000544.pro", "pariah", "ecpariah",
        "crowbar", "alesis", "epai43", "epai37", "epai44", "epai41", "gl_alesis"
    ]

    for pat in patterns:
        matches = [info['name'] for k, info in foxx_files.items() if pat in k]
        print(f"Pattern '{pat}': {matches}")

    # Also search for any scripts added or modified with alesis, dog, crowbar
    scripts = [info['name'] for k, info in foxx_files.items() if k.startswith('scripts\\') and ('crow' in k or 'bar' in k or 'dog' in k or 'pariah' in k or 'tribe' in k)]
    print(f"\nTarget scripts in Foxx master.dat:")
    for s in sorted(scripts)[:25]:
        print(f"  {s}")

if __name__ == "__main__":
    main()
