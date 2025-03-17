from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from app.config import MONGO_URI , JWT_SECRET
from app.routers import auth, users, quantum_random, keys, g_buffer
import os

app = FastAPI(title="Microservicio | APIRest. FastApi. Mongo DB ATLAS. Oauth2JWT. Qiskit. Docker. Render.")

app.include_router(auth.router,prefix="/auth",tags=["Autenticación"])
app.include_router(users.router,prefix="/users",tags=["Usuarios"])
app.include_router(quantum_random.router,prefix="/random",tags=["Aleatoriedad cuántica(QRNG)"])
app.include_router(keys.router,prefix="/keys",tags=["Generador de claves seguras(Quantum-randomness)"])
app.include_router(g_buffer.router,prefix="/buffer",tags=["Endpoints mejorados haciendo uso de un buffer global"])

# Ruta absoluta a la carpeta landing_page dentro de app/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "landing_page")
PDF_PATH = "statics/documentacion.pdf"
app.mount("/statics", StaticFiles(directory="statics"), name="statics")



app.mount("/", StaticFiles(directory=static_dir, html=True), name="landing")


                   
@app.get("/",summary="Carga el Landing Page.",tags=["Página de inicio"])
def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))


    
    
          
