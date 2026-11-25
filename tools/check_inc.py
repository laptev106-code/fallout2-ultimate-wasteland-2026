import re

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\compile.exe", "rb") as f:
    data = f.read()

idx = data.find(b"Set include directory")
if idx != -1:
    print(data[idx-100:idx+200])
