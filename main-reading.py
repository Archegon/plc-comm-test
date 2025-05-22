import snap7
import time
from snap7.util import *
from snap7 import Area


class OutputType:
    BOOL = 1
    INT = 2
    REAL = 3
    DWORD = 4


class S7_200:
    def __init__(self, ip, localtsap, remotetsap):
        self.plc = snap7.client.Client()
        self.plc.set_connection_type(3)
        self.plc.set_connection_params(ip, localtsap, remotetsap)

        try:
            self.plc.connect(ip, 0, 0)
            if self.plc.get_connected():
                print("Connected to S7-200 Smart")
                self.plc.get_cpu_info()
        except Exception as e:
            print(f"Connection failed: {e}")

    def _resolve_area(self, mem):
        mem = mem.lower()
        if mem.startswith("db"):
            return Area.DB
        elif mem.startswith("ai") or mem.startswith("iw"):
            return Area.PE
        elif mem.startswith("aq") or mem.startswith("qw"):
            return Area.PA
        elif mem.startswith("q"):
            return Area.PA
        elif mem.startswith("i"):
            return Area.PE
        elif mem.startswith("v") or mem.startswith("m"):
            return Area.MK
        else:
            raise ValueError(f"Unknown memory area for '{mem}'")

    def getMem(self, mem, returnByte=False):
        mem = mem.lower()
        length = 1
        out_type = None
        bit = 0
        start = 0
        db_number = 0

        if mem.startswith("db"):
            db_number = int(mem.split('.')[0][2:])
            sub = mem.split('.')[1]

            if sub.startswith("dbx"):
                out_type = OutputType.BOOL
                start = int(sub[3:].split('.')[0])
                bit = int(sub.split('.')[1])
                length = 1
            elif sub.startswith("dbb"):
                out_type = OutputType.INT
                start = int(sub[3:])
                length = 1
            elif sub.startswith("dbw"):
                out_type = OutputType.INT
                start = int(sub[3:])
                length = 2
            elif sub.startswith("dbd"):
                out_type = OutputType.REAL
                start = int(sub[3:])
                length = 4
            area = Area.DB
        else:
            area = self._resolve_area(mem)

            if mem[1] == 'x':  # Bit
                out_type = OutputType.BOOL
                start = int(mem[2:].split('.')[0])
                bit = int(mem.split('.')[1])
                length = 1
            elif mem[1] == 'b':  # Byte
                out_type = OutputType.INT
                start = int(mem[2:])
                length = 1
            elif mem[1] == 'w':  # Word
                out_type = OutputType.INT
                start = int(mem[2:])
                length = 2
            elif mem[1] == 'd':  # DWord or REAL
                start = int(mem[2:])
                length = 4
                if mem.startswith("vd"):
                    out_type = OutputType.REAL
                else:
                    out_type = OutputType.DWORD
            elif mem.startswith(("aiw", "aqw", "iw", "qw", "vw")):
                start = int(mem[3:])
                length = 2
                out_type = OutputType.INT
            elif mem.startswith("vd"):
                start = int(mem[2:])
                length = 4
                out_type = OutputType.REAL

        data = self.plc.read_area(area, db_number, start, length)

        if returnByte:
            return data
        if out_type == OutputType.BOOL:
            return get_bool(data, 0, bit)
        elif out_type == OutputType.INT:
            return get_int(data, 0)
        elif out_type == OutputType.REAL:
            return get_real(data, 0)
        elif out_type == OutputType.DWORD:
            return get_dword(data, 0)

    def writeMem(self, mem, value):
        mem = mem.lower()
        data = self.getMem(mem, returnByte=True)

        length = 1
        out_type = None
        bit = 0
        start = 0
        db_number = 0

        if mem.startswith("db"):
            db_number = int(mem.split('.')[0][2:])
            sub = mem.split('.')[1]

            if sub.startswith("dbx"):
                out_type = OutputType.BOOL
                start = int(sub[3:].split('.')[0])
                bit = int(sub.split('.')[1])
                set_bool(data, 0, bit, int(value))
            elif sub.startswith("dbb"):
                out_type = OutputType.INT
                start = int(sub[3:])
                set_int(data, 0, value)
            elif sub.startswith("dbw"):
                out_type = OutputType.INT
                start = int(sub[3:])
                set_int(data, 0, value)
            elif sub.startswith("dbd"):
                out_type = OutputType.REAL
                start = int(sub[3:])
                set_real(data, 0, value)
            area = Area.DB
        else:
            area = self._resolve_area(mem)

            if mem[1] == 'x':
                out_type = OutputType.BOOL
                start = int(mem[2:].split('.')[0])
                bit = int(mem.split('.')[1])
                set_bool(data, 0, bit, int(value))
            elif mem[1] == 'b':
                out_type = OutputType.INT
                start = int(mem[2:])
                set_int(data, 0, value)
            elif mem[1] == 'w':
                out_type = OutputType.INT
                start = int(mem[2:])
                set_int(data, 0, value)
            elif mem[1] == 'd':
                start = int(mem[2:])
                if mem.startswith("vd"):
                    out_type = OutputType.REAL
                    set_real(data, 0, value)
                else:
                    out_type = OutputType.DWORD
                    set_dword(data, 0, value)
            elif mem.startswith(("aqw", "qw", "vw")):
                out_type = OutputType.INT
                start = int(mem[3:])
                set_int(data, 0, value)
            elif mem.startswith("vd"):
                out_type = OutputType.REAL
                start = int(mem[2:])
                set_real(data, 0, value)

        return self.plc.write_area(area, db_number, start, data)

    def disconnect(self):
        self.plc.disconnect()

