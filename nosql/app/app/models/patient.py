from beanie import Document
from typing import List, Optional

from nosql.app.app.models.diagnosis import Diagnosis

class Patient(Document):
    patient_id: str
    age: Optional[int]
    gender: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    bmi: Optional[float]
    diagnoses: List[Diagnosis] =  []
    allergies: List[str] = []

    class Settings:
        name = "patients"



