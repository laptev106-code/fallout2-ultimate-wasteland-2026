import json

with open(r"C:\Users\Геннадий\.gemini\antigravity\brain\a3e3fb8b-370c-4ec1-90c9-bd8542c080cd\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT":
            content = data.get("content", "")
            if any(w in content.lower() for w in ["управлен", "кнопк", "клавиш", "подсвет", "раскладк", "shift", "tab", "мудр"]):
                print(f"Step {data.get('step_index')}: {content}")
