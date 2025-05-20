import time
from snap7.logo import Logo
from snap7.util import get_int, set_int, get_real, get_bool

# PLC connection settings
PLC_IP = "192.168.2.1"

# Create and connect Logo client
client = Logo()
client.connect(PLC_IP, 0, 0)

# === LOGO Area Codes ===
LOGO_INPUTS = 0x81
LOGO_OUTPUTS = 0x82
LOGO_MEMORY = 0x83

# === Helper functions ===

def read_aiw(byte_addr: int) -> int:
    """Read a 16-bit signed integer from analog input word (AIWxx)"""
    data = client.read_area(LOGO_INPUTS, 0, byte_addr, 2)
    return get_int(data, 0)

def write_aqw(byte_addr: int, value: int):
    """Write a 16-bit signed integer to analog output word (AQWxx)"""
    buffer = bytearray(2)
    set_int(buffer, 0, value)
    client.write_area(LOGO_OUTPUTS, 0, byte_addr, buffer)

def read_vw(byte_addr: int) -> int:
    """Read 16-bit signed integer from memory word VWxx"""
    data = client.read_area(LOGO_MEMORY, 0, byte_addr, 2)
    return get_int(data, 0)

def read_vd(byte_addr: int) -> float:
    """Read 32-bit REAL from memory double word VDxxx"""
    data = client.read_area(LOGO_MEMORY, 0, byte_addr, 4)
    return get_real(data, 0)

def set_memory_bit(byte_addr: int, bit_index: int, value: bool):
    """Set or clear a bit in memory (M area)"""
    data = bytearray(client.read_area(LOGO_MEMORY, 0, byte_addr, 1))
    if value:
        data[0] |= (1 << bit_index)
    else:
        data[0] &= ~(1 << bit_index)
    client.write_area(LOGO_MEMORY, 0, byte_addr, data)

# === Real-time Loop ===

try:
    # Example: set M14.3
    # set_memory_bit(14, 3, True)

    while True:
        # Read analog inputs
        pressure_1 = read_aiw(16)
        pressure_2 = read_aiw(18)
        oxygen_conc = read_aiw(20)
        temperature = read_aiw(22)
        humidity = read_aiw(32)

        # Display sensor data
        print("[SENSOR DATA]")
        print(f"  Pressure Sensors    : {pressure_1}, {pressure_2}")
        print(f"  Oxygen Concentration: {oxygen_conc}")
        print(f"  Temperature         : {temperature}")
        print(f"  Humidity            : {humidity}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user. Closing connection...")
    client.disconnect()
