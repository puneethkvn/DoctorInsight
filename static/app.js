/**
 * DoctorInsight - Medical Document Intelligence
 * Full-Screen Login Page + Photo-Identical Dashboard
 */

let currentPatient = {
  id: "doc_p01",
  name: "Harold Jenkins (71y, Male)"
};

let allPatientsList = [];
let currentAnalysis = null;
let currentDoc = null;
let currentUser = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", async () => {
  initAuthSession();
  await loadAllPatientsDirectory();
  loadPatientRecord(currentPatient.id, currentPatient.name);
});

async function loadAllPatientsDirectory() {
  try {
    const res = await fetch("/api/samples");
    if (!res.ok) return;
    const data = await res.json();
    allPatientsList = data.samples || [];

    if (document.getElementById("patientsActiveBadge")) {
      document.getElementById("patientsActiveBadge").textContent = `${allPatientsList.length} Patients Active`;
    }

    // 1. Populate Top Header Patient Selector Dropdown (15 Patients)
    const dropdownMenu = document.getElementById("patientDropdownMenu");
    if (dropdownMenu && allPatientsList.length > 0) {
      dropdownMenu.innerHTML = allPatientsList.map((doc, idx) => {
        const pName = doc.patient?.name || "Patient";
        const pAge = doc.patient?.age || "--";
        const pGen = doc.patient?.gender || "--";
        const label = `${pName} (${pAge}y, ${pGen})`;
        return `
          <button class="dropdown-item" onclick="selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}')" style="display: flex; flex-direction: column; align-items: flex-start; gap: 0.1rem; padding: 0.55rem 0.75rem; border-bottom: 1px solid #f4f4f5;">
            <span style="font-weight: 700; color: #18181b; font-size: 0.84rem;">${idx + 1}. ${pName} (${pAge}y, ${pGen})</span>
            <span style="font-size: 0.73rem; color: #0284c7; font-weight: 600;">${doc.title}</span>
          </button>
        `;
      }).join("");
    }

    // 2. Populate Dashboard 15-Patient Interactive Table
    renderDashboardPatientsTable();

    // 3. Populate Tab 6: Patient Directory Grid (15 Patients)
    renderPatientsDirectoryGrid();

    // 4. Populate Demo Cases Modal (15 Patients)
    const demoModalList = document.getElementById("demoCasesModalList");
    if (demoModalList && allPatientsList.length > 0) {
      demoModalList.innerHTML = allPatientsList.map((doc, idx) => {
        const pName = doc.patient?.name || "Patient";
        const pAge = doc.patient?.age || "--";
        const pGen = doc.patient?.gender || "--";
        const label = `${pName} (${pAge}y, ${pGen})`;
        return `
          <button class="dropdown-item" onclick="selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); closeDemoDataModal();" style="border: 1px solid #e4e4e7; border-radius: 0.5rem; padding: 0.6rem 0.8rem;">
            <div style="font-weight: 800; font-size: 0.85rem; color: #18181b;">${idx + 1}. ${pName} (${pAge}y, ${pGen})</div>
            <div style="font-size: 0.76rem; color: #0284c7; font-weight: 600; margin-top: 0.1rem;">${doc.title}</div>
          </button>
        `;
      }).join("");
    }

    // 5. Populate Documents Tab Library Grid (.PDF & .TXT Files)
    const docsLibGrid = document.getElementById("documentsLibraryGrid");
    if (docsLibGrid && allPatientsList.length > 0) {
      docsLibGrid.innerHTML = allPatientsList.map((doc, idx) => {
        const pName = doc.patient?.name || "Patient";
        const pAge = doc.patient?.age || "--";
        const pGen = doc.patient?.gender || "--";
        const label = `${pName} (${pAge}y, ${pGen})`;
        const pdfBtn = doc.pdf_url ? `<a href="${doc.pdf_url}" target="_blank" class="btn-demo-data" style="padding: 0.25rem 0.55rem; font-size: 0.72rem; text-decoration: none;">📕 Open PDF</a>` : "";
        const txtBtn = doc.txt_url ? `<a href="${doc.txt_url}" target="_blank" class="btn-demo-data" style="padding: 0.25rem 0.55rem; font-size: 0.72rem; text-decoration: none;">📄 Open TXT</a>` : "";
        return `
          <div style="border: 1px solid #e4e4e7; border-radius: 0.6rem; padding: 0.85rem; background: #fafafa; display: flex; flex-direction: column; justify-content: space-between; gap: 0.5rem;">
            <div>
              <div style="font-weight: 800; font-size: 0.88rem; color: #18181b;">${idx + 1}. ${pName} (${pAge}y, ${pGen})</div>
              <div style="font-size: 0.76rem; color: #0284c7; font-weight: 600; margin-top: 0.15rem;">${doc.title}</div>
            </div>
            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.25rem;">
              <button class="btn-ask-rag" style="padding: 0.25rem 0.6rem; font-size: 0.72rem;" onclick="selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}')">Load Notes</button>
              ${pdfBtn}
              ${txtBtn}
            </div>
          </div>
        `;
      }).join("");
    }
  } catch (err) {
    console.error("Failed to load patient directory:", err);
  }
}

function filterPatientDirectory() {
  const input = document.getElementById("patientDirectorySearchInput");
  const q = input ? input.value.trim().toLowerCase() : "";
  renderPatientsDirectoryGrid(q);
}

function renderPatientsDirectoryGrid(filterQuery = "") {
  const directoryGrid = document.getElementById("patientsDirectoryGrid");
  if (!directoryGrid || !allPatientsList.length) return;

  const filtered = allPatientsList.filter((doc, idx) => {
    if (!filterQuery) return true;
    const pName = (doc.patient?.name || "").toLowerCase();
    const pUhid = (doc.patient?.uhid || `MED-2026-0${idx + 1}`).toLowerCase();
    const title = (doc.title || "").toLowerCase();
    const diags = (doc.diagnoses || []).join(" ").toLowerCase();
    const topRisk = (doc.top_risk || "").toLowerCase();
    return pName.includes(filterQuery) || pUhid.includes(filterQuery) || title.includes(filterQuery) || diags.includes(filterQuery) || topRisk.includes(filterQuery);
  });

  if (document.getElementById("patientsActiveBadge")) {
    document.getElementById("patientsActiveBadge").textContent = `${filtered.length} of ${allPatientsList.length} Patients Shown`;
  }

  if (filtered.length === 0) {
    directoryGrid.innerHTML = `<div class="content-box-card" style="grid-column: 1 / -1; text-align: center; color: #71717a; padding: 2rem;">No matching patient records found for "${filterQuery}".</div>`;
    return;
  }

  directoryGrid.innerHTML = filtered.map((doc) => {
    const idx = allPatientsList.findIndex(d => d.id === doc.id);
    const pName = doc.patient?.name || "Patient";
    const pAge = doc.patient?.age || "--";
    const pGen = doc.patient?.gender || "--";
    const pUhid = doc.patient?.uhid || `MED-2026-0${idx + 1}`;
    const label = `${pName} (${pAge}y, ${pGen})`;
    const isActive = doc.id === currentPatient.id;
    const riskCount = doc.risk_count || 6;
    const highRiskCount = doc.high_risk_count || 3;
    const medCount = doc.med_count || 5;
    const alertCount = doc.alert_count || 5;
    const topRisk = doc.top_risk || "Multi-Factor Clinical Precaution";
    const diags = (doc.diagnoses && doc.diagnoses.length > 0) ? doc.diagnoses.slice(0, 2).join(" • ") : doc.title;
    const pdfBtn = doc.pdf_url ? `<a href="${doc.pdf_url}" target="_blank" onclick="event.stopPropagation()" class="btn-demo-data" style="padding: 0.25rem 0.5rem; font-size: 0.71rem; text-decoration: none;">📕 PDF</a>` : "";
    const txtBtn = doc.txt_url ? `<a href="${doc.txt_url}" target="_blank" onclick="event.stopPropagation()" class="btn-demo-data" style="padding: 0.25rem 0.5rem; font-size: 0.71rem; text-decoration: none;">📄 TXT</a>` : "";

    return `
      <div class="content-box-card" style="cursor: pointer; transition: all 0.15s; border-left: 4px solid ${isActive ? '#16a34a' : '#18181b'}; background: ${isActive ? '#f0fdf4' : 'white'}; display: flex; flex-direction: column; justify-content: space-between;" onclick="selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-analysis');">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; gap: 0.4rem;">
            <h3 style="font-size: 0.96rem; font-weight: 800; color: #09090b;">${idx + 1}. ${pName} (${pAge}y) ${isActive ? '<span style="background:#16a34a;color:white;font-size:0.62rem;padding:0.1rem 0.38rem;border-radius:999px;vertical-align:middle;">ACTIVE</span>' : ''}</h3>
            <span style="font-size: 0.68rem; font-weight: 700; background: #f4f4f5; padding: 0.15rem 0.45rem; border-radius: 0.25rem; color: #52525b;">${pGen}</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span style="font-size: 0.73rem; color: #71717a; font-family: monospace;">UHID: ${pUhid}</span>
            <div style="display: flex; gap: 0.3rem;">
              <span style="font-size: 0.68rem; font-weight: 800; background: #fee2e2; color: #991b1b; padding: 0.12rem 0.42rem; border-radius: 999px;">⚠️ ${riskCount} Risks (${highRiskCount} High)</span>
              <span style="font-size: 0.68rem; font-weight: 800; background: #e0f2fe; color: #0369a1; padding: 0.12rem 0.42rem; border-radius: 999px;">💊 ${medCount} Meds</span>
            </div>
          </div>
          <p style="font-size: 0.81rem; font-weight: 700; color: #0284c7; margin-bottom: 0.3rem;">🩺 ${doc.title}</p>
          <p style="font-size: 0.74rem; color: #3f3f46; margin-bottom: 0.35rem;"><strong>Diagnoses:</strong> ${diags}</p>
          <div style="font-size: 0.73rem; background: #fef2f2; color: #991b1b; padding: 0.3rem 0.5rem; border-radius: 0.35rem; margin-bottom: 0.6rem; border-left: 3px solid #ef4444;">
            <strong>Priority Alert:</strong> ${topRisk} (${alertCount} Drug Safety Alerts)
          </div>
        </div>
        <div style="display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap; border-top: 1px solid #e4e4e7; padding-top: 0.55rem;">
          <button class="btn-ask-rag" style="padding: 0.26rem 0.55rem; font-size: 0.71rem;" onclick="event.stopPropagation(); selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-analysis');">🔬 8-Cards</button>
          <button class="btn-demo-data" style="padding: 0.26rem 0.5rem; font-size: 0.71rem; color: #991b1b; border-color: #fca5a5;" onclick="event.stopPropagation(); selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-risks');">⚠️ Risks</button>
          <button class="btn-demo-data" style="padding: 0.26rem 0.5rem; font-size: 0.71rem; color: #0369a1; border-color: #bae6fd;" onclick="event.stopPropagation(); selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-meds');">💊 Meds</button>
          <button class="btn-demo-data" style="padding: 0.26rem 0.5rem; font-size: 0.71rem;" onclick="event.stopPropagation(); selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-ai-chat');">💬 Ask AI</button>
          ${pdfBtn}
          ${txtBtn}
        </div>
      </div>
    `;
  }).join("");
}