plc = S7_200("192.168.2.1", 0x0100, 0x0200)

try:
    while True:
        print("[ANALOG INPUTS (AIW)]")
        print("  Pressure Sensor 1 (AIW16)       :", plc.getMem("AIW16"))
        print("  Pressure Sensor 2 (AIW18)       :", plc.getMem("AIW18"))
        print("  Oxygen Concentration (AIW20)    :", plc.getMem("AIW20"))
        print("  Temperature Sensor (AIW22)      :", plc.getMem("AIW22"))
        print("  Humidity Sensor (AIW32)         :", plc.getMem("AIW32"))

        print("\n[ANALOG OUTPUTS (AQW)]")
        print("  Main Oxygen Valve (AQW16)       :", plc.getMem("AQW16"))
        print("  Fan Speed Control (AQW18)       :", plc.getMem("AQW18"))

        print("[PRESSURE CONTROL VARIABLES]")
        print("  Baseline Pressure (VD400)       :", plc.getMem("DB1.DBD400"))
        print("  Cocoon Pressure (VD500)         :", plc.getMem("DB1.DBD500"))
        print("  Target Setpoint (VD512)         :", plc.getMem("DB1.DBD512"))
        print("  Rate of Change (VD516)          :", plc.getMem("DB1.DBD516"))
        print("  Intermediate Value (VD508)      :", plc.getMem("DB1.DBD508"))
        print("  Calculated Pressure (VD550)     :", plc.getMem("DB1.DBD550"))
        print("  Oxygen Flow Rate (VD566)        :", plc.getMem("DB1.DBD566"))

        print("\n[TEMPERATURE VARIABLES]")
        print("  Current Temp (VD408)            :", plc.getMem("DB1.DBD408"))
        print("  Humidity (VD412)           :", plc.getMem("DB1.DBD412"))
        print("  Temp Control Range (VD524)      :", plc.getMem("DB1.DBD524"))
        print("  Temp Set Point (VD900)       :", plc.getMem("DB1.DBD900"))
        print("  Control Param 1 (VD904)         :", plc.getMem("DB1.DBD904"))
        print("  Control Param 2 (VD908)         :", plc.getMem("DB1.DBD908"))
        print("  Control Param 3 (VD912)         :", plc.getMem("DB1.DBD912"))
        print("  Temp Adjustment Factor (VD916)  :", plc.getMem("DB1.DBD916"))

        print("\n[STATUS BITS]")
        print("  M3.0 - Startup                  :", plc.getMem("VX3.0"))
        print("  M3.1 - Running                  :", plc.getMem("VX3.1"))
        print("  M3.2 - Pressurizing             :", plc.getMem("VX3.2"))
        print("  M3.3 - Depressurizing           :", plc.getMem("VX3.3"))
        print("  M3.4-M3.7 - Reserved            :", [plc.getMem(f"VX3.{i}") for i in range(4, 8)])

        print("  M4.0 - Mode: Rest & Relax       :", plc.getMem("VX4.0"))
        print("  M4.1 - Mode: Health & Wellness :", plc.getMem("VX4.1"))
        print("  M4.2 - Mode: Professional       :", plc.getMem("VX4.2"))
        print("  M4.3 - Mode: Custom             :", plc.getMem("VX4.3"))

        print("  M5.0 - Compression: Beginner    :", plc.getMem("VX5.0"))
        print("  M5.1 - Compression: Normal      :", plc.getMem("VX5.1"))
        print("  M5.2 - Compression: Fast        :", plc.getMem("VX5.2"))

        print("  M5.3 - Duration: 60min          :", plc.getMem("VX5.3"))
        print("  M5.4 - Duration: 90min          :", plc.getMem("VX5.4"))
        print("  M5.5 - Duration: 120min         :", plc.getMem("VX5.5"))

        print("\n--- Refreshing in 1s ---\n")
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user. Disconnecting...")
    plc.disconnect()