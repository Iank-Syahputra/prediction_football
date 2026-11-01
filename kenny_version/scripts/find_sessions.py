import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'WEEK \d Sesi \d', text)
print("Unique WEEK Sesi matches:", set(matches))
