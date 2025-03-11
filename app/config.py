# Configuraciones generales (variables de entorno, conexión a MongoDB, etc.)
 
# Aqui tambien cargaremos las variables de entorno del archivo .env (ignorado por .gitignore)

import os
from dotenv import load_dotenv 


# Cargamos las vraibles desde .env. Una vez cargadas, accedemos a ellas, a través de os.getenv.
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")


print("llego hasta aqui")