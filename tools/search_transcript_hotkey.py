import json

with open(r"C:\Users\Геннадий\.gemini\antigravity\brain\a3e3fb8b-370c-4ec1-90c9-bd8542c080cd\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = data.get("content", "")
        if "hotkey conflict" in content or "W hotkey" in content or "мудрили" in content or "подсвечивает" in content:
            print(f"Step {data.get('step_index')}: {content[:300]}...")
