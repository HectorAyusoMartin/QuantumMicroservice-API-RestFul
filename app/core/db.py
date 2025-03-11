from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from bson import ObjectId

import os

# Cargar la URI de la base de datos desde el entorno
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "microservicio"

# Conectar a MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]

#async def create_user(user: dict):
   # """Crea un nuevo usuario en la base de datos."""
    #result = await users_collection.insert_one(user)
    #return str(result.inserted_id)

async def create_user(user: dict):
    """Crea un nuevo usuario en la base de datos con la contraseña hasheada."""
    from app.core.security import get_password_hash # --> Evitando importación circular.
    if "password" in user:
        user["hashed_password"] = get_password_hash(user.pop("password"))  # ✅ Hashear la contraseña correctamente
    
    result = await users_collection.insert_one(user)
    return str(result.inserted_id)


async def get_user(username: str) -> User:
    """Recupera un usuario por su nombre de usuario."""
    user_data = await users_collection.find_one({"username": username})
    if user_data:
        return User(**user_data)
    return None

async def update_user(username: str, updated_data: dict):
    """Actualiza la información de un usuario."""
    result = await users_collection.update_one({"username": username}, {"$set": updated_data})
    return result.modified_count > 0

async def delete_user(username: str):
    """Elimina un usuario de la base de datos."""
    result = await users_collection.delete_one({"username": username})
    return result.deleted_count > 0

#async def list_users():
   # """Devuelve una lista de todos los usuarios."""
    #users = await users_collection.find().to_list(100)
    #return users

async def list_users():
    """Devuelve una lista de todos los usuarios."""
    users = await users_collection.find().to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])  # Convertir ObjectId a string
    return users