import json

with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/chatgpt_share_parsed.json', 'r', encoding='utf-8') as f:
    msgs = json.load(f)

# Let's get the last 8 messages of the conversation to see both questions and answers
last_segment = msgs[-8:]

with open('D:/AG games mods/fallout2-ultimate-wasteland-2026/tools/last_dialogues.txt', 'w', encoding='utf-8') as out:
    for m in last_segment:
        out.write(f"\n{'='*50}\n[{m['role'].upper()}]\n{'='*50}\n")
        out.write(m['text'] + "\n")

print(f"Dumped last {len(last_segment)} messages to last_dialogues.txt")
