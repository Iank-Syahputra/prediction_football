import os
from PIL import Image

try:
    import pytesseract
    text = pytesseract.image_to_string(Image.open(r"C:\Users\Kenny\Downloads\Screenshot (7800).png"))
    print("=== OCR Output ===")
    print(text[:2000])
except Exception as e:
    print("pytesseract error/not available:", e)

