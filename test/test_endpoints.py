import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


# TEST(1) --> Creación de usuario y verificación de que es posible su posterior autenticación.
@pytest.mark.asyncio
async def test_register_user():
    """
    - Primero se loguea como admin para obtener un token JWT.
    - Luego, usa el token para crear un usuario nuevo en `POST /users/`.
    """

    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "1234"}
    )
    
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

   
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
        headers=headers
    )

    assert response.status_code == 201, response.text
    assert "id" in response.json() 

