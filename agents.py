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
        "patient_age": intake["age"],
        "patient_sex": intake["sex"],
        "reported_symptoms": ", ".join(intake["symptoms"]) or "None",
        "symptom_duration_hours": intake["durationHours"],
        "heart_rate_bpm": intake["vitals"]["heartRate"],
        "systolic_bp_mmhg": intake["vitals"]["systolicBP"],
        "diastolic_bp_mmhg": intake["vitals"]["diastolicBP"],
        "oxygen_saturation_percent": intake["vitals"]["spo2"],
        "temperature_celsius": intake["vitals"]["temperatureC"],
        "detected_flags": ", ".join(flags) if flags else "None",
        "assessment": "Structured intake for triage; flags are non-diagnostic safety signals.",
        "_intake_obj": intake,
        "_flags": flags
    }

# 2) Risk Scoring Agent
def risk_scoring_agent(intake_output: Dict):
    age = intake_output.get("patient_age")
    dur = intake_output.get("symptom_duration_hours")
    hr = intake_output.get("heart_rate_bpm")
    sbp = intake_output.get("systolic_bp_mmhg")
    spo2 = intake_output.get("oxygen_saturation_percent")
    temp = intake_output.get("temperature_celsius")
    flags = intake_output.get("_flags", [])
    
    risk = 0
    risk_factors = []

    if age is not None:
        if age >= 75: risk += 3; risk_factors.append(f"Age >= 75 (+3)")
        elif age >= 60: risk += 2; risk_factors.append(f"Age 60-74 (+2)")
        elif age >= 40: risk += 1; risk_factors.append(f"Age 40-59 (+1)")

    if dur is not None:
        if dur >= 72: risk += 2; risk_factors.append(f"Duration >= 72h (+2)")
        elif dur >= 24: risk += 1; risk_factors.append(f"Duration 24-72h (+1)")

    if spo2 is not None and spo2 < 92: risk += 4; risk_factors.append(f"Low SpO2 {spo2}% (+4)")
    if sbp is not None and sbp < 90: risk += 3; risk_factors.append(f"Low SBP {sbp} mmHg (+3)")
    if hr is not None and hr > 120: risk += 2; risk_factors.append(f"Tachycardia {hr} bpm (+2)")
    if temp is not None and temp >= 39: risk += 1; risk_factors.append(f"High fever {temp}°C (+1)")

    flag_weights = {
        "chest_pain": 4, "dyspnea": 3, "severe_headache": 2,
        "low_spo2": 4, "low_bp": 3, "tachycardia": 2, "high_fever": 1
    }
    for f in flags:
        w = flag_weights.get(f, 0)
        if w > 0:
            risk += w
            risk_factors.append(f"Flag '{f}' (+{w})")

    tier = "low"
    if risk >= 9: tier = "high"
    elif risk >= 5: tier = "moderate"

    return {
        "agent": "risk_scoring",
        "timestamp": now(),
        "risk_score": risk,
        "risk_tier": tier,
        "risk_factors": ", ".join(risk_factors) if risk_factors else "No significant risk factors",
        "scoring_model": "Composite rule-based from age, vitals, duration, and flags",
        "_risk": risk,
        "_tier": tier
    }

# 3) Severity Prediction Agent
def severity_prediction_agent(intake_output: Dict, risk_output: Dict):
    spo2 = intake_output.get("oxygen_saturation_percent")
    sbp = intake_output.get("systolic_bp_mmhg")
    hr = intake_output.get("heart_rate_bpm")
    symptoms_str = intake_output.get("reported_symptoms", "")
    r = risk_output.get("_risk", 0)
    
    severity = "mild"
    if r >= 9: severity = "critical"
    elif r >= 6: severity = "severe"
    elif r >= 3: severity = "moderate"

    drivers = []
    if spo2 is not None and spo2 < 92: drivers.append(f"Low oxygen saturation ({spo2}%)")
    if "chest pain" in symptoms_str.lower(): drivers.append("Reported chest pain")
    if "shortness of breath" in symptoms_str.lower() or "dyspnea" in symptoms_str.lower(): drivers.append("Breathing difficulty")
    if sbp is not None and sbp < 90: drivers.append(f"Low blood pressure ({sbp} mmHg)")
    if hr is not None and hr > 120: drivers.append(f"Rapid heart rate ({hr} bpm)")

    return {
        "agent": "severity_prediction",
        "timestamp": now(),
        "severity_band": severity.upper(),
        "severity_drivers": ", ".join(drivers) if drivers else "No critical severity drivers",
        "risk_score_basis": f"Based on composite risk score of {r}",
        "classification_note": "Non-diagnostic severity band for triage demo only",
        "_severity": severity
    }

