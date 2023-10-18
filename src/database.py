from motor.motor_asyncio import AsyncIOMotorClient


async def get_async_session():
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
    database = client["SN_API"]
    return database
