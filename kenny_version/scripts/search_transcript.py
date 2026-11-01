import json

transcript_path = r"C:\Users\Kenny\.gemini\antigravity\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea\.system_generated\logs\transcript.jsonl"
with open(transcript_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        content = str(data.get('content', ''))
        if any(k in content.lower() for k in ['pertemuan', 'sesi 6', 'logbook pertemuan', 'paket']):
            print(f"Line {i} ({data.get('type')}, {data.get('source')}):")
            for sub in content.split('\n'):
                if any(k in sub.lower() for k in ['pertemuan', 'sesi 6', 'logbook pertemuan', 'paket']):
                    print("  ", sub[:120])

