"""
Endpoints mejorados haciendo uso de un global buffer para mejorar la rapidez de respuesta de las peticiones.
Se implementa un hilo en segundo plano que prellena el buffer continuamente.
Este Daemon se iniciará desde el landing p.
"""

from fastapi import APIRouter, HTTPException, status, Query
import threading
import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

router = APIRouter()
simulator = AerSimulator()



# buffer global de bits y uso de lock para concurrencia

global_buffer =[]
buffer_lock = threading.Lock()

#Constante para capacidad máxima del buffer:

BUFFER_MAX_CAPACITY = 6500

# Variables para el manejo del dameon de llenado de buffer
buffer_thread_started = False
buffer_thread = None


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
    """
    Función auxiliar que rellena el buffer de forma síncrona, agregando n lotes
    de bits (cada lote son 28 bits, porque usamos un circuito cuántico con el máximo
    de qubits permitidos con AER(28 qubits). Cada qubit genera un bit aleatorio.).
    """
    
    global global_buffer
    global_buffer = generate_random_bits()
    for i in range(n-1):
        global_buffer.extend(generate_random_bits()) # .extend extiende la [lista] como unica, .append anida [listas],[listas].
        
def background_buffer_filler():
    """
    Hilo en segundo plano para rellenar el buffer hasta su máximo.
    Se ejecuta de forma continua en segundo plano.
    
    """     
    while True:
        with buffer_lock:
            if len(global_buffer) < BUFFER_MAX_CAPACITY:
                #Si es asi añadimos un lote de 28 bits ( 1 shoot del qc )
                global_buffer.extend(generate_random_bits())  
        time.sleep(0.1) # Esto es una micro pausa con el objetivo de nos aturar la CPU
        
#Aqui iniciamos el hilo de backgound_buffer_filler() como un dameon para que corra en segundo plano:
#buffer_thread = threading.Thread(target=backgorund_buffer_filler, daemon = True)
#buffer_thread.start()

def start_buffer_thread():
    """
    Arranca el hilo de llenado del buffer si no está ya iniciado.
    Esta función se llamará desde el endpoint de la landing page.
    """
    global buffer_thread_started, buffer_thread
    if not buffer_thread_started:
        buffer_thread = threading.Thread(target=background_buffer_filler, daemon=True)
        buffer_thread.start()
        buffer_thread_started = True
        
        
        
def get_bits_from_buffer(n:int)->list:
    
    """
    Extrae n bits del buffer global. Si no hay suficientes bits,
    espera (bloqueando brevemente) hasta que se llenen.
    """

    
    
    global global_buffer #-> para acceder a global buffer
    
    
    while True:
        
        with buffer_lock:
            if len(global_buffer) >= n:
                
                 bits = global_buffer[:n] #-> rebanada para obtener el n de bits del principio hasta el numero indicado
                 global_buffer = global_buffer[n:] # ->  modificados el buffer para quitar de el los numeros que he os sacado.
        
                 return bits
             
        time.sleep(0.01) #Espera un poquito y vuelve a comprobar


# Funciones / operaciones de endpoints

@router.get("/test",summary="Test de prueba de funcionamiento del buffer. Devuelve Bytes en hexadecimal.")
def get_random_bytes(size: int = Query(8)):
    
    """
    Devuelve una sewcuencia de bytes aleatorios en hexadecimal haciendo uso delk buffer
    
    """
    
    total_bits = size * 8
    bits = []
    test = False
    
    # Ahora recolectamos bits hasta alcanzar la cantidad requerida
    
    while len(bits) < total_bits:
        bits.extend(get_bits_from_buffer(total_bits - len(bits)))
        
    # Ahora convertimos los bits a bytes
    
    byte_array = [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]
    
    if byte_array:
        test = True
    
    return {"tets_random_bytes": bytes(byte_array).hex()},{"Buffer funcionando correctamente":test}

@router.get("/state",summary="Devuelve el estado del buffer")
def info():
   

    from app.routers.g_buffer import global_buffer, buffer_lock
    with buffer_lock:
        current_buffer_length = len(global_buffer)
    return {"buffer_length": current_buffer_length}


@router.get("/on",summary="Inicializa el buffer")
def on()->dict:
    
    start_buffer_thread()
    
    return {"Estado del buffer: Activado": True}

@router.get("/off",summary="Detiene el buffer")
def off()->dict:
    
    buffer_stop_event = threading.Event()
    return {"Estado del buffer: Detenido": False}



if __name__ == "__main__":
    
    start_buffer_thread()
    # Puedes probar llenando el buffer y extrayendo algunos bits
    print("Buffer inicial:", global_buffer)
    time.sleep(1)  # Espera un segundo para que el background thread haga su trabajo
    bits = get_bits_from_buffer(50)
    print("Bits extraídos (50):", bits)
    print("Buffer restante:", len(global_buffer))
    time.sleep(15) #esperamos 30 segundos
    print("buffer final despues de 30 segundos",global_buffer)
    print(f"el número de bits en la fase final del buffer + 15sec es de {len(global_buffer)}")
     
