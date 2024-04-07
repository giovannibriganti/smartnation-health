from pymongo import MongoClient
from patient_model import Patient

client = MongoClient()

MONGOSTRING = ""


def create_db_client() -> MongoClient:
    """
    Creates a MongoDB client and returns the database instance.

    Returns:
        MongoClient: The MongoDB client instance.
    """
    client = MongoClient()
    db = client.smartNationAI
    return db


def close_db_client(db: MongoClient) -> None:
    """
    Closes the MongoDB client.

    Args:
        db (MongoClient): The MongoDB client instance.
    """
    db.client.close()


def load_to_mongodb(patient: Patient) -> None:
    """
    Loads a patient object into the MongoDB database.

    Args:
        patient (Patient): The patient object to be loaded into the database.
    """
    db = create_db_client()
    db.patients.insert_one(patient.dict()).inserted_id
    close_db_client(db)


def get_from_mongodb(patient_id: str) -> Patient:
    """
    Retrieves a patient object from the MongoDB database based on the provided patient ID.

    Args:
        patient_id (str): The ID of the patient to retrieve from the database.

    Returns:
        Patient: The patient object retrieved from the database.
    """
    db = create_db_client()
    results = db.patients.find_one({"patient_id": patient_id})
    close_db_client(db)
    return results