function renderDashboardPatientsTable() {
  const tbody = document.getElementById("dashboardPatientsTableBody");
  if (!tbody || !allPatientsList.length) return;

  tbody.innerHTML = allPatientsList.map((doc, idx) => {
    const pName = doc.patient?.name || "Patient";
    const pAge = doc.patient?.age || "--";
    const pGen = doc.patient?.gender || "--";
    const pUhid = doc.patient?.uhid || `MED-2026-0${idx + 1}`;
    const label = `${pName} (${pAge}y, ${pGen})`;
    const isActive = doc.id === currentPatient.id;
    const rowBg = isActive ? "#fefce8" : "white";
    const activePill = isActive ? `<span style="background:#16a34a;color:white;font-size:0.65rem;padding:0.12rem 0.4rem;border-radius:999px;margin-left:0.4rem;">ACTIVE</span>` : "";
    const pdfBtn = doc.pdf_url ? `<a href="${doc.pdf_url}" target="_blank" onclick="event.stopPropagation()" class="btn-demo-data" style="padding: 0.22rem 0.5rem; font-size: 0.72rem; text-decoration: none;">📕 PDF</a>` : "";
    const txtBtn = doc.txt_url ? `<a href="${doc.txt_url}" target="_blank" onclick="event.stopPropagation()" class="btn-demo-data" style="padding: 0.22rem 0.5rem; font-size: 0.72rem; text-decoration: none;">📄 TXT</a>` : "";

    return `
      <tr style="border-bottom: 1px solid #f4f4f5; background: ${rowBg}; cursor: pointer; transition: background 0.15s;" onclick="selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}')">
        <td style="padding: 0.65rem 0.75rem; font-weight: 700; color: #71717a;">${idx + 1}</td>
        <td style="padding: 0.65rem 0.75rem; font-weight: 800; color: #09090b;">${pName}${activePill}</td>
        <td style="padding: 0.65rem 0.75rem; color: #52525b;">${pAge}y / ${pGen}</td>
        <td style="padding: 0.65rem 0.75rem; font-family: monospace; font-size: 0.76rem; color: #71717a;">${pUhid}</td>
        <td style="padding: 0.65rem 0.75rem; font-weight: 600; color: #0284c7;">🩺 ${doc.title}</td>
        <td style="padding: 0.65rem 0.75rem; text-align: right; white-space: nowrap;">
          <div style="display: inline-flex; gap: 0.35rem; align-items: center;">
            <button class="btn-ask-rag" style="padding: 0.25rem 0.6rem; font-size: 0.73rem;" onclick="event.stopPropagation(); selectPatient('${doc.id}', '${label.replace(/'/g, "\\'")}'); navigateToTab('tab-analysis');">Analyze ➔</button>
            ${pdfBtn}
            ${txtBtn}
          </div>
        </td>
      </tr>
    `;
  }).join("");
}

// ==========================================
// SOLE ADMIN (PUNEETH K.V.N.) + PHONE OTP AUTHENTICATION
// ==========================================

let selectedOtpRole = "PATIENT";
let lastDispatchedOtpCode = "";
let lastDispatchedPhone = "";

function isPuneethAdmin(name, email) {
  const n = (name || "").trim().toLowerCase().replace(/\./g, "").replace(/\s+/g, "");
  const e = (email || "").trim().toLowerCase();
  return n === "puneethkvn" || n === "puneeth" || e === "puneeth.kvn@gmail.com";
}

function initAuthSession() {
  const loginPage = document.getElementById("fullLoginPage");
  const isLoginPath = window.location.pathname.includes("/login");
  const savedUser = localStorage.getItem("DOCTORINSIGHT_AUTH_V3");

  if (isLoginPath) {
    loginPage.style.display = "flex";
    loadAuthUsersRegistry();
    return;
  }

  if (savedUser) {
    try {
      const parsed = JSON.parse(savedUser);
      // Enforce strict rule: Only Puneeth K.V.N. can be ADMIN; others must be OTP-verified PATIENT or GUEST
      if (isPuneethAdmin(parsed.name, parsed.email)) {
        parsed.role = "ADMIN";
        parsed.name = "Puneeth K.V.N.";
        parsed.email = "puneeth.kvn@gmail.com";
        parsed.otp_verified = true;
      } else if (!parsed.otp_verified || !parsed.phone) {
        // Non-admin without verified OTP must verify OTP
        localStorage.removeItem("DOCTORINSIGHT_AUTH_V3");
        loginPage.style.display = "flex";
        switchLoginTab("otp");
        return;
      } else if (parsed.role !== "GUEST" && parsed.role !== "PATIENT") {
        parsed.role = "PATIENT";
      }
      currentUser = parsed;
      updateUserInterface(currentUser);
      loginPage.style.display = "none";
      loadAuthUsersRegistry();
      return;
    } catch (e) {
      localStorage.removeItem("DOCTORINSIGHT_AUTH_V3");
    }
  }

  // Default initial session on /dashboard is Sole Admin Puneeth K.V.N.
  currentUser = {
    name: "Puneeth K.V.N.",
    email: "puneeth.kvn@gmail.com",
    phone: "Admin Master Account",
    role: "ADMIN",
    otp_verified: true,
    avatar_initial: "P",
    provider: "admin_google",
    timestamp: Date.now()
  };
  localStorage.setItem("DOCTORINSIGHT_AUTH_V3", JSON.stringify(currentUser));
  updateUserInterface(currentUser);
  loginPage.style.display = "none";
  loadAuthUsersRegistry();
}

function switchLoginTab(mode) {
  const otpPanel = document.getElementById("otpLoginPanel");
  const adminPanel = document.getElementById("adminLoginPanel");
  const btnOtp = document.getElementById("tabBtnOtpLogin");
  const btnAdmin = document.getElementById("tabBtnAdminLogin");

  if (mode === "admin") {
    if (otpPanel) otpPanel.style.display = "none";
    if (adminPanel) adminPanel.style.display = "block";
    if (btnAdmin) {
      btnAdmin.style.background = "#18181b";
      btnAdmin.style.color = "#facc15";
    }
    if (btnOtp) {
      btnOtp.style.background = "transparent";
      btnOtp.style.color = "#52525b";
    }
  } else {
    if (otpPanel) otpPanel.style.display = "block";
    if (adminPanel) adminPanel.style.display = "none";
    if (btnOtp) {
      btnOtp.style.background = "#18181b";
      btnOtp.style.color = "#ffffff";
    }
    if (btnAdmin) {
      btnAdmin.style.background = "transparent";
      btnAdmin.style.color = "#52525b";
    }
  }
}

function selectOtpRole(role) {
  selectedOtpRole = role === "GUEST" ? "GUEST" : "PATIENT";
  const cardP = document.getElementById("roleCardPatient");
  const cardG = document.getElementById("roleCardGuest");
  const radios = document.getElementsByName("otpRoleRadio");
  radios.forEach(r => { r.checked = (r.value === selectedOtpRole); });

  if (selectedOtpRole === "PATIENT") {
    if (cardP) { cardP.style.borderColor = "#0284c7"; cardP.style.background = "#f0f9ff"; cardP.style.color = "#0369a1"; }
    if (cardG) { cardG.style.borderColor = "#e4e4e7"; cardG.style.background = "#ffffff"; cardG.style.color = "#52525b"; }
  } else {
    if (cardG) { cardG.style.borderColor = "#18181b"; cardG.style.background = "#f4f4f5"; cardG.style.color = "#18181b"; }
    if (cardP) { cardP.style.borderColor = "#e4e4e7"; cardP.style.background = "#ffffff"; cardP.style.color = "#52525b"; }
  }
}

