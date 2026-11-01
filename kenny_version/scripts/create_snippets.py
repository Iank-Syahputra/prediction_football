import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

p19 = r'C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Senin_19_Okt_2026.png'
p23 = r'C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\Bukti_Presensi_Jumat_23_Okt_2026.png'
plog = r'C:\Users\Kenny\Desktop\Divisi Artificial Intelligence Starterpack kelompok 1\LOGBOOK (Minggu 3) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf'

b19 = get_b64(p19)
b23 = get_b64(p23)
blog = get_b64(plog)

js_content = f'''
// SNIPPET FOR SENIN 19 OKT (WEEK 3 SESI 1)
const b64_19 = "{b19}";
async function uploadSenin19(inputElement) {{
    const res = await fetch("data:image/png;base64," + b64_19);
    const blob = await res.blob();
    const file = new File([blob], "Bukti_Presensi_Senin_19_Okt_2026.png", {{type: "image/png"}});
    const dt = new DataTransfer();
    dt.items.add(file);
    inputElement.files = dt.files;
    inputElement.dispatchEvent(new Event("change", {{bubbles: true}}));
}}

// SNIPPET FOR JUMAT 23 OKT (WEEK 3 SESI 2)
const b64_23 = "{b23}";
async function uploadJumat23(inputElement) {{
    const res = await fetch("data:image/png;base64," + b64_23);
    const blob = await res.blob();
    const file = new File([blob], "Bukti_Presensi_Jumat_23_Okt_2026.png", {{type: "image/png"}});
    const dt = new DataTransfer();
    dt.items.add(file);
    inputElement.files = dt.files;
    inputElement.dispatchEvent(new Event("change", {{bubbles: true}}));
}}

// SNIPPET FOR LOGBOOK WEEK 3
const b64_log = "{blog}";
async function uploadLogbook(inputElement) {{
    const res = await fetch("data:application/pdf;base64," + b64_log);
    const blob = await res.blob();
    const file = new File([blob], "LOGBOOK (Minggu 3) Kegiatan Fast Track - Divisi Artificial Intelligence - Kenny Helim.pdf", {{type: "application/pdf"}});
    const dt = new DataTransfer();
    dt.items.add(file);
    inputElement.files = dt.files;
    inputElement.dispatchEvent(new Event("change", {{bubbles: true}}));
}}
'''

with open(r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\upload_snippets.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print('Generated upload_snippets.js successfully!')
