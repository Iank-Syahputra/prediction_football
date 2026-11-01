from PIL import Image
import numpy as np

img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
print("Image format:", img.format, "size:", img.size)
arr = np.array(img)
print("Shape:", arr.shape)
print("Background sample at (0,0):", arr[0,0])
print("Max RGBA:", arr.max(axis=(0,1)))