async function sendLoginOtp() {
  const nameInput = document.getElementById("otpLoginNameField");
  const phoneInput = document.getElementById("otpLoginPhoneField");
  const errorBox = document.getElementById("otpErrorBox");
  const banner = document.getElementById("otpDispatchBanner");
  const otpInput = document.getElementById("otpCodeInput");

  if (errorBox) errorBox.style.display = "none";

  const name = (nameInput?.value || "").trim();
  const phone = (phoneInput?.value || "").trim();

  if (!name) {
    if (errorBox) {
      errorBox.textContent = "Please enter your Full Name before requesting an OTP.";
      errorBox.style.display = "block";
    }
    nameInput?.focus();
    return;
  }

  if (!phone || phone.replace(/\D/g, "").length < 10) {
    if (errorBox) {
      errorBox.textContent = "Please enter a valid 10-digit mobile phone number to receive your OTP.";
      errorBox.style.display = "block";
    }
    phoneInput?.focus();
    return;
  }

  try {
    const res = await fetch("/api/auth/send-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name,
        phone: phone,
        role: selectedOtpRole
      })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Could not send OTP to phone number.");
    }

    lastDispatchedOtpCode = data.otp_code;
    lastDispatchedPhone = data.phone;

    if (banner) {
      banner.style.display = "block";
      document.getElementById("otpBannerPhoneText").textContent = `📲 SMS OTP Connected to ${data.phone} (${data.role})`;
      document.getElementById("otpBannerCodeText").innerHTML =
        `Your 6-digit verification OTP is: <strong style="font-size: 1rem; letter-spacing: 2px; background: #fff; padding: 0.12rem 0.45rem; border-radius: 0.25rem; border: 1px solid #eab308;">${data.otp_code}</strong>`;
    }

    if (otpInput) {
      otpInput.disabled = false;
      otpInput.style.background = "#ffffff";
      otpInput.placeholder = "Enter 6-digit OTP (e.g. " + data.otp_code + ")";
      otpInput.focus();
    }

    showToast(`📲 OTP ${data.otp_code} sent to ${data.phone} for ${data.role} login!`);
  } catch (err) {
    if (errorBox) {
      errorBox.textContent = err.message;
      errorBox.style.display = "block";
    }
  }
}

function autoFillReceivedOtp() {
  const otpInput = document.getElementById("otpCodeInput");
  if (otpInput && lastDispatchedOtpCode) {
    otpInput.disabled = false;
    otpInput.style.background = "#ffffff";
    otpInput.value = lastDispatchedOtpCode;
    showToast("✓ 6-digit OTP auto-filled from connected phone SMS!");
  }
}

async function verifyLoginOtpAndSignIn(event) {
  event.preventDefault();
  const name = (document.getElementById("otpLoginNameField")?.value || "").trim();
  const phone = (document.getElementById("otpLoginPhoneField")?.value || "").trim();
  const otp = (document.getElementById("otpCodeInput")?.value || "").trim();
  const errorBox = document.getElementById("otpErrorBox");

  if (errorBox) errorBox.style.display = "none";

  if (!otp || otp.length !== 6) {
    if (errorBox) {
      errorBox.textContent = "Please click 'Get OTP' and enter the valid 6-digit OTP sent to your phone number.";
      errorBox.style.display = "block";
    }
    return;
  }

  try {
    const res = await fetch("/api/auth/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name,
        phone: phone,
        otp: otp,
        role: selectedOtpRole
      })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Invalid OTP code.");
    }

    currentUser = data.user;
    localStorage.setItem("DOCTORINSIGHT_AUTH_V3", JSON.stringify(currentUser));
    updateUserInterface(currentUser);
    await loadAuthUsersRegistry();

    // Reset OTP inputs
    document.getElementById("otpCodeInput").value = "";
    document.getElementById("otpDispatchBanner").style.display = "none";

    // Hide login page and enter dashboard
    document.getElementById("fullLoginPage").style.display = "none";
    if (window.location.pathname.includes("/login")) {
      window.history.pushState({}, "", "/dashboard");
    }

    showToast(`✓ Verified Phone OTP! Signed in as ${currentUser.role}: ${currentUser.name} (${currentUser.phone})`);
  } catch (err) {
    if (errorBox) {
      errorBox.textContent = err.message;
      errorBox.style.display = "block";
    }
  }
}

function redirectToOtpVerification(suggestedName, role) {
  closeGoogleAuthModal();
  document.getElementById("fullLoginPage").style.display = "flex";
  switchLoginTab("otp");
  selectOtpRole(role || "PATIENT");
  const nameField = document.getElementById("otpLoginNameField");
  if (nameField) {
    nameField.value = suggestedName || "";
  }
  const phoneField = document.getElementById("otpLoginPhoneField");
  if (phoneField) {
    setTimeout(() => phoneField.focus(), 80);
  }
  showToast(`Only Puneeth K.V.N. is Admin. Please enter your phone number & verify OTP to sign in as ${role}.`);
}

function showLoginPage() {
  closeUserDropdown();
  document.getElementById("fullLoginPage").style.display = "flex";
}

function openGoogleAccountSelector() {
  document.getElementById("googleAuthModal").style.display = "flex";
}

function closeGoogleAuthModal() {
  document.getElementById("googleAuthModal").style.display = "none";
}

async function completeAdminLogin(name, email) {
  closeGoogleAuthModal();

  if (!isPuneethAdmin(name, email)) {
    redirectToOtpVerification(name, "PATIENT");
    return;
  }

  try {
    const res = await fetch("/api/auth/google", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: "Puneeth K.V.N.", email: "puneeth.kvn@gmail.com" })
    });
    const data = await res.json();
    currentUser = data.user || {
      name: "Puneeth K.V.N.",
      email: "puneeth.kvn@gmail.com",
      phone: "Admin Master Account",
      role: "ADMIN",
      otp_verified: true,
      avatar_initial: "P"
    };
  } catch (err) {
    currentUser = {
      name: "Puneeth K.V.N.",
      email: "puneeth.kvn@gmail.com",
      phone: "Admin Master Account",
      role: "ADMIN",
      otp_verified: true,
      avatar_initial: "P"
    };
  }

  localStorage.setItem("DOCTORINSIGHT_AUTH_V3", JSON.stringify(currentUser));
  updateUserInterface(currentUser);
  await loadAuthUsersRegistry();

  document.getElementById("fullLoginPage").style.display = "none";
  if (window.location.pathname.includes("/login")) {
    window.history.pushState({}, "", "/dashboard");
  }
  showToast("🛡️ Signed in as Sole Admin: Puneeth K.V.N.");
}

async function completeAccountLogin(name, email) {
  if (isPuneethAdmin(name, email)) {
    await completeAdminLogin(name, email);
  } else {
    redirectToOtpVerification(name, "PATIENT");
  }
}

function submitEmailLoginForm(event) {
  event.preventDefault();
  const name = document.getElementById("loginNameField").value.trim() || "User";
  const email = document.getElementById("loginEmailField").value.trim();
  if (!isPuneethAdmin(name, email)) {
    redirectToOtpVerification(name, "PATIENT");
    return;
  }
  completeAdminLogin("Puneeth K.V.N.", "puneeth.kvn@gmail.com");
}

function updateUserInterface(user) {
  if (!user) return;
  const isAdmin = isPuneethAdmin(user.name, user.email) && user.role === "ADMIN";
  const role = isAdmin ? "ADMIN" : (user.role === "GUEST" ? "GUEST" : "PATIENT");
  const initial = (user.name || "P")[0].toUpperCase();
  const phoneDisplay = isAdmin ? "Admin Master Account" : (user.phone || "Phone OTP Verified");

  if (document.getElementById("userAvatarLetter")) {
    document.getElementById("userAvatarLetter").textContent = initial;
  }
  if (document.getElementById("menuUserName")) {
    document.getElementById("menuUserName").textContent = user.name || "User";
  }
  if (document.getElementById("menuUserEmail")) {
    document.getElementById("menuUserEmail").textContent = user.email || "";
  }
  if (document.getElementById("menuUserPhone")) {
    document.getElementById("menuUserPhone").textContent = `📱 ${phoneDisplay}`;
  }

  // Header Role Badge
  const headerBadge = document.getElementById("headerRoleBadge");
  if (headerBadge) {
    if (isAdmin) {
      headerBadge.textContent = "🛡️ ADMIN (Puneeth K.V.N.)";
      headerBadge.style.background = "#fef9c3";
      headerBadge.style.color = "#854d0e";
      headerBadge.style.borderColor = "#fde047";
    } else if (role === "PATIENT") {
      headerBadge.textContent = `🧑 PATIENT (${user.phone || "OTP ✓"})`;
      headerBadge.style.background = "#e0f2fe";
      headerBadge.style.color = "#0369a1";
      headerBadge.style.borderColor = "#bae6fd";
    } else {
      headerBadge.textContent = `👤 GUEST (${user.phone || "OTP ✓"})`;
      headerBadge.style.background = "#f4f4f5";
      headerBadge.style.color = "#3f3f46";
      headerBadge.style.borderColor = "#d4d4d8";
    }
  }

  // Dropdown Role Badge & Status
  const menuRoleBadge = document.getElementById("menuUserRoleBadge");
  if (menuRoleBadge) {
    menuRoleBadge.textContent = role;
    menuRoleBadge.style.background = isAdmin ? "#18181b" : (role === "PATIENT" ? "#0284c7" : "#52525b");
    menuRoleBadge.style.color = isAdmin ? "#facc15" : "#ffffff";
  }
  const menuOtpStatus = document.getElementById("menuOtpStatus");
  if (menuOtpStatus) {
    menuOtpStatus.innerHTML = isAdmin
      ? `<span>🛡️</span> Sole Admin Privilege Active`
      : `<span>✓</span> Phone OTP Verified (${user.phone || ""})`;
  }

  // Profile & Security Tab
  if (document.getElementById("profileAvatarBig")) {
    document.getElementById("profileAvatarBig").textContent = initial;
    document.getElementById("profileBigName").textContent = user.name || "User";
    document.getElementById("profileBigEmail").textContent = user.email || "";
  }
  if (document.getElementById("profileRolePill")) {
    const pill = document.getElementById("profileRolePill");
    pill.textContent = isAdmin ? "SOLE ADMIN" : `${role} (OTP VERIFIED)`;
    pill.style.background = isAdmin ? "#18181b" : (role === "PATIENT" ? "#0284c7" : "#52525b");
    pill.style.color = isAdmin ? "#facc15" : "#ffffff";
  }
  if (document.getElementById("profileSessionStatusText")) {
    document.getElementById("profileSessionStatusText").textContent = isAdmin
      ? "● Sole Admin Session Active (Puneeth K.V.N.)"
      : `● OTP-Verified ${role} Session Active (${user.phone || ""})`;
  }
  if (document.getElementById("profileRoleValue")) {
    document.getElementById("profileRoleValue").textContent = isAdmin
      ? "ADMIN (Puneeth K.V.N. Only)"
      : `${role} (Phone OTP Authenticated)`;
  }
  if (document.getElementById("profilePhoneValue")) {
    document.getElementById("profilePhoneValue").textContent = phoneDisplay;
  }
  if (document.getElementById("profileOtpStatusValue")) {
    document.getElementById("profileOtpStatusValue").textContent = isAdmin
      ? "✓ Admin Master Verified"
      : `✓ 6-Digit OTP Verified (${user.phone || ""})`;
  }
  if (document.getElementById("profileAccessValue")) {
    document.getElementById("profileAccessValue").textContent = isAdmin
      ? "Full Admin Read & Write"
      : `${role} Clinical View & AI Assistant`;
  }
}

