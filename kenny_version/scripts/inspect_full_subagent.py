import json

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

d = json.loads(lines[280])
content = d.get('content', '')
print("Length of content:", len(content))

# Look for user_keyboard_input, type_text, or execute_javascript
for step in content.split('### Step '):
    header = step.split('\n')[0]
    if any(k in step for k in ['Kenny', 'Igris', 'BATCH', '0812']):
        print(f"--- Step {header} ---")
        for line in step.split('\n')[:15]:
            print(line[:120])
