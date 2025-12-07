from datetime import datetime
from typing import Dict, List
from uuid import uuid4

# Try to import LLM service, but don't fail if it's not available
try:
    from llm_service import generate_personalized_first_aid, explain_recommendations
    LLM_AVAILABLE = True
except Exception as e:
    print(f"Warning: LLM service not available: {e}")
    LLM_AVAILABLE = False
    # Define fallback functions
    def generate_personalized_first_aid(symptoms, severity, vitals):
        return []
    def explain_recommendations(specialties, severity, drivers):
        return ""

def now() -> str:
    return datetime.utcnow().isoformat() + "Z"

def safe_number(x, fallback=None):
    try:
        if x is None:
            return fallback
        n = float(x)
        return n
    except Exception:
        return fallback

def normalize_symptoms(text: str) -> List[str]:
    text = (text or "").lower()
    tokens = [t.strip() for t in text.replace("\n", ",").split(",")]
    return [t for t in tokens if t]

# 1) Symptom Intake Agent
def symptom_intake_agent(payload: Dict):
    vit = payload.get("vitals", {}) or {}
    intake = {
        "age": safe_number(payload.get("age"), None),
        "sex": payload.get("sex") or "unspecified",
        "symptoms": normalize_symptoms(payload.get("symptomsText", "")),
        "durationHours": safe_number(payload.get("durationHours"), None),
        "vitals": {
            "heartRate": safe_number(vit.get("heartRate"), None),
            "systolicBP": safe_number(vit.get("systolicBP"), None),
            "diastolicBP": safe_number(vit.get("diastolicBP"), None),
            "spo2": safe_number(vit.get("spo2"), None),
            "temperatureC": safe_number(vit.get("temperatureC"), None),
        },
    }

    flags = []
    if intake["vitals"]["spo2"] is not None and intake["vitals"]["spo2"] < 92: flags.append("low_spo2")
    if intake["vitals"]["systolicBP"] is not None and intake["vitals"]["systolicBP"] < 90: flags.append("low_bp")
    if intake["vitals"]["heartRate"] is not None and intake["vitals"]["heartRate"] > 120: flags.append("tachycardia")
    if intake["vitals"]["temperatureC"] is not None and intake["vitals"]["temperatureC"] >= 39.0: flags.append("high_fever")
    s = set(intake["symptoms"])
    if "chest pain" in s: flags.append("chest_pain")
    if "shortness of breath" in s: flags.append("dyspnea")
    if "severe headache" in s: flags.append("severe_headache")

    return {
        "agent": "symptom_intake",
        "timestamp": now(),
        "intake": intake,
        "flags": flags,
        "note": "Structured intake for triage; flags are non-diagnostic safety signals."
    }

# 2) Risk Scoring Agent
def risk_scoring_agent(intake_output: Dict):
    intake = intake_output["intake"]
    flags = intake_output["flags"]
    risk = 0

    age = intake.get("age")
    if age is not None:
        if age >= 75: risk += 3
        elif age >= 60: risk += 2
        elif age >= 40: risk += 1

    dur = intake.get("durationHours")
    if dur is not None:
        if dur >= 72: risk += 2
        elif dur >= 24: risk += 1

    vit = intake["vitals"]
    if vit.get("spo2") is not None and vit["spo2"] < 92: risk += 4
    if vit.get("systolicBP") is not None and vit["systolicBP"] < 90: risk += 3
    if vit.get("heartRate") is not None and vit["heartRate"] > 120: risk += 2
    if vit.get("temperatureC") is not None and vit["temperatureC"] >= 39: risk += 1

    flag_weights = {
        "chest_pain": 4, "dyspnea": 3, "severe_headache": 2,
        "low_spo2": 4, "low_bp": 3, "tachycardia": 2, "high_fever": 1
    }
    for f in flags:
        risk += flag_weights.get(f, 0)

    tier = "low"
    if risk >= 9: tier = "high"
    elif risk >= 5: tier = "moderate"

    return {
        "agent": "risk_scoring",
        "timestamp": now(),
        "riskScore": risk,
        "riskTier": tier,
        "rationale": "Rule-based composite score from age, duration, vitals, and flags."
    }

