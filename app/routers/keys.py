"""
Generador de diferentes tipos de Keys funcionales para criptografía, creadas con aleatoriedad 
cuántica real con Qiskit, con un circuito cuántico que coloca qubits en superposicíon, para mas 
tarde medirlos, y hacerlos que colapsen en uno de sus dos estados básicos |0) ó |1).
El colapso de los qubits nos brinda una aleatoriedad muchisimo mas profunda que la pseudo-aleatoriedad
de librerias como random(). Esta aleatoriedad superior nos proporciona a la vez mayor seguridad en procesos
criptográficos. 


"""



from fastapi import APIRouter, HTTPException, status, Query
from .g_buffer import get_bits_from_buffer
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator #Borrar si no se usa!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import sympy
from Crypto.PublicKey import RSA


router = APIRouter()
simulator = AerSimulator()

def generate_qubit()->int:
    
    """
    Devuelve un bit cuántico en uno de sus estados básicos {Z == |0> , |1>}, previamente en una superposición cuántica:(|0> y |1> a la vez)
    La aleatoriedad del integer devuelto es real. No es pseudo-aleatoriedad como cuando usamos la libreria random().
    La aleatoriedad cuántica se consigue cuando, al medir un qubit en superoposición, lo hacemos colapsar a (0) ó (1) de forma aleatoria (50%)
    
    """
    
    return get_bits_from_buffer(1)[0]

def generate_qiskit_bytes(size: int):
    """
    
    Genera una cantidad de bytes aleatorios usando qubits en superposición.
    
    """
    total_bits = size * 8
    bits = get_bits_from_buffer(total_bits)
    byte_array = [
        
        int("".join(map(str,bits[i:i+8])),2)
        for i in range(0,total_bits,8)
    ]

    return bytes(byte_array)

def generate_qiskit_prime(bits: int):
    """
    
    Genera un número primo usando la libreria de qiskit.
    
    """
    while True:
        candidate = int.from_bytes(generate_qiskit_bytes(bits // 8), byteorder="big") | 1 
        if sympy.isprime(candidate):
            return candidate

@router.get("/aes",summary="Genera una clave AES con aleatoriedad cuántica.")
def generate_aes_key(size: int = Query(32, description="Tamaño de la clave en bytes (16, 24 o 32)")):
    """
    
    Genera una clave AES aleatoria de 128, 192 o 256 bits con Qiskit.
    
    """
    
    if size not in [16, 24, 32]:
        return {"error": "El tamaño debe ser 16, 24 o 32 bytes."}
    
    key = generate_qiskit_bytes(size)
    return {"aes_key": key.hex()}

#@router.get("/rsa", summary="Genera un par de claves RSA con aleatoriedad cuántica.")
#def generate_rsa_key():
    """
    Genera un par de claves RSA de 2048 bits usando bits del buffer global.
    """
    #p = generate_qiskit_prime(1024)
    #q = generate_qiskit_prime(1024)
    #key = RSA.construct((p * q, 65537))
    #private_key = key.export_key().decode()
    #public_key = key.publickey().export_key().decode()
    #return {"rsa_private_key": private_key, "rsa_public_key": public_key}

@router.get("/uuid",summary="Genera un UUID aleatorio con aleatoriedad cuántica")
def generate_uuid():
    """
    Genera un UUID aleatorio con Qiskit.
    
    """
    uuid_bytes = generate_qiskit_bytes(16)  
    return {"uuid": uuid_bytes.hex()}


@router.get("/otp",summary="Genera una clave secreta para OTP con aleatoriedad cuántica.")
def generate_otp_secret():
    """
    Genera una clave secreta para OTP con Qiskit.
    
    """
    otp_bytes = generate_qiskit_bytes(10)  
    
    return {"otp_secret": otp_bytes.hex()}





if __name__ == "__main__":
    
    print("[+] O.K : Todo funcionando")
    
    generate_qiskit_bytes(10)
    
    


