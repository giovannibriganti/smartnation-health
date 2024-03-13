from fastapi import APIRouter, HTTPException, status

from nosql.app.app.models.patient import Patient
from nosql.app.app.models.chatbot_query import ChatbotQuery, ChatbotAnswer

router = APIRouter()

@router.get("/patients/{id}", response_description="Patient info card", status_code=status.HTTP_200_OK)
async def get_patient_info(id: str) -> Patient:
    patient = await Patient.find_one(Patient.patient_id == id)
    print(f"patient: {patient}")
    if(patient == None):
        raise HTTPException(
            status_code=204,
            detail="Patient with provided ID not found"
        )
    else:
        return patient

@router.post("/patients", response_description="New patient added", status_code=status.HTTP_201_CREATED)
async def post_patient(patient: Patient) -> None:
    await patient.create()

@router.post("/chatbot", response_description="Patient found", status_code=status.HTTP_200_OK)
async def chabot_query(query: ChatbotQuery):
    patient = await Patient.find_one(Patient.patient_id == query.patient_id)
    if(patient == None):
        raise HTTPException(
            status_code=204,
            detail="Patient with provided ID not found"
        )
    else:
        return ChatbotAnswer(
            patient.patient_id,
            patient.age,
            patient.gender,
            patient.height,
            patient.weight,
            patient.bmi,
            patient.diagnoses,
            patient.allergies,
            query.question
        )



