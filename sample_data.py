"""
DoctorInsight - 15 Comprehensive Clinical Patient Records
"""

SAMPLE_DOCUMENTS = {
    "patient_01": {
        "id": "doc_p01",
        "title": "Geriatric Care: Hypertension, Hyperlipidemia & BPH",
        "category": "Internal & Geriatric Medicine",
        "patient": {
            "name": "Harold Jenkins",
            "age": 71,
            "gender": "Male",
            "uhid": "HJ-MED-2026-1001",
            "admission_date": "2026-10-01",
            "discharge_date": "2026-10-04"
        },
        "content": """METROPOLITAN INTERNAL MEDICINE CLINICAL RECORD
Patient Name: Harold Jenkins | Age: 71 | Sex: Male | UHID: HJ-MED-2026-1001
Attending Physician: Dr. Sarah Vance, MD

CHIEF COMPLAINTS:
Routine 6-month chronic disease follow-up for hypertension, hyperlipidemia, and benign prostatic hyperplasia. Reports mild morning knee stiffness and occasional postural lightheadedness when rising rapidly.

PRIMARY DIAGNOSIS:
1. Essential Hypertension (Moderate, Stage 2).
2. Primary Hyperlipidemia (Elevated LDL cholesterol).
3. Benign Prostatic Hyperplasia (BPH) with lower urinary tract symptoms.
4. Bilateral Knee Osteoarthritis.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Blood Pressure: 138/84 mmHg | Pulse Rate: 68 bpm
- Fasting Blood Sugar: 98 mg/dL | HbA1c: 5.7%
- Serum Creatinine: 1.0 mg/dL (eGFR 78 mL/min) | Serum Potassium: 4.6 mEq/L
- Total Cholesterol: 196 mg/dL | LDL: 114 mg/dL | HDL: 44 mg/dL | PSA: 2.4 ng/mL

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Lisinopril 20 mg - 1 tablet orally once daily morning (ACE Inhibitor for BP).
2. Tab. Atorvastatin 20 mg - 1 tablet orally daily at bedtime (Statin for lipids).
3. Tab. Tamsulosin 0.4 mg - 1 tablet orally daily 30 minutes after dinner (Alpha-1 blocker for BPH).
4. Tab. Paracetamol 500 mg - 1 tablet orally every 8 hours as needed for joint pain.
5. Tab. Cholecalciferol (Vitamin D3) 1000 IU - 1 tablet daily with breakfast.

CONTRAINDICATIONS & MEDICATION ALERTS:
- STRICTLY AVOID NSAIDs (Ibuprofen, Naproxen) with Lisinopril as they impair renal perfusion and raise blood pressure.
- ORTHOSTATIC HYPOTENSION ALERT: Lisinopril + Tamsulosin can cause dizziness upon standing. Sit on bed edge before rising.

DIETARY & LIFESTYLE GUIDANCE:
- Low sodium DASH diet (<2g salt/day).
- Hydrate with 1.8 Liters water daily; limit evening fluids after 8 PM.
- Walk 25 minutes daily on flat ground."""
    },

    "patient_02": {
        "id": "doc_p02",
        "title": "Cardiology: Acute STEMI & Post-PCI LAD Drug-Eluting Stent",
        "category": "Interventional Cardiology",
        "patient": {
            "name": "Rajesh Varma",
            "age": 59,
            "gender": "Male",
            "uhid": "MHI-CARD-2026-1002",
            "admission_date": "2026-09-20",
            "discharge_date": "2026-09-24"
        },
        "content": """METROPOLITAN HEART INSTITUTE - CARDIOLOGY DISCHARGE SUMMARY
Patient Name: Rajesh Varma | Age: 59 | Sex: Male | UHID: MHI-CARD-2026-1002
Attending Cardiologist: Dr. Arvind Deshmukh, MD, DM

CHIEF COMPLAINTS:
Severe retrosternal crushing chest pain radiating to left arm and jaw with diaphoresis for 3 hours.

PRIMARY DIAGNOSIS:
1. Acute Anterior Wall ST-Elevation Myocardial Infarction (STEMI).
2. Single-Vessel Coronary Artery Disease (95% Proximal LAD Occlusion - Post DES Stent).
3. Primary Dyslipidemia.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- High-Sensitivity Troponin-I: Peak 4,200 ng/L (Down to 180 ng/L)
- Total Cholesterol: 245 mg/dL | LDL: 168 mg/dL | HDL: 34 mg/dL
- Serum Creatinine: 1.0 mg/dL | HbA1c: 5.8%
- 2D Echocardiogram: Anterior wall hypokinesis, LVEF 46%.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Aspirin 75 mg - 1 tablet orally once daily after lunch (Antiplatelet).
2. Tab. Ticagrelor 90 mg - 1 tablet orally twice daily morning and night (Dual Antiplatelet Therapy).
3. Tab. Atorvastatin 80 mg - 1 tablet orally daily at bedtime (High-intensity statin).
4. Tab. Metoprolol Succinate ER 25 mg - 1 tablet orally once daily morning (Beta-blocker).
5. Tab. Ramipril 2.5 mg - 1 tablet orally once daily at bedtime (ACE inhibitor).
6. Tab. Pantoprazole 40 mg - 1 tablet orally once daily empty stomach morning.

CONTRAINDICATIONS & MEDICATION ALERTS:
- CRITICAL STENT THROMBOSIS ALERT: Never skip or stop Ticagrelor or Aspirin without cardiologist approval. Premature cessation causes fatal stent clotting.
- Avoid grapefruit juice (inhibits Atorvastatin and Ticagrelor clearance).

DIETARY & LIFESTYLE GUIDANCE:
- Strict zero trans-fat Mediterranean cardiac diet.
- Avoid lifting >5 kg for 4 weeks; light brisk walk 20 mins daily."""
    },

    "patient_03": {
        "id": "doc_p03",
        "title": "Nephrology: Type 2 Diabetes & Stage 3b Chronic Kidney Disease",
        "category": "Nephrology & Metabolic Care",
        "patient": {
            "name": "Ramesh Kumar Sharma",
            "age": 58,
            "gender": "Male",
            "uhid": "MGH-NEPH-2026-1003",
            "admission_date": "2026-09-28",
            "discharge_date": "2026-10-04"
        },
        "content": """METROPOLITAN GENERAL HOSPITAL - NEPHROLOGY DISCHARGE RECORD
Patient Name: Ramesh Kumar Sharma | Age: 58 | Sex: Male | UHID: MGH-NEPH-2026-1003
Consulting Nephrologist: Dr. Sunita Kulkarni, MD, DM

CHIEF COMPLAINTS:
Bilateral pitting leg swelling for 3 weeks, uncontrolled blood sugars (240-280 mg/dL), fatigue, and BP 168/102 mmHg.

PRIMARY DIAGNOSIS:
1. Type 2 Diabetes Mellitus with Diabetic Nephropathy (Stage 3b CKD).
2. Secondary Renovascular Hypertension.
3. Anemia of Chronic Kidney Disease (Hb 9.4 g/dL).

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Fasting Blood Sugar: 212 mg/dL | Postprandial: 278 mg/dL | HbA1c: 9.2%
- Serum Creatinine: 2.3 mg/dL (Elevated from 1.4) | eGFR: 34 mL/min/1.73m²
- Blood Urea Nitrogen (BUN): 52 mg/dL | Serum Potassium: 5.1 mEq/L (Borderline Hyperkalemia)
- Urine Albumin-to-Creatinine Ratio (UACR): 380 mg/g.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Inj. Insulin Glargine (Lantus) - 14 Units Subcutaneously at 10:00 PM bedtime daily.
2. Inj. Insulin Lispro (Humalog) - 6 Units Subcutaneously 15 mins before breakfast and dinner.
3. Tab. Telmisartan 40 mg - 1 tablet orally once daily after breakfast.
4. Tab. Torsemide 10 mg - 1 tablet orally once daily morning after food (Diuretic).
5. Tab. Sodium Bicarbonate 500 mg - 1 tablet orally twice daily with meals.
6. Tab. Ferrous Ascorbate 100 mg - 1 tablet orally daily after dinner.

CONTRAINDICATIONS & MEDICATION ALERTS:
- STRICTLY CONTRAINDICATED: NSAIDs (Ibuprofen, Diclofenac, Naproxen) cause acute kidney injury.
- METFORMIN CONTRAINDICATION: Metformin discontinued due to eGFR <35 lactic acidosis hazard.

DIETARY & LIFESTYLE GUIDANCE:
- Renal-diabetic diet: Low sodium (<2g/day), low potassium (avoid coconut water, citrus, raw spinach).
- Fluid restriction: Maximum 1.5 Liters per 24 hours."""
    },

    "patient_04": {
        "id": "doc_p04",
        "title": "Pulmonology: Acute Severe Bronchial Asthma Exacerbation",
        "category": "Pediatric & Pulmonary Emergency",
        "patient": {
            "name": "Aarav Joshi",
            "age": 14,
            "gender": "Male",
            "uhid": "CSH-PULM-2026-1004",
            "admission_date": "2026-10-05",
            "discharge_date": "2026-10-07"
        },
        "content": """CHILDREN'S SPECIALTY HOSPITAL - PULMONARY SUMMARY
Patient Name: Aarav Joshi | Age: 14 | Sex: Male | UHID: CSH-PULM-2026-1004
Attending Physician: Dr. Sanjay Mehra, MD

CHIEF COMPLAINTS:
Sudden shortness of breath, audible wheezing, and nocturnal dry cough triggered by seasonal pollen and dust exposure.

PRIMARY DIAGNOSIS:
1. Acute Moderate-to-Severe Exacerbation of Bronchial Asthma.
2. Allergic Rhinitis.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- SpO2: 91% on room air at triage -> Improved to 98% on treatment
- Respiratory Rate: 28 breaths/min | Heart Rate: 112 bpm
- Peak Expiratory Flow Rate (PEFR): Initial 185 L/min -> Post-bronchodilator 340 L/min.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Budesonide Inhaler (Budecort 200 mcg) - 2 puffs twice daily via spacer device (Controller).
2. Salbutamol Inhaler (Asthalin 100 mcg) - 2 puffs every 4-6 hours as needed for wheezing (Rescue).
3. Tab. Prednisolone 20 mg - 1 tablet orally once daily morning with breakfast for 5 days.
4. Tab. Montelukast 10 mg - 1 tablet orally daily at bedtime for 30 days.
5. Tab. Cetirizine 5 mg - 1 tablet orally daily at bedtime for 7 days.

CONTRAINDICATIONS & MEDICATION ALERTS:
- INHALER CAUTION: Always rinse mouth and gargle with warm water after using Budecort steroid inhaler to prevent oral thrush.
- Avoid Beta-blockers and Aspirin/NSAIDs which can trigger bronchospasm.

DIETARY & LIFESTYLE GUIDANCE:
- Keep rescue Salbutamol inhaler in school bag at all times.
- Avoid dust mites, cold drinks, incense smoke, and pet dander."""
    },

    "patient_05": {
        "id": "doc_p05",
        "title": "Orthopedics: Post-Op Right Total Knee Arthroplasty (TKA)",
        "category": "Orthopedic Joint Surgery",
        "patient": {
            "name": "Nirmala Devi",
            "age": 66,
            "gender": "Female",
            "uhid": "OJR-ORTH-2026-1005",
            "admission_date": "2026-10-01",
            "discharge_date": "2026-10-06"
        },
        "content": """ORTHOPEDIC & JOINT RECONSTRUCTION CENTER - DISCHARGE SUMMARY
Patient Name: Nirmala Devi | Age: 66 | Sex: Female | UHID: OJR-ORTH-2026-1005
Operative Surgeon: Dr. Vikramaditya Rao, MS (Ortho)

CHIEF COMPLAINTS:
End-stage right knee osteoarthritis with varus deformity; admitted for elective Total Knee Replacement.

PRIMARY DIAGNOSIS:
1. Severe Grade IV Primary Osteoarthritis of Right Knee (Post Total Knee Arthroplasty).
2. Post-Operative Venous Thromboembolism (DVT) Prophylaxis State.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Post-op Hemoglobin: 10.4 g/dL | Platelets: 260,000 /mcL
- Bilateral Lower Limb Venous Doppler: Negative for Deep Vein Thrombosis (DVT)
- Right Knee AP/Lateral Radiograph:Tricompartmental prosthesis in optimal alignment; knee flexion 90 degrees.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Rivaroxaban 10 mg - 1 tablet orally once daily with lunch for 14 days (Anticoagulant for DVT prevention).
2. Tab. Tramadol 37.5 mg + Paracetamol 325 mg - 1 tablet orally twice daily after food for pain.
3. Tab. Paracetamol 650 mg - 1 tablet orally thrice daily.
4. Tab. Pantoprazole 40 mg - 1 tablet orally once daily morning before breakfast.
5. Tab. Calcium Carbonate 500 mg + Vitamin D3 - 1 tablet daily with lunch.

CONTRAINDICATIONS & MEDICATION ALERTS:
- ANTICOAGULANT BLEEDING ALERT: Do not miss Rivaroxaban doses (prevents fatal pulmonary embolism). Avoid concurrent NSAIDs (Diclofenac/Ibuprofen) due to GI bleeding risk.

DIETARY & LIFESTYLE GUIDANCE:
- Perform hourly ankle pump exercises and quadriceps sets 3 times daily.
- Walk using 4-pod walker support; never squat or sit cross-legged on floor."""
    },

    "patient_06": {
        "id": "doc_p06",
        "title": "Geriatric Neurology: Orthostatic Hypotension & High Fall Risk",
        "category": "Geriatric Medicine",
        "patient": {
            "name": "Ananth Narayan",
            "age": 74,
            "gender": "Male",
            "uhid": "CCG-GER-2026-1006",
            "admission_date": "2026-10-06",
            "discharge_date": "2026-10-07"
        },
        "content": """CENTRAL GERIATRIC CLINIC - CONSULTATION SUMMARY
Patient Name: Ananth Narayan | Age: 74 | Sex: Male | UHID: CCG-GER-2026-1006
Attending Geriatrician: Dr. Malini Sengupta, MD

CHIEF COMPLAINTS:
Recurrent morning occipital headaches, postural dizziness upon standing up from bed, and ambulatory BP fluctuations.

PRIMARY DIAGNOSIS:
1. Stage 2 Essential Hypertension with Postural Orthostatic Hypotension.
2. Benign Prostatic Hyperplasia (BPH).
3. Age-Related Mild Cerebral Small Vessel Ischemic Disease.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Blood Pressure Sitting: 172/94 mmHg -> Standing (3 min): 138/82 mmHg (34 mmHg systolic drop)
- Heart Rate: 64 bpm | Serum Creatinine: 1.1 mg/dL | eGFR: 68 mL/min
- Serum Sodium: 140 mEq/L | Serum Potassium: 4.4 mEq/L | Timed Up-and-Go (TUG): 12.8s.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Amlodipine 5 mg - 1 tablet orally once daily morning after breakfast.
2. Tab. Telmisartan 40 mg - 1 tablet orally once daily morning after breakfast.
3. Tab. Silodosin 8 mg - 1 tablet orally once daily at bedtime after dinner.
4. Sachet Cholecalciferol 60,000 IU - once weekly with milk for 8 weeks.

CONTRAINDICATIONS & MEDICATION ALERTS:
- FALL RISK ALERT: Silodosin + Antihypertensives cause significant postural hypotension. Sit at bedside for 60 seconds before standing.
- Avoid nasal/oral decongestants (Pseudoephedrine) which spike BP and cause acute urinary retention.

DIETARY & LIFESTYLE GUIDANCE:
- Maintain daily sitting and standing BP log.
- Install grab bars and nightlights in bathroom corridor to prevent nocturnal falls."""
    },

    "patient_07": {
        "id": "doc_p07",
        "title": "Endocrinology: Graves' Disease (Hyperthyroidism) & Tachycardia",
        "category": "Endocrinology & Metabolism",
        "patient": {
            "name": "Priya Nair",
            "age": 34,
            "gender": "Female",
            "uhid": "END-THYR-2026-1007",
            "admission_date": "2026-10-02",
            "discharge_date": "2026-10-05"
        },
        "content": """METROPOLITAN ENDOCRINE CENTER - CLINICAL SUMMARY
Patient Name: Priya Nair | Age: 34 | Sex: Female | UHID: END-THYR-2026-1007
Consulting Endocrinologist: Dr. Raghavendra Iyer, MD, DM (Endocrinology)

CHIEF COMPLAINTS:
Unintentional weight loss of 7 kg over 2 months despite increased appetite, resting palpitations, heat intolerance, fine hand tremors, and anxiety.

PRIMARY DIAGNOSIS:
1. Primary Hyperthyroidism secondary to Graves' Disease.
2. Thyrotoxic Sinus Tachycardia.
3. Mild Graves' Ophthalmopathy.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Serum TSH: <0.01 mIU/L (Markedly suppressed, Ref: 0.4-4.5)
- Free T4 (fT4): 3.8 ng/dL (Elevated, Ref: 0.8-1.8) | Free T3 (fT3): 11.2 pg/mL (Elevated)
- TSH Receptor Antibodies (TRAb): Strongly Positive (8.4 IU/L)
- Resting Heart Rate: 116 bpm | Blood Pressure: 134/76 mmHg
- Complete Blood Count: WBC 6,800 /mcL, Absolute Neutrophil Count (ANC) 4,100 /mcL (Normal baseline)
- Liver Function Test: AST 28 U/L, ALT 31 U/L (Normal).

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Carbimazole (Neo-Mercazole) 10 mg - 2 tablets (20 mg) orally twice daily after meals (Antithyroid drug).
2. Tab. Propranolol 40 mg - 1 tablet orally twice daily morning and evening (Beta-blocker for tachycardia and tremors).
3. Carboxymethylcellulose 0.5% Eye Drops - 2 drops in both eyes 4 times daily (Lubricating drops for ophthalmopathy).
4. Tab. Calcium + Vitamin D3 - 1 tablet daily after lunch (Prevents thyrotoxic bone loss).

CONTRAINDICATIONS & MEDICATION ALERTS:
- AGRANULOCYTOSIS WARNING (CRITICAL): Carbimazole can rarely cause severe drop in white blood cells (agranulocytosis). Stop Carbimazole IMMEDIATELY and check CBC if you develop fever, sore throat, or mouth ulcers.
- HEPATOTOXICITY ALERT: Monitor liver enzymes; report yellowing of eyes or dark urine.
- Do not stop Propranolol abruptly as it may trigger rebound tachycardia or thyroid storm.

DIETARY & LIFESTYLE GUIDANCE:
- Avoid iodinated contrast dyes, kelp, seaweed, and excess iodine supplements.
- Strictly avoid caffeine, energy drinks, and smoking (smoking worsens Graves' eye disease).
- Wear UV-protective sunglasses outdoors and elevate head of bed at night."""
    },

    "patient_08": {
        "id": "doc_p08",
        "title": "Gastroenterology: Bleeding Peptic Ulcer & H. pylori Eradication",
        "category": "Gastroenterology & Hepatology",
        "patient": {
            "name": "Vikramaditya Singh",
            "age": 45,
            "gender": "Male",
            "uhid": "GAS-ULC-2026-1008",
            "admission_date": "2026-09-29",
            "discharge_date": "2026-10-03"
        },
        "content": """INSTITUTE OF GASTROENTEROLOGY - DISCHARGE RECORD
Patient Name: Vikramaditya Singh | Age: 45 | Sex: Male | UHID: GAS-ULC-2026-1008
Attending Gastroenterologist: Dr. Nikhil Chawla, MD, DM (Gastro)

CHIEF COMPLAINTS:
Burning epigastric pain for 4 weeks, worsened after taking over-the-counter Diclofenac for backache, followed by 2 episodes of dark coffee-ground emesis and melena (black tarry stools).

PRIMARY DIAGNOSIS:
1. Acute Duodenal Ulcer (Forrest Class IIb) with Resolved Upper Gastrointestinal Bleed.
2. Helicobacter pylori (H. pylori) Infection (RUT Positive).
3. NSAID-Induced Erosions & Mild Post-Hemorrhagic Anemia.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Upper GI Endoscopy (EGD): 1.2 cm clean-based ulcer in first part of duodenum (D1) with adherent clot treated via endoscopic hemoclip; antral gastritis.
- Rapid Urease Test (RUT): Positive for H. pylori.
- Hemoglobin: 10.6 g/dL (Stabilized from 9.8 g/dL) | Urea: 34 mg/dL | Creatinine: 0.9 mg/dL.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Esomeprazole 40 mg - 1 tablet orally twice daily 30 minutes before breakfast and dinner for 14 days, then once daily for 6 weeks (Proton Pump Inhibitor).
2. Tab. Clarithromycin 500 mg - 1 tablet orally twice daily with meals for 14 days (Antibiotic).
3. Cap. Amoxicillin 1000 mg - 1 capsule orally twice daily with meals for 14 days (Antibiotic).
4. Syp. Sucralfate 10 mL - orally four times daily 1 hour before meals and at bedtime (Mucosal cytoprotective).

CONTRAINDICATIONS & MEDICATION ALERTS:
- ABSOLUTE CONTRAINDICATION: Strictly avoid all NSAIDs (Diclofenac, Ibuprofen, Aspirin, Naproxen, Piroxicam). Will cause life-threatening recurrent ulcer perforation or bleeding.
- Complete the full 14-day H. pylori triple therapy antibiotic course to prevent bacterial resistance.

DIETARY & LIFESTYLE GUIDANCE:
- Bland, soft, non-spicy diet; avoid chili, black pepper, citrus juices, vinegar, and deep-fried foods.
- Complete abstinence from alcohol, tobacco smoking, and strong coffee.
- Emergency Signs: Vomiting blood, black tarry stools, or sudden severe abdominal rigidity."""
    },

    "patient_09": {
        "id": "doc_p09",
        "title": "Cardiology: Non-Valvular Atrial Fibrillation & Apixaban Therapy",
        "category": "Cardiac Electrophysiology",
        "patient": {
            "name": "Meera Patel",
            "age": 62,
            "gender": "Female",
            "uhid": "CAR-AFIB-2026-1009",
            "admission_date": "2026-10-01",
            "discharge_date": "2026-10-04"
        },
        "content": """HEART RHYTHM & ELECTROPHYSIOLOGY CENTER
Patient Name: Meera Patel | Age: 62 | Sex: Female | UHID: CAR-AFIB-2026-1009
Attending Electrophysiologist: Dr. R. Patel, MD, DM

CHIEF COMPLAINTS:
Episodic fluttering palpitations in chest, mild exertional breathlessness, and easy fatigability over past 10 days.

PRIMARY DIAGNOSIS:
1. Paroxysmal Non-Valvular Atrial Fibrillation (CHA2DS2-VASc Score: 3 - High Stroke Risk).
2. Essential Hypertension.
3. Mild Left Atrial Enlargement.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- 12-Lead ECG: Irregularly irregular rhythm with absent P waves, ventricular rate 114 bpm -> Controlled to 74 bpm.
- 2D Echocardiogram: LVEF 58%, Left Atrium 4.2 cm, no valvular stenosis or intracardiac thrombus.
- Serum TSH: 2.1 mIU/L (Normal) | Serum Creatinine: 0.85 mg/dL | eGFR: 81 mL/min.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Apixaban (Eliquis) 5 mg - 1 tablet orally twice daily (Every 12 hours, Morning and Night) (Direct Oral Anticoagulant for stroke prevention).
2. Tab. Bisoprolol 5 mg - 1 tablet orally once daily morning (Beta-blocker for ventricular rate control).
3. Tab. Telmisartan 40 mg - 1 tablet orally once daily morning (BP control).
4. Tab. Rosuvastatin 10 mg - 1 tablet orally daily at bedtime.

CONTRAINDICATIONS & MEDICATION ALERTS:
- STROKE PREVENTION ALERT: Do not skip Apixaban doses. Skipping anticoagulation sharply increases risk of cardioembolic ischemic stroke.
- BLEEDING RISK: Avoid NSAIDs, Aspirin, or herbal blood thinners (Ginkgo, high-dose fish oil) while taking Apixaban.

DIETARY & LIFESTYLE GUIDANCE:
- Avoid triggers of atrial fibrillation: Alcohol ("holiday heart"), excess caffeine, energy drinks, and sleep deprivation.
- Use a soft-bristle toothbrush and electric razor to minimize gum or skin bleeding."""
    },

    "patient_10": {
        "id": "doc_p10",
        "title": "Neurology: Chronic Migraine with Visual Aura & Prophylaxis",
        "category": "Clinical Neurology",
        "patient": {
            "name": "Rohan Deshmukh",
            "age": 29,
            "gender": "Male",
            "uhid": "NEU-MIG-2026-1010",
            "admission_date": "2026-10-05",
            "discharge_date": "2026-10-06"
        },
        "content": """METROPOLITAN NEUROLOGY & HEADACHE CLINIC
Patient Name: Rohan Deshmukh | Age: 29 | Sex: Male | UHID: NEU-MIG-2026-1010
Consulting Neurologist: Dr. Ananya Bose, MD, DM (Neurology)

CHIEF COMPLAINTS:
Severe unilateral throbbing right-sided headaches occurring 10-12 days per month, preceded by 20 minutes of zigzag flickering visual scotoma (aura), photophobia, phonophobia, and nausea.

PRIMARY DIAGNOSIS:
1. Chronic Migraine with Visual Aura.
2. Risk of Medication-Overuse (Rebound) Headache.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- MRI Brain with MR Angiography (MRA): Normal brain parenchyma and intracranial vessels; no space-occupying lesion or aneurysm.
- Blood Pressure: 118/76 mmHg | Heart Rate: 70 bpm
- Fundoscopy: Normal optic discs, no papilledema.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Sumatriptan 50 mg - 1 tablet orally at very onset of migraine headache (Maximum 2 tablets in 24 hours, max 8 days/month) (Abortive Triptan).
2. Tab. Naproxen 500 mg + Domperidone 10 mg - 1 tablet orally with Sumatriptan for acute attack nausea and pain.
3. Tab. Topiramate 25 mg - 1 tablet orally daily at bedtime for 2 weeks, then increase as directed (Daily migraine prophylaxis).
4. Tab. Riboflavin (Vitamin B2) 400 mg + Magnesium Oxide 400 mg - 1 tablet daily with lunch.

CONTRAINDICATIONS & MEDICATION ALERTS:
- MEDICATION OVERUSE WARNING: Do NOT take Sumatriptan or painkillers more than 2 days per week (8 days/month), as frequent use causes chronic daily rebound headaches.
- SEROTONIN SYNDROME & VASOSPASM ALERT: Never combine Sumatriptan with Ergotamines or SSRI/SNRI antidepressants without neurologist clearance.
- Topiramate requires high fluid intake (2.5 Liters/day) to prevent kidney stones (nephrolithiasis).

DIETARY & LIFESTYLE GUIDANCE:
- Maintain a daily Headache Trigger Diary.
- Avoid classic dietary triggers: Aged cheese, dark chocolate, MSG, processed meats (nitrates), red wine, and skipping meals (fasting).
- Maintain strict sleep-wake schedule (7-8 hours nightly) and limit screen glare."""
    },

    "patient_11": {
        "id": "doc_p11",
        "title": "Rheumatology: Seropositive Rheumatoid Arthritis on Methotrexate",
        "category": "Rheumatology & Immunology",
        "patient": {
            "name": "Lakshmi Subramanian",
            "age": 52,
            "gender": "Female",
            "uhid": "RHE-RA-2026-1011",
            "admission_date": "2026-10-03",
            "discharge_date": "2026-10-05"
        },
        "content": """CENTER FOR RHEUMATOLOGY & AUTOIMMUNE DISEASES
Patient Name: Lakshmi Subramanian | Age: 52 | Sex: Female | UHID: RHE-RA-2026-1011
Consulting Rheumatologist: Dr. Karthikeya Murthy, MD, DM (Rheumatology)

CHIEF COMPLAINTS:
Symmetric swelling, tenderness, and morning stiffness (>90 minutes) in bilateral wrist, metacarpophalangeal (MCP), and proximal interphalangeal (PIP) hand joints for 4 months.

PRIMARY DIAGNOSIS:
1. Active Seropositive Rheumatoid Arthritis (DAS28-ESR Score: 5.1 - Moderate-to-High Disease Activity).
2. Secondary Vitamin D Insufficiency.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Anti-CCP Antibodies: Strongly Positive (210 U/mL, Ref: <20) | Rheumatoid Factor (RF): Positive (96 IU/mL)
- Erythrocyte Sedimentation Rate (ESR): 58 mm/hr (Elevated) | C-Reactive Protein (CRP): 24 mg/L (Elevated)
- CBC: Hb 11.4 g/dL, WBC 7,400, Platelets 310,000 | ALT: 22 U/L | Creatinine: 0.8 mg/dL
- Chest X-Ray & Mantoux/IGRA: Negative for latent tuberculosis; HBsAg/Anti-HCV Negative.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Methotrexate (Folitrax) 15 mg - Take ONCE WEEKLY ONLY on SUNDAYS after breakfast (DMARD anchor therapy).
2. Tab. Folic Acid 5 mg - Take ONCE WEEKLY on TUESDAYS (48 hours after Methotrexate) to prevent mucosal and hematologic side effects.
3. Tab. Hydroxychloroquine (HCQS) 200 mg - 1 tablet orally once daily with dinner.
4. Tab. Deflazacort 6 mg - 1 tablet orally once daily morning after breakfast for 4 weeks (Bridging low-dose steroid).
5. Tab. Calcium + Vitamin D3 - 1 tablet daily after lunch.

CONTRAINDICATIONS & MEDICATION ALERTS:
- CRITICAL BLACK-BOX DOSING ALERT: Methotrexate MUST BE TAKEN ONCE A WEEK ONLY (Sundays), NEVER DAILY! Accidental daily intake causes fatal bone marrow suppression and liver toxicity.
- CONTRAINDICATION: Strictly avoid Trimethoprim-Sulfamethoxazole (Bactrim/Septran) antibiotic while on Methotrexate due to severe pancytopenia interaction.
- Complete alcohol abstinence required to prevent Methotrexate hepatotoxicity.

DIETARY & LIFESTYLE GUIDANCE:
- Perform warm water hand-soaks in the morning followed by gentle range-of-motion finger exercises.
- Anti-inflammatory diet rich in omega-3 fatty acids (walnuts, flaxseeds, fish) and leafy greens.
- Re-check CBC, Liver Function (AST/ALT), and Creatinine every 6 weeks."""
    },

    "patient_12": {
        "id": "doc_p12",
        "title": "Hepatology: Decompensated Cirrhosis / NASH & Ascites Management",
        "category": "Hepatology & Liver Care",
        "patient": {
            "name": "Kabir Khan",
            "age": 48,
            "gender": "Male",
            "uhid": "HEP-CIR-2026-1012",
            "admission_date": "2026-09-27",
            "discharge_date": "2026-10-03"
        },
        "content": """LIVER & DIGESTIVE DISEASES INSTITUTE - DISCHARGE SUMMARY
Patient Name: Kabir Khan | Age: 48 | Sex: Male | UHID: HEP-CIR-2026-1012
Consulting Hepatologist: Dr. Farhan Qureshi, MD, DM (Hepatology)

CHIEF COMPLAINTS:
Progressive abdominal distension (ascites) over 2 weeks, mild ankle swelling, daytime sleepiness, and history of metabolic syndrome / fatty liver disease.

PRIMARY DIAGNOSIS:
1. Non-Alcoholic Steatohepatitis (NASH)-Related Liver Cirrhosis (Child-Pugh Class B).
2. Portal Hypertension with Moderate Ascites & Grade I Esophageal Varices (Non-bleeding).
3. Early Minimal Hepatic Encephalopathy.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Total Bilirubin: 2.4 mg/dL | Direct Bilirubin: 1.3 mg/dL
- Serum Albumin: 2.9 g/dL (Low, Ref: 3.5-5.0) | INR: 1.45
- AST: 68 U/L | ALT: 54 U/L | Alkaline Phosphatase: 132 U/L
- Serum Sodium: 133 mEq/L | Serum Potassium: 4.3 mEq/L | Creatinine: 1.0 mg/dL
- Ultrasound Abdomen & FibroScan: Nodular liver contour, splenomegaly (14.5 cm), moderate free fluid; Liver Stiffness 24.5 kPa.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Spironolactone (Aldactone) 100 mg - 1 tablet orally once daily morning after breakfast (Aldosterone antagonist for ascites).
2. Tab. Furosemide (Lasix) 40 mg - 1 tablet orally once daily morning after breakfast (Maintain 100:40 ratio with Spironolactone).
3. Syp. Lactulose (Duphalac) 20 mL - orally twice to thrice daily, titrated to achieve 2-3 soft bowel movements per day (Clears gut ammonia to prevent hepatic encephalopathy).
4. Tab. Rifaximin 550 mg - 1 tablet orally twice daily after meals (Reduces ammonia-producing gut flora).
5. Tab. Carvedilol 3.125 mg - 1 tablet orally twice daily (Non-selective beta-blocker for portal hypertension / variceal prophylaxis).

CONTRAINDICATIONS & MEDICATION ALERTS:
- STRICT CONTRAINDICATION: Avoid all NSAIDs ( precipitate hepatorenal syndrome and variceal bleeding), sedatives/benzodiazepines (Alprazolam/Zolpidem precipitate hepatic coma), and high-dose Paracetamol (>2g/day).
- Do NOT allow constipation: If fewer than 2 bowel movements occur in a day, increase Lactulose dose to prevent ammonia build-up and confusion.

DIETARY & LIFESTYLE GUIDANCE:
- Strict No-Added-Salt Diet (<2g sodium/day) to prevent fluid re-accumulation in abdomen.
- High-protein vegetarian/dairy/fish diet (1.2g/kg/day) with a mandatory late-night complex carbohydrate snack (prevents muscle catabolism).
- Weigh yourself every morning before breakfast; report weight gain >2 kg in 3 days."""
    },

    "patient_13": {
        "id": "doc_p13",
        "title": "Obstetrics: Gestational Diabetes Mellitus (GDM) & Maternal Anemia",
        "category": "Obstetrics & Maternal-Fetal Care",
        "patient": {
            "name": "Sneha Reddy",
            "age": 27,
            "gender": "Female",
            "uhid": "OBS-GDM-2026-1013",
            "admission_date": "2026-10-04",
            "discharge_date": "2026-10-06"
        },
        "content": """MATERNAL & FETAL MEDICINE CENTER - ANTENATAL SUMMARY
Patient Name: Sneha Reddy | Age: 27 | Sex: Female | UHID: OBS-GDM-2026-1013
Consulting Obstetrician: Dr. Vasundhara Rao, MD, FRCOG

CHIEF COMPLAINTS:
Primigravida at 28 weeks gestation presenting for evaluation of abnormal 75g Oral Glucose Tolerance Test (OGTT) and mild maternal fatigue. Normal fetal movements perceived.

PRIMARY DIAGNOSIS:
1. Primigravida at 28 Weeks Gestation with Gestational Diabetes Mellitus (GDM).
2. Moderate Maternal Iron-Deficiency Anemia in Pregnancy.
3. Single Live Intrauterine Fetus in Cephalic Presentation.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- 75g OGTT Results: Fasting: 106 mg/dL (Target <95) | 1-Hour: 194 mg/dL (Target <180) | 2-Hour: 162 mg/dL (Target <153)
- HbA1c: 6.1% | Hemoglobin: 9.8 g/dL | Serum Ferritin: 14 ng/mL (Low)
- Blood Pressure: 114/72 mmHg | Urine Dipstick: Protein Negative, Ketones Negative
- Obstetric Ultrasound & Biometry: Fetal weight 1,180g (65th percentile), Amniotic Fluid Index (AFI) 13 cm, Normal Umbilical Artery Doppler.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Inj. Regular Human Insulin (Actrapid) - 4 Units Subcutaneously 20 minutes before breakfast and 4 Units before dinner (Titrate per glucometer log).
2. Tab. Metformin 500 mg SR - 1 tablet orally with lunch.
3. Tab. Ferrous Bisglycinate 100 mg + Folic Acid - 1 tablet orally twice daily with orange/lemon water (Do not take at the same time as calcium).
4. Tab. Calcium Citrate Malate 500 mg + Vitamin D3 - 1 tablet orally daily after lunch (Keep 2-hour gap from iron tablet).

CONTRAINDICATIONS & MEDICATION ALERTS:
- PREGNANCY TERATOGENICITY ALERT: Strictly avoid ACE inhibitors, ARBs, Statins, Tetracyclines, Fluoroquinolones, and NSAIDs during pregnancy.
- IRON-CALCIUM INTERACTION: Never take Iron and Calcium tablets together at the same meal, as calcium blocks intestinal iron absorption by 50%.

DIETARY & LIFESTYLE GUIDANCE:
- Medical Nutrition Therapy (MNT): Split meals into 3 moderate meals + 3 small protein snacks to prevent post-meal glucose spikes.
- Perform 4-point home glucometer monitoring (Fasting, and 2 hours post-breakfast, lunch, dinner). Targets: Fasting <95 mg/dL, 2-hr Post-meal <120 mg/dL.
- Daily Fetal Kick Count: Ensure at least 10 fetal kicks within a 2-hour period after meals; walk 15 minutes after each main meal."""
    },

    "patient_14": {
        "id": "doc_p14",
        "title": "Pulmonology: GOLD Stage III COPD & Chronic Bronchitis",
        "category": "Thoracic & Pulmonary Medicine",
        "patient": {
            "name": "Suresh Babu",
            "age": 67,
            "gender": "Male",
            "uhid": "PUL-COPD-2026-1014",
            "admission_date": "2026-09-30",
            "discharge_date": "2026-10-05"
        },
        "content": """CHEST & THORACIC MEDICINE INSTITUTE - DISCHARGE SUMMARY
Patient Name: Suresh Babu | Age: 67 | Sex: Male | UHID: PUL-COPD-2026-1014
Attending Pulmonologist: Dr. Gautam Chatterjee, MD, DM (Pulmonary Medicine)

CHIEF COMPLAINTS:
Worsening exertional breathlessness (mMRC Grade 3), productive cough with mucopurulent sputum for 5 days, and wheezing. Former 30-pack-year smoker.

PRIMARY DIAGNOSIS:
1. Chronic Obstructive Pulmonary Disease (COPD - GOLD Stage III, Group E) with Acute Infective Exacerbation.
2. Mild Secondary Pulmonary Arterial Hypertension.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Spirometry (Post-Bronchodilator): FEV1/FVC Ratio: 0.54 | FEV1: 44% Predicted (Severe airflow limitation)
- Arterial Blood Gas (ABG): pH 7.38, pCO2 46 mmHg, pO2 68 mmHg, SpO2 93% on room air (Target SpO2: 88-92%)
- Chest X-Ray: Bilateral hyperinflated lung fields, flattened diaphragms, no lobar consolidation.
- WBC: 11,800 /mcL | CRP: 18 mg/L | Serum Electrolytes & Renal Function: Normal.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tiotropium 18 mcg + Formoterol 12 mcg Inhaler (Duova) - 2 puffs once daily every morning via spacer (LAMA + LABA Dual Bronchodilator).
2. Levosalbutamol + Ipratropium Nebulization / Inhaler (Duolin) - 2 puffs every 6 hours as needed for acute dyspnea.
3. Tab. Azithromycin 500 mg - 1 tablet orally once daily for 3 more days (Completing 5-day course).
4. Tab. Acebrophylline 100 mg SR - 1 tablet orally twice daily after meals (Mucolytic & bronchodilator).
5. Tab. N-Acetylcysteine 600 mg Effervescent - 1 tablet dissolved in half glass water twice daily (Sputum clearance).

CONTRAINDICATIONS & MEDICATION ALERTS:
- OXYGEN TARGET ALERT: In chronic COPD (CO2 retainer risk), titrate supplemental oxygen to maintain SpO2 strictly between 88% and 92%. Excessive high-flow oxygen can depress respiratory drive and cause CO2 narcosis.
- CONTRAINDICATION: Avoid non-selective Beta-blockers (Propranolol) and sedating antihistamines/cough suppressants (Codeine).

DIETARY & LIFESTYLE GUIDANCE:
- Practice Pursed-Lip Breathing and diaphragmatic breathing exercises 3 times daily.
- Annual Influenza vaccine and Pneumococcal vaccination (PCV20) recommended.
- Complete avoidance of tobacco smoke, biomass fuel fumes, and cold winter smog."""
    },

    "patient_15": {
        "id": "doc_p15",
        "title": "Infectious Disease: Community-Acquired Pneumonia & Penicillin Allergy",
        "category": "Internal Medicine & Infectious Disease",
        "patient": {
            "name": "Kavita Krishnan",
            "age": 41,
            "gender": "Female",
            "uhid": "INF-CAP-2026-1015",
            "admission_date": "2026-10-02",
            "discharge_date": "2026-10-06"
        },
        "content": """METROPOLITAN INFECTIOUS DISEASE & INTERNAL MEDICINE UNIT
Patient Name: Kavita Krishnan | Age: 41 | Sex: Female | UHID: INF-CAP-2026-1015
Attending Physician: Dr.Siddharth Menon, MD (Internal Medicine)

CHIEF COMPLAINTS:
High-grade fever (102.8°F) with chills and rigors, right-sided pleuritic chest pain on deep inspiration, and rust-colored productive cough for 4 days.

PRIMARY DIAGNOSIS:
1. Right Lower Lobe Community-Acquired Pneumonia (CAP - CURB-65 Score: 1).
2. Documented Severe IgE-Mediated Penicillin / Amoxicillin Anaphylaxis Allergy.

CLINICAL INVESTIGATIONS & LAB RESULTS:
- Chest X-Ray PA View: Homogeneous air-space consolidation in right lower lobe with air bronchograms; no pleural effusion.
- Temperature: 98.6°F at discharge (Afebrile for 48 hours) | SpO2: 97% on room air | BP: 120/78 mmHg
- Total Leukocyte Count (WBC): 15,600 /mcL at admission -> Down to 8,900 /mcL
- Serum Procalcitonin: 1.8 ng/mL -> Down to 0.25 ng/mL | CRP: 64 mg/L -> 14 mg/L
- Sputum Gram Stain & Culture: Streptococcus pneumoniae sensitive to respiratory fluoroquinolones and macrolides.

DISCHARGE MEDICATIONS & PRESCRIPTION:
1. Tab. Levofloxacin 750 mg - 1 tablet orally once daily morning for 5 more days (Respiratory Fluoroquinolone chosen due to severe Penicillin allergy).
2. Tab. Ambroxol 30 mg + Guaifenesin - 1 tablet orally thrice daily after food (Expectorant).
3. Tab. Paracetamol 650 mg - 1 tablet orally every 6-8 hours as needed for fever or pleuritic chest ache.
4. Cap. Saccharomyces boulardii + Lactic Acid Bacillus Probiotic - 1 capsule twice daily (Prevents antibiotic-associated diarrhea).

CONTRAINDICATIONS & MEDICATION ALERTS:
- SEVERE ALLERGY CONTRAINDICATION (CRITICAL): Patient has documented ANAPHYLAXIS to Penicillins (Amoxicillin, Augmentin, Piperacillin, Ampicillin) and Cephalosporins. NEVER administer Beta-lactam antibiotics!
- FLUOROQUINOLONE INTERACTION & CAUTION: Take Levofloxacin at least 2 hours apart from antacids, iron, calcium, or multivitamins (divalent cations block Levofloxacin absorption). Stop immediately if Achilles tendon pain/swelling occurs.

DIETARY & LIFESTYLE GUIDANCE:
- Drink 2.5 to 3.0 Liters of warm fluids, soups, and oral rehydration daily to thin bronchial secretions.
- Use Incentive Spirometer 10 breaths every 2 hours while awake to expand right lower lung lobe and prevent atelectasis.
- Repeat Chest X-Ray in 6 weeks to confirm complete radiological resolution of consolidation."""
    }
}
