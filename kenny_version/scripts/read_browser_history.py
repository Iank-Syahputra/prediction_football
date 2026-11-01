import sqlite3
import shutil
import os

history_paths = [
    os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History',
    os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\History'
]

temp_path = r'C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\data\temp_history.db'

for hpath in history_paths:
    if os.path.exists(hpath):
        print("Checking history:", hpath)
        try:
            shutil.copy2(hpath, temp_path)
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            query = """
            SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') 
            FROM urls 
            WHERE url LIKE '%1FAIpQLSdVPxekg5o3NyjLmiG3UgvyAHbwlQSqiBAMjyWroEiDXOwHHA%'
               OR url LIKE '%1FAIpQLSfaoPBT-SCmdU4KGH2CmnVHMAsc704VRVlWYsfUVj1Ybm30aw%'
               OR url LIKE '%1FAIpQLSdRBjdOI45WhyHgdCDujatOMl6KFhjNO5lP7qY18d6FYSFWlw%'
               OR url LIKE '%forms%'
            ORDER BY last_visit_time DESC LIMIT 30
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for r in rows:
                print(f"[{r[2]}] {r[1]} -> {r[0]}")
            conn.close()
        except Exception as e:
            print("Error reading history:", e)
