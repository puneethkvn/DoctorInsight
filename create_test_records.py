"""
Script to generate all 15 patient clinical record files (.txt and .pdf) in medical_records/ directory.
"""

import os
import fitz  # PyMuPDF
from sample_data import SAMPLE_DOCUMENTS

RECORDS_DIR = os.path.join(os.path.dirname(__file__), "medical_records")
os.makedirs(RECORDS_DIR, exist_ok=True)

for key, doc_info in SAMPLE_DOCUMENTS.items():
    p_name = doc_info["patient"]["name"].lower().replace(" ", "_")
    base_name = f"{doc_info['id']}_{p_name}"
    txt_path = os.path.join(RECORDS_DIR, f"{base_name}.txt")
    pdf_path = os.path.join(RECORDS_DIR, f"{base_name}.pdf")

    content = doc_info["content"].strip()

    # 1. Write TXT file
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Write PDF file
    doc = fitz.open()
    lines = content.split("\n")
    page = doc.new_page(width=595, height=842)
    y_pos = 50
    margin_left = 50

    for line in lines:
        if y_pos > 790:
            page = doc.new_page(width=595, height=842)
            y_pos = 50

        font_size = 9.5
        font_name = "helv"
        color = (0.1, 0.1, 0.1)

        line_strip = line.strip()
        if any(line_strip.startswith(h) for h in ["METROPOLITAN", "CHILDREN", "ORTHOPEDIC", "CENTRAL", "INSTITUTE", "HEART", "CENTER", "LIVER", "MATERNAL", "CHEST"]):
            font_size = 12.5
            font_name = "hebo"
            color = (0.05, 0.35, 0.65)
        elif any(line_strip.startswith(h) for h in ["CHIEF", "PRIMARY", "CLINICAL", "DISCHARGE", "CONTRAINDICATIONS", "DIETARY"]):
            font_size = 10.5
            font_name = "hebo"
            y_pos += 4

        page.insert_text(fitz.Point(margin_left, y_pos), line_strip, fontsize=font_size, fontname=font_name, color=color)
        y_pos += (font_size + 4)

    doc.save(pdf_path)
    doc.close()

print(f"Generated {len(SAMPLE_DOCUMENTS)} TXT and PDF files in {RECORDS_DIR}")