async function loadAuthUsersRegistry() {
  const tbody = document.getElementById("authUsersTableBody");
  if (!tbody) return;
  try {
    const res = await fetch("/api/auth/users");
    if (!res.ok) return;
    const data = await res.json();
    const users = data.users || [];
    tbody.innerHTML = users.map(u => {
      const isA = u.role === "ADMIN";
      const badgeStyle = isA
        ? "background:#18181b;color:#facc15;"
        : (u.role === "PATIENT" ? "background:#e0f2fe;color:#0369a1;" : "background:#f4f4f5;color:#52525b;");
      return `
        <tr style="border-bottom: 1px solid #f4f4f5;">
          <td style="padding: 0.5rem 0.45rem; font-weight: 800; color: #09090b;">${u.name || "User"}</td>
          <td style="padding: 0.5rem 0.45rem;"><span style="font-size:0.65rem;font-weight:800;padding:0.12rem 0.45rem;border-radius:999px;${badgeStyle}">${u.role}</span></td>
          <td style="padding: 0.5rem 0.45rem; font-family: monospace; font-size: 0.75rem; color: #0284c7;">${u.phone || "--"}</td>
          <td style="padding: 0.5rem 0.45rem; color: #16a34a; font-weight: 700; font-size: 0.74rem;">✓ ${isA ? "Sole Admin" : "OTP Verified"}</td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    console.error("Failed to load auth users registry:", err);
  }
}

function handleLogout() {
  localStorage.removeItem("DOCTORINSIGHT_AUTH_V3");
  currentUser = null;
  closeUserDropdown();
  document.getElementById("fullLoginPage").style.display = "flex";
  switchLoginTab("otp");
}

function toggleUserDropdown() {
  const menu = document.getElementById("userDropdownMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function closeUserDropdown() {
  document.getElementById("userDropdownMenu").style.display = "none";
}

// Close dropdowns on outside click
window.addEventListener("click", (e) => {
  if (!e.target.closest("#userAvatarBtn") && !e.target.closest("#headerRoleBadge") && !e.target.closest("#userDropdownMenu")) {
    closeUserDropdown();
  }
  if (!e.target.closest(".patient-selector-btn") && !e.target.closest("#patientDropdownMenu")) {
    document.getElementById("patientDropdownMenu").style.display = "none";
  }
});

// ==========================================
// SIDEBAR & TAB NAVIGATION
// ==========================================

function toggleSidebar() {
  const shell = document.getElementById("appMainShell") || document.querySelector(".app-shell");
  if (!shell) return;
  const isCollapsed = shell.classList.toggle("sidebar-collapsed");
  showToast(isCollapsed ? "Sidebar collapsed to icon rail" : "Sidebar expanded");
}

function navigateToTab(tabId) {
  const loginPage = document.getElementById("fullLoginPage");
  if (loginPage && !window.location.pathname.includes("/login")) {
    loginPage.style.display = "none";
  }

  document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
  const navBtn = document.getElementById("nav-" + tabId.replace("tab-", ""));
  if (navBtn) navBtn.classList.add("active");

  document.querySelectorAll(".tab-view").forEach(view => view.classList.remove("active"));
  const targetView = document.getElementById(tabId);
  if (targetView) targetView.classList.add("active");

  if (tabId === "tab-patients") {
    renderPatientsDirectoryGrid();
    const searchInput = document.getElementById("patientDirectorySearchInput");
    if (searchInput) setTimeout(() => searchInput.focus(), 80);
  } else if (tabId === "tab-ai-chat") {
    const chatInput = document.getElementById("chatAssistantInput");
    if (chatInput) setTimeout(() => chatInput.focus(), 80);
  } else if (tabId === "tab-profile") {
    loadAuthUsersRegistry();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function togglePatientDropdown() {
  const menu = document.getElementById("patientDropdownMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function selectPatient(docId, label) {
  document.getElementById("patientDropdownMenu").style.display = "none";
  document.getElementById("currentPatientLabel").textContent = `Patient: ${label}`;
  currentPatient = { id: docId, name: label };
  renderDashboardPatientsTable();
  filterPatientDirectory();
  loadPatientRecord(docId, label);
  showToast(`Loaded clinical record: ${label}`);
}

async function loadTestFile(filename, label) {
  document.getElementById("patientDropdownMenu").style.display = "none";
  closeDemoDataModal();
  document.getElementById("currentPatientLabel").textContent = `Patient: ${label}`;

  try {
    const formData = new FormData();
    formData.append("filename", filename);

    const res = await fetch("/api/records/load", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("Could not load test record");
    const data = await res.json();
    currentPatient = { id: data.document_id, name: label };
    loadPatientRecord(data.document_id, label);

  } catch (err) {
    console.error("Error loading test file:", err);
  }
}

// ==========================================
// PATIENT RECORD & CLINICAL ANALYSIS
// ==========================================

async function loadPatientRecord(docId, label) {
  try {
    const res = await fetch(`/api/documents/${docId}`);
    if (!res.ok) throw new Error("Document retrieval failed");
    currentDoc = await res.json();

    if (document.getElementById("tabDocumentPre")) {
      document.getElementById("tabDocumentPre").textContent = currentDoc.content || "";
    }

    if (document.getElementById("tabDocActiveHeader") && currentDoc.patient) {
      document.getElementById("tabDocActiveHeader").textContent =
        `${currentDoc.patient.name} (${currentDoc.patient.age}y, ${currentDoc.patient.gender}) • UHID: ${currentDoc.patient.uhid || "--"} • ${currentDoc.title}`;
    }

    await runClinicalEngine(docId);

  } catch (err) {
    console.error("Error loading record:", err);
  }
}

async function runClinicalEngine(docId) {
  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document_id: docId })
    });

    if (!res.ok) throw new Error("Analysis failed");
    const data = await res.json();
    currentAnalysis = data.analysis;

    updateDashboardMetrics(currentAnalysis, currentDoc);
    renderStructuredAnalysis(currentAnalysis, currentDoc);

  } catch (err) {
    console.error("Analysis engine error:", err);
  }
}

function updateDashboardMetrics(analysis, doc) {
  if (!analysis) return;

  const risks = analysis.risk_analysis || [];
  const meds = analysis.prescription_summary || [];
  const summary = analysis.document_summary || {};
  const findings = summary.key_findings || [];
  const totalCount = allPatientsList.length || 15;

  document.getElementById("statTotalDocs").textContent = totalCount.toString();
  document.getElementById("statAnalyzedDocs").textContent = `${totalCount}/${totalCount}`;
  document.getElementById("statRiskCount").textContent = risks.length.toString();
  document.getElementById("statMedCount").textContent = meds.length > 0 ? meds.length.toString() : "2";

  // Update Sidebar Navigation Badges
  if (document.getElementById("navBadgePatients")) document.getElementById("navBadgePatients").textContent = totalCount.toString();
  if (document.getElementById("navBadgeDocs")) document.getElementById("navBadgeDocs").textContent = totalCount.toString();
  if (document.getElementById("navBadgeRisks")) document.getElementById("navBadgeRisks").textContent = risks.length.toString();
  if (document.getElementById("navBadgeMeds")) document.getElementById("navBadgeMeds").textContent = meds.length.toString();
  if (document.getElementById("sidebarRagStatusSub")) document.getElementById("sidebarRagStatusSub").textContent = `MiniLM Embeddings • ${totalCount} Docs`;
  if (document.getElementById("profileIndexedCount")) document.getElementById("profileIndexedCount").textContent = `${totalCount} Patient Records`;

  document.getElementById("dashPatientTitle").textContent = `${doc.patient?.name || 'Patient'} (${doc.patient?.age || '--'}y, ${doc.patient?.gender || '--'}) — ${doc.title}`;
  const diags = summary.primary_diagnosis || [];
  document.getElementById("dashDiagnosisPreview").textContent = diags.length > 0 
    ? `Primary Diagnoses: ${diags.join(", ")}` 
    : "Primary Diagnoses: Routine clinical care and evaluation.";

  // Populate Dashboard Key Vitals & Lab Parameters
  if (document.getElementById("dashVitalsList")) {
    document.getElementById("dashVitalsList").innerHTML = findings.length > 0
      ? findings.map(f => `<li style="margin-bottom: 0.25rem;">${f}</li>`).join("")
      : "<li>Routine vital signs within clinical limits.</li>";
  }

  // Populate Dashboard Active Prescriptions Schedule
  if (document.getElementById("dashMedsPreviewList")) {
    document.getElementById("dashMedsPreviewList").innerHTML = meds.length > 0
      ? meds.map(m => `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.35rem 0.6rem; background: white; border: 1px solid #e4e4e7; border-radius: 0.4rem;">
            <span style="font-weight: 700; color: #18181b;">💊 ${m.drug_name} (${m.dosage})</span>
            <span style="font-size: 0.74rem; color: #0284c7; font-weight: 600;">${m.frequency} • ${m.instructions}</span>
          </div>
        `).join("")
      : "<div>Standard clinical care regimen.</div>";
  }

  // Populate Dashboard Active Record PDF/TXT buttons
  if (document.getElementById("dashActiveRecordLinks") && doc) {
    const pdfBtn = doc.pdf_url ? `<a href="${doc.pdf_url}" target="_blank" class="btn-demo-data" style="text-decoration: none;">📕 Open PDF Record</a>` : "";
    const txtBtn = doc.txt_url ? `<a href="${doc.txt_url}" target="_blank" class="btn-demo-data" style="text-decoration: none;">📄 Open TXT Record</a>` : "";
    document.getElementById("dashActiveRecordLinks").innerHTML = `
      ${pdfBtn}
      ${txtBtn}
      <button class="btn-demo-data" onclick="navigateToTab('tab-analysis')">🔬 Full 8-Card Analysis</button>
      <button class="btn-demo-data" onclick="navigateToTab('tab-risks')">⚠️ Risk Alerts (${risks.length})</button>
      <button class="btn-demo-data" onclick="navigateToTab('tab-meds')">💊 Medications (${meds.length})</button>
      <button class="btn-demo-data" onclick="navigateToTab('tab-ai-chat')">💬 Ask AI Assistant</button>
      <button class="btn-ask-rag" onclick="exportClinicalReport()">📥 Export Report</button>
    `;
  }

  const highRisks = risks.filter(r => r.severity === "HIGH");
  if (highRisks.length > 0) {
    document.getElementById("dashRiskSnippet").innerHTML = `
      <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.6rem 0.8rem; border-radius: 0.4rem; margin-bottom: 0.5rem;">
        <strong style="color: #991b1b; font-size: 0.82rem;">${highRisks[0].risk_factor}</strong>
        <div style="font-size: 0.76rem; color: #7f1d1d; margin-top: 0.2rem;">${highRisks[0].details}</div>
      </div>
      <div style="font-size: 0.78rem; color: #71717a;">Action: ${highRisks[0].recommended_action}</div>
    `;
  } else if (risks.length > 0) {
    document.getElementById("dashRiskSnippet").innerHTML = `
      <div style="background: #fefce8; border-left: 4px solid #f59e0b; padding: 0.6rem 0.8rem; border-radius: 0.4rem; margin-bottom: 0.5rem;">
        <strong style="color: #92400e; font-size: 0.82rem;">${risks[0].risk_factor}</strong>
        <div style="font-size: 0.76rem; color: #78350f; margin-top: 0.2rem;">${risks[0].details}</div>
      </div>
      <div style="font-size: 0.78rem; color: #71717a;">Action: ${risks[0].recommended_action}</div>
    `;
  }
}

function renderStructuredAnalysis(analysis, doc) {
  if (!analysis) return;

  const summary = analysis.document_summary || {};
  const diags = summary.primary_diagnosis || [];
  const findings = summary.key_findings || [];
  const risks = analysis.risk_analysis || [];
  const alerts = analysis.medication_alerts || [];
  const rxList = analysis.prescription_summary || [];
  const guidance = analysis.patient_guidance || {};
  const pName = doc?.patient?.name || "Patient";
  const pAge = doc?.patient?.age || "--";
  const pGen = doc?.patient?.gender || "--";
  const pUhid = doc?.patient?.uhid || "--";
  const patientHeaderStr = `${pName} (${pAge}y, ${pGen}) • UHID: ${pUhid} • ${doc?.title || "Clinical Record"}`;

  if (document.getElementById("analysisDocSubtitle") && doc) {
    document.getElementById("analysisDocSubtitle").textContent = patientHeaderStr;
  }

  // Card 1: Primary Diagnoses
  const diagHtml = diags.map(d => `
    <div style="background: #f4f4f5; padding: 0.45rem 0.75rem; border-radius: 0.4rem; font-weight: 600; font-size: 0.85rem; color: #18181b;">
      🩺 ${d}
    </div>
  `).join("");
  document.getElementById("analysisDiagnosesList").innerHTML = diagHtml || "<div>No primary diagnoses recorded.</div>";

  // Card 2: Laboratory & Diagnostic Findings
  const labsHtml = findings.map(f => `<li style="margin-bottom: 0.35rem;">${f}</li>`).join("");
  document.getElementById("analysisLabsList").innerHTML = labsHtml || "<li>No abnormal parameters.</li>";

  // Card 3: Clinical Course & Assessment
  document.getElementById("analysisCourseText").textContent = summary.hospital_course || "Standard therapeutic care given.";

  // Card 4: High-Priority Risk Radar (inside 8-card view)
  if (document.getElementById("analysisRisksCardList")) {
    const risksCardHtml = risks.map(r => `
      <div style="padding: 0.5rem 0.7rem; border-radius: 0.4rem; border-left: 3px solid ${r.severity === 'HIGH' ? '#ef4444' : '#f59e0b'}; background: ${r.severity === 'HIGH' ? '#fef2f2' : '#fefce8'};">
        <div style="font-weight: 700; font-size: 0.82rem; color: #18181b;">${r.risk_factor} <span style="font-size: 0.68rem; color: ${r.severity === 'HIGH' ? '#dc2626' : '#d97706'};">(${r.severity})</span></div>
        <div style="font-size: 0.76rem; color: #52525b; margin-top: 0.15rem;">${r.recommended_action}</div>
      </div>
    `).join("");
    document.getElementById("analysisRisksCardList").innerHTML = risksCardHtml || "<div>No active risks flagged.</div>";
  }

  // Card 5: Medication Safety & Contraindications (inside 8-card view)
  if (document.getElementById("analysisAlertsCardList")) {
    const alertsCardHtml = alerts.map(a => `
      <div style="padding: 0.5rem 0.7rem; border-radius: 0.4rem; border-left: 3px solid #ef4444; background: #fff5f5;">
        <div style="font-weight: 700; font-size: 0.82rem; color: #991b1b;">⚠️ ${a.medication} (${a.alert_type})</div>
        <div style="font-size: 0.76rem; color: #7f1d1d; margin-top: 0.15rem;">${a.message}</div>
      </div>
    `).join("");
    document.getElementById("analysisAlertsCardList").innerHTML = alertsCardHtml || "<div>No contraindication alerts.</div>";
  }

  // Card 6: Lifestyle & Dietary Protocol (inside 8-card view)
  if (document.getElementById("analysisLifestyleCardList")) {
    const steps = [...(guidance.lifestyle_steps || []), ...(guidance.dietary_advice || [])];
    document.getElementById("analysisLifestyleCardList").innerHTML =
      steps.map(s => `<li style="margin-bottom: 0.35rem;">${s}</li>`).join("") || "<li>Follow balanced low-sodium clinical diet.</li>";
  }

  // Card 7: Active Prescriptions Table
  const rxRows = rxList.map(rx => `
    <tr style="border-bottom: 1px solid #f4f4f5;">
      <td style="padding: 0.65rem 0.8rem; font-weight: 700;">💊 ${rx.drug_name}</td>
      <td style="padding: 0.65rem 0.8rem;"><span style="background: #e4e4e7; padding: 0.15rem 0.45rem; border-radius: 0.25rem; font-size: 0.78rem; font-weight: 600;">${rx.dosage}</span></td>
      <td style="padding: 0.65rem 0.8rem;">${rx.frequency}</td>
      <td style="padding: 0.65rem 0.8rem; color: #0284c7; font-weight: 600;">${rx.instructions}</td>
      <td style="padding: 0.65rem 0.8rem; color: #71717a;">${rx.purpose}</td>
    </tr>
  `).join("");
  document.getElementById("analysisRxTableBody").innerHTML = rxRows || `<tr><td colspan="5" style="text-align: center; padding: 1.5rem; color: #71717a;">No prescriptions found.</td></tr>`;

  // Card 8: Patient Care Guidance & Red Flags
  document.getElementById("analysisGuidanceText").innerHTML = `
    <div style="margin-bottom: 0.75rem;"><strong>Lay-Language Summary:</strong> ${guidance.lay_explanation || "Adhere to written instructions."}</div>
    <div style="margin-bottom: 0.5rem; color: #dc2626;"><strong>Emergency Red Flags:</strong> ${(guidance.red_flags || []).join(", ")}</div>
    <div style="color: #0284c7; font-weight: 600;">🗓️ Follow-up: ${guidance.follow_up || "Follow up in 2 weeks."}</div>
  `;

  // ==========================================
  // TAB 3: FULL RISK ALERTS (#tab-risks)
  // ==========================================
  if (document.getElementById("risksTabPatientSubtitle")) {
    document.getElementById("risksTabPatientSubtitle").textContent = `Active Patient: ${patientHeaderStr}`;
  }
  const highRiskCount = risks.filter(r => r.severity === "HIGH").length;
  if (document.getElementById("risksCountBadge")) {
    document.getElementById("risksCountBadge").textContent = `${risks.length} Risk Alerts (${highRiskCount} HIGH / ${risks.length - highRiskCount} MEDIUM)`;
  }

  const riskFullHtml = risks.map((r, idx) => `
    <div class="content-box-card" style="border-left: 5px solid ${r.severity === 'HIGH' ? '#ef4444' : '#f59e0b'}; background: ${r.severity === 'HIGH' ? '#fffafa' : '#fffdf5'};">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; flex-wrap: wrap; gap: 0.4rem;">
        <span style="font-weight: 800; font-size: 0.96rem; color: #09090b;">${idx + 1}. ${r.risk_factor}</span>
        <span style="font-size: 0.72rem; font-weight: 800; padding: 0.22rem 0.6rem; border-radius: 999px; background: ${r.severity === 'HIGH' ? '#fee2e2' : '#fef3c7'}; color: ${r.severity === 'HIGH' ? '#991b1b' : '#92400e'};">
          ${r.severity === 'HIGH' ? '🚨 HIGH SEVERITY RISK' : '⚠️ MEDIUM SEVERITY RISK'}
        </span>
      </div>
      <p style="font-size: 0.85rem; color: #3f3f46; margin-bottom: 0.5rem; line-height: 1.55;"><strong>Clinical Finding:</strong> ${r.details}</p>
      <div style="font-size: 0.81rem; color: #0369a1; font-weight: 700; background: #f0f9ff; padding: 0.45rem 0.7rem; border-radius: 0.4rem; border-left: 3px solid #0284c7;">
        🛡️ Recommended Clinical Action: ${r.recommended_action}
      </div>
    </div>
  `).join("");
  document.getElementById("fullRisksContainer").innerHTML = riskFullHtml || "<div class='content-box-card'>No active risks identified.</div>";

  // ==========================================
  // TAB 4: FULL MEDICATIONS & ALERTS (#tab-meds)
  // ==========================================
  if (document.getElementById("medsTabPatientSubtitle")) {
    document.getElementById("medsTabPatientSubtitle").textContent = `Active Patient: ${patientHeaderStr}`;
  }
  if (document.getElementById("medsCountBadge")) {
    document.getElementById("medsCountBadge").textContent = `${rxList.length} Active Meds • ${alerts.length} Safety Alerts`;
  }
  if (document.getElementById("fullMedsRxCount")) {
    document.getElementById("fullMedsRxCount").textContent = `${rxList.length} Prescribed Medications`;
  }
  if (document.getElementById("fullMedsAlertsCount")) {
    document.getElementById("fullMedsAlertsCount").textContent = `${alerts.length} Active Contraindication & Safety Warnings`;
  }

  if (document.getElementById("fullMedsRxContainer")) {
    const rxCardsHtml = rxList.map((rx, idx) => `
      <div style="border: 1px solid #e4e4e7; border-left: 4px solid #0284c7; border-radius: 0.6rem; padding: 0.85rem; background: #f8fafc; display: flex; flex-direction: column; justify-content: space-between; gap: 0.4rem;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem;">
            <span style="font-weight: 800; font-size: 0.92rem; color: #09090b;">${idx + 1}. 💊 ${rx.drug_name}</span>
            <span style="background: #0284c7; color: white; font-size: 0.72rem; font-weight: 800; padding: 0.15rem 0.5rem; border-radius: 999px;">${rx.dosage}</span>
          </div>
          <div style="font-size: 0.78rem; font-weight: 700; color: #0369a1; margin-bottom: 0.25rem;">⏱️ Schedule: ${rx.frequency}</div>
          <div style="font-size: 0.79rem; color: #3f3f46; margin-bottom: 0.25rem;"><strong>Instructions:</strong> ${rx.instructions}</div>
        </div>
        <div style="font-size: 0.74rem; color: #52525b; background: white; padding: 0.3rem 0.5rem; border-radius: 0.35rem; border: 1px solid #e4e4e7;">
          <strong>Clinical Purpose:</strong> ${rx.purpose}
        </div>
      </div>
    `).join("");
    document.getElementById("fullMedsRxContainer").innerHTML = rxCardsHtml || "<div>No active medications recorded.</div>";
  }

  const medsFullHtml = alerts.map((a, idx) => `
    <div class="content-box-card" style="border-left: 5px solid #ef4444; background: #fff5f5;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; flex-wrap: wrap; gap: 0.4rem;">
        <span style="font-weight: 800; font-size: 0.94rem; color: #991b1b;">${idx + 1}. ⚠️ ${a.medication}</span>
        <span style="font-size: 0.7rem; font-weight: 800; background: #fee2e2; color: #991b1b; padding: 0.2rem 0.55rem; border-radius: 999px;">${a.alert_type}</span>
      </div>
      <p style="font-size: 0.85rem; color: #7f1d1d; line-height: 1.55;">${a.message}</p>
    </div>
  `).join("");
  document.getElementById("fullMedsContainer").innerHTML = medsFullHtml || "<div class='content-box-card'>No drug-drug interaction warnings flagged.</div>";

  // ==========================================
  // TAB 5: AI ASSISTANT PATIENT CONTEXT BRIEFING
  // ==========================================
  if (document.getElementById("aiChatPatientBanner")) {
    document.getElementById("aiChatPatientBanner").textContent = `Active Patient Context: ${patientHeaderStr}`;
  }
  const streamBox = document.getElementById("chatStreamBox");
  if (streamBox) {
    const topDiags = diags.slice(0, 3).join("; ") || doc?.title || "Clinical evaluation";
    const topMeds = rxList.slice(0, 4).map(m => `${m.drug_name} (${m.dosage})`).join(", ") || "Standard regimen";
    const topRisks = risks.slice(0, 3).map(r => `${r.risk_factor} [${r.severity}]`).join("; ") || "Standard precautions";
    streamBox.innerHTML = `
      <div class="chat-msg assistant" style="border-left: 4px solid #0284c7;">
        <div style="font-weight: 800; color: #09090b; margin-bottom: 0.35rem;">🤖 DoctorInsight RAG Assistant — Active Patient Loaded: <strong>${pName} (${pAge}y, ${pGen})</strong></div>
        <div style="font-size: 0.84rem; color: #3f3f46; line-height: 1.55;">
          • <strong>Primary Diagnoses:</strong> ${topDiags}<br>
          • <strong>Active Prescriptions (${rxList.length}):</strong> ${topMeds}<br>
          • <strong>Priority Risk Radar (${risks.length}):</strong> ${topRisks}<br>
          • <strong>Medication Safety Alerts:</strong> ${alerts.length} contraindication/interaction checks active.
        </div>
        <div style="margin-top: 0.45rem; font-size: 0.78rem; color: #0284c7; font-weight: 700;">
          Ask any clinical question below or click a quick button above to run semantic vector retrieval over ${pName}'s medical record.
        </div>
      </div>
    `;
  }
}

// ==========================================
// INTERACTIVE ADD RISK ALERT & ADD MEDICATION
// ==========================================

function toggleAddRiskForm() {
  const card = document.getElementById("addRiskFormCard");
  if (!card) return;
  card.style.display = card.style.display === "none" ? "block" : "none";
}

async function submitAddRiskAlert(event) {
  event.preventDefault();
  const risk_factor = document.getElementById("newRiskFactorInput").value.trim();
  const severity = document.getElementById("newRiskSeverityInput").value;
  const details = document.getElementById("newRiskDetailsInput").value.trim();
  const recommended_action = document.getElementById("newRiskActionInput").value.trim();

  if (!risk_factor || !details) return;

  try {
    const res = await fetch(`/api/patients/${currentPatient.id}/risks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ risk_factor, severity, details, recommended_action })
    });
    if (!res.ok) throw new Error("Failed to add risk alert");

    document.getElementById("newRiskFactorInput").value = "";
    document.getElementById("newRiskDetailsInput").value = "";
    document.getElementById("newRiskActionInput").value = "";
    document.getElementById("addRiskFormCard").style.display = "none";

    await loadAllPatientsDirectory();
    await loadPatientRecord(currentPatient.id, currentPatient.name);
    showToast(`Added ${severity} risk alert: ${risk_factor}`);
  } catch (err) {
    showToast("Error adding risk alert: " + err.message);
  }
}

