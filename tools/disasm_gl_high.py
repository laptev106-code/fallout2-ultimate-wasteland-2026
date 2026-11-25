with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\gl_highlighting.int", "rb") as f:
    data = f.read()

# find where "Key" is read
idx = data.find(b"mods\\sfall-mods.ini")
print("Found sfall-mods.ini at offset", idx)
idx2 = data.find(b"Highlighting")
print("Found Highlighting at offset", idx2)
