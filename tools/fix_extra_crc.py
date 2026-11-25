import re, os

def update_extra_crc(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="cp1251", errors="ignore") as f:
        content = f.read()
    
    # Replace ;ExtraCRC= or ExtraCRC= with ExtraCRC=0xf18aa577,0xe1680293
    pattern = r"(?m)^;?\s*ExtraCRC\s*=.*$"
    replacement = "ExtraCRC=0xf18aa577,0xe1680293"
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
    else:
        content += f"\n{replacement}\n"
        
    with open(file_path, "w", encoding="cp1251", errors="ignore") as f:
        f.write(content)
    print(f"Updated ExtraCRC in {file_path}")

for root in ["E:/Fallout2_Ultimate/Fallout2_Gameplay", "E:/Fallout2_Ultimate/Fallout2_HD"]:
    update_extra_crc(os.path.join(root, "ddraw.ini"))
