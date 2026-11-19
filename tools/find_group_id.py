import re

with open('d:/AG games mods/fallout2-ultimate-wasteland-2026/tools/vk_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find group id
matches = re.findall(r'public_id["\']?\s*:\s*(\d+)|"group_id["\']?\s*:\s*(\d+)|"id["\']?\s*:\s*(\d+)|"owner_id["\']?\s*:\s*(-?\d+)', text)
print("IDs:", set([x for t in matches for x in t if x]))

# Search for any board or topic links
topics = re.findall(r'topic-\d+_\d+', text)
print("Topics:", set(topics))

# Search for "board" or "topic"
boards = re.findall(r'board\d+', text)
print("Boards:", set(boards))

# Search for any .txt
txts = re.findall(r'https?://[^\s"\'<>]+\.txt', text)
print("TXTs:", txts)