function toggleAddMedForm() {
  const card = document.getElementById("addMedFormCard");
  if (!card) return;
  card.style.display = card.style.display === "none" ? "block" : "none";
}

async function submitAddMedication(event) {
  event.preventDefault();
  const drug_name = document.getElementById("newMedNameInput").value.trim();
  const dosage = document.getElementById("newMedDosageInput").value.trim();
  const frequency = document.getElementById("newMedFreqInput").value.trim();
  const purpose = document.getElementById("newMedPurposeInput").value.trim();
  const instructions = document.getElementById("newMedInstructionsInput").value.trim();
  const alert_message = document.getElementById("newMedAlertInput").value.trim();

  if (!drug_name || !dosage) return;

  try {
    const res = await fetch(`/api/patients/${currentPatient.id}/medications`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        drug_name,
        dosage,
        frequency,
        instructions,
        purpose,
        alert_type: "CLINICAL SAFETY ALERT",
        alert_message
      })
    });
    if (!res.ok) throw new Error("Failed to add medication");

    document.getElementById("newMedNameInput").value = "";
    document.getElementById("newMedDosageInput").value = "";
    document.getElementById("newMedFreqInput").value = "";
    document.getElementById("newMedPurposeInput").value = "";
    document.getElementById("newMedInstructionsInput").value = "";
    document.getElementById("newMedAlertInput").value = "";
    document.getElementById("addMedFormCard").style.display = "none";

    await loadAllPatientsDirectory();
    await loadPatientRecord(currentPatient.id, currentPatient.name);
    showToast(`Added medication: ${drug_name} (${dosage})`);
  } catch (err) {
    showToast("Error adding medication: " + err.message);
  }
}

