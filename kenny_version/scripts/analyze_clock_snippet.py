from PIL import Image
import numpy as np

img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png')
w, h = img.size
print("Width:", w, "Height:", h)

# Find bounding box of bright pixels (the text)
gray = np.array(img.convert('L'))
threshold = 150
y_indices, x_indices = np.where(gray > threshold)
print("Text X bounds:", x_indices.min(), "to", x_indices.max())
print("Text Y bounds:", y_indices.min(), "to", y_indices.max())

# Split into top line (time) and bottom line (date)
mid_y = (y_indices.min() + y_indices.max()) // 2
print("Mid Y approx:", mid_y)
y_top = y_indices[y_indices < mid_y]
y_bottom = y_indices[y_indices >= mid_y]
print("Time line Y:", y_top.min(), "to", y_top.max(), "height:", y_top.max() - y_top.min() + 1)
print("Date line Y:", y_bottom.min(), "to", y_bottom.max(), "height:", y_bottom.max() - y_bottom.min() + 1)
