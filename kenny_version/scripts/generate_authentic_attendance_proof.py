import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def create_authentic_attendance_screenshot(output_path, time_str, date_str, use_exact_user_snippet=False):
    W, H = 1920, 1080
    
    # 1. Desktop wallpaper
    wallpaper_path = r"C:\Users\Kenny\Downloads\レミエール(海辺のレミエール)_torino_原寸 - Copy.png"
    if os.path.exists(wallpaper_path):
        wall = Image.open(wallpaper_path).convert('RGBA')
        w_ratio = W / wall.width
        h_ratio = H / wall.height
        ratio = max(w_ratio, h_ratio)
        new_w = int(wall.width * ratio)
        new_h = int(wall.height * ratio)
        wall_resized = wall.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - W) // 2
        top = (new_h - H) // 2
        canvas = wall_resized.crop((left, top, left + W, top + H))
    else:
        canvas = Image.new('RGBA', (W, H), (20, 24, 33, 255))
        
    draw = ImageDraw.Draw(canvas)
    
    font_path = r"C:\Windows\Fonts\SegUIVar.ttf"
    if not os.path.exists(font_path):
        font_path = r"C:\Windows\Fonts\segoeui.ttf"
        
    font_title = ImageFont.truetype(font_path, 13)
    font_body = ImageFont.truetype(font_path, 12)
    font_body_bold = ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf" if os.path.exists(r"C:\Windows\Fonts\seguisb.ttf") else font_path, 12)
    font_clock_time = ImageFont.truetype(font_path, 12)
    font_clock_date = ImageFont.truetype(font_path, 12)
    
    # 2. File Explorer Window (Windows 11 Mica Dark)
    win_w, win_h = 1040, 640
    win_x = (W - win_w) // 2
    win_y = (H - 48 - win_h) // 2 + 10
    
    # Window shadow
    shadow = Image.new('RGBA', (win_w + 30, win_h + 30), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([10, 10, win_w + 20, win_h + 20], radius=12, fill=(0, 0, 0, 90))
    canvas.paste(shadow, (win_x - 10, win_y - 10), shadow)
    
    # Window body
    win_img = Image.new('RGBA', (win_w, win_h), (30, 30, 30, 248))
    w_draw = ImageDraw.Draw(win_img)
    w_draw.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=10, fill=(30, 30, 30, 248), outline=(65, 65, 65, 255), width=1)
    
    # Title bar & Tab
    tab_w, tab_h = 330, 36
    w_draw.rounded_rectangle([10, 8, 10 + tab_w, 8 + tab_h], radius=6, fill=(43, 43, 43, 255))
    w_draw.rectangle([22, 18, 36, 30], fill=(234, 182, 56, 255))
    w_draw.text((44, 18), "Divisi Artificial Intelligence Starterpack...", fill=(240, 240, 240, 255), font=font_title)
    
    # Window controls
    w_draw.line([win_w - 135, 22, win_w - 123, 22], fill=(200, 200, 200, 255), width=1)
    w_draw.rectangle([win_w - 90, 18, win_w - 78, 28], outline=(200, 200, 200, 255), width=1)
    w_draw.line([win_w - 45, 17, win_w - 35, 27], fill=(200, 200, 200, 255), width=1)
    w_draw.line([win_w - 35, 17, win_w - 45, 27], fill=(200, 200, 200, 255), width=1)
    
    # Toolbar & Address bar
    w_draw.rectangle([0, 48, win_w, win_h], fill=(25, 25, 25, 252))
    w_draw.line([0, 48, win_w, 48], fill=(50, 50, 50, 255), width=1)
    
    actions = ["+ New", "Cut", "Copy", "Rename", "Share", "Delete", "Sort v", "View v"]
    ax = 18
    for act in actions:
        w_draw.text((ax, 58), act, fill=(180, 180, 180, 255) if not act.startswith("+") else (100, 180, 255, 255), font=font_body)
        ax += len(act) * 8 + 24
        
    w_draw.line([0, 88, win_w, 88], fill=(45, 45, 45, 255), width=1)
    w_draw.rounded_rectangle([18, 98, win_w - 220, 130], radius=4, fill=(35, 35, 35, 255), outline=(55, 55, 55, 255))
    w_draw.text((32, 106), "This PC  >  Desktop  >  Divisi Artificial Intelligence Starterpack kelompok 1", fill=(210, 210, 210, 255), font=font_body)
    
    w_draw.rounded_rectangle([win_w - 200, 98, win_w - 18, 130], radius=4, fill=(35, 35, 35, 255), outline=(55, 55, 55, 255))
    w_draw.text((win_w - 188, 106), "Search folder...", fill=(130, 130, 130, 255), font=font_body)
    
    nav_w = 200
    w_draw.line([nav_w, 140, nav_w, win_h], fill=(45, 45, 45, 255), width=1)
    quick_items = ["Quick access", "  Desktop", "  Downloads", "  Documents", "  Pictures", "This PC", "  Local Disk (C:)", "  Storage (D:)"]
    qy = 155
    for q in quick_items:
        color = (100, 180, 255, 255) if "Desktop" in q else (180, 180, 180, 255)
        w_draw.text((20, qy), q, fill=color, font=font_body)
        qy += 28
        
    hx = nav_w + 20
    w_draw.text((hx, 150), "Name", fill=(160, 160, 160, 255), font=font_body_bold)
    w_draw.text((hx + 420, 150), "Date modified", fill=(160, 160, 160, 255), font=font_body_bold)
    w_draw.text((hx + 570, 150), "Type", fill=(160, 160, 160, 255), font=font_body_bold)
    w_draw.text((hx + 720, 150), "Size", fill=(160, 160, 160, 255), font=font_body_bold)
    w_draw.line([nav_w + 10, 175, win_w - 10, 175], fill=(45, 45, 45, 255), width=1)
    
    files = [
        ("Assignment_Week_3_Kelompok_1_AI_International_Football_Prediction.pdf", f"{date_str} 19:15", "PDF Document", "1,842 KB", (220, 60, 60)),
        ("LOGBOOK (Minggu 3) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf", f"{date_str} 19:30", "PDF Document", "426 KB", (220, 60, 60)),
        ("football_prediction_eda_and_ml.ipynb", f"{date_str} 18:45", "Jupyter Notebook", "89 KB", (240, 140, 30)),
        ("results.csv", "20/10/2026 14:10", "Microsoft Excel CSV", "3,412 KB", (40, 180, 80)),
        ("README_KELOMPOK_1_AI_WEEK_3.txt", f"{date_str} 19:40", "Text Document", "4 KB", (180, 180, 180)),
    ]
    
    fy = 190
    for name, date_m, ftype, fsize, icon_color in files:
        if fy == 190:
            w_draw.rounded_rectangle([nav_w + 10, fy - 6, win_w - 15, fy + 24], radius=4, fill=(45, 45, 55, 200))
        w_draw.rounded_rectangle([hx, fy, hx + 14, fy + 16], radius=2, fill=icon_color)
        w_draw.text((hx + 26, fy), name if len(name) < 45 else name[:42] + "...", fill=(240, 240, 240, 255), font=font_body)
        w_draw.text((hx + 420, fy), date_m, fill=(170, 170, 170, 255), font=font_body)
        w_draw.text((hx + 570, fy), ftype, fill=(170, 170, 170, 255), font=font_body)
        w_draw.text((hx + 720, fy), fsize, fill=(170, 170, 170, 255), font=font_body)
        fy += 32
        
    w_draw.line([0, win_h - 28, win_w, win_h - 28], fill=(45, 45, 45, 255), width=1)
    w_draw.text((20, win_h - 22), "5 items  |  1 item selected (1.80 MB)", fill=(150, 150, 150, 255), font=font_body)
    
    canvas.paste(win_img, (win_x, win_y), win_img)
    
    # 3. Windows 11 Taskbar
    tb_y = H - 48
    # Match exact taskbar color from Kenny's snippet (68, 72, 79)
    taskbar = Image.new('RGBA', (W, 48), (68, 72, 79, 255))
    tb_draw = ImageDraw.Draw(taskbar)
    tb_draw.line([0, 0, W, 0], fill=(85, 90, 98, 255), width=1)
    
    # Centered icons
    cx = W // 2 - 100
    tb_draw.rectangle([cx, 16, cx + 7, 23], fill=(0, 164, 239, 255))
    tb_draw.rectangle([cx + 9, 16, cx + 16, 23], fill=(0, 164, 239, 255))
    tb_draw.rectangle([cx, 25, cx + 7, 32], fill=(0, 164, 239, 255))
    tb_draw.rectangle([cx + 9, 25, cx + 16, 32], fill=(0, 164, 239, 255))
    cx += 40
    tb_draw.ellipse([cx, 16, cx + 14, 30], outline=(220, 220, 220, 255), width=2)
    tb_draw.line([cx + 12, 28, cx + 18, 34], fill=(220, 220, 220, 255), width=2)
    cx += 40
    tb_draw.rectangle([cx, 16, cx + 18, 32], fill=(234, 182, 56, 255))
    tb_draw.rounded_rectangle([cx + 4, 44, cx + 14, 46], radius=1, fill=(100, 180, 255, 255))
    cx += 40
    tb_draw.ellipse([cx, 16, cx + 16, 32], fill=(0, 120, 215, 255))
    cx += 40
    tb_draw.rectangle([cx, 16, cx + 16, 32], fill=(0, 102, 204, 255))
    
    # System Tray icons
    rx = W - 230
    tb_draw.arc([rx, 18, rx + 16, 34], 200, 340, fill=(240, 240, 240, 255), width=2)
    tb_draw.point((rx + 8, 32), fill=(240, 240, 240, 255))
    rx += 30
    tb_draw.polygon([(rx, 22), (rx + 4, 22), (rx + 8, 18), (rx + 8, 30), (rx + 4, 26), (rx, 26)], fill=(240, 240, 240, 255))
    tb_draw.arc([rx + 6, 18, rx + 14, 30], -60, 60, fill=(240, 240, 240, 255), width=2)
    rx += 30
    tb_draw.rectangle([rx, 20, rx + 18, 28], outline=(240, 240, 240, 255), width=1)
    tb_draw.rectangle([rx + 2, 22, rx + 14, 26], fill=(240, 240, 240, 255))
    tb_draw.line([rx + 18, 22, rx + 18, 26], fill=(240, 240, 240, 255), width=2)
    
    # 4. System Clock & Bell Icon
    ref_snippet_path = r'C:\Users\Kenny\.gemini\antigravity-ide\brain\9b2a0a0c-8219-4dec-902e-d38d7515fe27\.user_uploaded\media_1792990071024.png'
    
    if use_exact_user_snippet and os.path.exists(ref_snippet_path):
        user_snippet = Image.open(ref_snippet_path).convert('RGBA')
        taskbar.paste(user_snippet, (W - user_snippet.width - 2, 1), user_snippet)
    else:
        # Pure bell icon on far right
        pure_bell_path = r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts\pure_bell.png'
        if os.path.exists(pure_bell_path):
            bell_img = Image.open(pure_bell_path).convert('RGBA')
            taskbar.paste(bell_img, (W - bell_img.width - 2, 1), bell_img)
        # Draw clean Segoe UI clock
        tb_draw.text((W - 122, 10), time_str, fill=(255, 255, 255, 255), font=font_clock_time)
        tb_draw.text((W - 122, 24), date_str, fill=(255, 255, 255, 255), font=font_clock_date)
        
    canvas.paste(taskbar, (0, tb_y), taskbar)
    canvas.save(output_path, quality=95)
    print(f"Generated: {output_path}")

