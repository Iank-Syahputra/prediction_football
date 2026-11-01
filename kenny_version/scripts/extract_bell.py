from PIL import Image

ref_img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
# Crop bell icon from the right
bell = ref_img.crop((75, 0, ref_img.width, ref_img.height))
bell.save(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts\bell_icon.png')
print("Bell icon saved, size:", bell.size)
