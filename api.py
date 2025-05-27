"""
Bits to create a button for:
Pressure_Rate_Set_Flag	M3.0
AC_state	M11.4
Intercom_State	M14.3
Depressurisation_Confirm	M15.1
Ceiling_Lights_State	M13.5


Bits to read and display values from:
Equalise_state	M3.2
Running_state	M3.3
Pressuring_state	M3.4
Stablising_state	M3.5
Depressurise_state	M3.6
Stop_state	M3.7

Selected mode:
Mode_Rest	M4.0
Mode_Health	M4.1
Mode_Professional	M4.2
Mode_Custom	M4.3
Mode_o2_100	M4.4
Mode_o2_120	M4.5

Selected compression rate:
Compression_Beginner	M5.0
Compression_Normal	M5.1
Compression_Fast	M5.2

Selected duration:
Duration_60m	M5.3
Duration_90m	M5.4
Duration_120m	M5.5

Current_temp	VD408
Current_humidity	VD412
Ambient_O2_Percent	VD420
Display_Current_Pressure	VD504
"""
from fastapi import FastAPI
from pydantic import BaseModel
from plc import S7_200

app = FastAPI()
plc = S7_200("192.168.2.1", 0x0100, 0x0200)

# --- Request Model ---
class BitWriteRequest(BaseModel):
    address: str  # e.g. "VX3.0"
    value: bool

# --- Read Route ---
@app.get("/status")
def read_status():
    return {
        # Bit states to display
        "Equalise_state": plc.getMem("VX3.2"),
        "Running_state": plc.getMem("VX3.3"),
        "Pressuring_state": plc.getMem("VX3.4"),
        "Stabilising_state": plc.getMem("VX3.5"),
        "Depressurise_state": plc.getMem("VX3.6"),
        "Stop_state": plc.getMem("VX3.7"),

        "Mode_Rest": plc.getMem("VX4.0"),
        "Mode_Health": plc.getMem("VX4.1"),
        "Mode_Professional": plc.getMem("VX4.2"),
        "Mode_Custom": plc.getMem("VX4.3"),
        "Mode_o2_100": plc.getMem("VX4.4"),
        "Mode_o2_120": plc.getMem("VX4.5"),

        "Compression_Beginner": plc.getMem("VX5.0"),
        "Compression_Normal": plc.getMem("VX5.1"),
        "Compression_Fast": plc.getMem("VX5.2"),

        "Duration_60m": plc.getMem("VX5.3"),
        "Duration_90m": plc.getMem("VX5.4"),
        "Duration_120m": plc.getMem("VX5.5"),

        # Realtime float values
        "Current_temp": plc.getMem("DB1.DBD408"),
        "Current_humidity": plc.getMem("DB1.DBD412"),
        "Ambient_O2_Percent": plc.getMem("DB1.DBD420"),
        "Display_Current_Pressure": plc.getMem("DB1.DBD504")
    }

# --- Bit Read ---
@app.get("/read-bit")
def read_memory_bit(address: str):
    return {"address": address, "value": plc.getMem(address)}

# --- Bit Write ---
@app.post("/write-bit")
def write_memory_bit(req: BitWriteRequest):
    plc.writeMem(req.address, req.value)
    return {"address": req.address, "new_value": req.value}

# --- Button control bits ---
@app.get("/button-status")
def button_status():
    return {
        "Pressure_Rate_Set_Flag": plc.getMem("VX3.0"),
        "AC_state": plc.getMem("VX11.4"),
        "Intercom_State": plc.getMem("VX14.3"),
        "Depressurisation_Confirm": plc.getMem("VX15.1"),
        "Ceiling_Lights_State": plc.getMem("VX13.5")
    }