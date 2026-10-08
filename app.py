"""
DoctorInsight - Medical Document Analysis System
FastAPI Backend & Application Service Layer
"""

import os
import uuid
import time
import json
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sample_data import SAMPLE_DOCUMENTS
from rag_pipeline import (
    index_document,
    generate_doctorinsight_analysis,
    extract_rule_based_clinical_insights,
    query_rag_engine,
    vector_db,
    extract_text_from_pdf,
    preprocess_text
)

app = FastAPI(
    title="DoctorInsight API",
    description="Medical Document Analysis System",
    version="1.0.0"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Medical records directory
RECORDS_DIR = os.path.join(os.path.dirname(__file__), "medical_records")
os.makedirs(RECORDS_DIR, exist_ok=True)
app.mount("/medical_records", StaticFiles(directory=RECORDS_DIR), name="medical_records")

# Persistent storage file
DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), "data_store.json")

# In-memory document storage
DOCUMENTS_STORE: Dict[str, Dict[str, Any]] = {}
ANALYSIS_CACHE: Dict[str, Dict[str, Any]] = {}
USER_ACCOUNTS: Dict[str, Dict[str, Any]] = {}

def save_persistent_store():
    """Saves user accounts and custom patient records to disk."""
    try:
        custom_docs = {
            k: v for k, v in DOCUMENTS_STORE.items()
            if v.get("source") != "Sample Record"
        }
        payload = {
            "user_accounts": USER_ACCOUNTS,
            "custom_documents": custom_docs,
            "updated_at": time.time()
        }
        with open(DATA_STORE_FILE, "w", encoding="utf-8") as fp:
            json.dump(payload, fp, indent=2)
    except Exception as e:
        print(f"[DoctorInsight] Persistence warning: {e}")

