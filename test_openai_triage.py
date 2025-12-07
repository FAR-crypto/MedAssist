import json
import requests
import os

# Verify key is set
print(f'OPENAI_API_KEY set: {bool(os.environ.get("OPENAI_API_KEY"))}')
print()

payload = {
    'patientName': 'Sarah Mitchell',
    'age': 52,
    'sex': 'Female',
    'symptomsText': 'chest pain, shortness of breath, severe headache, dizziness',
    'durationHours': 4,
    'vitals': {
        'heartRate': 115,
        'systolicBP': 95,
        'diastolicBP': 65,
        'spo2': 90,
        'temperatureC': 39.2
    }
}

print('=== SENDING CRITICAL CASE TO BACKEND WITH OPENAI ===')
print(f'Patient: {payload["patientName"]} (Age: {payload["age"]})')
print(f'Symptoms: {payload["symptomsText"]}')
print()

try:
    resp = requests.post('http://localhost:8000/api/triage', json=payload)
    data = resp.json()
    
    print('=== SEVERITY ASSESSMENT ===')
    print(f'Risk Score: {data["final"]["report"]["triage"]["riskScore"]}')
    print(f'Risk Tier: {data["final"]["report"]["triage"]["riskTier"]}')
    print(f'Severity Band: {data["final"]["report"]["triage"]["severityBand"].upper()}')
    print(f'Priority Level: {data["final"]["report"]["triage"]["emergencyPriority"]}')
    print()
    
    print('=== RECOMMENDED SPECIALTIES ===')
    for spec in data["final"]["report"]["recommendations"]["suggestedSpecialties"]:
        print(f'  • {spec}')
    print()
    
    print('=== FIRST AID RECOMMENDATIONS (WITH OPENAI) ===')
    for idx, aid in enumerate(data["final"]["report"]["recommendations"]["firstAid"], 1):
        print(f'{idx}. {aid}')
    print()
    
    print('=== ACTION GUIDANCE ===')
    print(data["final"]["report"]["recommendations"]["generalGuidance"])
    print()
    
    print('=== SEVERITY DRIVERS ===')
    for driver in data["final"]["report"]["rationale"]["severityDrivers"]:
        print(f'  • {driver}')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
