from pydantic import BaseModel
from typing import Optional, List

from nosql.app.app.models.diagnosis import Diagnosis

class ChatbotQuery(BaseModel):
    """
    Represents a chatbot query.

    Attributes:
        patient_id (str): The ID of the patient.
        question (str): The query/question asked by the patient.
        chat_history (Optional[str]): The chat history, if available.

    """

    patient_id: str
    question: str
    chat_history: Optional[str]


class ChatbotAnswer(BaseModel):
    """
    Represents a chatbot answer.

    Attributes:
        patient_id (int): The ID of the patient.
        age (Optional[int]): The age of the patient.
        gender (Optional[str]): The gender of the patient.
        height (Optional[int]): The height of the patient.
        weight (Optional[int]): The weight of the patient.
        bmi (Optional[float]): The BMI (Body Mass Index) of the patient.
        diagnoses (List[Diagnosis]): A list of diagnoses.
        allergies (List[str]): A list of allergies.
        question (str): The original question/query.

    """

    patient_id: int
    age: Optional[int]
    gender: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    bmi: Optional[float]
    diagnoses: List[Diagnosis] = []
    allergies: List[str] = []
    question: str
    
