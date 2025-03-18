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
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator #Borrar si no se usa!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from qiskit.circuit.library import QFT
import sympy
from Crypto.PublicKey import RSA
import numpy as np
import random


router = APIRouter()
simulator = AerSimulator()

#==============================================================================================================================================================================


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

def generate_full_entropy_qc(num_qubits:int)->QuantumCircuit:
    """
    Esta función crea un circuito de alta altropia. Usa superposición de qubits, entrelazamiento,
    variaciones de estados basicos, rotaciones aleatorias del eje Z, y aplicación de la trasformada
    cuántica de Fourier.
    """
    # Crear registros cuánticos y clásicos para evitar errores de indexación
    qreg = QuantumRegister(num_qubits, 'q')
    creg = ClassicalRegister(num_qubits, 'c')
    qc = QuantumCircuit(qreg, creg)
    
    # 1. Poner todos los qubits en superposición con Hadamard
    for i in range(num_qubits):
        qc.h(qreg[i])
        
    # 2. Entrelazar los qubits en cadena con puertas CNOT
    for i in range(num_qubits - 1):
        qc.cx(qreg[i], qreg[i+1])
        
    # 3. Agregar compuertas de fase aleatorias (S, T) y rotación Z para cada qubit
    for i in range(num_qubits):
        if random.choice([True, False]):
            qc.s(qreg[i])
        if random.choice([True, False]):
            qc.t(qreg[i])
        angle = np.random.uniform(0, 2*np.pi)
        qc.rz(angle, qreg[i])
    
    # 4. Aplicar QFT para mezclar aún más la entropía
    qft_circuit = QFT(num_qubits)
    qc.append(qft_circuit.to_instruction(), qreg)
    
    # Medir todos los qubits para extraer la semilla
    qc.measure(qreg, creg)
    
    return qc
    
    


# =============================================================================================================================================================================


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

@router.get("/seed",summary="Genera una semilla con máxima entropía, utilizando un circuito cuántico con fases de superposicíon, entrelazamiento, compuertas de fase aleatorias y una trasformada cuántica de Fourier")
def generate_seed(num_qubits:int = 24)->dict:
    
    """
    """

    qc = generate_full_entropy_qc(num_qubits)
    transpile_qc = transpile(qc,simulator)
    result = simulator.run(transpile_qc,shots=1).result()
    counts = result.get_counts()
    seed = list(counts.keys())[0]
    
    seed_hex = "qrs_" + format(int(seed, 2), f'0{num_qubits//4}x')

    
    if not seed:
        return {"quantic_random_seed":"error"}
    
    return {"quantic_random_seed": seed_hex}

# =============================================================================================================================================================================


if __name__ == "__main__":
    
    print("[+] O.K : Todo funcionando")
    
    qc1 = generate_full_entropy_qc(8)
    
    print(type(qc1))
    
   
    
    