# 4) Doctor Recommendation Agent
def doctor_recommendation_agent(intake_output: Dict):
    symptoms_str = intake_output.get("reported_symptoms", "").lower()
    spo2 = intake_output.get("oxygen_saturation_percent")
    specialties = []
    recommendations = []

    if "chest pain" in symptoms_str or "shortness of breath" in symptoms_str: 
        specialties.append("Cardiology")
        recommendations.append("Cardiac assessment needed")
    if "fever" in symptoms_str or "cough" in symptoms_str: 
        specialties.append("General Medicine")
        recommendations.append("Infectious disease screening")
    if "severe headache" in symptoms_str or "dizziness" in symptoms_str: 
        specialties.append("Neurology")
        recommendations.append("Neurological evaluation")
    if "abdominal pain" in symptoms_str or "vomiting" in symptoms_str: 
        specialties.append("Gastroenterology")
        recommendations.append("GI assessment needed")
    if spo2 is not None and spo2 < 92: 
        specialties.append("Pulmonology")
        recommendations.append("Respiratory support may be needed")

    if not specialties:
        specialties.append("General Medicine")
        recommendations.append("General clinical evaluation")

    return {
        "agent": "doctor_recommendation",
        "timestamp": now(),
        "suggested_specialties": ", ".join(specialties),
        "clinical_recommendations": ", ".join(recommendations),
        "recommendation_basis": "Symptom/vital pattern analysis",
        "_specialties": specialties
    }

# 5) Emergency Priority Classifier
def emergency_priority_classifier(severity_output: Dict, intake_output: Dict):
    severity = severity_output.get("_severity", "mild").upper()
    flags_str = intake_output.get("detected_flags", "")
    flags = set([f.strip() for f in flags_str.split(",") if f.strip() and f.strip() != "None"])
    
    priority = "P3"
    priority_name = "Non-Urgent"
    
    if "CRITICAL" in severity: 
        priority = "P1"
        priority_name = "EMERGENCY"
    elif "SEVERE" in severity: 
        priority = "P2"
        priority_name = "URGENT"

    if any(f in flags for f in ["chest_pain", "low_spo2", "low_bp"]):
        if priority == "P3":
            priority = "P2"
            priority_name = "URGENT"

    guidance_map = {
        "P1": "Immediate emergency response advised. Call emergency services now.",
        "P2": "Prompt clinical evaluation recommended. Seek medical care urgently.",
        "P3": "Non-urgent; monitor symptoms and seek routine care if symptoms persist or worsen."
    }
    guidance = guidance_map.get(priority, "Unknown priority")

    return {
        "agent": "emergency_priority",
        "timestamp": now(),
        "priority_level": priority,
        "priority_name": priority_name,
        "classification_basis": f"Severity: {severity}, Critical Flags: {', '.join(flags) if flags else 'None'}",
        "action_guidance": guidance,
        "_priority": priority
    }