// ==========================================
// DASHBOARD SEARCH & ASK RAG
// ==========================================

async function executeDashboardRagQuery() {
  const input = document.getElementById("dashboardRagInput");
  const query = input.value.trim();
  if (!query) return;

  navigateToTab("tab-ai-chat");
  document.getElementById("chatAssistantInput").value = query;
  await sendAssistantChatMessage();
  input.value = "";
}

async function askSuggestedRagQuestion(questionText) {
  navigateToTab("tab-ai-chat");
  document.getElementById("chatAssistantInput").value = questionText;
  await sendAssistantChatMessage();
}

async function sendAssistantChatMessage() {
  const input = document.getElementById("chatAssistantInput");
  const query = input.value.trim();
  if (!query) return;

  input.value = "";
  appendChatStream("user", query);

  const streamBox = document.getElementById("chatStreamBox");
  const tempMsg = document.createElement("div");
  tempMsg.className = "chat-msg assistant";
  tempMsg.innerHTML = "<em>Grounded retrieval across vector chunks...</em>";
  streamBox.appendChild(tempMsg);
  streamBox.scrollTop = streamBox.scrollHeight;

  const savedApiKey = localStorage.getItem("DOCTORINSIGHT_GEMINI_KEY") || null;

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        document_id: currentPatient.id,
        query: query,
        api_key: savedApiKey
      })
    });

    if (!res.ok) throw new Error("Query failed");
    const data = await res.json();

    let citationHtml = "";
    if (data.citations && data.citations.length > 0) {
      citationHtml = `
        <div style="margin-top: 0.6rem; padding-top: 0.4rem; border-top: 1px solid #e4e4e7; font-size: 0.74rem; color: #71717a;">
          <strong>Retrieved Source (${data.citations[0].similarity_percent || 92}% match):</strong> ${data.citations[0].section} — "${data.citations[0].snippet}"
        </div>
      `;
    }

    const formattedAnswer = (data.answer || "")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\n/g, "<br>");

    tempMsg.innerHTML = `<div style="line-height: 1.6;">${formattedAnswer}</div>${citationHtml}`;

  } catch (err) {
    tempMsg.innerHTML = `<span style="color: #dc2626;">Error: ${err.message}</span>`;
  }

  streamBox.scrollTop = streamBox.scrollHeight;
}

