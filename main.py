from fastapi import FastAPI, Response # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from agents import orchestrate_case
from reportlab.lib.pagesizes import letter  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore
import io
from models import TriageRequest, TriageResponse

app = FastAPI(title="Multi-Agent Emergency Healthcare Triage (Demo)",
              description="Demo-only triage orchestration. Not medical advice.",
              version="0.1.0")

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CASES = {}
CASE_COUNTER = 1

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/triage", response_model=TriageResponse)
def triage(req: TriageRequest):
    global CASE_COUNTER
    payload = req.dict()
    if len(CASES) >= 1000:
        return {"error": "Case limit reached (1000). No more cases can be created."}
    payload["case_number"] = CASE_COUNTER
    result = orchestrate_case(payload)
    CASES[str(CASE_COUNTER)] = result
    result["caseId"] = str(CASE_COUNTER)
    CASE_COUNTER += 1
    return result

@app.get("/api/case/{case_id}", response_model=TriageResponse)
def get_case(case_id: str):
    data = CASES.get(case_id)
    if not data:
        return {"caseId": case_id, "createdAt": "", "ledger": [], "final": {}}
    return data

# PDF download endpoint
@app.get("/api/case/{case_id}/pdf")
def get_case_pdf(case_id: str):
    data = CASES.get(case_id)
    if not data:
        return Response(content="Case not found", status_code=404)
    report = data["final"]["report"]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "EMERGENCY HEALTHCARE TRIAGE REPORT")
    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Patient Name: {report['summary'].get('patientName','-')}")
    y -= 15
    p.drawString(50, y, f"Case ID: {report.get('caseId','-')}")
    y -= 15
    p.drawString(50, y, f"Generated: {report.get('generatedAt','-')}")
    y -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Patient Information")
    y -= 18
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Age: {report['summary'].get('age','-')}")
    p.drawString(200, y, f"Sex: {report['summary'].get('sex','-')}")
    y -= 15
    p.drawString(50, y, f"Symptoms: {', '.join(report['summary'].get('symptoms',[]))}")
    y -= 15
    p.drawString(50, y, f"Duration: {report['summary'].get('durationHours','-')} hours")
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Triage Assessment")
    y -= 18
    p.setFont("Helvetica", 10)
    triage = report.get('triage',{})
    p.drawString(50, y, f"Risk Score: {triage.get('riskScore','-')}")
    p.drawString(200, y, f"Risk Tier: {triage.get('riskTier','-')}")
    y -= 15
    p.drawString(50, y, f"Severity Band: {triage.get('severityBand','-')}")
    p.drawString(200, y, f"Priority: {triage.get('emergencyPriority','-')}")
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "First Aid Recommendations")
    y -= 18
    p.setFont("Helvetica", 10)
    for fa in report.get('recommendations',{}).get('firstAid',[]):
        p.drawString(60, y, f"- {fa}")
        y -= 13
        if y < 60:
            p.showPage()
            y = 750
    y -= 10
    p.setFont("Helvetica", 8)
    p.drawString(50, y, "Disclaimer: Informational triage demo; not medical diagnosis or treatment.")
    p.save()
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=triage_case_{case_id}.pdf"})

