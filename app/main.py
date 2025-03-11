from fastapi import FastAPI
from app.config import MONGO_URI , JWT_SECRET
from app.routers import auth, users, quantum_random, keys

app = FastAPI(title="Microservicio de generación de aleatoriedad cuántica")

app.include_router(auth.router,prefix="/auth",tags=["Autenticación"])
app.include_router(users.router,prefix="/users",tags=["Usuarios"])
app.include_router(quantum_random.router,prefix="/random",tags=["Aleatoriedad cuántica(QRNG)"])
app.include_router(keys.router,prefix="/keys",tags=["Generador de claves seguras(Quantum-randomness)"])

                   
                   
@app.get("/")
async def root():
    return{
        "meesage":"El microservicio está funcionando",
        "mongo_uri": MONGO_URI,
        "jwt_secret": JWT_SECRET
    }


