from pydantic import BaseModel

class Diagnosis(BaseModel):
    term: str
    id: str