# 3) Severity Prediction Agent
def severity_prediction_agent(intake_output: Dict, risk_output: Dict):
    vit = intake_output["intake"]["vitals"]
    symptoms = set(intake_output["intake"]["symptoms"])
    r = risk_output["riskScore"]
    severity = "mild"
    if r >= 9: severity = "critical"
    elif r >= 6: severity = "severe"
    elif r >= 3: severity = "moderate"

    drivers = []
    if vit.get("spo2") is not None and vit["spo2"] < 92: drivers.append("low oxygen saturation")
    if "chest pain" in symptoms: drivers.append("reported chest pain")
    if "shortness of breath" in symptoms: drivers.append("breathing difficulty")
    if vit.get("systolicBP") is not None and vit["systolicBP"] < 90: drivers.append("low blood pressure")
    if vit.get("heartRate") is not None and vit["heartRate"] > 120: drivers.append("rapid heart rate")

    return {
        "agent": "severity_prediction",
        "timestamp": now(),
        "severityBand": severity,
        "keyDrivers": drivers,
        "caution": "Non-diagnostic severity band for triage demo only."
    }

# 4) Doctor Recommendation Agent
def doctor_recommendation_agent(intake_output: Dict):
    symptoms = set(intake_output["intake"]["symptoms"])
    vit = intake_output["intake"]["vitals"]
    specialties = []

    if "chest pain" in symptoms or "shortness of breath" in symptoms: specialties.append("Cardiology")
    if "fever" in symptoms or "cough" in symptoms: specialties.append("General Medicine")
    if "severe headache" in symptoms or "dizziness" in symptoms: specialties.append("Neurology")
    if "abdominal pain" in symptoms or "vomiting" in symptoms: specialties.append("Gastroenterology")
    if vit.get("spo2") is not None and vit["spo2"] < 92: specialties.append("Pulmonology")

    if not specialties:
        specialties.append("General Medicine")

    return {
        "agent": "doctor_recommendation",
        "timestamp": now(),
        "specialties": specialties,
        "note": "Specialties suggested from symptom/vitals patterns."
    }

# 5) Emergency Priority Classifier
def emergency_priority_classifier(severity_output: Dict, intake_output: Dict):
    severity = severity_output["severityBand"]
    flags = set(intake_output["flags"])
    priority = "P3"
    if severity == "critical": priority = "P1"
    elif severity == "severe": priority = "P2"

    if any(f in flags for f in ["chest_pain", "low_spo2", "low_bp"]):
        if priority == "P3":
            priority = "P2"

    guidance = {
        "P1": "Immediate emergency response advised.",
        "P2": "Prompt clinical evaluation recommended.",
        "P3": "Non-urgent; monitor and seek routine care if symptoms persist or worsen."
    }[priority]

    return {
        "agent": "emergency_priority",
        "timestamp": now(),
        "priority": priority,
        "guidance": guidance
    }

# 6) Medical Report Agent
def medical_report_agent(case_id: str, intake_output: Dict, risk_output: Dict, severity_output: Dict, doctor_output: Dict, priority_output: Dict):
    # Add first aid recommendations - enhanced with LLM for personalization
    symptoms_list = intake_output["intake"]["symptoms"]
    severity = severity_output["severityBand"]
    vitals = intake_output["intake"]["vitals"]
    
    # Try LLM-enhanced first aid, fall back to rule-based if LLM unavailable
    first_aid = generate_personalized_first_aid(symptoms_list, severity, vitals)
    if not first_aid or first_aid[0].startswith("Error") or first_aid[0].startswith("LLM"):
        # Fallback to rule-based first aid
        first_aid = []
        symptoms = set(symptoms_list)
        if "chest pain" in symptoms:
            first_aid.append("Keep the person calm and seated. Call emergency services immediately.")
        if "shortness of breath" in symptoms:
            first_aid.append("Help the person sit upright. Loosen tight clothing. Seek medical help if severe.")
        if "fever" in symptoms:
            first_aid.append("Keep hydrated. Use a cool compress. Monitor temperature.")
        if severity == "critical":
            first_aid.append("Do not give anything by mouth. Monitor breathing and pulse. Be ready to perform CPR if needed.")
        if not first_aid:
            first_aid.append("Monitor symptoms and seek medical attention if they worsen.")

    report = {
        "caseId": case_id,
        "generatedAt": now(),
        "disclaimer": "Informational triage demo; not medical diagnosis or treatment.",
        "summary": {
            "patientName": intake_output.get("patientName") or "",
            "age": intake_output["intake"]["age"],
            "sex": intake_output["intake"]["sex"],
            "symptoms": intake_output["intake"]["symptoms"],
            "durationHours": intake_output["intake"]["durationHours"],
            "vitals": intake_output["intake"]["vitals"],
        },
        "triage": {
            "riskScore": risk_output["riskScore"],
            "riskTier": risk_output["riskTier"],
            "severityBand": severity_output["severityBand"],
            "emergencyPriority": priority_output["priority"],
        },
        "recommendations": {
            "suggestedSpecialties": doctor_output["specialties"],
            "generalGuidance": priority_output["guidance"],
            "firstAid": first_aid,
        },
        "rationale": {
            "riskModel": risk_output["rationale"],
            "severityDrivers": severity_output["keyDrivers"],
            "notes": intake_output["flags"],
        },
    }
    return {
        "agent": "medical_report",
        "timestamp": now(),
        "report": report
    }

