import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'browser_subagent' in line:
            data = json.loads(line)
            for c in data.get('tool_calls', []):
                if c.get('name') == 'browser_subagent':
                    args = c.get('args', {})
                    print(f"Line {i}: {args.get('TaskName')}")
