import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in [220, 221, 222, 228, 229, 230]:
    if idx < len(lines):
        d = json.loads(lines[idx])
        print(f"=== Line {idx} ({d.get('type')}, {d.get('source')}) ===")
        tc = d.get('tool_calls', [])
        for c in tc:
            print("Tool Call:", c.get('name'))
            if c.get('name') == 'browser_subagent':
                print("Task:\n", c.get('args', {}).get('Task')[:1000])
        if d.get('content'):
            print("Content:\n", str(d.get('content'))[:500])