def load_persistent_store():
    """Loads saved user accounts and custom patient records from disk."""
    if os.path.exists(DATA_STORE_FILE):
        try:
            with open(DATA_STORE_FILE, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                for email, acc in data.get("user_accounts", {}).items():
                    USER_ACCOUNTS[email] = acc
                for doc_id, doc in data.get("custom_documents", {}).items():
                    DOCUMENTS_STORE[doc_id] = doc
        except Exception as e:
            print(f"[DoctorInsight] Load store warning: {e}")

# Seed 15 preloaded patient documents into store
for doc_key, doc_info in SAMPLE_DOCUMENTS.items():
    d_id = doc_info["id"]
    p_name_slug = doc_info["patient"]["name"].lower().replace(" ", "_")
    base_file = f"{d_id}_{p_name_slug}"
    DOCUMENTS_STORE[d_id] = {
        "id": d_id,
        "title": doc_info["title"],
        "category": doc_info["category"],
        "patient": doc_info["patient"],
        "content": doc_info["content"],
        "source": f"{base_file}.pdf",
        "pdf_url": f"/medical_records/{base_file}.pdf",
        "txt_url": f"/medical_records/{base_file}.txt",
        "created_at": time.time(),
        "chunks_indexed": False
    }

# Load any custom added patients and user accounts from disk
load_persistent_store()


# ==========================================
# Pydantic Schemas
# ==========================================

class GoogleAuthRequest(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None
    sub: Optional[str] = None
    phone: Optional[str] = None
    otp: Optional[str] = None
    role: Optional[str] = None

class EmailAuthRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = "User"
    phone: Optional[str] = None
    otp: Optional[str] = None
    role: Optional[str] = "PATIENT"

class SendOtpRequest(BaseModel):
    name: str
    phone: str
    role: str = "PATIENT"  # PATIENT or GUEST
    email: Optional[str] = None

class VerifyOtpRequest(BaseModel):
    name: str
    phone: str
    otp: str
    role: str = "PATIENT"  # PATIENT or GUEST
    email: Optional[str] = None

class TextUploadRequest(BaseModel):
    title: Optional[str] = "Clinical Record Note"
    patient_name: Optional[str] = "Patient Record"
    patient_age: Optional[int] = 45
    patient_gender: Optional[str] = "Unspecified"
    content: str

class AnalyzeRequest(BaseModel):
    document_id: str
    api_key: Optional[str] = None

class QueryRequest(BaseModel):
    document_id: str
    query: str
    api_key: Optional[str] = None


# In-memory OTP store: phone_digits -> {otp, name, role, phone_formatted, email, expires_at, verified}
OTP_STORE: Dict[str, Dict[str, Any]] = {}


def is_puneeth_admin(name: Optional[str], email: Optional[str]) -> bool:
    """Strictly checks whether the user is Puneeth K.V.N. (the sole Admin)."""
    n = (name or "").strip().lower().replace(".", "").replace(" ", "")
    e = (email or "").strip().lower()
    return n in ("puneethkvn", "puneeth") or e == "puneeth.kvn@gmail.com"


def normalize_phone(phone_raw: str) -> str:
    """Extracts digits from phone number and validates length (10-15 digits)."""
    digits = "".join(ch for ch in (phone_raw or "") if ch.isdigit())
    if len(digits) == 10:
        return "+91" + digits
    if 10 < len(digits) <= 15:
        return "+" + digits
    return ""


# ==========================================
# Root & Health Endpoints
# ==========================================

@app.get("/")
@app.get("/login")
@app.get("/dashboard")
@app.get("/patients")
@app.get("/documents")
@app.get("/analysis")
@app.get("/medications")
@app.get("/www.doctorinsight.com")
@app.get("/www.doctorinsight.com/dashboard")
@app.get("/www.doctorinsight.com/login")
def serve_app():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "DoctorInsight API Running."}


@app.get("/api/network-info")
def get_network_info():
    """Returns live public internet tunnel URL, custom domain links, and LAN access URLs."""
    import socket
    lan_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    public_tunnel_url = ""
    pub_file = os.path.join(os.path.dirname(__file__), "public_url.txt")
    if os.path.exists(pub_file):
        try:
            with open(pub_file, "r", encoding="utf-8") as fp:
                public_tunnel_url = fp.read().strip()
        except Exception:
            pass

    return {
        "brand_domain": "www.doctorinsight.com",
        "custom_domain_local": "http://www.doctorinsight.127.0.0.1.sslip.io/dashboard",
        "custom_domain_lan": f"http://www.doctorinsight.{lan_ip}.sslip.io/dashboard",
        "custom_route_url": "http://localhost:5173/www.doctorinsight.com",
        "lan_url": f"http://{lan_ip}:5173/dashboard",
        "public_tunnel_url": public_tunnel_url,
        "localhost_url": "http://localhost:5173/dashboard"
    }


@app.get("/api/health")
def health_check():
    """System health check."""
    return {
        "status": "online",
        "application": "DoctorInsight",
        "version": "1.0.0",
        "active_documents": len(DOCUMENTS_STORE),
        "registered_accounts": len(USER_ACCOUNTS),
        "timestamp": time.time()
    }


# ==========================================
# Authentication: Sole Admin (Puneeth K.V.N.) + Phone OTP for Guest/Patient
# ==========================================

@app.post("/api/auth/send-otp")
def send_phone_otp(payload: SendOtpRequest):
    """Generates and dispatches a 6-digit OTP bound to the user's phone number for Guest or Patient sign-in."""
    import random
    clean_phone = normalize_phone(payload.phone)
    if not clean_phone:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid 10-digit mobile phone number (e.g. 9876543210 or +91 9876543210)."
        )

    name = (payload.name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Please enter your full name.")

    role = (payload.role or "PATIENT").strip().upper()
    if role not in ("PATIENT", "GUEST"):
        role = "PATIENT"

    otp_code = f"{random.randint(100000, 999999)}"
    OTP_STORE[clean_phone] = {
        "otp": otp_code,
        "name": name,
        "phone": clean_phone,
        "role": role,
        "email": (payload.email or f"{clean_phone.replace('+', '')}@otp.patient.in").strip().lower(),
        "created_at": time.time(),
        "expires_at": time.time() + 300,  # 5 minutes validity
        "verified": False
    }

    return {
        "success": True,
        "phone": clean_phone,
        "role": role,
        "otp_code": otp_code,
        "expires_in_seconds": 300,
        "message": f"OTP sent to {clean_phone} for {role} verification.",
        "sms_preview": f"[DoctorInsight SMS to {clean_phone}] Hello {name}, your {role} verification OTP is {otp_code}. Valid for 5 minutes."
    }


@app.post("/api/auth/verify-otp")
def verify_phone_otp(payload: VerifyOtpRequest):
    """Verifies the 6-digit OTP connected to the phone number and signs the user in as Guest or Patient."""
    clean_phone = normalize_phone(payload.phone)
    if not clean_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format.")

    record = OTP_STORE.get(clean_phone)
    if not record:
        raise HTTPException(
            status_code=401,
            detail="No OTP was requested for this phone number. Please click 'Get OTP' first."
        )

    if time.time() > record["expires_at"]:
        raise HTTPException(
            status_code=401,
            detail="This OTP has expired. Please request a new OTP for your phone number."
        )

    entered_otp = (payload.otp or "").strip()
    if entered_otp != record["otp"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid OTP code! Only users who receive and enter the correct OTP for their phone number can sign in as Guest or Patient."
        )

    record["verified"] = True
    name = (payload.name or record["name"] or "Verified User").strip()
    email = (payload.email or record["email"] or f"{clean_phone.replace('+', '')}@otp.user").strip().lower()

    # Enforce strict rule: Only Puneeth K.V.N. can ever be ADMIN; all OTP sign-ins are PATIENT or GUEST
    requested_role = (payload.role or record["role"] or "PATIENT").strip().upper()
    if requested_role not in ("PATIENT", "GUEST"):
        requested_role = "PATIENT"
    final_role = "ADMIN" if is_puneeth_admin(name, email) else requested_role

    user_id = f"otp_{clean_phone.replace('+', '')}"
    account = {
        "id": user_id,
        "name": name,
        "email": email,
        "phone": clean_phone,
        "role": final_role,
        "otp_verified": True,
        "avatar_initial": name[0].upper(),
        "auth_provider": "phone_otp",
        "created_at": time.time(),
        "last_login": time.time()
    }
    USER_ACCOUNTS[clean_phone] = account
    save_persistent_store()

    return {
        "success": True,
        "token": f"token_{user_id}_{int(time.time())}",
        "user": account,
        "message": f"Phone {clean_phone} OTP verified! Signed in as {final_role} ({name})."
    }


@app.post("/api/auth/google")
def google_auth(payload: GoogleAuthRequest):
    """Logs in Admin (Puneeth K.V.N. ONLY). All other users must verify Phone + OTP as Guest or Patient."""
    email = payload.email.lower().strip()
    name = (payload.name or "").strip()
    if not email:
        raise HTTPException(status_code=400, detail="Invalid email address.")

    if not is_puneeth_admin(name, email):
        # Non-admin users MUST have a verified phone + OTP to sign in as Guest or Patient
        clean_phone = normalize_phone(payload.phone or "")
        otp_record = OTP_STORE.get(clean_phone) if clean_phone else None
        if not otp_record or not payload.otp or payload.otp.strip() != otp_record.get("otp"):
            raise HTTPException(
                status_code=403,
                detail="Only Puneeth K.V.N. is Admin. Guests and Patients must enter their Phone Number and verify OTP to sign in."
            )
        assigned_role = (payload.role or otp_record.get("role") or "PATIENT").upper()
        if assigned_role not in ("PATIENT", "GUEST"):
            assigned_role = "PATIENT"
        phone_val = clean_phone
        otp_verified = True
    else:
        assigned_role = "ADMIN"
        name = "Puneeth K.V.N."
        email = "puneeth.kvn@gmail.com"
        phone_val = payload.phone or "+919999999999"
        otp_verified = True

    user_id = payload.sub or f"usr_{uuid.uuid4().hex[:10]}"
    account = {
        "id": user_id,
        "name": name,
        "email": email,
        "phone": phone_val,
        "role": assigned_role,
        "otp_verified": otp_verified,
        "avatar_initial": name[0].upper(),
        "avatar": payload.avatar or f"https://api.dicebear.com/7.x/initials/svg?seed={name}",
        "auth_provider": "admin_google" if assigned_role == "ADMIN" else "google_otp",
        "created_at": time.time(),
        "last_login": time.time()
    }
    USER_ACCOUNTS[email] = account
    save_persistent_store()

    return {
        "success": True,
        "token": f"token_{user_id}_{int(time.time())}",
        "user": account,
        "message": f"Signed in successfully as {account['name']} ({assigned_role})"
    }


@app.post("/api/auth/email")
def email_auth(payload: EmailAuthRequest):
    """Admin email sign-in for Puneeth K.V.N. only; others require Phone + OTP."""
    email = payload.email.lower().strip()
    name = (payload.name or "").strip()
    if not is_puneeth_admin(name, email):
        raise HTTPException(
            status_code=403,
            detail="Only Puneeth K.V.N. is Admin. Please use the Patient / Guest Phone Number + OTP form to sign in."
        )

    user_id = "admin_puneeth_kvn"
    account = {
        "id": user_id,
        "name": "Puneeth K.V.N.",
        "email": "puneeth.kvn@gmail.com",
        "phone": "+919999999999",
        "role": "ADMIN",
        "otp_verified": True,
        "avatar_initial": "P",
        "auth_provider": "admin_credentials",
        "created_at": time.time(),
        "last_login": time.time()
    }
    USER_ACCOUNTS[email] = account
    save_persistent_store()

    return {
        "success": True,
        "token": f"token_{user_id}_{int(time.time())}",
        "user": account,
        "message": "Welcome back, Admin Puneeth K.V.N.!"
    }


@app.get("/api/auth/users")
def list_authenticated_users():
    """Returns all registered/verified users and their roles (ADMIN, PATIENT, GUEST)."""
    # Ensure Puneeth K.V.N. is always listed as sole ADMIN
    admin_entry = {
        "id": "admin_puneeth_kvn",
        "name": "Puneeth K.V.N.",
        "email": "puneeth.kvn@gmail.com",
        "phone": "Admin Primary",
        "role": "ADMIN",
        "otp_verified": True,
        "auth_provider": "admin_google"
    }
    users_list = [admin_entry]
    for k, acc in USER_ACCOUNTS.items():
        if is_puneeth_admin(acc.get("name"), acc.get("email")):
            continue
        # Ensure non-Puneeth accounts never have ADMIN role
        acc_copy = dict(acc)
        if acc_copy.get("role") == "ADMIN":
            acc_copy["role"] = "PATIENT"
        users_list.append(acc_copy)
    return {"users": users_list, "total": len(users_list)}


# ==========================================
# Test Medical Records Discovery (medical_records/ folder)
# ==========================================

@app.get("/api/records/list")
def list_test_records():
    """Lists real test medical record files stored on disk."""
    records = []
    if os.path.exists(RECORDS_DIR):
        for f in sorted(os.listdir(RECORDS_DIR)):
            if f.endswith(".txt"):
                fpath = os.path.join(RECORDS_DIR, f)
                pdf_f = f.replace(".txt", ".pdf")
                has_pdf = os.path.exists(os.path.join(RECORDS_DIR, pdf_f))
                
                # Read title from first few lines
                title = f.replace("_", " ").replace(".txt", "").title()
                try:
                    with open(fpath, "r", encoding="utf-8") as fp:
                        lines = [l.strip() for l in fp.readlines() if l.strip()]
                        if lines:
                            title = lines[0]
                except Exception:
                    pass

                records.append({
                    "filename": f,
                    "title": title,
                    "txt_path": fpath,
                    "has_pdf": has_pdf,
                    "pdf_filename": pdf_f if has_pdf else None,
                    "size_bytes": os.path.getsize(fpath)
                })
    return {"records": records}


@app.post("/api/records/load")
def load_test_record_file(filename: str = Form(...)):
    """Loads and indexes a selected test file from medical_records/ into the system."""
    fpath = os.path.join(RECORDS_DIR, filename)
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail=f"File {filename} not found in medical_records/")

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    clean_text = preprocess_text(content)
    chunks = index_document(doc_id, clean_text)

    # Extract patient name if available
    patient_name = "Patient Record"
    for line in clean_text.split("\n"):
        if "patient name:" in line.lower():
            parts = line.split(":")
            if len(parts) > 1:
                patient_name = parts[1].split("|")[0].strip()
                break

    title = filename.replace("_", " ").replace(".txt", "").title()
    first_lines = [l.strip() for l in clean_text.split("\n") if l.strip()]
    if first_lines:
        title = first_lines[0]

    doc_entry = {
        "id": doc_id,
        "title": title,
        "category": "Clinical File",
        "patient": {
            "name": patient_name,
            "age": 60,
            "gender": "Clinical",
            "uhid": f"MED-{uuid.uuid4().hex[:6].upper()}"
        },
        "content": clean_text,
        "source": filename,
        "created_at": time.time(),
        "chunks_indexed": True,
        "chunk_count": len(chunks)
    }
    DOCUMENTS_STORE[doc_id] = doc_entry
    save_persistent_store()

    return {
        "success": True,
        "document_id": doc_id,
        "title": doc_entry["title"],
        "patient": doc_entry["patient"],
        "chunk_count": len(chunks),
        "message": f"Successfully loaded record '{filename}'."
    }


