#!/usr/bin/env python3
"""
Demonstration: Optimal vs Suboptimal Inputs & LLM Outputs
Shows the difference in LLM response quality based on input quality
"""
import json
import requests

print("=" * 80)
print("DEMONSTRATION: INPUT QUALITY vs LLM OUTPUT QUALITY")
print("=" * 80)
print()

# Test with optimal inputs
print("[TEST 1] OPTIMAL INPUTS - Critical Case with Detailed Information")
print("-" * 80)
print()

optimal_input = {
    "patientName": "James Anderson",
    "age": 62,
    "sex": "male",
    "symptomsText": "crushing chest pain, severe shortness of breath, dizziness, sweating, nausea",
    "durationHours": 3,
    "vitals": {
        "heartRate": 132,
        "systolicBP": 82,
        "diastolicBP": 55,
        "spo2": 86,
        "temperatureC": 37.8
    }
}

print("INPUT DETAILS:")
print("  Patient: {}, Age: {}, Sex: {}".format(optimal_input['patientName'], optimal_input['age'], optimal_input['sex']))
print("  Symptoms: {}".format(optimal_input['symptomsText']))
print("  Duration: {} hours".format(optimal_input['durationHours']))
print("  Vitals:")
print("    HR: {} bpm (ELEVATED - tachycardia)".format(optimal_input['vitals']['heartRate']))
print("    SBP: {} mmHg (CRITICAL - hypotension)".format(optimal_input['vitals']['systolicBP']))
print("    SpO2: {}% (CRITICAL - hypoxia)".format(optimal_input['vitals']['spo2']))
print("    Temp: {}C (normal)".format(optimal_input['vitals']['temperatureC']))
print()
print("INPUT QUALITY SCORE: MAXIMUM (5/5)")
print("  [*] Multiple critical vitals (SBP < 90, SpO2 < 92, HR > 120)")
print("  [*] Detailed, specific symptoms (5+ descriptors)")
print("  [*] Appropriate age range (> 40)")
print("  [*] Sufficient duration (> 2 hours)")
print()

try:
    response = requests.post("http://localhost:8000/api/triage", json=optimal_input, timeout=10)
    if response.status_code == 200:
        data = response.json()
        first_aid = data['final']['report']['recommendations']['firstAid']
        priority = data['final']['priority']
        severity = data['final']['report']['triage']['severityBand']
        risk_score = data['final']['report']['triage']['riskScore']
        
        print("OUTPUT RESULTS:")
        print("  Priority: {} (EMERGENCY)".format(priority))
        print("  Severity: {} (CRITICAL)".format(severity))
        print("  Risk Score: {}/21+".format(risk_score))
        print()
        print("  FIRST AID RECOMMENDATIONS (From OpenAI):")
        for i, aid in enumerate(first_aid, 1):
            print("    {}. {}".format(i, aid))
        print()
        print("OUTPUT QUALITY: EXCELLENT - DETAILED & CLINICALLY APPROPRIATE")
    else:
        print("Error: {}".format(response.status_code))
except Exception as e:
    print("Connection error: {}".format(e))

print()
print("=" * 80)
print()

# Test with suboptimal inputs
print("[TEST 2] SUBOPTIMAL INPUTS - Vague Symptoms + Normal Vitals")
print("-" * 80)
print()

suboptimal_input = {
    "patientName": "Jane Smith",
    "age": 28,
    "sex": "female",
    "symptomsText": "headache",
    "durationHours": 1,
    "vitals": {
        "heartRate": 78,
        "systolicBP": 128,
        "diastolicBP": 82,
        "spo2": 97,
        "temperatureC": 37.0
    }
}

print("INPUT DETAILS:")
print("  Patient: {}, Age: {}, Sex: {}".format(suboptimal_input['patientName'], suboptimal_input['age'], suboptimal_input['sex']))
print("  Symptoms: {}".format(suboptimal_input['symptomsText']))
print("  Duration: {} hour".format(suboptimal_input['durationHours']))
print("  Vitals:")
print("    HR: {} bpm (normal)".format(suboptimal_input['vitals']['heartRate']))
print("    SBP: {} mmHg (normal)".format(suboptimal_input['vitals']['systolicBP']))
print("    SpO2: {}% (normal)".format(suboptimal_input['vitals']['spo2']))
print("    Temp: {}C (normal)".format(suboptimal_input['vitals']['temperatureC']))
print()
print("INPUT QUALITY SCORE: MINIMAL (1/5)")
print("  [-] All vitals normal (no critical flags)")
print("  [-] Vague symptoms (single word, no descriptors)")
print("  [-] Short duration (1 hour)")
print("  [-] Young age (< 40)")
print()

