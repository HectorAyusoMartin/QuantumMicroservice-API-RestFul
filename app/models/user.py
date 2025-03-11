"""

Modelos de datos (Pydantic) para los usuarios

"""

from pydantic import BaseModel

class User(BaseModel):
    
    username:str
    hashed_password:str