# ==========================================
# Document Upload & New Patient Creation Endpoints
# ==========================================

def generate_record_files(base_name: str, text_content: str):
    """Generates both .txt and .pdf files in medical_records/ and returns their URLs."""
    txt_filename = f"{base_name}.txt"
    pdf_filename = f"{base_name}.pdf"
    txt_path = os.path.join(RECORDS_DIR, txt_filename)
    pdf_path = os.path.join(RECORDS_DIR, pdf_filename)

    try:
        with open(txt_path, "w", encoding="utf-8") as fp:
            fp.write(text_content)
    except Exception:
        pass

    try:
        import fitz
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        y_pos = 50
        for line in text_content.split("\n"):
            if y_pos > 790:
                page = doc.new_page(width=595, height=842)
                y_pos = 50
            page.insert_text(fitz.Point(50, y_pos), line.strip(), fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))
            y_pos += 13.5
        doc.save(pdf_path)
        doc.close()
    except Exception:
        pass

    return f"/medical_records/{pdf_filename}", f"/medical_records/{txt_filename}"


@app.post("/api/upload/text")
def upload_text_document(payload: TextUploadRequest):
    """Creates a new patient clinical record from direct entry."""
    content = payload.content.strip()
    if not content or len(content) < 20:
        raise HTTPException(status_code=400, detail="Document text is too short or empty (minimum 20 characters required).")

    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    clean_text = preprocess_text(content)
    chunks = index_document(doc_id, clean_text)
    uhid_str = f"UHID-{uuid.uuid4().hex[:6].upper()}"

    safe_name = "".join(c if c.isalnum() else "_" for c in (payload.patient_name or "patient").lower())
    base_name = f"{doc_id}_{safe_name}"
    pdf_url, txt_url = generate_record_files(base_name, clean_text)

    doc_entry = {
        "id": doc_id,
        "title": payload.title or "Clinical Record",
        "category": "Clinical Entry",
        "patient": {
            "name": payload.patient_name or "New Patient",
            "age": payload.patient_age or 45,
            "gender": payload.patient_gender or "Unspecified",
            "uhid": uhid_str
        },
        "content": clean_text,
        "source": f"{base_name}.pdf",
        "pdf_url": pdf_url,
        "txt_url": txt_url,
        "created_at": time.time(),
        "chunks_indexed": True,
        "chunk_count": len(chunks)
    }
    DOCUMENTS_STORE[doc_id] = doc_entry
    save_persistent_store()

    return {
        "success": True,
        "document_id": doc_id,
        "title": doc_entry["title"],
        "patient": doc_entry["patient"],
        "pdf_url": pdf_url,
        "txt_url": txt_url,
        "chunk_count": len(chunks),
        "message": "Successfully created and indexed patient record."
    }


