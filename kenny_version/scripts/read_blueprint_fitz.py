import fitz # PyMuPDF
doc = fitz.open(r'C:\Users\Kenny\Downloads\AI_Football_Prediction_Blueprint_compressed - Muh ihram Syahputra (2).pdf')
print("Pages in Blueprint:", len(doc))
for i in range(min(5, len(doc))):
    page = doc[i]
    print(f"--- Page {i+1} ---")
    print(page.get_text()[:300])
