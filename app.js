// Localization dictionary
const translations = {
  en: {
    title: "Multi-Agent Emergency Healthcare Triage",
    disclaimer: "Demo only. Not a medical diagnosis or treatment. If you feel unsafe or in danger, seek emergency care immediately.",
    triageForm: "Triage form",
    patientName: "Patient Name",
    age: "Age",
    sex: "Sex",
    symptoms: "Symptoms (comma or newline separated)",
    duration: "Symptom duration (hours)",
    locationHint: "Location hint",
    vitals: "Vitals",
    runTriage: "Run triage",
    status: "Status",
    result: "Triage result",
    severity: "Severity band",
    priority: "Priority",
    specialties: "Suggested specialties",
    communityPlan: "Community plan",
    report: "Auto-generated report",
    ledger: "Agent ledger (explainability)",
    history: "Case History",
    downloadPDF: "Download PDF"
  },
  hi: {
    title: "मल्टी-एजेंट आपातकालीन स्वास्थ्य ट्रायज",
    disclaimer: "केवल डेमो। यह कोई चिकित्सा निदान या उपचार नहीं है। यदि आप असुरक्षित या खतरे में महसूस करते हैं, तो तुरंत आपातकालीन देखभाल लें।",
    triageForm: "ट्रायज फॉर्म",
    patientName: "रोगी का नाम",
    age: "आयु",
    sex: "लिंग",
    symptoms: "लक्षण (कॉमा या नई पंक्ति से अलग करें)",
    duration: "लक्षणों की अवधि (घंटे)",
    locationHint: "स्थान",
    vitals: "महत्वपूर्ण संकेत (वैकल्पिक)",
    runTriage: "ट्रायज चलाएँ",
    status: "स्थिति",
    result: "ट्रायज परिणाम",
    severity: "गंभीरता",
    priority: "प्राथमिकता",
    specialties: "सुझाई गई विशेषज्ञताएँ",
    communityPlan: "सामुदायिक योजना",
    report: "स्वतः-जनित रिपोर्ट",
    ledger: "एजेंट लेजर (व्याख्यात्मकता)",
    history: "मामलों का इतिहास",
    downloadPDF: "पीडीएफ डाउनलोड करें"
  },
  kn: {
    title: "ಬಹು-ಏಜೆಂಟ್ ತುರ್ತು ಆರೋಗ್ಯ ತ್ರೈಯಾಜ್",
    disclaimer: "ಡೆಮೊ ಮಾತ್ರ. ಇದು ವೈದ್ಯಕೀಯ ನಿರ್ಧಾರ ಅಥವಾ ಚಿಕಿತ್ಸೆ ಅಲ್ಲ. ನೀವು ಅಪಾಯದಲ್ಲಿದ್ದರೆ ಅಥವಾ ಭಯಗೊಂಡಿದ್ದರೆ ತಕ್ಷಣ ತುರ್ತು ಸೇವೆಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    triageForm: "ತ್ರೈಯಾಜ್ ಫಾರ್ಮ್",
    patientName: "ರೋಗಿಯ ಹೆಸರು",
    age: "ವಯಸ್ಸು",
    sex: "ಲಿಂಗ",
    symptoms: "ಲಕ್ಷಣಗಳು (ಅಲ್ಪವಿರಾಮ ಅಥವಾ ಹೊಸ ಸಾಲು ಬಳಸಿ)",
    duration: "ಲಕ್ಷಣಗಳ ಅವಧಿ (ಗಂಟೆ)",
    locationHint: "ಸ್ಥಳ",
    vitals: "ಪ್ರಮುಖ ಸೂಚನೆಗಳು (ಐಚ್ಛಿಕ)",
    runTriage: "ತ್ರೈಯಾಜ್ ಚಾಲನೆ ಮಾಡಿ",
    status: "ಸ್ಥಿತಿ",
    result: "ತ್ರೈಯಾಜ್ ಫಲಿತಾಂಶ",
    severity: "ತೀವ್ರತೆ",
    priority: "ಪ್ರಾಮುಖ್ಯತೆ",
    specialties: "ಸೂಚಿಸಲಾದ ಪರಿಣತಿಗಳು",
    communityPlan: "ಸಮುದಾಯ ಯೋಜನೆ",
    report: "ಸ್ವಯಂ-ಉತ್ಪಾದಿತ ವರದಿ",
    ledger: "ಏಜೆಂಟ್ ಲೆಡ್ಜರ್ (ವಿವರಣೆ)",
    history: "ಕೇಸ್ ಇತಿಹಾಸ",
    downloadPDF: "ಪಿಡಿಎಫ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ"
  }
};

