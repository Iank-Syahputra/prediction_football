import os
from PIL import Image, ImageDraw, ImageFont

# Load reference image
ref_img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
print("Ref size:", ref_img.size)

# Find Segoe UI font file
font_path = r"C:\Windows\Fonts\SegUIVar.ttf"
if not os.path.exists(font_path):
    font_path = r"C:\Windows\Fonts\segoeui.ttf"
print("Using font path:", font_path)

# Windows 11 taskbar clock uses 12px Segoe UI Variable
font_time = ImageFont.truetype(font_path, 12)
font_date = ImageFont.truetype(font_path, 12)

# Create test clock
test_img = Image.new('RGBA', (120, 46), (68, 72, 79, 255))
draw = ImageDraw.Draw(test_img)
draw.text((10, 8), "11.47", fill=(255, 255, 255, 255), font=font_time)
draw.text((10, 22), "26/10/2026", fill=(255, 255, 255, 255), font=font_date)

test_img.save(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts\test_clock.png')
print("Test clock saved successfully.")
