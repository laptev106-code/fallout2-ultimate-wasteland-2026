import re

with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\compile.exe", "rb") as f:
    data = f.read()

# Look for usage strings
matches = re.findall(b"-[a-zA-Z0-9]+", data)
print("Option flags found:", set(m.decode('latin1') for m in matches[:50]))

# Search for "usage" or help text
text = data.decode('latin1', errors='ignore')
idx = text.find("sfall edition")
if idx != -1:
    print("Near sfall edition:")
    print(text[idx-200:idx+800])
