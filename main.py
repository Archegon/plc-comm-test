import time
from snap7 import Client
from snap7.util import get_int, set_int
from snap7.type import Area

# PLC connection settings
PLC_IP = "192.168.2.1"
RACK = 0
SLOT = 0

# Create and connect client
client = Client()
client.connect(PLC_IP, RACK, SLOT)

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

# === Real-time Loop ===

try:
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
