"""

Endpoints mejorados haciendo uso de un global buffer para mejorar la rapidez de respuesta de las peticiones
# TODO: omplementar el [buffer] para los metodos existentes de los disntintos endpoints

"""

from fastapi import APIRouter, HTTPException, status, Query
import threading
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

router = APIRouter()
simulator = AerSimulator()



# buffer global de bits y uso de lock para concurrencia

global_buffer =[]
buffer_lock = threading.Lock()


# Funciones de generación dbits aleatorios y uso del buffer

def generate_random_bits():
    
    num_qubits = 28
    
    qc = QuantumCircuit(num_qubits,num_qubits)
    
    for qubit in range(num_qubits):
        qc.h(qubit)
        qc.measure(qubit,qubit)
        
    
        
    traspiled_qc = transpile(qc,simulator)
    result = simulator.run(traspiled_qc,shots=1).result()
    counts = result.get_counts()
    
    try:
        bits_str = next(iter(counts))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No se encontraron los Qubits")
    
    return [int(b) for b in bits_str[::-1]]


def refill_buffer(n:int)->None:
    
    global global_buffer
    global_buffer = generate_random_bits()
    for i in range(n-1):
        global_buffer.extend(generate_random_bits()) # .extend extiende la [lista] como unica, .append anida [listas],[listas].
        
        
def get_bits_from_buffer(n:int)->list:
    """Extraemos bits que necesitemos, y rellenamos el buffer primero si no son suficientes. Ademas usamos with lock, para bloquear el acceso al buffer."""
    
    
    global global_buffer #-> para acceder a global buffer
    
    
    
    with buffer_lock:
        if len(global_buffer) < n:
            refill_buffer(n)
        bits = global_buffer[:n] #-> rebanada para obtener el n de bits del principio hasta el numero indicado
        global_buffer = global_buffer[n:] # ->  modificados el buffer para quitar de el los numeros que he os sacado.
        
    return bits


# Funciones / operaciones de endpoints

@router.get("/bytes")
def get_random_bytes(size: int = Query(8)):
    
    """
    Devuelve una sewcuencia de bytes aleatorios en hexadecimal haciendo uso delk buffer
    
    """
    
    total_bits = size * 8
    bits = []
    
    # Ahora recolectamos bits hasta alcanzar la cantidad requerida
    
    while len(bits) < total_bits:
        bits.extend(get_bits_from_buffer(total_bits - len(bits)))
        
    # Ahora convertimos los bits a bytes
    
    byte_array = [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]
    
    return {"random_bytes": bytes(byte_array).hex()}



if __name__ == "__main__":
    
    refill_buffer(4)
     
   # print(global_buffer)
   
    print(type(get_bits_from_buffer(3)))
    
    print(global_buffer)
    
    for i in get_bits_from_buffer(3):
        print(i)
    




