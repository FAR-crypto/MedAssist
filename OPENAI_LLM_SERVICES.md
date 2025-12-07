# OpenAI LLM Service - Capabilities Overview

## Active Services Provided

The OpenAI LLM service provides **4 main functions** for medical triage assistance:

---

## 1. **generate_case_report(case_summary: dict, similar_cases: List[str]) → dict**

**Purpose:** Generate a detailed clinical case report with OpenAI (ChatGPT) integration and RAG (Retrieval-Augmented Generation).

**Input:**
- `case_summary` (dict): Patient case information
  - `patientName`: Patient identifier
  - `age`: Patient age
  - `sex`: Patient gender
  - `symptoms`: List of reported symptoms
  - `durationHours`: Duration of symptoms
  - `vitals`: Vital signs (HR, BP, SpO2, temp)
  - `severity`: Clinical severity band (mild/moderate/severe/critical)

- `similar_cases` (List[str]): Prior similar cases for RAG context (optional)

**Output:** Dictionary with keys:
- `summary_text`: Concise clinical summary (short paragraph)
- `first_aid`: List of 3+ prioritized first-aid actions

**Behavior:**
- If OpenAI unavailable or API key not set → Falls back to rule-based logic
- Uses `gpt-3.5-turbo` (or configurable via `OPENAI_MODEL` env var)
- Temperature: 0.2 (low randomness, more deterministic)
- Max tokens: 500

**Example Output:**
```json
{
  "summary_text": "Case for Sarah Mitchell: severity=critical. Symptoms: chest pain, shortness of breath, severe headache, dizziness.",
  "first_aid": [
    "Keep the person calm and seated. Call emergency services immediately.",
    "Help the person sit upright. Loosen tight clothing. Seek medical help if severe.",
    "Do not give anything by mouth. Monitor breathing and pulse. Be ready to perform CPR if needed."
  ]
}
```

---

## 2. **generate_personalized_first_aid(symptoms: List[str], severity: str, vitals: dict) → List[str]**

**Purpose:** Generate tailored first-aid recommendations based on patient symptoms and severity.

**Input:**
- `symptoms`: List of patient symptoms (e.g., ["chest pain", "shortness of breath"])
- `severity`: Severity classification (mild/moderate/severe/critical)
- `vitals`: Patient vital signs dictionary

**Output:** List of 3-5 concise, actionable first-aid steps

**Behavior:**
- Each action ≤ 120 characters for brevity
- Actions ordered by urgency (most critical first)
- Emphasizes when to call emergency services
- Falls back to simple rules if LLM unavailable

**Example Output:**
```
[
  "Keep the person calm and seated; call emergency services immediately.",
  "Help the person sit upright and monitor breathing; seek urgent care if severe.",
  "Keep hydrated and use a cool compress; monitor temperature."
]
```

---

## 3. **explain_recommendations(specialties: List[str], severity: str, drivers: List[str]) → str**

**Purpose:** Provide human-friendly, non-technical explanation for recommended medical specialties.

**Input:**
- `specialties`: List of recommended specialist types (e.g., ["Cardiology", "Neurology"])
- `severity`: Clinical severity level
- `drivers`: Key clinical drivers for the recommendation (e.g., ["Low oxygen saturation", "Chest pain"])

**Output:** Single paragraph explanation (< 60 words, non-technical language)

**Behavior:**
- Converts clinical jargon to patient-friendly language
- Explains WHY each specialty is recommended
- Falls back to simple format if LLM unavailable

**Example Output:**
```
"Because of your low oxygen levels, rapid heartbeat, and chest pain, we recommend seeing a cardiologist 
(heart specialist) and pulmonologist (lung specialist) who can check for heart and breathing problems."
```

---

## 4. **_call_chat(prompt: str, temperature: float, max_tokens: int) → str**

**Purpose:** Internal helper function to call OpenAI ChatCompletion API.

**System Prompt:**
```
"You are a helpful medical triage assistant. Provide concise, safety-first 
first-aid steps and explainable recommendations. Keep answers short."
```

**Parameters:**
- `prompt`: Custom instruction for the LLM
- `temperature`: 0.2 (low creativity, deterministic responses)
- `max_tokens`: 200-500 depending on use case

**Behavior:**
- Returns empty string if API call fails
- Graceful degradation if OPENAI_API_KEY not set
- Model: `gpt-3.5-turbo` (or env var `OPENAI_MODEL`)

---

## Integration Points in Medical Triage Pipeline

### Where Each Service is Used:

1. **medical_report_agent()** (agents.py, line ~320)
   - Calls `generate_case_report()` to create enhanced patient report
   - Generates first aid recommendations with LLM context
   - Falls back to rule-based recommendations if LLM unavailable

2. **agents.py import block** (lines 8-15)
   - Imports: `generate_personalized_first_aid`, `explain_recommendations`
   - Sets `LLM_AVAILABLE = True` if import succeeds
   - Defines fallback functions if import fails

---

## Fallback Behavior

If **OpenAI unavailable or API key not set**, the system:
- Still generates medical recommendations via rule-based logic
- Uses symptom/vital pattern matching instead of LLM
- Returns safe, evidence-based defaults
- Ensures system continues functioning without external dependencies

---

## Configuration

**Environment Variables:**
- `OPENAI_API_KEY`: Required for LLM service activation
  - Set via: `$env:OPENAI_API_KEY = "sk-..."` (PowerShell temp)
  - Or: `setx OPENAI_API_KEY "sk-..."` (Windows persistent)

- `OPENAI_MODEL`: Optional model selection
  - Default: `gpt-3.5-turbo`
  - Alternative: `gpt-4`, `gpt-4-turbo-preview`, etc.

---

## Current Status (as of Dec 7, 2025)

✅ **OpenAI LLM Service: ACTIVE**
- API Key: Set and loaded
- Model: gpt-3.5-turbo
- All 4 functions operational
- Backend integration: Working
- Frontend: Running on port 8080, Backend: port 8000

**Test Results:**
- Generate case report: ✅ Success
- First aid generation: ✅ Success
- Explanation generation: ✅ Success
- Integration with 7-agent pipeline: ✅ Complete
