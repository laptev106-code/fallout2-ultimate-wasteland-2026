import json

with open(r"C:\Users\Геннадий\.gemini\antigravity\brain\a3e3fb8b-370c-4ec1-90c9-bd8542c080cd\.system_generated\logs\transcript_full.jsonl", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        data = json.loads(line)
        if 4310 <= data.get("step_index", 0) <= 4330:
            print(f"=== STEP {data.get('step_index')} ({data.get('type')}) ===")
            content = data.get("content", "")
            if isinstance(content, str):
                print(content[:600])
