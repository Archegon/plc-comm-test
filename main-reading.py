import snap7
from snap7.util import *


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
        except Exception as e:
            print(f"Connection failed: {e}")

    def _resolve_area(self, mem):
        mem = mem.lower()
        if mem.startswith("ai") or mem.startswith("iw"):
            return 0x81  # Input
        elif mem.startswith("aq") or mem.startswith("qw"):
            return 0x82  # Output
        elif mem.startswith("q"):
            return 0x82  # Output bit
        elif mem.startswith("i"):
            return 0x81  # Input bit
        elif mem.startswith("v") or mem.startswith("m"):
            return 0x83  # Memory
        else:
            raise ValueError(f"Unknown memory area for '{mem}'")

    def getMem(self, mem, returnByte=False):
        mem = mem.lower()
        area = self._resolve_area(mem)
        length = 1
        out_type = None
        bit = 0
        start = 0

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
        elif mem.startswith("aiw") or mem.startswith("aqw") or mem.startswith("iw") or mem.startswith("qw") or mem.startswith("vw"):
            start = int(mem[3:])
            length = 2
            out_type = OutputType.INT
        elif mem.startswith("vd"):
            start = int(mem[2:])
            length = 4
            out_type = OutputType.REAL

        data = self.plc.read_area(area, 0, start, length)

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

        area = self._resolve_area(mem)
        length = 1
        out_type = None
        bit = 0
        start = 0

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
        elif mem.startswith("aqw") or mem.startswith("qw") or mem.startswith("vw"):
            out_type = OutputType.INT
            start = int(mem[3:])
            set_int(data, 0, value)
        elif mem.startswith("vd"):
            out_type = OutputType.REAL
            start = int(mem[2:])
            set_real(data, 0, value)

        return self.plc.write_area(area, 0, start, data)

    def disconnect(self):
        self.plc.disconnect()

plc = S7_200("192.168.2.1", 0x0100, 0x0200)

# Read analog inputs (AIW)
print("Pressure Sensor (AIW16):", plc.getMem("AIW16"))
print("Oxygen Sensor  (AIW20):", plc.getMem("AIW20"))

# Read memory REALs (VD)
print("Baseline Pressure (VD400):", plc.getMem("VD400"))
print("Flow Rate        (VD566):", plc.getMem("VD566"))

plc.disconnect()