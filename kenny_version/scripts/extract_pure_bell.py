from PIL import Image

ref_img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
print("Ref size:", ref_img.size)

# Crop pure bell icon
pure_bell = ref_img.crop((88, 0, ref_img.width, ref_img.height))
pure_bell.save(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts\pure_bell.png')
print("Pure bell size:", pure_bell.size)