function appendChatStream(role, text) {
  const streamBox = document.getElementById("chatStreamBox");
  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.textContent = text;
  streamBox.appendChild(div);
  streamBox.scrollTop = streamBox.scrollHeight;
}

let demoStepIndex = 0;
let demoAutoTimer = null;

const DEMO_TOUR_STEPS = [
  {
    title: "Step 1/6: Clinical Dashboard & 15 Patient Records",
    desc: "Overview of 15 indexed patients, active risk radar, vitals, and 1-click PDF/TXT medical records.",
    action: () => {
      selectPatient("doc_p02", "Rajesh Varma (59y, Male)");
      navigateToTab("tab-dashboard");
    }
  },
  {
    title: "Step 2/6: Structured 8-Card Clinical Analysis",
    desc: "Automated extraction of Primary Diagnoses, Lab Vitals, Clinical Course, Risks, Contraindications, Diet, Prescriptions & Red Flags.",
    action: () => {
      navigateToTab("tab-analysis");
    }
  },
  {
    title: "Step 3/6: Clinical Risk Radar (HIGH / MEDIUM Severity)",
    desc: "Identifies life-threatening hazards such as Dual Antiplatelet (DAPT) Stent Thrombosis and Renal Impairment.",
    action: () => {
      navigateToTab("tab-risks");
    }
  },
  {
    title: "Step 4/6: Medication Safety & Contraindication Alerts",
    desc: "Flags strict drug interactions (e.g., NSAIDs contraindicated, Methotrexate weekly black-box alert, Penicillin anaphylaxis).",
    action: () => {
      navigateToTab("tab-meds");
    }
  },
  {
    title: "Step 5/6: Grounded RAG AI Clinical Assistant",
    desc: "Executes semantic vector search (all-MiniLM-L6-v2) across medical record chunks with source citations.",
    action: () => {
      askSuggestedRagQuestion("What medications are prescribed and what are the high-risk precautions?");
    }
  },
  {
    title: "Step 6/6: Medical Record Files (.PDF & .TXT) & Report Export",
    desc: "View raw clinical notes, open any of the 15 patient PDF/TXT files, or export the full clinical intelligence report.",
    action: () => {
      navigateToTab("tab-documents");
    }
  }
];

function startLiveDemo() {
  demoStepIndex = 0;
  renderDemoControllerBar();
  runDemoStep(0);
}

function renderDemoControllerBar() {
  let bar = document.getElementById("liveDemoTourBar");
  if (!bar) {
    bar = document.createElement("div");
    bar.id = "liveDemoTourBar";
    bar.style.cssText = "position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#18181b;color:white;padding:0.85rem 1.25rem;border-radius:0.85rem;box-shadow:0 16px 35px rgba(0,0,0,0.35);z-index:19999;display:flex;align-items:center;gap:1.25rem;border:1px solid #3f3f46;min-width:680px;max-width:92vw;";
    document.body.appendChild(bar);
  }
  bar.style.display = "flex";
  updateDemoBarContent();
}

function updateDemoBarContent() {
  const bar = document.getElementById("liveDemoTourBar");
  if (!bar) return;
  const step = DEMO_TOUR_STEPS[demoStepIndex];
  bar.innerHTML = `
    <div style="flex:1;">
      <div style="font-size:0.72rem;font-weight:800;color:#facc15;text-transform:uppercase;letter-spacing:0.05em;">⚡ LIVE PROJECT DEMONSTRATION MODE</div>
      <div style="font-size:0.95rem;font-weight:800;color:white;margin-top:0.1rem;">${step.title}</div>
      <div style="font-size:0.78rem;color:#d4d4d8;margin-top:0.1rem;">${step.desc}</div>
    </div>
    <div style="display:flex;align-items:center;gap:0.45rem;white-space:nowrap;">
      <button onclick="prevDemoStep()" style="background:#27272a;color:white;border:1px solid #3f3f46;padding:0.45rem 0.75rem;border-radius:0.45rem;font-size:0.78rem;font-weight:700;cursor:pointer;">◀ Prev</button>
      <button onclick="nextDemoStep()" style="background:#facc15;color:#18181b;border:none;padding:0.45rem 0.9rem;border-radius:0.45rem;font-size:0.78rem;font-weight:800;cursor:pointer;">Next Step ➔</button>
      <button onclick="toggleAutoPlayDemo()" id="demoAutoPlayBtn" style="background:#0284c7;color:white;border:none;padding:0.45rem 0.75rem;border-radius:0.45rem;font-size:0.78rem;font-weight:700;cursor:pointer;">${demoAutoTimer ? "⏸ Pause" : "▶ Auto-Play"}</button>
      <button onclick="closeLiveDemoBar()" style="background:transparent;color:#a1a1aa;border:none;padding:0.4rem 0.5rem;font-size:0.9rem;cursor:pointer;" title="Close Demo Bar">✕</button>
    </div>
  `;
}

function runDemoStep(idx) {
  demoStepIndex = idx;
  updateDemoBarContent();
  DEMO_TOUR_STEPS[demoStepIndex].action();
}

function nextDemoStep() {
  demoStepIndex = (demoStepIndex + 1) % DEMO_TOUR_STEPS.length;
  runDemoStep(demoStepIndex);
}

function prevDemoStep() {
  demoStepIndex = (demoStepIndex - 1 + DEMO_TOUR_STEPS.length) % DEMO_TOUR_STEPS.length;
  runDemoStep(demoStepIndex);
}

function toggleAutoPlayDemo() {
  if (demoAutoTimer) {
    clearInterval(demoAutoTimer);
    demoAutoTimer = null;
    updateDemoBarContent();
    showToast("Auto-Play paused.");
  } else {
    showToast("▶ Auto-Play started (advances every 5 seconds)");
    demoAutoTimer = setInterval(() => {
      nextDemoStep();
    }, 5000);
    updateDemoBarContent();
  }
}

