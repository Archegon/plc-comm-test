import time
from snap7 import Client
from snap7.util import get_int, set_int
from snap7.type import Area

# === Initialize and connect to LOGO! PLC ===
client = Client()
client.set_connection_type(3)
client.set_connection_params("192.168.2.1", 0x0100, 0x0200)
client.connect("192.168.2.1", 0, 0)

# === Helper functions ===

def read_vw(byte_addr: int) -> int:
    """Read a 16-bit signed integer from memory word VWxx"""
    data = client.read_area(Area.MK, 0, byte_addr, 2)
    return get_int(data, 0)

def write_aqw(byte_addr: int, value: int):
    """Write 16-bit signed integer to analog output word AQWxx"""
    buffer = bytearray(2)
    set_int(buffer, 0, value)
    client.write_area(Area.PA, 0, byte_addr, buffer)

# === Real-time Monitoring Loop ===

try:
    while True:
        # === Analog Inputs via VWx memory mappings ===
        # AIW16 (Pressure Sensor 1) → VW12
        pressure_1 = read_vw(12)

        # AIW18 (Pressure Sensor 2) → VW14
        pressure_2 = read_vw(14)

        # AIW20 (Oxygen Concentration Sensor) → VW16
        oxygen_concentration = read_vw(16)

        # AIW22 (Temperature Sensor) → VW18
        temperature = read_vw(18)

        # AIW32 (Humidity Sensor) → VW28
        humidity = read_vw(28)

        # === Display Sensor Data ===
        print("[SENSOR READINGS]")
        print(f"  Pressure Sensor 1 (AIW16)       : {pressure_1}")
        print(f"  Pressure Sensor 2 (AIW18)       : {pressure_2}")
        print(f"  Oxygen Concentration (AIW20)    : {oxygen_concentration}")
        print(f"  Temperature Sensor (AIW22)      : {temperature}")
        print(f"  Humidity Sensor (AIW32)         : {humidity}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user. Disconnecting...")
    client.disconnect()
