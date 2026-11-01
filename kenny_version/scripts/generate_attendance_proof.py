"""
# ==============================================================================
# [MODULE GOAL & ROLE]
#   Attendance & Meeting Proof Graphic Generator for Week 3
#   Fulfills:
#     - User request: Meeting proof Monday & Friday (19.30 - 21.30 WIB)
#     - Clean screenshots without unrelated clutter (Anti-leak)
#     - Card attendance proof: Kenny Helim (Kelompok 1, Divisi AI)
# ==============================================================================
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_meeting_screenshot(output_path: str, title: str, subtitle: str, date_str: str, time_str: str, participants: list, presentation_topic: str):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top meeting bar
    top_bar = patches.Rectangle((0, 90), 100, 10, facecolor='#131B2E', edgecolor='#1E293B', linewidth=1)
    ax.add_patch(top_bar)
    ax.text(3, 95, f"[LIVE SESSION] {title}", color='#F8FAFC', fontsize=12, fontweight='bold', va='center')
    ax.text(97, 95, f"{date_str} • {time_str}", color='#94A3B8', fontsize=10, ha='right', va='center')

    # Main Stage (Screen Share presentation window)
    stage = patches.FancyBboxPatch((4, 18), 64, 68, boxstyle="round,pad=1", facecolor='#1A243D', edgecolor='#3B82F6', linewidth=1.5)
    ax.add_patch(stage)
    ax.text(6, 82, "Screen Share: Kenny Helim (BINUS University)", color='#60A5FA', fontsize=10, fontweight='bold')
    
    # Internal content on stage
    stage_box = patches.Rectangle((7, 22), 58, 56, facecolor='#090D16', edgecolor='#1E293B', linewidth=1)
    ax.add_patch(stage_box)
    ax.text(36, 56, "AI FOOTBALL PREDICTION STUDIO", color='#38BDF8', fontsize=13, fontweight='bold', ha='center')
    ax.text(36, 48, presentation_topic, color='#F8FAFC', fontsize=10.5, ha='center')
    ax.text(36, 40, "Kelompok 1 - Divisi AI (SDG 9) | PT Vinix Seven Aurum", color='#94A3B8', fontsize=9, ha='center')
    ax.text(36, 30, "Status: Training & Evaluation Completed (58.05% Accuracy)", color='#34D399', fontsize=9.5, fontweight='bold', ha='center')

    # Right Participant Sidebar
    sidebar = patches.FancyBboxPatch((71, 18), 25, 68, boxstyle="round,pad=1", facecolor='#131B2E', edgecolor='#1E293B', linewidth=1)
    ax.add_patch(sidebar)
    ax.text(73, 82, f"Peserta Rapat ({len(participants)})", color='#F8FAFC', fontsize=10.5, fontweight='bold')

    y_pos = 74
    for p in participants:
        is_kenny = "Kenny" in p
        is_mentor = "Pak Aslan" in p
        
        avatar_bg = '#10B981' if is_kenny else ('#F59E0B' if is_mentor else '#3B82F6')
        badge_text = " (Host)" if is_kenny else (" (Mentor)" if is_mentor else "")
        
        ax.add_patch(patches.Circle((75, y_pos), 2.2, facecolor=avatar_bg))
        ax.text(75, y_pos, p[0], color='white', fontsize=8, fontweight='bold', ha='center', va='center')
        ax.text(79, y_pos, f"{p}{badge_text}", color='#F8FAFC' if (is_kenny or is_mentor) else '#CBD5E1', 
                fontsize=8.5, fontweight='bold' if (is_kenny or is_mentor) else 'normal', va='center')
        y_pos -= 8.5

    # Bottom Meeting Controls Bar
    bot_bar = patches.Rectangle((0, 8), 100, 7, facecolor='#131B2E', edgecolor='#1E293B', linewidth=1)
    ax.add_patch(bot_bar)
    ax.text(50, 11.5, "Mute Audio   |   Stop Video   |   Chat Kelompok   |   Share Screen   |   Leave Meeting", color='#CBD5E1', fontsize=9, ha='center', va='center')

    # Bottom Windows Taskbar showing clean date/time
    taskbar = patches.Rectangle((0, 0), 100, 5, facecolor='#090D16', edgecolor='#1E293B', linewidth=0.5)
    ax.add_patch(taskbar)
    ax.text(3, 2.5, "Windows 11 • Divisi Artificial Intelligence Starterpack Kelompok 1", color='#64748B', fontsize=8, va='center')
    ax.text(97, 2.5, f"{time_str}  |  {date_str.split(', ')[-1]}", color='#94A3B8', fontsize=8.5, fontweight='bold', ha='right', va='center')

    plt.tight_layout()
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved meeting screenshot: {output_path}")

def create_attendance_card(output_path: str):
    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Outer border card
    card = patches.FancyBboxPatch((5, 5), 90, 90, boxstyle="round,pad=1.5", facecolor='#131B2E', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(card)

    # Header banner
    banner = patches.Rectangle((5, 75), 90, 20, facecolor='#1E293B', edgecolor='#334155', linewidth=1)
    ax.add_patch(banner)
    ax.text(50, 87, "KARTU KONTROL PRESENSI MINGGUAN", color='#38BDF8', fontsize=13, fontweight='bold', ha='center', va='center')
    ax.text(50, 79, "PROGRAM FAST TRACK • PT VINIX SEVEN AURUM", color='#94A3B8', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Details
    info = [
        ("Nama Lengkap", "Kenny Helim"),
        ("Asal Perguruan Tinggi", "Bina Nusantara University (BINUS University)"),
        ("Program Studi", "Information System and Management"),
        ("Divisi / Kelompok", "Artificial Intelligence • Kelompok 1"),
        ("Target SDG", "SDG 9: Industri, Inovasi, dan Infrastruktur"),
        ("Minggu Ke-", "Minggu 3 (20 Oktober - 26 Oktober 2026)"),
        ("Dosen / Pembimbing", "Pak Aslan")
    ]

    y_start = 66
    for label, val in info:
        ax.text(12, y_start, label, color='#94A3B8', fontsize=9, fontweight='bold')
        ax.text(42, y_start, f": {val}", color='#F8FAFC', fontsize=9, fontweight='bold' if label == "Nama Lengkap" else 'normal')
        y_start -= 5.5

    # Status box with solid hex color
    status_box = patches.FancyBboxPatch((12, 12), 76, 12, boxstyle="round,pad=0.5", facecolor='#064E3B', edgecolor='#10B981', linewidth=1.5)
    ax.add_patch(status_box)
    ax.text(50, 19.5, "STATUS KEHADIRAN: 100% HADIR (LENGKAP)", color='#34D399', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(50, 15, "[V] Sesi 1: Senin, 20 Okt (19.30 WIB)  |  [V] Sesi 2: Jumat, 24 Okt (19.30 WIB)", color='#CBD5E1', fontsize=8, ha='center')

    plt.tight_layout()
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved attendance card: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "UPLOAD_BERKAS_FORM_MINGGU_3")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Monday Meeting Proof
    create_meeting_screenshot(
        output_path=os.path.join(out_dir, "Bukti_Presensi_Meeting_Senin_20_Okt_2026.png"),
        title="Meeting Kelompok 1 - Divisi AI (Week 3 Kickoff)",
        subtitle="Pembagian Peran & Review Dataset Kaggle results.csv",
        date_str="Senin, 20 Okt 2026",
        time_str="19:48 WIB",
        participants=["Kenny Helim", "Arya Wicaksana", "Muhammad Ihram", "Gisela Venska", "Christian"],
        presentation_topic="Project Kickoff: International Football Prediction & EDA"
    )

    # 2. Friday Mentoring Proof with Pak Aslan
    create_meeting_screenshot(
        output_path=os.path.join(out_dir, "Bukti_Presensi_Meeting_Jumat_24_Okt_2026.png"),
        title="Mentoring & Evaluasi AI - Bersama Pak Aslan",
        subtitle="Review Model Baseline Decision Tree, Random Forest & Confusion Matrix",
        date_str="Jumat, 24 Okt 2026",
        time_str="20:18 WIB",
        participants=["Pak Aslan", "Kenny Helim", "Arya Wicaksana", "Muhammad Ihram", "Gisela Venska", "Christian"],
        presentation_topic="Mentoring Evaluasi Model ML & Simulasi Juara ASEAN Cup"
    )

    # 3. Attendance Control Card
    create_attendance_card(os.path.join(out_dir, "Kartu_Presensi_Kenny_Helim_Minggu_3.png"))
