import os
import json

try:
    from llm_service import generate_case_report
    print('✓ OpenAI LLM Service Available')
    print(f'✓ OPENAI_API_KEY is set: {bool(os.environ.get("OPENAI_API_KEY"))}')
    
    # Test with a sample case
    case = {
        'patientName': 'Test Patient',
        'age': 45,
        'symptoms': ['chest pain', 'shortness of breath'],
        'severity': 'severe'
    }
    
    result = generate_case_report(case, [])
    if result:
        print('✓ OpenAI API Call Successful')
        print('\n=== LLM GENERATED REPORT ===')
        print(json.dumps(result, indent=2))
    else:
        print('No LLM response received')
except ImportError as e:
    print(f'Error importing LLM service: {e}')
except Exception as e:
    print(f'Error calling OpenAI: {type(e).__name__}: {e}')
