import os
from pdfminer.high_level import extract_text

files = [
    r'C:\Users\Kenny\Downloads\AI_Football_Prediction_Blueprint_compressed - Muh ihram Syahputra (2).pdf',
    r'C:\Users\Kenny\Downloads\AI_Assignment Week 3.pdf',
    r'C:\Users\Kenny\Downloads\AI_Assignment Week 4.pdf'
]

for f in files:
    print(f"==================================================")
    print(f"FILE: {os.path.basename(f)}")
    print(f"==================================================")
    try:
        text = extract_text(f)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        print(f"Total lines: {len(lines)}")
        print("\n".join(lines[:40]))
        print("\n... [middle sample] ...\n")
        print("\n".join(lines[len(lines)//2 : len(lines)//2 + 20]))
        print("\n... [last lines] ...\n")
        print("\n".join(lines[-20:]))
    except Exception as e:
        print("Error extracting text:", e)
