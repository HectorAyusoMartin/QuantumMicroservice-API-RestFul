"""

Endpoints para la generación de números aleatorios con Qiskit.
Actualmente se usa la simulación con Qiskit Aer por alta latencia de los servidores IBM Quantum.


"""
from fastapi import APIRouter, HTTPException, status, Query
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from .g_buffer import *




router = APIRouter()
simulator = AerSimulator()      # Simulador Cuántico de Qiskit. Este microservicio podria interactuar con QPU's reales de IBM consumiendo su API. 
                                # A efectos prácticos, con una API gratuita, se haria denso al tener las QPU's listas de espera de mas de 1 hora.
                                # Por lo tanto, aqui se simula la computación cuámtica haciendo uso de Qiskit-Aer.


def generate_qubit()->int:
    
    """
    Devuelve un bit cuántico en uno de sus estados básicos {Z == |0> , |1>}, previamente en una superposición cuántica:(|0> y |1> a la vez)
    
    La aleatoriedad del integer devuelto es real. No es pseudo-aleatoriedad como cuando usamos la libreria random().
    
    La aleatoriedad cuántica se consigue cuando, al medir un qubit en superoposición, lo hacemos colapsar a (0) ó (1) de forma aleatoria (50%)
    
    """
    
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    
    transpile_qc = transpile(qc,simulator)
    result = simulator.run(transpile_qc,shots=1).result()
    n = result.get_counts()
   
    try:
        n = next(iter(n))
        
    except:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Qubit no encontrado")
    
   
    print(n)
    
    return int(n)
    
    
#Funciones Aleatoriedad:
@router.get("/basic",summary="Devuelve un bit aleatorio de alta entropía en formato JSON")
def get_random_bit()->dict:
    
    """
    Devuelve un diciconario{} con un bit aleatorio (0 o 1), usando aleatoriedad cuántica desde un QPU de IBM.
    
    """
    return {"random_bit":get_bits_from_buffer(1)}

@router.get("/range",summary="Devuelve un bit aleatorio dentro de un rango, especificando un máximo y un mínimo en formato JSON")
def get_random_number(min: int = Query(0), max: int = Query(100)):
    
    """
    Devuelve un número aleatorio cuántico dentro de un rango dado en la query.
    
    Ejemplo --> /random/range?min=11&max=50
    """
    if min >= max:
        raise HTTPException(status_code=400, detail="El valor mínimo debe ser menor que el máximo.")
    
    range_size = max - min
    num_bits = range_size.bit_length()
    
    # Extraemos los bits necesarios del buffer, en lugar de generarlos individualmente
    bits = get_bits_from_buffer(num_bits)
    
    random_number = min + int("".join(map(str, bits)), 2) % range_size
    return {"random_number": random_number}
    
@router.get("/bits",summary="Devuelve una cadena de bits de una longitud detarminada en la consulta en formato JSON.")
def get_random_bits(size: int = Query(8)):
    
    """
    Devuelve una cadena de bits cuánticos aleatorios de una dimensión dada.
    
    Ejmplo --> */random/bits?size=16
    
    """
    bits_list = get_bits_from_buffer(size)
    bits = "".join(str(b) for b in bits_list)
    return {"random_bits": bits}

@router.get("/bytes",summary="Devuelve una cadena de Bytes de una longitud determinada en la consulta en formato JSON")
def get_random_bytes(size: int = Query(8)):
    
    """
    Devuelve una secuencia de bytes aleatorios en formato hexadecimal.
    
    """
    
    bits = [generate_qubit() for _ in range(size * 8)]
    byte_array = [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]
    
    return {"random_bytes": bytes(byte_array).hex()}

@router.get("/float",summary="Devuelve un numero decimal aleatorio de alta entropía en formato JSON")
def get_random_float()->dict:
    """
    Devuelve un número flotante aleatorio entre 0 y 1 basado en qubits.
    
    """
    
    bits = [generate_qubit() for _ in range(10)]
    fraction = sum(bit * (2 ** -i) for i, bit in enumerate(bits, 1))
    
    return {"random_float": fraction}

@router.get("/bool",summary="Devuelve un booleano condicional aleatorio en formato JSON")
def get_bool()->dict:
    
    bit = get_bits_from_buffer(1)
    response = False
    print(bit)
    if bit == [1]:
        response = True
    
    return {"random_boolean":response}

if __name__ == "__main__":
    
    generate_qubit()