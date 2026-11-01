import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

d = json.loads(lines[279])
tc = d.get('tool_calls', [])
for c in tc:
    print("Task:\n", c.get('args', {}).get('Task'))

print("\n--- Subagent Output ---")
d2 = json.loads(lines[280])
print(d2.get('content'))
