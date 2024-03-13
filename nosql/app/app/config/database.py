from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from nosql.app.app.models.patient import Patient

client =  AsyncIOMotorClient("mongodb://0.0.0.0:27017")

db = client.smartNationAI
async def init_db():
    await init_beanie(database = db, document_models=[Patient])


async def close_db():
    db.client.close()