# 7) Resource-aware Community Coordinator
def community_response_coordinator(priority_output: Dict, location_hint: str = "Community Zone A"):
    resources = [
        {"name": "Ambulance A1", "type": "ambulance", "etaMinutes": 8, "available": True},
        {"name": "Ambulance A2", "type": "ambulance", "etaMinutes": 20, "available": True},
        {"name": "Clinic C1", "type": "clinic", "capacity": 2, "available": True},
        {"name": "Hospital H1", "type": "hospital", "icuBeds": 1, "available": True},
    ]
    plan = []
    pr = priority_output["priority"]
    if pr == "P1":
        amb = next((r for r in resources if r["type"] == "ambulance" and r["available"] and r["etaMinutes"] <= 10), None)
        hospital = next((r for r in resources if r["type"] == "hospital" and r["available"]), None)
        if amb and hospital:
            plan.append({"action": "dispatch", "resource": amb["name"], "detail": "Immediate dispatch"})
            plan.append({"action": "route", "resource": hospital["name"], "detail": "Route to ER intake"})
    elif pr == "P2":
        clinic = next((r for r in resources if r["type"] == "clinic" and r["available"]), None)
        plan.append({"action": "schedule", "resource": clinic["name"] if clinic else "Clinic TBD", "detail": "Same-day evaluation"})
    else:
        plan.append({"action": "self-care-info", "resource": "Community Health Portal", "detail": "Non-urgent guidance"})

    return {
        "agent": "community_coordinator",
        "timestamp": now(),
        "locationHint": location_hint,
        "plan": plan,
        "note": "Illustrative resource plan for demo."
    }

# Orchestrator
def orchestrate_case(payload: Dict):
    case_id = str(uuid4())
    # Use sequential case number if provided
    case_id = str(payload.get("case_number", "1"))
    intake = symptom_intake_agent(payload)
    if "patientName" in payload:
        intake["patientName"] = payload["patientName"]
    risk = risk_scoring_agent(intake)
    severity = severity_prediction_agent(intake, risk)
    doctor = doctor_recommendation_agent(intake)
    priority = emergency_priority_classifier(severity, intake)
    report = medical_report_agent(case_id, intake, risk, severity, doctor, priority)
    community = community_response_coordinator(priority, payload.get("locationHint", "Community Zone A"))

    # Build ledger with agent names and timestamps
    ledger = [
        {"step": "intake", "output": {"agent": "symptom_intake", "timestamp": now(), **intake}},
        {"step": "risk", "output": {"agent": "risk_scoring", "timestamp": now(), **risk}},
        {"step": "severity", "output": {"agent": "severity_prediction", "timestamp": now(), **severity}},
        {"step": "doctor", "output": {"agent": "doctor_recommendation", "timestamp": now(), **doctor}},
        {"step": "priority", "output": {"agent": "emergency_priority", "timestamp": now(), **priority}},
        {"step": "report", "output": {"agent": "medical_report", "timestamp": now(), **report}},
        {"step": "community", "output": {"agent": "community_coordinator", "timestamp": now(), **community}},
    ]
    final = {
        "severityBand": severity["severityBand"],
        "priority": priority["priority"],
        "specialties": doctor["specialties"],
        "report": report["report"],
        "communityPlan": community["plan"],
    }
    return {
        "caseId": case_id,
        "createdAt": now(),
        "ledger": ledger,
        "final": final
    }