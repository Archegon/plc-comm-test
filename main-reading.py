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
    while True:
        baseline_pressure     = read_vd(400)
        cocoon_pressure       = read_vd(500)
        target_setpoint       = read_vd(512)
        pressure_change_rate  = read_vd(516)
        calculated_pressure   = read_vd(550)
        oxygen_flow_rate      = read_vd(566)

        print("[PRESSURE READINGS]")
        print(f"  VD400 - Baseline Pressure     : {baseline_pressure:.2f}")
        print(f"  VD500 - Cocoon Pressure       : {cocoon_pressure:.2f}")
        print(f"  VD512 - Target Pressure       : {target_setpoint:.2f}")
        print(f"  VD516 - Pressure Change Rate  : {pressure_change_rate:.2f}")
        print(f"  VD550 - Calculated Pressure   : {calculated_pressure:.2f}")
        print(f"  VD566 - Oxygen Flow Rate      : {oxygen_flow_rate:.2f}")
        print()

        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user. Closing connection...")
    client.disconnect()
