import os

base = r"E:\Fallout2_Ultimate\Fallout2_Gameplay\DATA\text"
for root, dirs, files in os.walk(base):
    for f in files:
        fp = os.path.join(root, f)
        print(f"\n--- {os.path.relpath(fp, base)} ---")
        try:
            with open(fp, 'r', encoding='cp1251') as fh:
                content = fh.readlines()
                print(f"Total lines: {len(content)}")
                print("First 5 lines:")
                for line in content[:5]:
                    print(" ", line.strip())
        except Exception as e:
            print("Error reading cp1251:", e)
