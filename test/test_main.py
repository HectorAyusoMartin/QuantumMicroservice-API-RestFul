"""

Prueba de testing: 

                - Envia un GET a la API
                - Verifica que el código de respuesta sea un 200 OK
                - Comprueba que la respuesta tenga el mensaje que se espera

"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "El microservicio está funcionando"}  
