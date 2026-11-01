import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

d = json.loads(lines[280])
content = d.get('content', '')

for step in content.split('### Step '):
    header = step.split('\n')[0]
    if header.startswith('16:') or header.startswith('24:'):
        print(f"=== {header} ===")
        print(step)
