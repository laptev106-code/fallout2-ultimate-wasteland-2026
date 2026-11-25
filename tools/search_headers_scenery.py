import os, re

headers_dir = r"D:\AG games mods\fallout2-ultimate-wasteland-2026\tools\headers"

def search_headers(pattern):
    print(f"=== Searching for: {pattern} ===")
    regex = re.compile(pattern, re.IGNORECASE)
    for root, dirs, files in os.walk(headers_dir):
        for f in files:
            if f.endswith(".h"):
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8", errors="ignore") as h:
                    for i, line in enumerate(h):
                        if regex.search(line):
                            print(f"{f}:{i+1} -> {line.strip()}")

search_headers("get_script")
search_headers("has_script")
search_headers("script_ptr")
search_headers("PROTO_SC_")
