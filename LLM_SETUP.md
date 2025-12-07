# OpenAI LLM Integration Setup

## Installation

The LLM layer has been integrated into the Multi-Agent Triage System. To enable it, you need to set up your OpenAI API key.

### Step 1: Get an OpenAI API Key

1. Visit [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Sign up or log in to your OpenAI account
3. Create a new API key
4. Copy the key (you'll only see it once)

### Step 2: Set Environment Variable

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

**On Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Or create a .env file in the backend directory:**
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 3: Restart Backend

```powershell
cd "c:\Users\Akshatachatter\Downloads\multi-agent triage system\backend"
& "C:/Program Files/Python312/python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Features Enabled

### 1. **Enhanced First Aid Recommendations**
- LLM generates personalized first aid steps based on patient symptoms and severity
- Falls back to rule-based recommendations if LLM is unavailable
- Example: For chest pain + high BP + age 65, it generates specific cardiac-focused first aid

### 2. **Narrative Medical Reports**
- LLM generates professional medical summaries
- Endpoint: `GET /api/case/{case_id}/narrative`
- Returns a 2-3 sentence clinical summary in professional language

### 3. **Specialist Recommendation Explanation**
- LLM explains why specific specialists are recommended
- Embedded in the triage report automatically
- Shows clinical reasoning in professional terms

### 4. **Symptom Clarification**
- Endpoint: `POST /api/clarify-symptom?symptom=chest+pain`
- LLM generates follow-up questions to clarify vague symptoms
- Useful for initial patient intake

### 5. **Multi-Language Translation**
- LLM can translate reports to any language on demand
- Extends beyond fixed language translations

## API Endpoints

### Get Narrative Report
```bash
GET http://localhost:8000/api/case/1/narrative
```

Response:
```json
{
  "caseId": "1",
  "narrative": "Patient is a 45-year-old presenting with acute chest pain and elevated heart rate. Risk assessment indicates high severity due to low oxygen saturation and abnormal vitals. Immediate cardiology consultation is recommended with emergency transport."
}
```

### Clarify Symptom
```bash
POST http://localhost:8000/api/clarify-symptom?symptom=chest+pain
```

Response:
```json
{
  "clarification": "1. Is the pain sharp or dull?\n2. Does it radiate to your arm or neck?\n3. When did it start and how long has it lasted?\n4. Is it worse with physical activity or breathing?"
}
```

## Costs

- **GPT-3.5-turbo**: ~$0.0015 per 1K tokens (very affordable)
- Each triage generates ~2-3 LLM calls
- Estimated cost: ~$0.01 per patient triaged

## Fallback Behavior

If OpenAI API is not configured or fails:
- First aid recommendations fall back to rule-based system
- Narrative generation returns a note that LLM is unavailable
- Triage system continues to work normally
- **No disruption to core functionality**

## Security Notes

- Never commit your API key to version control
- Keep API key in environment variables only
- Monitor usage on [OpenAI dashboard](https://platform.openai.com/account/billing/overview)
- Set usage limits to prevent unexpected charges

## Troubleshooting

**"LLM service not configured"**
- API key not set in environment
- Set `OPENAI_API_KEY` and restart the backend

**High latency on first aid generation**
- LLM calls add ~1-2 seconds per request
- This is normal - can be optimized with caching

**API errors**
- Check your API key is valid
- Verify you have credit on your OpenAI account
- Check rate limits: https://platform.openai.com/account/rate-limits

## Future Enhancements

- Cache LLM responses to reduce costs
- Add support for other LLM providers (Claude, Cohere, etc.)
- Implement streaming for real-time narrative generation
- Add fine-tuning for healthcare-specific language