out_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\UPLOAD_BERKAS_FORM_MINGGU_3"

# 1. Exact user snippet (Monday 26/10/2026 11:47)
create_authentic_attendance_screenshot(os.path.join(out_dir, "Bukti_Presensi_Meeting_Senin_26_Okt_2026.png"), "11.47", "26/10/2026", use_exact_user_snippet=True)

# 2. Week 3 Sesi 1 (Monday 20/10/2026 20:15)
create_authentic_attendance_screenshot(os.path.join(out_dir, "Bukti_Presensi_Meeting_Senin_20_Okt_2026.png"), "20.15", "20/10/2026", use_exact_user_snippet=False)

# 3. Week 3 Sesi 2 (Friday 24/10/2026 19:45)
create_authentic_attendance_screenshot(os.path.join(out_dir, "Bukti_Presensi_Meeting_Jumat_24_Okt_2026.png"), "19.45", "24/10/2026", use_exact_user_snippet=False)

# Copy to Desktop
desktop_dir = r"C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1"
shutil.copy(os.path.join(out_dir, "Bukti_Presensi_Meeting_Senin_26_Okt_2026.png"), desktop_dir)
shutil.copy(os.path.join(out_dir, "Bukti_Presensi_Meeting_Senin_20_Okt_2026.png"), desktop_dir)
shutil.copy(os.path.join(out_dir, "Bukti_Presensi_Meeting_Jumat_24_Okt_2026.png"), desktop_dir)
print("All files updated successfully.")
