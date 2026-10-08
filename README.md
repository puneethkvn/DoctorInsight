# DoctorInsight — Medical Document Analysis System

An AI-powered clinical intelligence web application for analyzing patient records, hospital discharge summaries, and prescriptions.

---

## 🌟 Key Features

1. **Document Ingestion & Analysis**
   - Upload PDF or TXT medical documents, or paste clinical notes directly.
   - Extracts diagnoses, clinical history, and critical lab findings.

2. **Automated Clinical Insights**
   - **Document Summary:** Highlights primary diagnoses, vitals, lab anomalies, and hospital course.
   - **Risk Factor Stratification:** Identifies high, medium, and low clinical risks with actionable preventative steps.
   - **Medication Safety Alerts:** Flags contraindications (e.g., NSAID risks in renal failure), drug interactions, and strict compliance warnings.
   - **Prescription Schedule:** Clear breakdown of medications, dosages, timings (morning, bedtime, with food), and clinical purpose.
   - **Patient Care Guidance:** Plain-language recovery advice, lifestyle/diet restrictions, and emergency red-flag warnings.

3. **Context-Aware Medical Q&A Chat**
   - Real-time conversational assistant to ask questions about the uploaded medical record.
   - Grounded directly in the document's content with reference context.

4. **Speech & Audio Support**
   - Built-in text-to-speech for listening to care instructions aloud.
   - Microphone input for hands-free query dictation.

---

## 🚀 How to Run

Double-click `run_app.bat` or run:
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Then open your web browser at:
**[http://localhost:8000](http://localhost:8000)**
