import json

with open(r"C:\Users\Геннадий\.gemini\antigravity\brain\a3e3fb8b-370c-4ec1-90c9-bd8542c080cd\.system_generated\logs\transcript_full.jsonl", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        data = json.loads(line)
        if data.get("step_index") in [6338, 6339, 6340, 6341]:
            print(f"=== STEP {data.get('step_index')} ===")
            print(str(data.get("content", ""))[:1500])
            if "tool_calls" in data:
                print("TOOL CALLS:", data["tool_calls"])
