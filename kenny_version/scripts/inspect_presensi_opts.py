import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in [195, 213]:
    if idx < len(lines):
        d = json.loads(lines[idx+1])
        c = d.get('content', '')
        for line in c.split('\n'):
            if 'WEEK' in line or 'Sesi' in line or 'aria-label' in line:
                print(line[:120])
