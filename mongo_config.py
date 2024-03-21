from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import motor.motor_asyncio
import datetime
from config import DB_USER, DB_PASS


uri = f"mongodb+srv://artemyavtushieenko:SjCImCQWemzRyJHl@cluster0.rd276wj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a new async client and connect to the server
# client = motor.motor_asyncio.AsyncIOMotorClient(uri)

# Create a new async client and connect to the server
# async def init_db():
#     client = motor.motor_asyncio.AsyncIOMotorClient(uri, uuidRepresentation="standard")
#     await init_beanie(database=client.db_name, document_models=[User])


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.test_db

users_collection = db.users
files_collection = db.files














