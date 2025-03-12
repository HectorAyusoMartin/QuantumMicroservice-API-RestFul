from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import MONGO_URI , JWT_SECRET
from app.routers import auth, users, quantum_random, keys
import os

app = FastAPI(title="Microservicio | APIRest. FastApi. Mongo DB ATLAS. Oauth2JWT. Qiskit. Docker. Render.")

app.include_router(auth.router,prefix="/auth",tags=["Autenticación"])
app.include_router(users.router,prefix="/users",tags=["Usuarios"])
app.include_router(quantum_random.router,prefix="/random",tags=["Aleatoriedad cuántica(QRNG)"])
app.include_router(keys.router,prefix="/keys",tags=["Generador de claves seguras(Quantum-randomness)"])

# Ruta absoluta a la carpeta landing_page dentro de app/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "landing_page")



    
# Servir archivos estáticos (CSS, JS, imágenes, etc.)



# Montamos toda la carpeta landing_page para que index.html pueda encontrar los archivos sin cambiar rutas
app.mount("/", StaticFiles(directory=static_dir, html=True), name="landing")


                   
@app.get("/",summary="Carga el Landing Page.",tags=["Página de inicio"])
def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/help",summary="Carga la documentación del proyecto",tags=["Documentación del proyecto"])
def serve_docu():
    return None



    
    
          
