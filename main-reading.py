import time
from snap7 import Client
from snap7.util import get_real
from snap7.type import Area

# === Initialize and Connect ===
client = Client()
client.set_connection_type(3)
client.set_connection_params("192.168.2.1", 0x0100, 0x0200)
client.connect("192.168.2.1", 0, 0)

# === Helper function ===

def read_vd(byte_addr: int) -> float:
    """Read 32-bit REAL from memory double word VDxxx"""
    data = client.read_area(Area.MK, 0, byte_addr, 4)
    return get_real(data, 0)

# === Real-time Loop ===

try:
    for addr in range(0, 256, 4):
        try:
            value = read_vd(addr)
            print(f"VD{addr}: {value:.2f}")
        except Exception as e:
            print(f"VD{addr}: {e}")


except KeyboardInterrupt:
    print("Interrupted by user. Closing connection...")
    client.disconnect()