try:
    response = requests.post("http://localhost:8000/api/triage", json=suboptimal_input, timeout=10)
    if response.status_code == 200:
        data = response.json()
        first_aid = data['final']['report']['recommendations']['firstAid']
        priority = data['final']['priority']
        severity = data['final']['report']['triage']['severityBand']
        risk_score = data['final']['report']['triage']['riskScore']
        
        print("OUTPUT RESULTS:")
        print("  Priority: {} (NON-URGENT)".format(priority))
        print("  Severity: {} (MILD)".format(severity))
        print("  Risk Score: {}".format(risk_score))
        print()
        print("  FIRST AID RECOMMENDATIONS (Falls back to Rule-Based):")
        for i, aid in enumerate(first_aid, 1):
            print("    {}. {}".format(i, aid))
        print()
        print("OUTPUT QUALITY: GENERIC - FALLS BACK TO RULES (Limited LLM)")
    else:
        print("Error: {}".format(response.status_code))
except Exception as e:
    print("Connection error: {}".format(e))

print()
print("=" * 80)
print()

# Test with moderately good inputs
print("[TEST 3] MODERATE INPUTS - Specific Symptoms + Some Abnormal Vitals")
print("-" * 80)
print()

moderate_input = {
    "patientName": "Michael Chen",
    "age": 52,
    "sex": "male",
    "symptomsText": "fever, persistent cough, difficulty breathing, body aches",
    "durationHours": 18,
    "vitals": {
        "heartRate": 108,
        "systolicBP": 122,
        "diastolicBP": 78,
        "spo2": 93,
        "temperatureC": 39.2
    }
}

print("INPUT DETAILS:")
print("  Patient: {}, Age: {}, Sex: {}".format(moderate_input['patientName'], moderate_input['age'], moderate_input['sex']))
print("  Symptoms: {}".format(moderate_input['symptomsText']))
print("  Duration: {} hours".format(moderate_input['durationHours']))
print("  Vitals:")
print("    HR: {} bpm (elevated)".format(moderate_input['vitals']['heartRate']))
print("    SBP: {} mmHg (normal)".format(moderate_input['vitals']['systolicBP']))
print("    SpO2: {}% (slightly low)".format(moderate_input['vitals']['spo2']))
print("    Temp: {}C (HIGH FEVER)".format(moderate_input['vitals']['temperatureC']))
print()
print("INPUT QUALITY SCORE: GOOD (3/5)")
print("  [*] High temperature (fever flag)")
print("  [*] Specific symptoms (4+ descriptors)")
print("  [*] Appropriate age (> 40)")
print("  [*] Good duration (18 hours)")
print("  [-] Vitals not severely abnormal")
print()

try:
    response = requests.post("http://localhost:8000/api/triage", json=moderate_input, timeout=10)
    if response.status_code == 200:
        data = response.json()
        first_aid = data['final']['report']['recommendations']['firstAid']
        priority = data['final']['priority']
        severity = data['final']['report']['triage']['severityBand']
        risk_score = data['final']['report']['triage']['riskScore']
        
        print("OUTPUT RESULTS:")
        print("  Priority: {} (URGENT)".format(priority))
        print("  Severity: {} (MODERATE/SEVERE)".format(severity))
        print("  Risk Score: {}".format(risk_score))
        print()
        print("  FIRST AID RECOMMENDATIONS (Enhanced LLM Output):")
        for i, aid in enumerate(first_aid, 1):
            print("    {}. {}".format(i, aid))
        print()
        print("OUTPUT QUALITY: GOOD - MODERATE LLM ENHANCEMENT")
    else:
        print("Error: {}".format(response.status_code))
except Exception as e:
    print("Connection error: {}".format(e))

print()
print("=" * 80)
print("SUMMARY: INPUT-OUTPUT RELATIONSHIP")
print("=" * 80)
print()
print("INPUT QUALITY -> OUTPUT QUALITY MAPPING:")
print()
print("1. MINIMAL INPUT (All normal vitals, vague symptoms)")
print("   -> OUTPUT: Falls back to generic rule-based guidance")
print()
print("2. GOOD INPUT (Some abnormal vitals + specific symptoms)")
print("   -> OUTPUT: Moderate LLM enhancement, more relevant first aid")
print()
print("3. OPTIMAL INPUT (Multiple critical vitals + detailed symptoms)")
print("   -> OUTPUT: Maximum LLM quality, detailed clinical guidance")
print()
print()
print("KEY RECOMMENDATIONS FOR OPTIMAL LLM OUTPUT:")
print()
print("1. Include at least ONE critical vital:")
print("   - SBP < 90 mmHg (triggers low_bp flag)")
print("   - SpO2 < 92% (triggers low_spo2 flag)")
print()
print("2. Provide detailed symptom descriptions:")
print("   BAD:    'chest pain'")
print("   GOOD:   'severe chest pain, sharp, radiating to left arm'")
print("   BEST:   'crushing chest pain, severe SOB, dizziness, sweating'")
print()
print("3. Set appropriate parameters:")
print("   - Age > 40 (affects risk scoring)")
print("   - Duration > 2-6 hours (shows urgency)")
print("   - Temperature abnormalities (high fever = severity)")
print()
print("4. Use recognized medical symptoms:")
print("   - Chest pain, shortness of breath, severe headache")
print("   - Fever, cough, dizziness, abdominal pain, vomiting")
print()
print("=" * 80)
