from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from nosql.app.app.models.patient import Patient

client =  AsyncIOMotorClient("mongodb://0.0.0.0:27017")

db = client.smartNationAI

async def init_db():
    """
    Initializes the Beanie database connection.

    This function initializes the Beanie connection to the MongoDB database and registers
    the Patient document model.

    """
    await init_beanie(database=db, document_models=[Patient])

async def close_db():
    """
    Closes the MongoDB connection.

    This function closes the connection to the MongoDB database.

    """
    db.client.close()