function setLanguage(lang) {
  const t = translations[lang] || translations.en;
  document.getElementById('app-title').textContent = t.title;
  const disclaimer = document.querySelector('.disclaimer');
  if (disclaimer) disclaimer.textContent = t.disclaimer;
  const labels = document.querySelectorAll('label span');
  labels.forEach(label => {
    const text = label.textContent.trim().toLowerCase();
    if (text.includes('patient') || text.includes('रोगी') || text.includes('ರೋಗಿ')) label.textContent = t.patientName;
    else if (text.includes('age') || text.includes('आयु') || text.includes('ವಯಸ್')) label.textContent = t.age;
    else if (text === 'sex' || text.includes('लिंग') || text.includes('ಲಿಂಗ')) label.textContent = t.sex;
    else if (text.includes('symptom') || text.includes('लक्षण') || text.includes('ಲಕ್ಷಣ')) label.textContent = t.symptoms;
    else if (text.includes('duration') || text.includes('अवधि') || text.includes('ಅವಧಿ')) label.textContent = t.duration;
    else if (text.includes('location') || text.includes('स्थान') || text.includes('ಸ್ಥಳ')) label.textContent = t.locationHint;
  });
  const fieldsets = document.querySelectorAll('fieldset');
  fieldsets.forEach(fs => {
    if (fs.querySelector('legend')) fs.querySelector('legend').textContent = t.vitals;
  });
  document.getElementById('submit-btn').textContent = t.runTriage;
  const h2s = document.querySelectorAll('h2');
  h2s.forEach(h2 => {
    const text = h2.textContent.trim().toLowerCase();
    if (text.includes('triage form') || text.includes('ट्रायज') || text.includes('ತ್ರೈಯಾಜ್')) h2.textContent = t.triageForm;
    if (text.includes('result') || text.includes('परिणाम') || text.includes('ಫಲಿತಾ')) h2.textContent = t.result;
    if (text.includes('ledger') || text.includes('लेजर') || text.includes('ಲೆಡ್ಜರ್')) h2.textContent = t.ledger;
    if (text.includes('history') || text.includes('इतिहास') || text.includes('ಇತಿಹಾಸ')) h2.textContent = t.history;
  });
  const ps = document.querySelectorAll('p strong');
  ps.forEach(p => {
    const text = p.textContent.trim();
    if (text.includes('Severity') || text.includes('गंभीरता') || text.includes('ತೀವ್ರತೆ')) p.textContent = t.severity + ':';
    if (text.includes('Priority') || text.includes('प्राथमिकता') || text.includes('ಪ್ರಾಮುಖ್ಯತೆ')) p.textContent = t.priority + ':';
    if (text.includes('Suggested') || text.includes('सुझाई') || text.includes('ಸೂಚಿಸಲಾದ')) p.textContent = t.specialties + ':';
    if (text.includes('Community') || text.includes('सामुदायिक') || text.includes('ಸಮುದಾಯ')) p.textContent = t.communityPlan + ':';
  });
}

document.getElementById('lang-select').addEventListener('change', (e) => {
  setLanguage(e.target.value);
  localStorage.setItem('triageLang', e.target.value);
});

// Set initial language
setLanguage(localStorage.getItem('triageLang') || 'en');
const API_BASE = "http://localhost:8000";

