import os
from pdfminer.high_level import extract_text

f = r'C:\Users\Kenny\Downloads\AI_Assignment Week 4.pdf'
text = extract_text(f)
with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\scripts\week4_assignment_text.txt', 'w', encoding='utf-8') as out:
    out.write(text)

print("Saved week4_assignment_text.txt, length:", len(text))
for line in text.split('\n')[:40]:
    if line.strip():
        print(line.strip())
