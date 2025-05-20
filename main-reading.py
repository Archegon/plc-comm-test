from snap7 import Client
from snap7.util import get_real
from snap7.type import Area

# === Setup and Connect ===
client = Client()
client.set_connection_type(3)  # For S7-200 Smart: ISO-on-TCP, TSAP-based
client.set_connection_params("192.168.2.1", 0x0100, 0x0200)
client.connect("192.168.2.1", 0, 0)

# === Helper function to read REAL from M area (VDxxx) ===
def read_vd(byte_addr: int) -> float:
    data = client.read_area(Area.MK, 0, byte_addr, 4)
    return get_real(data, 0)

# === Read and display all pressure-related values ===
baseline_pressure     = read_vd(400)  # VD400
cocoon_pressure       = read_vd(500)  # VD500
target_pressure       = read_vd(512)  # VD512
pressure_change_rate  = read_vd(516)  # VD516
calculated_pressure   = read_vd(550)  # VD550
oxygen_flow_rate      = read_vd(566)  # VD566

print("[PRESSURE VALUES - REALS]")
print(f"  VD400 - Baseline Pressure     : {baseline_pressure:.2f}")
print(f"  VD500 - Cocoon Pressure       : {cocoon_pressure:.2f}")
print(f"  VD512 - Target Pressure       : {target_pressure:.2f}")
print(f"  VD516 - Pressure Change Rate  : {pressure_change_rate:.2f}")
print(f"  VD550 - Calculated Pressure   : {calculated_pressure:.2f}")
print(f"  VD566 - Oxygen Flow Rate      : {oxygen_flow_rate:.2f}")

client.disconnect()