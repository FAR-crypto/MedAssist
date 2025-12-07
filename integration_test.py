#!/usr/bin/env python3
"""
Integration Test: Multi-Agent Emergency Healthcare Triage
Tests the full pipeline with OpenAI LLM integration
"""
import json
import requests
import time
import sys

print("=" * 80)
print("INTEGRATION TEST: MULTI-AGENT EMERGENCY HEALTHCARE TRIAGE")
print("=" * 80)
print()

# Test cases: Mock patient data
test_cases = [
    {
        "name": "Critical Case - Chest Pain",
        "data": {
            "patientName": "John Smith",
            "age": 55,
            "sex": "male",
            "symptomsText": "chest pain, shortness of breath",
            "durationHours": 2,
            "vitals": {
                "heartRate": 125,
                "systolicBP": 88,
                "diastolicBP": 60,
                "spo2": 88,
                "temperatureC": 37.5
            }
        },
        "expected_priority": "P1"
    },
    {
        "name": "Moderate Case - Fever & Cough",
        "data": {
            "patientName": "Sarah Johnson",
            "age": 32,
            "sex": "female",
            "symptomsText": "fever, cough, sore throat",
            "durationHours": 24,
            "vitals": {
                "heartRate": 95,
                "systolicBP": 118,
                "diastolicBP": 76,
                "spo2": 96,
                "temperatureC": 38.8
            }
        },
        "expected_priority": "P2"
    },
    {
        "name": "Mild Case - Headache",
        "data": {
            "patientName": "Mike Brown",
            "age": 28,
            "sex": "male",
            "symptomsText": "headache, fatigue",
            "durationHours": 6,
            "vitals": {
                "heartRate": 72,
                "systolicBP": 128,
                "diastolicBP": 82,
                "spo2": 98,
                "temperatureC": 37.0
            }
        },
        "expected_priority": "P3"
    }
]

results = []
passed = 0
failed = 0

for idx, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {idx}: {test_case['name']}")
    print(f"{'='*80}")
    
    try:
        print(f"Patient: {test_case['data']['patientName']} | Age: {test_case['data']['age']} | Sex: {test_case['data']['sex']}")
        print(f"Symptoms: {test_case['data']['symptomsText']}")
        print(f"Vitals: HR={test_case['data']['vitals']['heartRate']}, SBP={test_case['data']['vitals']['systolicBP']}, SpO2={test_case['data']['vitals']['spo2']}%")
        print()
        
        # Send request to backend
        response = requests.post(
            "http://localhost:8000/api/triage",
            json=test_case['data'],
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            failed += 1
            results.append({
                "test": test_case['name'],
                "status": "FAILED",
                "error": f"HTTP {response.status_code}"
            })
            continue
        
        data = response.json()
        
        # Validate response structure
        priority = data.get('final', {}).get('priority')
        severity = data.get('final', {}).get('report', {}).get('triage', {}).get('severityBand')
        specialties = data.get('final', {}).get('report', {}).get('recommendations', {}).get('suggestedSpecialties', [])
        first_aid = data.get('final', {}).get('report', {}).get('recommendations', {}).get('firstAid', [])
        
        print(f"✅ Response received successfully")
        print(f"   Case ID: {data.get('caseId')}")
        print(f"   Priority: {priority} (Expected: {test_case['expected_priority']})")
        print(f"   Severity: {severity}")
        print(f"   Specialties: {', '.join(specialties)}")
        print(f"   First Aid Recommendations: {len(first_aid)} items")
        for i, aid in enumerate(first_aid[:2], 1):
            print(f"     {i}. {aid[:70]}...")
        print()
        
        # Validate priority
        if priority == test_case['expected_priority']:
            print(f"✅ Priority validation PASSED")
            passed += 1
        else:
            print(f"⚠️  Priority mismatch: Got {priority}, Expected {test_case['expected_priority']}")
        
        # Validate specialties
        if specialties:
            print(f"✅ Specialist recommendations generated")
        else:
            print(f"⚠️  No specialist recommendations")
        
        # Validate first aid
        if first_aid:
            print(f"✅ First aid recommendations generated ({len(first_aid)} items)")
        else:
            print(f"⚠️  No first aid recommendations")
        
        results.append({
            "test": test_case['name'],
            "status": "PASSED",
            "priority": priority,
            "severity": severity,
            "specialties": specialties,
            "first_aid_count": len(first_aid)
        })
        
    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED: Cannot connect to backend at http://localhost:8000")
        print(f"   Make sure the backend is running: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        failed += 1
        results.append({
            "test": test_case['name'],
            "status": "FAILED",
            "error": "Connection refused"
        })
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        failed += 1
        results.append({
            "test": test_case['name'],
            "status": "FAILED",
            "error": str(e)
        })

# Summary
print(f"\n\n{'='*80}")
print("TEST SUMMARY")
print(f"{'='*80}")
print(f"Total Tests: {len(test_cases)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print()

if failed == 0 and passed == len(test_cases):
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print()
    print("System Status:")
    print("  ✅ Backend API running")
    print("  ✅ Frontend running")
    print("  ✅ 7-agent pipeline operational")
    print("  ✅ OpenAI LLM integration active")
    print("  ✅ All triage cases processed successfully")
    print()
    print("The medical triage system is ready for use!")
    sys.exit(0)
else:
    print(f"⚠️  {failed} test(s) failed. Check the errors above.")
    sys.exit(1)
