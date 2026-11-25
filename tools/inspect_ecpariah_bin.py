with open(r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\extracted_rpu\ecpariah.int", "rb") as f:
    data = f.read()

print("File size:", len(data))
# Extract printable strings
import re
strings = re.findall(b"[a-zA-Z0-9_]{3,}", data)
print("Strings:", [s.decode('ascii') for s in strings])
