from snap7 import Client
from snap7.util import get_int
from snap7.type import Area

client = Client()
client.set_connection_type(3)
client.set_connection_params("192.168.2.1", 0x0100, 0x0200)
client.connect("192.168.2.1", 0, 0)

def read_vw(byte_addr: int) -> int:
    data = client.read_area(Area.MK, 0, byte_addr, 2)
    return get_int(data, 0)

aiw16_value = read_vw(12)  # VW12 is internally mapped to AI1 (AIW16)
print(f"AIW16 (via VW12) = {aiw16_value}")

client.disconnect()
