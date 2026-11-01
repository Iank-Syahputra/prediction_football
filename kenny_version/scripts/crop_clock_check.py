from PIL import Image

img = Image.open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\UPLOAD_BERKAS_FORM_MINGGU_3\Bukti_Presensi_Meeting_Senin_26_Okt_2026.png')
crop = img.crop((1750, 1032, 1920, 1080))
crop.save(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\artifacts\clock_crop_check.png')
print("Clock crop saved")
