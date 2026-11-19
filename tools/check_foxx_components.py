import os
import glob

base = "E:/Fallout2_Ultimate/Fallout2_Gameplay"

def check_file(pattern):
    matches = glob.glob(os.path.join(base, "**", pattern), recursive=True)
    return matches

print("Checking candidate files:")
for item in ["*blur*", "*glass*", "*kaga*", "*pixote*", "*guide*", "*руководств*", "*pdf*", "*reload*"]:
    m = check_file(item)
    print(f" {item}: {len(m)} found -> {[os.path.basename(x) for x in m[:3]]}")
