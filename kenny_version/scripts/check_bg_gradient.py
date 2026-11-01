from PIL import Image
import numpy as np

img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
arr = np.array(img)
# Sample top row background colors from left to right
print("Row 5 colors:")
for x in range(0, 117, 15):
    print(f"x={x}: {arr[5, x]}")
