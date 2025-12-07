#!/usr/bin/env python3
"""
GUIDE: Proper Inputs for Optimal LLM Outputs
Medical Triage System - Input Best Practices
"""
import json
import requests

print("=" * 80)
print("GUIDE: PROPER INPUTS FOR OPTIMAL LLM OUTPUTS")
print("=" * 80)
print()

print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║           INPUT PARAMETERS & LLM OUTPUT QUALITY FACTORS                   ║")
print("╚════════════════════════════════════════════════════════════════════════════╝")
print()

print("1. PATIENT NAME")
print("   ├─ Format: String (any text)")
print("   ├─ Length: 1-100 characters")
print("   ├─ Examples: 'John Smith', 'Maria Garcia', 'Ahmed Hassan'")
print("   ├─ Impact on LLM: ✅ Shows in report header (minimal LLM impact)")
print("   └─ Best Practice: Use real or realistic names")
print()

print("2. AGE")
print("   ├─ Format: Integer (0-120)")
print("   ├─ Impact on LLM: ⭐⭐⭐ HIGH - Age affects risk scoring")
print("   ├─ Ranges:")
print("   │  ├─ < 40: Lower baseline risk")
print("   │  ├─ 40-59: Moderate risk (+1)")
print("   │  ├─ 60-74: Higher risk (+2)")
print("   │  └─ 75+: Highest risk (+3)")
print("   └─ Examples: 25, 45, 65, 78")
print()

print("3. SEX")
print("   ├─ Format: String ('male' or 'female')")
print("   ├─ Impact on LLM: ✅ Minimal (informational)")
print("   └─ Examples: 'male', 'female', 'unspecified'")
print()

print("4. SYMPTOMS (CRITICAL FOR LLM)")
print("   ├─ Format: Comma or newline separated list")
print("   ├─ Impact on LLM: ⭐⭐⭐⭐⭐ CRITICAL - Drives all recommendations")
print("   ├─ Recognized Symptoms:")
print("   │  ├─ 'chest pain' → Cardiology (+4 risk)")
print("   │  ├─ 'shortness of breath' → Pulmonology (+3 risk)")
print("   │  ├─ 'severe headache' → Neurology (+2 risk)")
print("   │  ├─ 'fever' → General Medicine (+0 base, flag dependent)")
print("   │  ├─ 'cough' → General Medicine")
print("   │  ├─ 'dizziness' → Neurology")
print("   │  ├─ 'abdominal pain' → Gastroenterology")
print("   │  └─ 'vomiting' → Gastroenterology")
print("   ├─ LLM Output Improvement:")
print("   │  └─ More detailed symptoms = More specific first aid from OpenAI")
print("   └─ Examples:")
print("      GOOD:    'chest pain, shortness of breath, sweating'")
print("      BETTER:  'severe chest pain, shortness of breath, dizziness, sweating'")
print("      BEST:    'crushing chest pain, severe shortness of breath, dizziness, sweating, nausea'")
print()

print("5. DURATION (Hours)")
print("   ├─ Format: Integer (0-720)")
print("   ├─ Impact on LLM: ⭐⭐⭐ MODERATE - Affects severity assessment")
print("   ├─ Risk Scoring:")
print("   │  ├─ < 24h: No risk bonus")
print("   │  ├─ 24-72h: +1 risk")
print("   │  └─ ≥ 72h: +2 risk")
print("   └─ Examples: 1, 6, 24, 48, 72, 120")
print()

print("6. VITAL SIGNS (MOST IMPORTANT FOR LLM)")
print("   ├─ Impact on LLM: ⭐⭐⭐⭐⭐ CRITICAL - Determines severity band")
print("   │")
print("   ├─ HEART RATE (HR) - Beats per minute")
print("   │  ├─ Normal: 60-100 bpm")
print("   │  ├─ Alert Threshold: > 120 bpm (+2 risk, tachycardia flag)")
print("   │  └─ Examples: 72, 95, 120, 135, 150")
print("   │")
print("   ├─ SYSTOLIC BP (SBP) - Top number")
print("   │  ├─ Normal: 110-130 mmHg")
print("   │  ├─ CRITICAL: < 90 mmHg (+3 risk, low_bp flag) 🚨")
print("   │  ├─ Alert: > 140 mmHg")
print("   │  └─ Examples: 56, 88, 118, 140, 160")
print("   │")
print("   ├─ DIASTOLIC BP (DBP) - Bottom number")
print("   │  ├─ Normal: 70-85 mmHg")
print("   │  ├─ Alert: < 60 or > 95 mmHg")
print("   │  └─ Examples: 60, 76, 82, 95")
print("   │")
print("   ├─ OXYGEN SATURATION (SpO2) - Percentage")
print("   │  ├─ Normal: 95-100%")
print("   │  ├─ CRITICAL: < 92% (+4 risk, low_spo2 flag) 🚨")
print("   │  └─ Examples: 88, 90, 92, 96, 98")
print("   │")
print("   └─ TEMPERATURE (°C)")
print("      ├─ Normal: 36.5-37.5°C")
print("      ├─ Alert: ≥ 39°C (+1 risk, high_fever flag)")
print("      └─ Examples: 37.0, 38.0, 38.8, 39.0, 39.5")
print()

