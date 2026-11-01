import os
from PIL import Image

path = r"C:\Users\Kenny\Downloads\Screenshot (7800).png"
print("Exists:", os.path.exists(path))
if os.path.exists(path):
    im = Image.open(path)
    print("Size:", im.size, "Mode:", im.mode, "Format:", im.format)
    # Let's copy it to artifact dir so we can inspect or view it if needed
    art_dir = r"C:\Users\Kenny\.gemini\antigravity\brain\fbe53b35-ce63-4718-9eae-05b6c9a776ea"
    os.makedirs(art_dir, exist_ok=True)
    dst = os.path.join(art_dir, "Screenshot_7800.png")
    im.save(dst)
    print("Saved copy to:", dst)

