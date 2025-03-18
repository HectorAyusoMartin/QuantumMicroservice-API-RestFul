from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from app.config import MONGO_URI , JWT_SECRET
from app.routers import auth, users, quantum_random, keys, g_buffer
import os

app = FastAPI(title="Microservicio - API RESTful | FastApi | Mongo DB ATLAS | Oauth2JWT | Qiskit | Docker | Render")

g_buffer.start_buffer_thread() # --> Inicia el Daemon de la carga de buffer en segundo plano

app.include_router(auth.router,prefix="/auth",tags=["Autenticación JWT"])
app.include_router(users.router,prefix="/users",tags=["CRUD de Usuarios"])
app.include_router(quantum_random.router,prefix="/random",tags=["Generador de aleatoriedad cuántica (Quantic Number Random Generation)"])
app.include_router(keys.router,prefix="/keys",tags=["Funciones criptográficas"])
app.include_router(g_buffer.router,prefix="/buffer",tags=["Buffer cuántico de 6500 QUbits"])

# Ruta absoluta a la carpeta landing_page dentro de app/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "landing_page")
PDF_PATH = "statics/documentacion.pdf"
app.mount("/statics", StaticFiles(directory="statics"), name="statics")



app.mount("/", StaticFiles(directory=static_dir, html=True), name="landing")


                   
@app.get("/",summary="Carga el Landing Page.",tags=["Página de inicio"])

def serve_index():
    
    return FileResponse(os.path.join(static_dir, "index.html"))







     
    
          
