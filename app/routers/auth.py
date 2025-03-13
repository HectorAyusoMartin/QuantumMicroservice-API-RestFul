"""
DocString:

Rutas para autenticación (login y JWT)

"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token, verify_passwords
from app.models.user import User
from app.core.db import get_user #Función a implementar que busca usuarios en la BBDD de MONGO DB aTLAS



router = APIRouter()



@router.post("/login",summary="Autentifica un usuario de la base de datos y devuelve un token JWT")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para iniciar sesion.
    
    """
    user = await get_user(form_data.username) # -> Buscar el usuario en la BBDD
    if not user or not verify_passwords(form_data.password,user.hashed_password):
        raise HTTPException(
            
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Las credenciales son incorrectas",
            headers={"WWW.Authenticate":"Bearer"},
            
            )
        
    access_token_expires = timedelta(minutes=30)
    acces_token = create_access_token(data={"sub":user.username}, expire_time=access_token_expires)
    
    return {"access_token": acces_token, "token_type":"bearer"}

