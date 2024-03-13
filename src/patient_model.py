from pydantic import BaseModel


class Patient(BaseModel):
    patient_id: str
    age: str | None = None
    gender: str | None = None
    height: str | None = None
    weight: str | None = None
    bmi: str | None = None
    diagnoses: list[str] | None = []
    allergies: list[str] | None = []
