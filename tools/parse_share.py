import json

with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/share_api.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

mapping = data.get('mapping', {})
current_id = data.get('current_node')
curr = current_id
chain = []
while curr and curr in mapping:
    chain.append(curr)
    curr = mapping[curr].get('parent')

chain.reverse()

out_msgs = []
for cid in chain:
    node = mapping.get(cid, {})
    msg = node.get('message')
    if not msg:
        continue
    author = msg.get('author', {}).get('role')
    parts = msg.get('content', {}).get('parts', [])
    text = '\n'.join([p for p in parts if isinstance(p, str)])
    if text.strip():
        out_msgs.append({'role': author, 'text': text})

print(f'Total messages extracted: {len(out_msgs)}')
with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/chatgpt_share_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(out_msgs, f, ensure_ascii=False, indent=2)

with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/chatgpt_share_readable.txt', 'w', encoding='utf-8') as f:
    for idx, m in enumerate(out_msgs):
        f.write(f"\n{'='*40}\n[{idx}] {m['role'].upper()}\n{'='*40}\n{m['text']}\n")

print('Saved readable transcript to chatgpt_share_readable.txt')
