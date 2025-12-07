from pydantic import BaseModel, Field  # type: ignore
from typing import List, Optional

class Vitals(BaseModel):
    heartRate: Optional[float] = None
    systolicBP: Optional[float] = None
    diastolicBP: Optional[float] = None
    spo2: Optional[float] = None
    temperatureC: Optional[float] = None

class TriageRequest(BaseModel):
    patientName: Optional[str] = ""
    age: Optional[int] = Field(None, ge=0, le=120)
    sex: Optional[str] = "unspecified"
    symptomsText: Optional[str] = ""
    durationHours: Optional[float] = Field(None, ge=0)
    vitals: Vitals
    locationHint: Optional[str] = "Community Zone A"

class AgentOutput(BaseModel):
    agent: str
    timestamp: str
    data: dict

class TriageResponse(BaseModel):
    caseId: str
    createdAt: str
    ledger: List[dict]
    final: dict