@app.post("/api/upload/file")
async def upload_file_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    patient_name: Optional[str] = Form(None),
    patient_age: Optional[int] = Form(None),
    patient_gender: Optional[str] = Form(None)
):
    """File upload supporting PDF, TXT, MD with automatic patient metadata extraction."""
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[1].lower()

    allowed_exts = [".pdf", ".txt", ".md"]
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file format '{ext}'. DoctorInsight accepts .pdf, .txt, or .md files."
        )

    file_bytes = await file.read()
    if not file_bytes or len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    extracted_text = ""
    if ext == ".pdf":
        try:
            extracted_text = extract_text_from_pdf(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Failed to extract text from PDF: {str(e)}")
    else:
        extracted_text = file_bytes.decode("utf-8", errors="ignore")

    extracted_text = preprocess_text(extracted_text)
    if not extracted_text or len(extracted_text.strip()) < 15:
        raise HTTPException(status_code=422, detail="No readable medical text could be extracted from this document.")

    # Auto-extract patient name, age, gender from document text if not explicitly provided
    import re
    detected_name = patient_name
    detected_age = patient_age
    detected_gender = patient_gender

    if not detected_name or detected_name == "Uploaded Patient":
        m_name = re.search(r"Patient Name:\s*([^\n\|]+)", extracted_text, re.IGNORECASE)
        if m_name:
            detected_name = m_name.group(1).strip()
        else:
            detected_name = os.path.splitext(filename)[0].replace("_", " ").title()

    if not detected_age:
        m_age = re.search(r"Age(?:/Gender|/Sex)?:\s*(\d+)", extracted_text, re.IGNORECASE)
        detected_age = int(m_age.group(1)) if m_age else 52

    if not detected_gender:
        if re.search(r"\bFemale\b", extracted_text, re.IGNORECASE):
            detected_gender = "Female"
        elif re.search(r"\bMale\b", extracted_text, re.IGNORECASE):
            detected_gender = "Male"
        else:
            detected_gender = "Clinical"

    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    chunks = index_document(doc_id, extracted_text)

    safe_name = "".join(c if c.isalnum() else "_" for c in detected_name.lower())
    base_name = f"{doc_id}_{safe_name}"
    pdf_url, txt_url = generate_record_files(base_name, extracted_text)

    doc_entry = {
        "id": doc_id,
        "title": title or filename,
        "category": "Uploaded Medical Record",
        "patient": {
            "name": detected_name,
            "age": detected_age,
            "gender": detected_gender,
            "uhid": f"UHID-{uuid.uuid4().hex[:6].upper()}"
        },
        "content": extracted_text,
        "source": filename,
        "pdf_url": pdf_url,
        "txt_url": txt_url,
        "created_at": time.time(),
        "chunks_indexed": True,
        "chunk_count": len(chunks)
    }
    DOCUMENTS_STORE[doc_id] = doc_entry
    save_persistent_store()

    return {
        "success": True,
        "document_id": doc_id,
        "title": doc_entry["title"],
        "patient": doc_entry["patient"],
        "pdf_url": pdf_url,
        "txt_url": txt_url,
        "chunk_count": len(chunks),
        "message": f"Successfully parsed and indexed '{filename}'."
    }


@app.get("/api/samples")
def list_sample_documents():
    """Returns all 15+ patient medical records with live clinical counts and PDF/TXT links."""
    samples = []
    for doc_id, doc in DOCUMENTS_STORE.items():
        insights = extract_rule_based_clinical_insights(doc.get("content", ""), [])
        custom_risks = doc.get("custom_risks", [])
        custom_meds = doc.get("custom_meds", [])
        custom_alerts = doc.get("custom_alerts", [])

        all_risks = custom_risks + insights.get("risk_analysis", [])
        all_meds = custom_meds + insights.get("prescription_summary", [])
        all_alerts = custom_alerts + insights.get("medication_alerts", [])
        diags = insights.get("document_summary", {}).get("primary_diagnosis", [])
        high_risks = [r for r in all_risks if r.get("severity") == "HIGH"]

        samples.append({
            "id": doc["id"],
            "title": doc["title"],
            "category": doc.get("category", "Clinical Record"),
            "patient": doc.get("patient", {}),
            "source": doc.get("source", "Sample Record"),
            "pdf_url": doc.get("pdf_url"),
            "txt_url": doc.get("txt_url"),
            "diagnoses": diags[:3],
            "risk_count": len(all_risks),
            "high_risk_count": len(high_risks),
            "med_count": len(all_meds),
            "alert_count": len(all_alerts),
            "top_risk": all_risks[0]["risk_factor"] if all_risks else "Routine Surveillance"
        })
    return {"samples": samples, "total": len(samples)}


@app.get("/api/documents/{doc_id}")
def get_document(doc_id: str):
    """Retrieve full text and metadata of a document."""
    doc = DOCUMENTS_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc


# ==========================================
# Core Medical Analysis & Interactive Risk/Medication Management
# ==========================================

class AddRiskRequest(BaseModel):
    severity: str = "HIGH"
    risk_factor: str
    details: str
    recommended_action: str

class AddMedicationRequest(BaseModel):
    drug_name: str
    dosage: str
    frequency: str
    instructions: str
    purpose: str
    alert_type: Optional[str] = "Clinical Precaution"
    alert_message: Optional[str] = None


@app.post("/api/patients/{doc_id}/risks")
def add_patient_risk_alert(doc_id: str, payload: AddRiskRequest):
    """Adds a new clinical risk alert to the specified patient record."""
    doc = DOCUMENTS_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Patient record not found.")

    if "custom_risks" not in doc:
        doc["custom_risks"] = []

    new_risk = {
        "severity": payload.severity.upper(),
        "risk_factor": payload.risk_factor.strip(),
        "details": payload.details.strip(),
        "recommended_action": payload.recommended_action.strip()
    }
    doc["custom_risks"].insert(0, new_risk)
    # Invalidate cache for this doc
    for k in list(ANALYSIS_CACHE.keys()):
        if k.startswith(doc_id):
            del ANALYSIS_CACHE[k]
    save_persistent_store()
    return {"success": True, "risk": new_risk, "total_custom_risks": len(doc["custom_risks"])}


@app.post("/api/patients/{doc_id}/medications")
def add_patient_medication(doc_id: str, payload: AddMedicationRequest):
    """Adds a new prescription and medication safety alert to the specified patient record."""
    doc = DOCUMENTS_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Patient record not found.")

    if "custom_meds" not in doc:
        doc["custom_meds"] = []
    if "custom_alerts" not in doc:
        doc["custom_alerts"] = []

    new_med = {
        "drug_name": payload.drug_name.strip(),
        "dosage": payload.dosage.strip(),
        "frequency": payload.frequency.strip(),
        "instructions": payload.instructions.strip(),
        "purpose": payload.purpose.strip()
    }
    doc["custom_meds"].insert(0, new_med)

    if payload.alert_message and payload.alert_message.strip():
        doc["custom_alerts"].insert(0, {
            "medication": f"{payload.drug_name.strip()} ({payload.dosage.strip()})",
            "alert_type": payload.alert_type or "Pharmacovigilance Alert",
            "message": payload.alert_message.strip()
        })

    for k in list(ANALYSIS_CACHE.keys()):
        if k.startswith(doc_id):
            del ANALYSIS_CACHE[k]
    save_persistent_store()
    return {"success": True, "medication": new_med}


@app.post("/api/analyze")
def run_analysis(req: AnalyzeRequest):
    """Runs the 5 DoctorInsight modules (Summary, Risks, Med Alerts, Rx, Guidance) and merges custom entries."""
    doc_id = req.document_id
    doc = DOCUMENTS_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    cache_key = f"{doc_id}_{bool(req.api_key)}"
    if cache_key in ANALYSIS_CACHE:
        return ANALYSIS_CACHE[cache_key]

    analysis = generate_doctorinsight_analysis(doc_id, doc["content"], api_key=req.api_key)

    # Merge any user-added custom risks, medications, or alerts
    if doc.get("custom_risks"):
        analysis["risk_analysis"] = doc["custom_risks"] + analysis.get("risk_analysis", [])
    if doc.get("custom_meds"):
        analysis["prescription_summary"] = doc["custom_meds"] + analysis.get("prescription_summary", [])
    if doc.get("custom_alerts"):
        analysis["medication_alerts"] = doc["custom_alerts"] + analysis.get("medication_alerts", [])

    res = {
        "document_id": doc_id,
        "title": doc["title"],
        "patient": doc["patient"],
        "analysis": analysis,
        "analyzed_at": time.time()
    }
    ANALYSIS_CACHE[cache_key] = res
    return res


# ==========================================
# RAG Query Engine
# ==========================================

@app.post("/api/query")
def execute_rag_query(req: QueryRequest):
    """Context-aware question answering."""
    doc_id = req.document_id
    doc = DOCUMENTS_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    chunks = vector_db.get_document_chunks(doc_id)
    if not chunks:
        index_document(doc_id, doc["content"])

    result = query_rag_engine(query, doc_id, doc["content"], api_key=req.api_key)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
