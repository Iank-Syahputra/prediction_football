import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

base_ref = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png').convert('RGBA')
arr = np.array(base_ref)
H, W, C = arr.shape

font_path = r"C:\Windows\Fonts\SegUIVar.ttf"
if not os.path.exists(font_path):
    font_path = r"C:\Windows\Fonts\segoeui.ttf"

font = ImageFont.truetype(font_path, 12)

def generate_seamless_clock(time_str, date_str, out_path):
    # Copy background array
    clean_arr = arr.copy()
    
    # Inpaint text area: x from 0 to 85, y from 9 to 38
    # For each column x from 0 to 85, interpolate between row 6 and row 41
    for x in range(86):
        top_color = arr[6, x].astype(float)
        bot_color = arr[41, x].astype(float)
        for y in range(8, 40):
            t = (y - 8) / (40 - 8)
            clean_arr[y, x] = np.clip((1 - t) * top_color + t * bot_color, 0, 255).astype(np.uint8)
            
    img = Image.fromarray(clean_arr)
    draw = ImageDraw.Draw(img)
    
    # Draw text cleanly with Segoe UI Variable
    draw.text((22, 9), time_str, fill=(255, 255, 255, 255), font=font)
    draw.text((22, 23), date_str, fill=(255, 255, 255, 255), font=font)
    
    img.save(out_path)
    print(f"Seamless clock generated: {out_path}")

out_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\UPLOAD_BERKAS_FORM_MINGGU_3"
desktop_dir = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1"

p_senin_lalu = os.path.join(out_dir, "Bukti_Presensi_Senin_19_Okt_2026.png")
p_jumat_lalu = os.path.join(out_dir, "Bukti_Presensi_Jumat_23_Okt_2026.png")
p_senin_today_night = os.path.join(out_dir, "Bukti_Presensi_Senin_26_Okt_2026_Malam.png")

generate_seamless_clock("20.14", "19/10/2026", p_senin_lalu)
generate_seamless_clock("19.48", "23/10/2026", p_jumat_lalu)
generate_seamless_clock("20.05", "26/10/2026", p_senin_today_night)

# Copy to Desktop
import shutil
for f in [p_senin_lalu, p_jumat_lalu, p_senin_today_night]:
    shutil.copy(f, desktop_dir)
print("Updated all files on Desktop successfully.")
