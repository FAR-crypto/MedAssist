"""Lightweight OpenAI wrapper for agents.

Provides:
- generate_personalized_first_aid(symptoms, severity, vitals) -> List[str]
- explain_recommendations(specialties, severity, drivers) -> str

If `openai` is unavailable or `OPENAI_API_KEY` is not set, the module falls back to safe, fast heuristics.
"""
import os
from typing import List

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
_HAS_OPENAI = False
try:
    import openai  # type: ignore
    if OPENAI_KEY:
        openai.api_key = OPENAI_KEY
        _HAS_OPENAI = True
except Exception:
    _HAS_OPENAI = False


def _call_chat(prompt: str, temperature: float = 0.2, max_tokens: int = 400) -> str:
    """Call OpenAI chat completion if available, otherwise return empty string."""
    if not _HAS_OPENAI:
        return ""
    try:
        resp = openai.ChatCompletion.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "system", "content": "You are a helpful medical triage assistant. Provide concise, safety-first first-aid steps and explainable recommendations. Keep answers short."},
                      {"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ""


def generate_personalized_first_aid(symptoms: List[str], severity: str, vitals: dict) -> List[str]:
    """Return a short list of first-aid suggestions tailored to symptoms and severity.

    Falls back to simple rules if LLM not available.
    """
    # Basic fallback rules
    if not _HAS_OPENAI:
        out = []
        s = set([x.lower() for x in (symptoms or [])])
        if "chest pain" in s:
            out.append("Keep the person calm and seated; call emergency services immediately.")
        if "shortness of breath" in s or "dyspnea" in s:
            out.append("Help the person sit upright and monitor breathing; seek urgent care if severe.")
        if "fever" in s:
            out.append("Keep hydrated and use a cool compress; monitor temperature.")
        if not out:
            out.append("Monitor symptoms closely and seek medical attention if they worsen.")
        return out

    # Build prompt
    prompt = f"Patient symptoms: {', '.join(symptoms or [])}\nSeverity: {severity}\nVitals: {vitals}\n\nProvide 3 concise, prioritized first-aid actions (each on its own line), starting with the most urgent. Keep each action <= 120 characters. Emphasize safety and when to call emergency services." 
    resp = _call_chat(prompt, temperature=0.2, max_tokens=200)
    if not resp:
        return []
    # Split into lines and clean
    lines = [l.strip(" -\n\r") for l in resp.splitlines() if l.strip()]
    # If the model returned a single paragraph, attempt to split by sentence
    if len(lines) == 1 and "." in lines[0]:
        parts = [p.strip() for p in lines[0].split('.') if p.strip()]
        return [p + '.' for p in parts][:3]
    return lines[:5]


def explain_recommendations(specialties: List[str], severity: str, drivers: List[str]) -> str:
    """Return a short human-friendly explanation for why the recommended specialties and actions were chosen."""
    if not _HAS_OPENAI:
        return f"Recommended specialties: {', '.join(specialties)}. Priority based on severity {severity} and drivers: {', '.join(drivers)}."
    prompt = f"Explain in one short paragraph why the following specialties are recommended: {', '.join(specialties)}. Severity: {severity}. Key drivers: {', '.join(drivers)}. Keep it under 60 words and use non-technical language." 
    resp = _call_chat(prompt, temperature=0.2, max_tokens=150)
    return resp or ""


def generate_case_report(case_summary: dict, similar_cases: List[str] = None) -> dict:
    """Generate a detailed case report using OpenAI if available.

    Returns a dict with keys: summary_text (string) and first_aid (list).
    Falls back to rule-based report when LLM not available.
    """
    if similar_cases is None:
        similar_cases = []
    if not _HAS_OPENAI:
        # Build a simple textual summary and reuse generate_personalized_first_aid
        first_aid = generate_personalized_first_aid(case_summary.get('symptoms', []), case_summary.get('severity', ''), case_summary.get('vitals', {}))
        summary_text = f"Case for {case_summary.get('patientName','Unknown')}: severity={case_summary.get('severity')}. Symptoms: {', '.join(case_summary.get('symptoms',[]))}."
        return {"summary_text": summary_text, "first_aid": first_aid}

    # Build prompt with similar cases (RAG)
    sim_text = '\n---\n'.join(similar_cases[:3]) if similar_cases else ''
    prompt = f"You are a clinical triage assistant.\nProvide a concise structured report for the following case: {case_summary}\n\nSimilar prior cases:\n{sim_text}\n\nReturn a JSON object with keys: summary (short paragraph), firstAid (list of 3 short actions)."
    resp = _call_chat(prompt, temperature=0.2, max_tokens=500)
    # naive parse: try to find JSON in response
    import json
    try:
        # If the model returned JSON, parse it
        jstart = resp.find('{')
        if jstart != -1:
            j = json.loads(resp[jstart:])
            return {"summary_text": j.get('summary',''), "first_aid": j.get('firstAid', [])}
    except Exception:
        pass
    # fallback to simple parsing
    fa = generate_personalized_first_aid(case_summary.get('symptoms', []), case_summary.get('severity', ''), case_summary.get('vitals', {}))
    summary_text = resp if resp else f"Case for {case_summary.get('patientName','Unknown')}"
    return {"summary_text": summary_text, "first_aid": fa}
"""
LLM Service Module - Fallback stub for disabled LLM features
"""
from typing import Dict, List, Optional

# LLM client disabled - always returns fallback values
client = None

def generate_medical_report_narrative(report: Dict) -> str:
    """Fallback - returns standard report format."""
    return "Standard report format (LLM not available)."

def generate_personalized_first_aid(symptoms: List[str], severity: str, vitals: Dict) -> List[str]:
    """Fallback - returns empty list for rule-based recommendations."""
    return []

def clarify_symptoms(vague_symptom: str) -> Dict:
    """Fallback - returns error message."""
    return {"error": "LLM service not available"}

def explain_recommendations(specialties: List[str], severity: str, drivers: List[str]) -> str:
    """Fallback - returns empty string."""
    return ""
