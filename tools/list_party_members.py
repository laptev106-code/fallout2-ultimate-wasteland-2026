import os
from check_party_txt import extract_file

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\mods"
p_miria = extract_file(os.path.join(base, "DB_Enchanced_Miria.dat"), "data/party.txt").decode('ascii', errors='ignore')
for l in p_miria.splitlines():
    if l.strip().startswith("[Party Member"):
        print(l.strip())