print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║                    TEST CASES FOR OPTIMAL LLM OUTPUT                      ║")
print("╚════════════════════════════════════════════════════════════════════════════╝")
print()

test_cases = [
    {
        "title": "CRITICAL CASE - Full LLM Activation",
        "description": "Multiple critical vitals + specific symptoms",
        "payload": {
            "patientName": "Robert Martinez",
            "age": 58,
            "sex": "male",
            "symptomsText": "severe chest pain, shortness of breath, dizziness, nausea, sweating",
            "durationHours": 2,
            "vitals": {
                "heartRate": 128,
                "systolicBP": 85,
                "diastolicBP": 58,
                "spo2": 87,
                "temperatureC": 37.2
            }
        },
        "expected": {
            "priority": "P1",
            "severity": "CRITICAL",
            "risk_score": 20,
            "llm_quality": "MAXIMUM - Multiple critical flags trigger extensive LLM analysis"
        }
    },
    {
        "title": "MODERATE CASE - Good LLM Output",
        "description": "Some vitals abnormal + descriptive symptoms",
        "payload": {
            "patientName": "Jennifer Wong",
            "age": 42,
            "sex": "female",
            "symptomsText": "fever, persistent cough, chest discomfort, fatigue, chills",
            "durationHours": 36,
            "vitals": {
                "heartRate": 102,
                "systolicBP": 125,
                "diastolicBP": 80,
                "spo2": 94,
                "temperatureC": 39.1
            }
        },
        "expected": {
            "priority": "P2",
            "severity": "SEVERE",
            "risk_score": 7,
            "llm_quality": "HIGH - Temperature + duration flags + fever symptoms"
        }
    },
    {
        "title": "MILD CASE - Reduced LLM Output",
        "description": "Normal vitals + minimal symptoms",
        "payload": {
            "patientName": "David Kumar",
            "age": 34,
            "sex": "male",
            "symptomsText": "mild headache, slight fatigue",
            "durationHours": 8,
            "vitals": {
                "heartRate": 72,
                "systolicBP": 128,
                "diastolicBP": 82,
                "spo2": 98,
                "temperatureC": 37.0
            }
        },
        "expected": {
            "priority": "P3",
            "severity": "MILD",
            "risk_score": 0,
            "llm_quality": "LOW - No critical flags, falls back to rule-based"
        }
    }
]

print("Test Case 1: CRITICAL CASE")
print(f"  Patient: {test_cases[0]['payload']['patientName']}")
print(f"  Symptoms: {test_cases[0]['payload']['symptomsText']}")
print(f"  Vitals:")
print(f"    • HR: {test_cases[0]['payload']['vitals']['heartRate']} bpm (ELEVATED)")
print(f"    • SBP: {test_cases[0]['payload']['vitals']['systolicBP']} mmHg 🚨 (CRITICAL)")
print(f"    • SpO2: {test_cases[0]['payload']['vitals']['spo2']}% 🚨 (CRITICAL)")
print(f"    • Temp: {test_cases[0]['payload']['vitals']['temperatureC']}°C")
print(f"  Expected Priority: {test_cases[0]['expected']['priority']}")
print(f"  LLM Output Quality: {test_cases[0]['expected']['llm_quality']}")
print()

print("Test Case 2: MODERATE CASE")
print(f"  Patient: {test_cases[1]['payload']['patientName']}")
print(f"  Symptoms: {test_cases[1]['payload']['symptomsText']}")
print(f"  Vitals:")
print(f"    • HR: {test_cases[1]['payload']['vitals']['heartRate']} bpm (elevated)")
print(f"    • SBP: {test_cases[1]['payload']['vitals']['systolicBP']} mmHg (normal)")
print(f"    • SpO2: {test_cases[1]['payload']['vitals']['spo2']}% (normal)")
print(f"    • Temp: {test_cases[1]['payload']['vitals']['temperatureC']}°C (ELEVATED)")
print(f"  Expected Priority: {test_cases[1]['expected']['priority']}")
print(f"  LLM Output Quality: {test_cases[1]['expected']['llm_quality']}")
print()

