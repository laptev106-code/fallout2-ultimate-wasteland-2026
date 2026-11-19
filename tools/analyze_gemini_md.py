import re

with open(r"C:\Users\Геннадий\.gemini\config\GEMINI.md", "r", encoding="utf-8") as f:
    text = f.read()

total_bytes = len(text.encode("utf-8"))
print(f"TOTAL BYTES: {total_bytes} / 24,000 ({(total_bytes/24000)*100:.1f}%)\n")

sections = re.split(r"(?=^## )", text, flags=re.M)
for s in sections:
    lines = s.strip().splitlines()
    header = lines[0] if lines else "Header"
    sec_bytes = len(s.encode("utf-8"))
    pct = (sec_bytes / total_bytes) * 100
    print(f"{header[:55]:<55} | {sec_bytes:>6} bytes | {pct:>5.1f}%")
