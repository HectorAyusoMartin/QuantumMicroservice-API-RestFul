"""
DocString:

En este módulo se definen las funciones de la seguridad de la API.

    - Hasheo de contraseñas usando Bcrypt.
    - Verificación de las contraseñas
    - Creación y validación  de tokens JWT
    
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.db import get_user # --> Para obtener el usuario de la bbdd
from app.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv


# Cargamos las variables del entorno:
load_dotenv()

# Configuracion del haseho de de contraseñas:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Variables para el uso de JWT
SECRET_KEY = os.getenv("JWT_SECRET","0a2b3c4d5e6f7g8h9i") # --> si JWT_SECRET no está definida, se usará el segundo paramtro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 25



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token:str = Depends(oauth2_scheme)) -> User:
    
    """
    Esta función obtiene el token desde la peticion. 
    Luego, decodifica el token JWT usando la SCRET_KEY.
    A continuación extrae el username del token y lo busca en la 
    base de datos.
    Si el usuario no existe, o esta invalidado, devuelve un 401.
    
    Argumentos:
    
        -token(string): Es el token generado previamente.
        
    Returns:
    
        -User: Si el usuario existe en la BBDD , lo retorna como un
               objeto User serializado por pydantic.

    """
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Error al validar las credenciales",
        headers={"WWW-Authenticate":"Bearer"},
    )
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get("sub")
        if username is None:
            raise exception
    
    except jwt.PyJWKError:
        raise exception
    
    user = await get_user(username) #--> desde app.core.db (la función busca el usuario en la BBDD)
    
    if user is None:
        raise exception
    
    return user

def get_password_hash(password:str) -> str:
    
    """
    Función que hashea la contraseña proporcionada.
    
    Argumentos:
    
        password(string): Contraseña a hashear.
        
    Returns:
    
        string: Devuelve el hash de la pass proporcionada.
    """
    return pwd_context.hash(password)

def verify_passwords(plain_pass:str,hashed_pass:str) -> bool:
    
    """
    Función que compara una clave en formato plano con una hasheada.
    
    Argumentos:
    
        plain_pass(string): La clave sin codificar, en texto plano.
        
        hashed_pass(string): La clave ya hasehada.
        
    Returns:
    
        bool: Devuelve True si la comparación resulta positiva y False
              si resulta negativa.
    
    """
    return pwd_context.verify(plain_pass,hashed_pass)

def create_access_token(data:dict,expire_time:timedelta = None) -> str:
    
    """
    Función para crear el token JWT. Recibe un {diccionario} con la información
    que se incluirá en el token,un tiempo de expiración(si no se especifica, se
    asigna por defecto 15 minutos a partir del tiempo actual).
    
    Argumentos:
    
        data(dict): Diccionario con los datos a codificar en el token.
        
        expire_time(timedelta, opcional): Duración del token.
        
    Returns:
    
        str: Devuelve el token JWT codificado en tipo string.
        
    """
    to_encode = data.copy()
    expire = datetime.now() + (expire_time if expire_time else timedelta(minutes=15))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    











