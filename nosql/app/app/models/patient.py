from beanie import Document
from typing import List, Optional

from nosql.app.app.models.diagnosis import Diagnosis

class Patient(Document):
    """
    Represents a patient.

    Inherits from Beanie's Document class.

    Attributes:
        patient_id (str): The ID of the patient.
        age (Optional[int]): The age of the patient.
        gender (Optional[str]): The gender of the patient.
        height (Optional[int]): The height of the patient.
        weight (Optional[int]): The weight of the patient.
        bmi (Optional[float]): The BMI (Body Mass Index) of the patient.
        diagnoses (List[Diagnosis]): A list of diagnoses.
        allergies (List[str]): A list of allergies.

    """

    patient_id: str
    age: Optional[int]
    gender: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    bmi: Optional[float]
    diagnoses: List[Diagnosis] = []
    allergies: List[str] = []

    class Settings:
        """
        Settings for the Patient document.

        Attributes:
            name (str): The name of the MongoDB collection for storing patient data.
        """
        name = "patients"
