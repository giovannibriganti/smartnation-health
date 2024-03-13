from pydantic import BaseModel
from typing import Optional, List

from nosql.app.app.models.diagnosis import Diagnosis

class ChatbotQuery(BaseModel):
    patient_id: str
    question: str
    chat_history: Optional[str]


class ChatbotAnswer(BaseModel):
    patient_id: int
    age: Optional[int]
    gender: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    bmi: Optional[float]
    diagnoses: List[Diagnosis] =  []
    allergies: List[str] = []
    question: str