print("Test Case 3: MILD CASE")
print(f"  Patient: {test_cases[2]['payload']['patientName']}")
print(f"  Symptoms: {test_cases[2]['payload']['symptomsText']}")
print(f"  Vitals:")
print(f"    • HR: {test_cases[2]['payload']['vitals']['heartRate']} bpm (normal)")
print(f"    • SBP: {test_cases[2]['payload']['vitals']['systolicBP']} mmHg (normal)")
print(f"    • SpO2: {test_cases[2]['payload']['vitals']['spo2']}% (normal)")
print(f"    • Temp: {test_cases[2]['payload']['vitals']['temperatureC']}°C (normal)")
print(f"  Expected Priority: {test_cases[2]['expected']['priority']}")
print(f"  LLM Output Quality: {test_cases[2]['expected']['llm_quality']}")
print()

print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║                      LLM OUTPUT QUALITY CHECKLIST                         ║")
print("╚════════════════════════════════════════════════════════════════════════════╝")
print()

print("✅ MAXIMUM LLM OUTPUT (Critical cases):")
print("   Requirements:")
print("   ├─ SBP < 90 OR SpO2 < 92 (at least one critical vital)")
print("   ├─ Temp ≥ 39°C (fever flag)")
print("   ├─ Specific symptoms (5+ words describing condition)")
print("   ├─ Age > 40")
print("   └─ Duration > 2 hours")
print()
print("   LLM Response: 2-3 detailed, clinically-appropriate first aid steps")
print()

print("⭐ GOOD LLM OUTPUT (Moderate cases):")
print("   Requirements:")
print("   ├─ HR > 100 OR Temp ≥ 38.5°C")
print("   ├─ Specific symptoms (fever, cough, chest discomfort, etc.)")
print("   ├─ Duration > 12 hours")
print("   └─ Age 30-65")
print()
print("   LLM Response: 1-2 relevant first aid recommendations")
print()

print("⚠️  LIMITED LLM OUTPUT (Mild cases):")
print("   Characteristics:")
print("   ├─ All vitals normal (HR 60-100, SBP 110-140, SpO2 >95, Temp <38)")
print("   ├─ Vague symptoms (just 'headache', 'fatigue')")
print("   ├─ Duration < 6 hours")
print("   └─ No critical flags")
print()
print("   LLM Response: Falls back to rule-based generic guidance")
print()

print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║                    HOW TO MAXIMIZE LLM OUTPUT QUALITY                     ║")
print("╚════════════════════════════════════════════════════════════════════════════╝")
print()

print("STEP 1: Input At Least ONE Critical Vital")
print("   ├─ Set SBP < 90 mmHg  (triggers low_bp flag)")
print("   └─ Set SpO2 < 92%     (triggers low_spo2 flag)")
print()

print("STEP 2: Include Specific Symptom Details")
print("   ❌ BAD:    'chest pain'")
print("   ✅ GOOD:   'severe chest pain, sharp, radiating to left arm'")
print("   ✅ BETTER: 'crushing chest pain, radiating to left arm and jaw, shortness of breath'")
print()

print("STEP 3: Add Duration (increases risk assessment)")
print("   ├─ 2-6 hours: Some urgency")
print("   ├─ 6-24 hours: Moderate urgency")
print("   └─ 24+ hours: High urgency")
print()

print("STEP 4: Combine Multiple Abnormal Vitals")
print("   ├─ SBP < 90 + HR > 120 = VERY CRITICAL")
print("   ├─ SpO2 < 92 + HR > 120 = VERY CRITICAL")
print("   └─ High Temp + Duration + Symptoms = MODERATE TO CRITICAL")
print()

print("STEP 5: Use Recognized Symptom Keywords")
print("   ├─ Chest pain")
print("   ├─ Shortness of breath")
print("   ├─ Severe headache")
print("   ├─ Fever")
print("   ├─ Cough")
print("   ├─ Dizziness")
print("   ├─ Abdominal pain")
print("   └─ Vomiting")
print()

print("=" * 80)
print("READY TO TEST? Run integration_test.py to see LLM in action!")
print("=" * 80)
