from pymongo import MongoClient

client = MongoClient()
from patient_model import Patient

MONGOSTRING = ""


def create_db_client():
    client = MongoClient()
    db = client.smartNationAI
    return db


def close_db_client(db) -> None:
    db.client.close()


def load_to_mongodb(patient: Patient) -> None:
    db = create_db_client()
    db.patients.insert_one(patient.dict()).inserted_id
    close_db_client(db)


def get_from_mongodb(patient_id: str) -> Patient:
    db = create_db_client()
    results = db.patients.find_one({"patient_id": patient_id})
    close_db_client(db)
    return results