const form = document.getElementById("triage-form");
const statusEl = document.getElementById("status");
const resultSection = document.getElementById("result");
const ledgerSection = document.getElementById("ledger");
const caseIdEl = document.getElementById("caseId");
const severityEl = document.getElementById("severity");
const priorityEl = document.getElementById("priority");
const specialtiesEl = document.getElementById("specialties");
const communityPlanEl = document.getElementById("communityPlan");
const reportEl = document.getElementById("report");
const ledgerEntriesEl = document.getElementById("ledgerEntries");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusEl.textContent = "";
  resultSection.classList.add("hidden");
  ledgerSection.classList.add("hidden");

  // Validate required fields (make vitals optional)
  const requiredFields = [
    'patientName', 'age', 'sex', 'symptomsText', 'durationHours', 'locationHint'
  ];
  let valid = true;
  requiredFields.forEach(name => {
    const el = form.elements[name];
    if (!el || !el.value || (el.type === 'number' && isNaN(Number(el.value)))) {
      el.classList.add('input-error');
      valid = false;
    } else {
      el.classList.remove('input-error');
    }
  });
  if (!valid) {
    statusEl.textContent = "Please fill in all required fields, including all vitals.";
    return;
  }

  const data = formDataToPayload(new FormData(form));
  try {
    const res = await fetch(`${API_BASE}/api/triage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Request failed");
    const json = await res.json();
    renderResult(json);
    renderLedger(json.ledger);
    statusEl.textContent = "Done.";
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Failed. Check inputs or backend status.";
  }
});

function formDataToPayload(fd) {
  const num = (v) => {
    const n = Number(v);
    return Number.isFinite(n) ? n : undefined;
  };
  return {
    patientName: fd.get("patientName") || "",
    age: num(fd.get("age")),
    sex: fd.get("sex") || "unspecified",
    symptomsText: fd.get("symptomsText") || "",
    durationHours: num(fd.get("durationHours")),
    vitals: {
      heartRate: num(fd.get("heartRate")),
      systolicBP: num(fd.get("systolicBP")),
      diastolicBP: num(fd.get("diastolicBP")),
      spo2: num(fd.get("spo2")),
      temperatureC: num(fd.get("temperatureC")),
    },
    locationHint: fd.get("locationHint") || "Community Zone A",
  };
}

function renderResult(data) {
  const report = data.final.report;
  const patientName = report.summary?.patientName || data.patientName || "-";
  document.getElementById("patientName").textContent = patientName;
  caseIdEl.textContent = report.caseId;
  severityEl.textContent = data.final.severityBand.toUpperCase();
  priorityEl.textContent = data.final.priority;
  specialtiesEl.textContent = (data.final.specialties || []).join(", ");

  communityPlanEl.innerHTML = "";
  (data.final.communityPlan || []).forEach((p) => {
    const li = document.createElement("li");
    li.textContent = `${p.action} — ${p.resource} (${p.detail || ''})`;
    communityPlanEl.appendChild(li);
  });

  // Format official medical report (build DOM safely)
  reportEl.innerHTML = '';
  reportEl.appendChild(buildOfficialReport(report, patientName));
  resultSection.classList.remove("hidden");

  // Save to case history
  saveCaseToHistory({
    caseId: report.caseId,
    patientName,
    date: report.generatedAt,
    summary: report.summary,
    triage: report.triage,
    recommendations: report.recommendations
  });
  renderCaseHistory();
}

function saveCaseToHistory(caseData) {
  let history = JSON.parse(localStorage.getItem('triageHistory') || '[]');
  history.unshift(caseData);
  // Keep only last 10 cases
  history = history.slice(0, 10);
  localStorage.setItem('triageHistory', JSON.stringify(history));
}

function renderCaseHistory() {
  const historyDiv = document.getElementById('caseHistory');
  if (!historyDiv) return;
  const history = JSON.parse(localStorage.getItem('triageHistory') || '[]');
  if (!history.length) {
    historyDiv.innerHTML = '<p>No previous cases.</p>';
    return;
  }
  // Build a table safely with DOM API
  historyDiv.innerHTML = '';
  const table = document.createElement('table');
  table.className = 'history-table';
  const thead = document.createElement('thead');
  const headRow = document.createElement('tr');
  ['Date','Patient','Case ID','Severity','Priority',''].forEach(h => { const th = document.createElement('th'); th.textContent = h; headRow.appendChild(th); });
  thead.appendChild(headRow);
  table.appendChild(thead);
  const tbody = document.createElement('tbody');
  history.forEach(c => {
    const tr = document.createElement('tr');
    const tdDate = document.createElement('td'); tdDate.textContent = new Date(c.date).toLocaleString(); tr.appendChild(tdDate);
    const tdPatient = document.createElement('td'); tdPatient.textContent = c.patientName || '-'; tr.appendChild(tdPatient);
    const tdCase = document.createElement('td'); tdCase.textContent = c.caseId; tr.appendChild(tdCase);
    const tdSeverity = document.createElement('td'); tdSeverity.textContent = c.triage?.severityBand?.toUpperCase() || '-'; tr.appendChild(tdSeverity);
    const tdPriority = document.createElement('td'); tdPriority.textContent = c.triage?.emergencyPriority || '-'; tr.appendChild(tdPriority);
    const tdBtn = document.createElement('td'); const btn = document.createElement('button'); btn.textContent = 'View'; btn.addEventListener('click', () => viewCaseHistory(c.caseId)); tdBtn.appendChild(btn); tr.appendChild(tdBtn);
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  historyDiv.appendChild(table);
}

window.viewCaseHistory = function(caseId) {
  const history = JSON.parse(localStorage.getItem('triageHistory') || '[]');
  const c = history.find(x => x.caseId === caseId);
  if (c) {
    // Simulate a result render for this case
    renderResult({
      final: {
        report: {
          caseId: c.caseId,
          generatedAt: c.date,
          summary: c.summary,
          triage: c.triage,
          recommendations: c.recommendations,
          disclaimer: 'Informational triage demo; not medical diagnosis or treatment.'
        },
        severityBand: c.triage?.severityBand,
        priority: c.triage?.emergencyPriority,
        specialties: c.recommendations?.suggestedSpecialties,
        communityPlan: []
      }
    });
  }
}

// Render history on load
renderCaseHistory();

function formatOfficialReport(report, patientName) {
  const summary = report.summary || {};
  const triage = report.triage || {};
  const recommendations = report.recommendations || {};
  const rationale = report.rationale || {};
  return `
    <div class="official-report stylish-gradient">
      <div class="report-header">
        <h3>EMERGENCY HEALTHCARE TRIAGE REPORT</h3>
        <div class="report-meta">
          <p><strong>Patient Name:</strong> ${patientName || '-'}</p>
          <p><strong>Case ID:</strong> ${report.caseId}</p>
          <p><strong>Generated:</strong> ${new Date(report.generatedAt).toLocaleString()}</p>
          <p style="color: #ff9999; font-size: 12px;"><em>${report.disclaimer}</em></p>
        </div>
      </div>

      <div class="report-section">
        <h4>PATIENT INFORMATION</h4>
        <table class="report-table">
          <tr>
            <td class="label">Name:</td>
            <td colspan="3">${patientName || '-'}</td>
          </tr>
          <tr>
            <td class="label">Age:</td>
            <td>${summary.age || 'Not provided'}</td>
            <td class="label">Sex:</td>
            <td>${summary.sex || 'Not specified'}</td>
          </tr>
          <tr>
            <td class="label">Reported Symptoms:</td>
            <td colspan="3">${(summary.symptoms || []).join(', ') || 'None reported'}</td>
          </tr>
          <tr>
            <td class="label">Duration:</td>
            <td colspan="3">${summary.durationHours ? summary.durationHours + ' hours' : 'Not specified'}</td>
          </tr>
        </table>
      </div>

      <div class="report-section">
        <h4>FIRST AID RECOMMENDATIONS</h4>
        <ul>
          ${(recommendations.firstAid || []).map(fa => `<li>${fa}</li>`).join('')}
        </ul>
      </div>

      <div class="report-section">
        <h4>VITAL SIGNS</h4>
        <table class="report-table">
          <tr>
            <td class="label">Heart Rate:</td>
            <td>${summary.vitals?.heartRate || 'N/A'} bpm</td>
            <td class="label">Systolic BP:</td>
            <td>${summary.vitals?.systolicBP || 'N/A'} mmHg</td>
          </tr>
          <tr>
            <td class="label">Diastolic BP:</td>
            <td>${summary.vitals?.diastolicBP || 'N/A'} mmHg</td>
            <td class="label">SpO₂:</td>
            <td>${summary.vitals?.spo2 || 'N/A'}%</td>
          </tr>
          <tr>
            <td class="label">Temperature:</td>
            <td colspan="3">${summary.vitals?.temperatureC ? summary.vitals.temperatureC + '°C' : 'N/A'}</td>
          </tr>
        </table>
      </div>

      <div class="report-section">
        <h4>TRIAGE ASSESSMENT</h4>
        <table class="report-table">
          <tr>
            <td class="label">Risk Score:</td>
            <td>${triage.riskScore || 'N/A'}</td>
            <td class="label">Risk Tier:</td>
            <td><strong>${triage.riskTier || 'Unknown'}</strong></td>
          </tr>
          <tr>
            <td class="label">Severity Band:</td>
            <td><strong style="color: #ff6b6b;">${triage.severityBand?.toUpperCase() || 'UNKNOWN'}</strong></td>
            <td class="label">Priority Level:</td>
            <td><strong style="color: #ffaa00;">${triage.emergencyPriority || 'UNCLASSIFIED'}</strong></td>
          </tr>
        </table>
      </div>

      <div class="report-section">
        <h4>CLINICAL RECOMMENDATIONS</h4>
        <p><strong>Suggested Specialties:</strong></p>
        <ul>
          ${(recommendations.suggestedSpecialties || []).map(s => `<li>${s}</li>`).join('')}
        </ul>
        <p><strong>General Guidance:</strong></p>
        <p style="background: #0f141d; padding: 10px; border-radius: 6px; border-left: 3px solid #4cc2ff;">
          ${recommendations.generalGuidance || 'No guidance available'}
        </p>
      </div>

      <div class="report-section">
        <h4>SEVERITY DRIVERS</h4>
        <ul>
          ${(rationale.severityDrivers || []).length > 0 
            ? rationale.severityDrivers.map(d => `<li>${d}</li>`).join('')
            : '<li>No critical factors identified</li>'}
        </ul>
      </div>

      <div class="report-section">
        <h4>CLINICAL NOTES</h4>
        <ul>
          ${(rationale.notes || []).length > 0 
            ? rationale.notes.map(n => `<li>${n}</li>`).join('')
            : '<li>No additional notes</li>'}
        </ul>
      </div>

      <div class="report-footer">
        <p style="color: #8aa0b6; font-size: 12px;">
          <em>This report is generated for informational and demonstration purposes only. It does not constitute medical diagnosis, treatment, or advice. For emergency situations, contact emergency services immediately.</em>
        </p>
      </div>
    </div>
  `;
}

function renderLedger(ledger) {
  ledgerEntriesEl.innerHTML = "";
  const agentNames = {
    'symptom_intake': '1) Symptom Intake Agent',
    'risk_scoring': '2) Risk Scoring Agent',
    'severity_prediction': '3) Severity Prediction Agent',
    'doctor_recommendation': '4) Doctor Recommendation Agent',
    'emergency_priority': '5) Emergency Priority Classifier',
    'medical_report': '6) Auto-generate Medical Report Agent',
    'community_coordinator': '7) Community Response Coordinator'
  };

  const agentColors = {
    'symptom_intake': '#70e000',
    'risk_scoring': '#ffaa00',
    'severity_prediction': '#ff6b6b',
    'doctor_recommendation': '#4cc2ff',
    'emergency_priority': '#ff6b6b',
    'medical_report': '#4cc2ff',
    'community_coordinator': '#70e000'
  };

  function formatValue(value) {
    if (Array.isArray(value)) return value.join(', ');
    if (value && typeof value === 'object') {
      try { return JSON.stringify(value, null, 2); } catch (e) { return String(value); }
    }
    return String(value === undefined || value === null ? '' : value);
  }

    ledger.forEach((entry) => {
      const details = document.createElement('details');
      details.style.margin = '16px 0';
      details.style.border = '2px solid #4cc2ff';
      details.style.borderRadius = '10px';
      details.style.overflow = 'hidden';
      details.style.backgroundColor = '#0f141d';

      const summary = document.createElement('summary');
      const agentKey = entry.output && entry.output.agent ? entry.output.agent : 'unknown_agent';
      const agentName = agentNames[agentKey] || agentKey;
      const agentColor = agentColors[agentKey] || '#4cc2ff';

      const titleDiv = document.createElement('div');
      titleDiv.style.display = 'flex';
      titleDiv.style.justifyContent = 'space-between';
      titleDiv.style.alignItems = 'center';

      const titleLeft = document.createElement('div');
      const strong = document.createElement('strong');
      strong.textContent = agentName;
      strong.style.color = agentColor;
      strong.style.fontSize = '15px';
      titleLeft.appendChild(strong);

      const timeSpan = document.createElement('span');
      timeSpan.textContent = `Timestamp: ${entry.output.timestamp || ''}`;
      timeSpan.style.color = '#8aa0b6';
      timeSpan.style.fontSize = '12px';

      titleDiv.appendChild(titleLeft);
      titleDiv.appendChild(timeSpan);

      summary.appendChild(titleDiv);
      summary.style.cursor = 'pointer';
      summary.style.padding = '14px 16px';
      summary.style.backgroundColor = 'rgba(76, 194, 255, 0.05)';
      summary.style.borderLeft = `4px solid ${agentColor}`;
      summary.style.display = 'block';
      summary.style.fontWeight = '600';

      const contentDiv = document.createElement('div');
      contentDiv.style.padding = '16px';
      contentDiv.style.borderTop = '1px solid #1f2a3a';
      contentDiv.style.backgroundColor = '#121823';

      // Create table from entry.output data
      const table = document.createElement('table');
      table.style.width = '100%';
      table.style.borderCollapse = 'collapse';
      table.style.fontSize = '13px';

      // Get keys from the output object excluding metadata
      const keys = Object.keys(entry.output || {}).filter(k => k !== 'agent' && k !== 'timestamp');
    
      // Create header
      const thead = document.createElement("thead");
      const headerRow = document.createElement("tr");
      headerRow.style.borderBottom = '2px solid #4cc2ff';
      headerRow.style.backgroundColor = 'rgba(76, 194, 255, 0.08)';
    
      const keyHeader = document.createElement("th");
      keyHeader.textContent = "Property";
      keyHeader.style.padding = '10px';
      keyHeader.style.textAlign = 'left';
      keyHeader.style.color = '#4cc2ff';
      keyHeader.style.fontWeight = '600';
    
      const valueHeader = document.createElement("th");
      valueHeader.textContent = "Value";
      valueHeader.style.padding = '10px';
      valueHeader.style.textAlign = 'left';
      valueHeader.style.color = '#4cc2ff';
      valueHeader.style.fontWeight = '600';
    
      headerRow.appendChild(keyHeader);
      headerRow.appendChild(valueHeader);
      thead.appendChild(headerRow);
      table.appendChild(thead);
    
      // Create body rows
      const tbody = document.createElement("tbody");
      keys.forEach((key, idx) => {
        const row = document.createElement("tr");
        row.style.borderBottom = '1px solid #1f2a3a';
        if (idx % 2 === 0) {
          row.style.backgroundColor = 'rgba(76, 194, 255, 0.02)';
        }
      
        const keyCell = document.createElement("td");
        keyCell.textContent = key;
        keyCell.style.padding = '10px';
        keyCell.style.fontWeight = '500';
        keyCell.style.color = '#8aa0b6';
        keyCell.style.whiteSpace = 'nowrap';
      
        const valueCell = document.createElement("td");
        const value = entry.output[key];
        const formattedValue = formatValue(value);
      
        valueCell.textContent = formattedValue;
        valueCell.style.padding = '10px';
        valueCell.style.color = '#e6edf3';
        valueCell.style.wordBreak = 'break-word';
      
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        tbody.appendChild(row);
      });
      table.appendChild(tbody);
    
      contentDiv.appendChild(table);
      details.appendChild(summary);
      details.appendChild(contentDiv);
      ledgerEntriesEl.appendChild(details);
    });
    ledgerSection.classList.remove("hidden");
}

function buildOfficialReport(report, patientName) {
  const container = document.createElement('div');
  container.className = 'official-report stylish-gradient';

  const header = document.createElement('div');
  header.className = 'report-header';
  const h3 = document.createElement('h3');
  h3.textContent = 'EMERGENCY HEALTHCARE TRIAGE REPORT';
  header.appendChild(h3);

  const meta = document.createElement('div');
  meta.className = 'report-meta';
  const pName = document.createElement('p'); pName.innerHTML = `<strong>Patient Name:</strong> ${patientName || '-'}`;
  const pCase = document.createElement('p'); pCase.innerHTML = `<strong>Case ID:</strong> ${report.caseId || '-'}`;
  const pGen = document.createElement('p'); pGen.innerHTML = `<strong>Generated:</strong> ${new Date(report.generatedAt).toLocaleString()}`;
  const pDisc = document.createElement('p'); pDisc.style.color = '#ff9999'; pDisc.style.fontSize = '12px'; pDisc.innerHTML = `<em>${report.disclaimer || ''}</em>`;
  meta.appendChild(pName); meta.appendChild(pCase); meta.appendChild(pGen); meta.appendChild(pDisc);
  header.appendChild(meta);
  container.appendChild(header);

  // Patient info
  const sectionPatient = document.createElement('div');
  sectionPatient.className = 'report-section';
  const h4p = document.createElement('h4'); h4p.textContent = 'PATIENT INFORMATION'; sectionPatient.appendChild(h4p);
  const table = document.createElement('table'); table.className = 'report-table';
  const tr1 = document.createElement('tr');
  const td1 = document.createElement('td'); td1.className = 'label'; td1.textContent = 'Name:'; const td2 = document.createElement('td'); td2.colSpan = 3; td2.textContent = patientName || '-';
  tr1.appendChild(td1); tr1.appendChild(td2); table.appendChild(tr1);
  const tr2 = document.createElement('tr');
  const t2a = document.createElement('td'); t2a.className = 'label'; t2a.textContent = 'Age:'; const t2b = document.createElement('td'); t2b.textContent = report.summary?.age || 'Not provided';
  const t2c = document.createElement('td'); t2c.className = 'label'; t2c.textContent = 'Sex:'; const t2d = document.createElement('td'); t2d.textContent = report.summary?.sex || 'Not specified';
  tr2.appendChild(t2a); tr2.appendChild(t2b); tr2.appendChild(t2c); tr2.appendChild(t2d); table.appendChild(tr2);
  const tr3 = document.createElement('tr');
  const t3a = document.createElement('td'); t3a.className = 'label'; t3a.textContent = 'Reported Symptoms:'; const t3b = document.createElement('td'); t3b.colSpan = 3; t3b.textContent = (report.summary?.symptoms || []).join(', ') || 'None reported';
  tr3.appendChild(t3a); tr3.appendChild(t3b); table.appendChild(tr3);
  sectionPatient.appendChild(table);
  container.appendChild(sectionPatient);

  // First aid
  const sectionFirst = document.createElement('div'); sectionFirst.className = 'report-section';
  const h4f = document.createElement('h4'); h4f.textContent = 'FIRST AID RECOMMENDATIONS'; sectionFirst.appendChild(h4f);
  const ulFA = document.createElement('ul'); (report.recommendations?.firstAid || []).forEach(fa => { const li = document.createElement('li'); li.textContent = fa; ulFA.appendChild(li); });
  sectionFirst.appendChild(ulFA); container.appendChild(sectionFirst);

  // Vitals
  const sectionVitals = document.createElement('div'); sectionVitals.className = 'report-section';
  const h4v = document.createElement('h4'); h4v.textContent = 'VITAL SIGNS'; sectionVitals.appendChild(h4v);
  const vt = document.createElement('table'); vt.className = 'report-table';
  const vtr = document.createElement('tr'); const vtd1 = document.createElement('td'); vtd1.className='label'; vtd1.textContent='Heart Rate:'; const vtd2 = document.createElement('td'); vtd2.textContent = report.summary?.vitals?.heartRate ? `${report.summary.vitals.heartRate} bpm` : 'N/A';
  const vtd3 = document.createElement('td'); vtd3.className='label'; vtd3.textContent='Systolic BP:'; const vtd4 = document.createElement('td'); vtd4.textContent = report.summary?.vitals?.systolicBP ? `${report.summary.vitals.systolicBP} mmHg` : 'N/A';
  vtr.appendChild(vtd1); vtr.appendChild(vtd2); vtr.appendChild(vtd3); vtr.appendChild(vtd4); vt.appendChild(vtr);
  sectionVitals.appendChild(vt); container.appendChild(sectionVitals);

  // Triage assessment
  const sectionT = document.createElement('div'); sectionT.className='report-section'; const h4t = document.createElement('h4'); h4t.textContent='TRIAGE ASSESSMENT'; sectionT.appendChild(h4t);
  const ttable = document.createElement('table'); ttable.className='report-table'; const trt = document.createElement('tr'); const tlabel1 = document.createElement('td'); tlabel1.className='label'; tlabel1.textContent='Risk Score:'; const tval1 = document.createElement('td'); tval1.textContent = report.triage?.riskScore || 'N/A';
  const tlabel2 = document.createElement('td'); tlabel2.className='label'; tlabel2.textContent='Risk Tier:'; const tval2 = document.createElement('td'); tval2.textContent = report.triage?.riskTier || 'Unknown';
  trt.appendChild(tlabel1); trt.appendChild(tval1); trt.appendChild(tlabel2); trt.appendChild(tval2); ttable.appendChild(trt); sectionT.appendChild(ttable); container.appendChild(sectionT);

  // Recommendations
  const sectionR = document.createElement('div'); sectionR.className='report-section'; const h4r = document.createElement('h4'); h4r.textContent='CLINICAL RECOMMENDATIONS'; sectionR.appendChild(h4r);
  const sp = document.createElement('p'); sp.innerHTML = '<strong>Suggested Specialties:</strong>'; sectionR.appendChild(sp);
  const ulSpec = document.createElement('ul'); (report.recommendations?.suggestedSpecialties || []).forEach(s => { const li = document.createElement('li'); li.textContent = s; ulSpec.appendChild(li); }); sectionR.appendChild(ulSpec);
  const gp = document.createElement('p'); gp.innerHTML = '<strong>General Guidance:</strong>'; sectionR.appendChild(gp);
  const guidance = document.createElement('p'); guidance.style.background = '#0f141d'; guidance.style.padding='10px'; guidance.style.borderRadius='6px'; guidance.style.borderLeft='3px solid #4cc2ff'; guidance.textContent = report.recommendations?.generalGuidance || 'No guidance available'; sectionR.appendChild(guidance);
  container.appendChild(sectionR);

  // Rationale
  const sectionRaz = document.createElement('div'); sectionRaz.className='report-section'; const h4ra = document.createElement('h4'); h4ra.textContent='SEVERITY DRIVERS'; sectionRaz.appendChild(h4ra);
  const ulRaz = document.createElement('ul'); (report.rationale?.severityDrivers || []).forEach(d => { const li = document.createElement('li'); li.textContent = d; ulRaz.appendChild(li); }); if (!ulRaz.children.length) { const li = document.createElement('li'); li.textContent='No critical factors identified'; ulRaz.appendChild(li); }
  sectionRaz.appendChild(ulRaz); container.appendChild(sectionRaz);

  // Notes
  const sectionNotes = document.createElement('div'); sectionNotes.className='report-section'; const h4n = document.createElement('h4'); h4n.textContent='CLINICAL NOTES'; sectionNotes.appendChild(h4n);
  const ulNotes = document.createElement('ul'); (report.rationale?.notes || []).forEach(n => { const li = document.createElement('li'); li.textContent = n; ulNotes.appendChild(li); }); if (!ulNotes.children.length) { const li = document.createElement('li'); li.textContent='No additional notes'; ulNotes.appendChild(li); }
  sectionNotes.appendChild(ulNotes); container.appendChild(sectionNotes);

  const footer = document.createElement('div'); footer.className='report-footer'; const pf = document.createElement('p'); pf.style.color='#8aa0b6'; pf.style.fontSize='12px'; pf.innerHTML = '<em>This report is generated for informational and demonstration purposes only. It does not constitute medical diagnosis, treatment, or advice. For emergency situations, contact emergency services immediately.</em>';
  footer.appendChild(pf); container.appendChild(footer);

  return container;
}