function closeLiveDemoBar() {
  if (demoAutoTimer) {
    clearInterval(demoAutoTimer);
    demoAutoTimer = null;
  }
  const bar = document.getElementById("liveDemoTourBar");
  if (bar) bar.style.display = "none";
}

// ==========================================
// MODALS, FILE UPLOAD & NEW PATIENT CREATION
// ==========================================

function openUploadModal() {
  document.getElementById("uploadDocModal").style.display = "flex";
}

function closeUploadModal() {
  document.getElementById("uploadDocModal").style.display = "none";
}

function openDemoDataModal() {
  document.getElementById("demoDataModal").style.display = "flex";
}

function closeDemoDataModal() {
  document.getElementById("demoDataModal").style.display = "none";
}

function openSafetyModal() {
  showToast("Safety Notice: DoctorInsight is an AI clinical decision-support platform. Always verify with a licensed physician.");
}

async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", file.name);

  closeUploadModal();
  showToast(`Uploading and indexing ${file.name}...`);

  try {
    const res = await fetch("/api/upload/file", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("File upload failed");
    const data = await res.json();
    const p = data.patient || {};
    const label = `${p.name || file.name} (${p.age || 52}y, ${p.gender || "Clinical"})`;

    await loadAllPatientsDirectory();
    selectPatient(data.document_id, label);
    showToast(`Successfully analyzed ${label}`);

  } catch (err) {
    showToast("Upload error: " + err.message);
  }
}

async function submitNewPatientRecord(event) {
  event.preventDefault();
  const name = document.getElementById("newPatientName").value.trim();
  const age = parseInt(document.getElementById("newPatientAge").value.trim(), 10) || 45;
  const gender = document.getElementById("newPatientGender").value;
  const title = document.getElementById("newPatientTitle").value.trim();
  const content = document.getElementById("newPatientContent").value.trim();

  if (!name || !content) return;

  closeUploadModal();
  showToast(`Creating clinical record for ${name}...`);

  try {
    const res = await fetch("/api/upload/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title,
        patient_name: name,
        patient_age: age,
        patient_gender: gender,
        content: content
      })
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Could not create patient record");
    }

    const data = await res.json();
    const label = `${name} (${age}y, ${gender})`;

    // Reset form
    document.getElementById("newPatientName").value = "";
    document.getElementById("newPatientAge").value = "";
    document.getElementById("newPatientTitle").value = "";
    document.getElementById("newPatientContent").value = "";

    await loadAllPatientsDirectory();
    selectPatient(data.document_id, label);
    showToast(`Added & analyzed ${label}`);

  } catch (err) {
    showToast("Error: " + err.message);
  }
}

function exportClinicalReport() {
  if (!currentAnalysis || !currentDoc) {
    showToast("No active analysis to export.");
    return;
  }

  const p = currentDoc.patient || {};
  const s = currentAnalysis.document_summary || {};
  const risks = currentAnalysis.risk_analysis || [];
  const alerts = currentAnalysis.medication_alerts || [];
  const rx = currentAnalysis.prescription_summary || [];
  const g = currentAnalysis.patient_guidance || {};

  const lines = [
    "======================================================================",
    "DOCTORINSIGHT - STRUCTURED CLINICAL INTELLIGENCE REPORT",
    "======================================================================",
    `Patient: ${p.name || "Unknown"} (${p.age || "--"}y, ${p.gender || "--"}) | UHID: ${p.uhid || "--"}`,
    `Record Title: ${currentDoc.title}`,
    "",
    "1. PRIMARY DIAGNOSES:",
    ...(s.primary_diagnosis || []).map(d => `   - ${d}`),
    "",
    "2. KEY LABORATORY & DIAGNOSTIC FINDINGS:",
    ...(s.key_findings || []).map(f => `   - ${f}`),
    "",
    "3. CLINICAL COURSE & ASSESSMENT:",
    `   ${s.hospital_course || ""}`,
    "",
    "4. CLINICAL RISK RADAR:",
    ...risks.map(r => `   [${r.severity}] ${r.risk_factor}: ${r.details} -> Action: ${r.recommended_action}`),
    "",
    "5. MEDICATION CONTRAINDICATIONS & WARNINGS:",
    ...alerts.map(a => `   [${a.alert_type}] ${a.medication}: ${a.message}`),
    "",
    "6. ACTIVE PRESCRIPTIONS:",
    ...rx.map(m => `   - ${m.drug_name} (${m.dosage}) | ${m.frequency} | ${m.instructions}`),
    "",
    "7. PATIENT CARE GUIDANCE & FOLLOW-UP:",
    `   Summary: ${g.lay_explanation || ""}`,
    `   Red Flags: ${(g.red_flags || []).join(", ")}`,
    `   Follow-Up: ${g.follow_up || ""}`,
    "======================================================================"
  ];

  const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const safeName = (p.name || "patient").toLowerCase().replace(/[^a-z0-9]/g, "_");
  a.href = url;
  a.download = `DoctorInsight_Report_${safeName}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast("Clinical report downloaded!");
}

function showToast(message) {
  const toast = document.getElementById("toastNotification");
  if (!toast) return;
  toast.textContent = message;
  toast.style.display = "block";
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => {
    toast.style.display = "none";
  }, 3500);
}

// ==========================================
// VOICE & SPEECH
// ==========================================

function speakClinicalSummary() {
  if (!currentAnalysis || !currentAnalysis.patient_guidance) return;
  const text = currentAnalysis.patient_guidance.lay_explanation || "Adhere to clinical therapy instructions.";
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 0.95;
    window.speechSynthesis.speak(u);
    showToast("🔊 Reading clinical summary aloud...");
  }
}

let recognition = null;
function toggleDictation() {
  const btn = document.getElementById("chatMicBtn");
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    showToast("Speech recognition not supported in this browser.");
    return;
  }
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!recognition) {
    recognition = new SpeechRec();
    recognition.onstart = () => { btn.style.background = "#fee2e2"; showToast("🎤 Listening..."); };
    recognition.onresult = (e) => {
      document.getElementById("chatAssistantInput").value = e.results[0][0].transcript;
      sendAssistantChatMessage();
    };
    recognition.onend = () => { btn.style.background = ""; };
  }
  recognition.start();
}

function saveGeminiSettings() {
  const key = document.getElementById("settingsGeminiKey").value.trim();
  if (key) {
    localStorage.setItem("DOCTORINSIGHT_GEMINI_KEY", key);
    showToast("Gemini API key saved for live LLM generation.");
  }
}

async function openPublicLinksModal() {
  const modal = document.getElementById("publicLinksModal");
  const container = document.getElementById("publicLinksContainer");
  if (!modal || !container) return;

  modal.style.display = "flex";
  container.innerHTML = `<div style="font-size: 0.82rem; color: #71717a;">Loading live public &amp; custom domain links...</div>`;

  try {
    const res = await fetch("/api/network-info");
    const info = await res.json();

    const links = [
      {
        label: "🌐 Custom Domain Link (Port 80 — No Port Needed)",
        url: info.custom_domain_local || "http://www.doctorinsight.127.0.0.1.sslip.io/dashboard",
        desc: "Direct www.doctorinsight custom domain resolved via sslip.io DNS on port 80"
      },
      {
        label: "📡 Public Wi-Fi / LAN Custom Domain Link",
        url: info.custom_domain_lan || "http://www.doctorinsight.10.166.223.47.sslip.io/dashboard",
        desc: "Open on any phone or laptop connected to the same network"
      },
      {
        label: "🔗 Branded Portal Route (www.doctorinsight.com)",
        url: info.custom_route_url || "http://localhost:5173/www.doctorinsight.com",
        desc: "Branded www.doctorinsight.com application route"
      }
    ];

    if (info.public_tunnel_url) {
      links.unshift({
        label: "🌍 Worldwide Public HTTPS Internet Link (Live Tunnel)",
        url: info.public_tunnel_url,
        desc: "Accessible from anywhere on the internet (mobile 4G/5G or remote devices)"
      });
    }

    container.innerHTML = links.map(item => `
      <div style="border: 1px solid #e4e4e7; border-left: 4px solid #16a34a; border-radius: 0.6rem; padding: 0.75rem 0.9rem; background: #fafafa;">
        <div style="font-size: 0.8rem; font-weight: 800; color: #09090b; margin-bottom: 0.2rem;">${item.label}</div>
        <div style="font-size: 0.73rem; color: #71717a; margin-bottom: 0.45rem;">${item.desc}</div>
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; background: white; border: 1px solid #d4d4d8; padding: 0.4rem 0.65rem; border-radius: 0.45rem;">
          <a href="${item.url}" target="_blank" style="font-family: monospace; font-size: 0.78rem; font-weight: 700; color: #0284c7; text-decoration: none; word-break: break-all;">${item.url}</a>
          <div style="display: flex; gap: 0.35rem; flex-shrink: 0;">
            <button type="button" class="btn-demo-data" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="copyPublicLink('${item.url}')">📋 Copy</button>
            <a href="${item.url}" target="_blank" class="btn-ask-rag" style="padding: 0.2rem 0.55rem; font-size: 0.7rem; text-decoration: none;">Open ↗</a>
          </div>
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<div style="color: #dc2626; font-size: 0.82rem;">Failed to load network links: ${err.message}</div>`;
  }
}

function closePublicLinksModal() {
  const modal = document.getElementById("publicLinksModal");
  if (modal) modal.style.display = "none";
}

function copyPublicLink(url) {
  navigator.clipboard.writeText(url).then(() => {
    showToast(`Copied link: ${url}`);
  }).catch(() => {
    showToast(`Link: ${url}`);
  });
}

