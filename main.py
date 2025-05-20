import time
from snap7 import Client
from snap7.util import get_int, set_int, get_real
from snap7.type import Area

client = Client()
client.set_connection_type(3)

# Now connect (still must provide IP, rack, slot)
client.connect("192.168.2.1", 0, 0)

# === Helper functions ===

def read_aiw(byte_addr: int) -> int:
    """Read a 16-bit signed integer from analog input word (AIW)"""
    data = client.read_area(Area.PE, 0, byte_addr, 2)
    return get_int(data, 0)

def write_aqw(byte_addr: int, value: int):
    """Write a 16-bit signed integer to analog output word (AQW)"""
    buffer = bytearray(2)
    set_int(buffer, 0, value)
    client.write_area(Area.PA, 0, byte_addr, buffer)

def read_vw(byte_addr: int) -> int:
    """Read 16-bit signed integer from memory word VWxx"""
    data = client.read_area(Area.MK, 0, byte_addr, 2)
    return get_int(data, 0)

def read_vd(byte_addr: int) -> float:
    """Read 32-bit REAL (float) from memory double word VDxxx"""
    data = client.read_area(Area.MK, 0, byte_addr, 4)
    return get_real(data, 0)

def set_memory_bit(byte_addr: int, bit_index: int, value: bool):
    """Set or clear a single bit in memory (M area)."""
    # Read 1 byte from the memory byte
    data = bytearray(client.read_area(Area.MK, 0, byte_addr, 1))
    if value:
        data[0] |= (1 << bit_index)   # Set bit
    else:
        data[0] &= ~(1 << bit_index)  # Clear bit
    client.write_area(Area.MK, 0, byte_addr, data)

# === Real-time Loop ===

try:
    #set_memory_bit(14, 3, True)

    while True:
        # Read analog inputs
        pressure_1 = read_aiw(16)
        pressure_2 = read_aiw(18)
        oxygen_conc = read_aiw(20)
        temperature = read_aiw(22)
        humidity = read_aiw(32)

        # Display sensor data
        print("[SENSOR DATA]")
        print(f"  Pressure Sensors   : {pressure_1}, {pressure_2}")
        print(f"  Oxygen Concentration: {oxygen_conc}")
        print(f"  Temperature         : {temperature}")
        print(f"  Humidity            : {humidity}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user. Closing connection...")
    client.disconnect()
    client.destroy()
