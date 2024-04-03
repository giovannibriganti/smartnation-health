from pydantic import BaseModel

class Patient(BaseModel):
    """
    Represents a patient with various attributes.

    Attributes:
        patient_id (str): The unique identifier of the patient.
        age (str, optional): The age of the patient. Defaults to None.
        gender (str, optional): The gender of the patient. Defaults to None.
        height (str, optional): The height of the patient. Defaults to None.
        weight (str, optional): The weight of the patient. Defaults to None.
        bmi (str, optional): The BMI (Body Mass Index) of the patient. Defaults to None.
        diagnoses (list[str], optional): List of diagnoses associated with the patient. 
            Defaults to an empty list.
        allergies (list[str], optional): List of allergies associated with the patient. 
            Defaults to an empty list.
    """
    patient_id: str
    age: str | None = None
    gender: str | None = None
    height: str | None = None
    weight: str | None = None
    bmi: str | None = None
    diagnoses: list[str] | None = []
    allergies: list[str] | None = []