# 6) Medical Report Agent
def medical_report_agent(case_id: str, intake_output: Dict, risk_output: Dict, severity_output: Dict, doctor_output: Dict, priority_output: Dict):
    # Add first aid recommendations - enhanced with LLM and retrieval if available
    intake_obj = intake_output.get("_intake_obj", {})
    symptoms_list = intake_obj.get("symptoms", [])
    severity = severity_output.get("_severity", "mild")
    vitals = intake_obj.get("vitals", {})

    # Attempt retrieval of similar cases to provide context
    similar_cases = []
    try:
        from embeddings_service import retrieve_similar_cases, upsert_case
        # build a short context string
        context_text = f"patient:{intake_output.get('patientName','')}; age:{intake_output.get('patient_age')}; symptoms:{','.join(symptoms_list)}"
        similar_cases = retrieve_similar_cases(context_text, k=3) or []
    except Exception:
        similar_cases = []

    # Try to generate enhanced report via LLM (RAG)
    enhanced = None
    try:
        from llm_service import generate_case_report
        case_summary = {
            "patientName": intake_output.get("patientName") or "",
            "age": intake_output.get("patient_age"),
            "sex": intake_output.get("patient_sex"),
            "symptoms": symptoms_list,
            "durationHours": intake_output.get("symptom_duration_hours"),
            "vitals": vitals,
            "severity": severity,
        }
        enhanced = generate_case_report(case_summary, similar_cases)
    except Exception:
        enhanced = None

    # first_aid default
    first_aid = []
    if enhanced and enhanced.get("first_aid"):
        first_aid = enhanced.get("first_aid")
    else:
        # fallback rules if LLM not available or returned nothing
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
            "age": intake_output.get("patient_age"),
            "sex": intake_output.get("patient_sex"),
            "symptoms": intake_obj.get("symptoms", []),
            "durationHours": intake_output.get("symptom_duration_hours"),
            "vitals": vitals,
        },
        "triage": {
            "riskScore": risk_output.get("_risk"),
            "riskTier": risk_output.get("_tier"),
            "severityBand": severity_output.get("_severity", "unknown"),
            "emergencyPriority": priority_output.get("_priority"),
        },
        "recommendations": {
            "suggestedSpecialties": doctor_output.get("_specialties", []),
            "generalGuidance": priority_output.get("action_guidance"),
            "firstAid": first_aid,
        },
        "rationale": {
            "riskModel": risk_output.get("scoring_model"),
            "severityDrivers": [d.strip() for d in severity_output.get("severity_drivers", "").split(",")] if severity_output.get("severity_drivers") else [],
            "notes": intake_output.get("_flags", []),
        },
    }

    # Upsert the case text into embedding DB for future retrieval (best-effort)
    try:
        from embeddings_service import upsert_case
        text_for_index = f"case:{case_id}; patient:{intake_output.get('patientName','')}; symptoms:{','.join(symptoms_list)}; severity:{severity}; summary:{';'.join(first_aid[:3])}"
        upsert_case(case_id, text_for_index)
    except Exception:
        pass
    return {
        "agent": "medical_report",
        "timestamp": now(),
        "case_id": report["caseId"],
        "report_status": "Generated",
        "patient_name": report["summary"].get("patientName", "N/A"),
        "triage_severity": report["triage"].get("severityBand", "Unknown").upper(),
        "emergency_priority": report["triage"].get("emergencyPriority", "Unknown"),
        "recommended_specialties": ", ".join(report["recommendations"].get("suggestedSpecialties", [])),
        "first_aid_actions": "; ".join(report["recommendations"].get("firstAid", [])) or "None",
        "report_url": f"/api/case/{report['caseId']}/pdf",
        "_report": report
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
    pr = priority_output.get("_priority", "P3")
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

    plan_text = "; ".join([f"{p.get('action', 'unknown')}: {p.get('resource', 'N/A')} ({p.get('detail', '')})" for p in plan]) if plan else "No immediate community resources needed"
    
    return {
        "agent": "community_coordinator",
        "timestamp": now(),
        "location": location_hint,
        "community_plan": plan_text,
        "resources_identified": str(len(plan)),
        "plan_note": "Illustrative resource coordination for demo",
        "_priority": priority_output.get("_priority"),
        "_plan": plan
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

    # Build ledger with cleaned output (remove internal keys starting with _)
    def clean_output(obj):
        return {k: v for k, v in obj.items() if not k.startswith("_")}

    ledger = [
        {"step": "intake", "output": clean_output(intake)},
        {"step": "risk", "output": clean_output(risk)},
        {"step": "severity", "output": clean_output(severity)},
        {"step": "doctor", "output": clean_output(doctor)},
        {"step": "priority", "output": clean_output(priority)},
        {"step": "report", "output": clean_output(report)},
        {"step": "community", "output": clean_output(community)},
    ]
    
    final = {
        "severityBand": severity.get("_severity", "unknown").lower(),
        "priority": priority.get("_priority"),
        "specialties": doctor.get("_specialties", []),
        "report": report.get("_report", {}),
        "communityPlan": community.get("_plan", []),
    }
    
    return {
        "caseId": case_id,
        "createdAt": now(),
        "ledger": ledger,
        "final": final
    }
