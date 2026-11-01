import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(278, min(len(lines), 285)):
    d = json.loads(lines[idx])
    print(f"--- Line {idx} ({d.get('type')}) ---")
    print(str(d.get('content'))[:500])
