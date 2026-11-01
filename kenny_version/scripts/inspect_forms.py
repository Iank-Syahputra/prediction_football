import os
import re
import json

base_dir = r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction\data"

for fname in ["form1.html", "form2.html", "form3.html"]:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print("=" * 60)
    print(f"FILE: {fname}")
    
    title_match = re.search(r"<title>(.*?)</title>", content)
    if title_match:
        print("Title:", title_match.group(1))
        
    og_title = re.search(r'<meta property="og:title" content="(.*?)"', content)
    if og_title:
        print("OG Title:", og_title.group(1))
        
    og_desc = re.search(r'<meta property="og:description" content="(.*?)"', content)
    if og_desc:
        print("OG Desc:", og_desc.group(1))
        
    # Extract FB_PUBLIC_LOAD_DATA_
    match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);', content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            # data structure: [null, [form_title, [questions...], form_desc, ...]]
            form_info = data[1]
            print("Form Title:", form_info[8] if len(form_info) > 8 else form_info[0])
            print("Form Subtitle/Desc:", form_info[0])
            questions = form_info[1]
            print(f"Total Questions/Fields: {len(questions)}")
            for q in questions:
                if q:
                    q_title = q[1]
                    q_id = q[4][0][0] if q[4] and q[4][0] else None
                    q_type = q[3] # 0: short text, 1: paragraph, 2: radio, 3: dropdown, 4: checkbox, 9: date, etc.
                    choices = [c[0] for c in q[4][0][1]] if q[4] and q[4][0] and len(q[4][0]) > 1 and q[4][0][1] else []
                    print(f"  - Field: '{q_title}' (ID: {q_id}, Type: {q_type})")
                    if choices:
                        print(f"    Choices: {choices[:10]}")
        except Exception as e:
            print("Could not parse FB_PUBLIC_LOAD_DATA_:", e)
    else:
        print("FB_PUBLIC_LOAD_DATA_ not found in content. Checking redirect or login requirement...")
        if "accounts.google.com" in content:
            print("  -> Requires Google Account Authentication!")
