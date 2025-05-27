from fastapi import FastAPI, Request, WebSocket
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from plc import S7_200
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

plc = S7_200("192.168.2.1", 0x0100, 0x0200)

class BitWriteRequest(BaseModel):
    address: str
    value: bool

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = read_status()
            await websocket.send_json(data)
            await asyncio.sleep(0.5)
    except Exception:
        await websocket.close()

@app.get("/status")
def read_status():
    return {
        "Equalise_state": plc.getMem("M3.2"),
        "Running_state": plc.getMem("M3.3"),
        "Pressuring_state": plc.getMem("M3.4"),
        "Stabilising_state": plc.getMem("M3.5"),
        "Depressurise_state": plc.getMem("M3.6"),
        "Stop_state": plc.getMem("M3.7"),

        "Mode_Rest": plc.getMem("M4.0"),
        "Mode_Health": plc.getMem("M4.1"),
        "Mode_Professional": plc.getMem("M4.2"),
        "Mode_Custom": plc.getMem("M4.3"),
        "Mode_o2_100": plc.getMem("M4.4"),
        "Mode_o2_120": plc.getMem("M4.5"),

        "Compression_Beginner": plc.getMem("M5.0"),
        "Compression_Normal": plc.getMem("M5.1"),
        "Compression_Fast": plc.getMem("M5.2"),

        "Current_temp": plc.getMem("VD408"),
        "Current_humidity": plc.getMem("VD412"),
        "Ambient_O2_Percent": plc.getMem("VD420"),
        "Display_Current_Pressure": plc.getMem("VD504"),
        "Current_Pressure_Target": plc.getMem("VD642"),
        "Seconds_Counter": plc.getMem("VD594"),
        "Minute_Counter": plc.getMem("VD598")
    }

@app.get("/read-bit")
def read_memory_bit(address: str):
    return {"address": address, "value": plc.getMem(address)}

@app.post("/write-bit")
def write_memory_bit(req: BitWriteRequest):
    plc.writeMem(req.address, req.value)
    return {"address": req.address, "new_value": req.value}

@app.get("/button-status")
def button_status():
    return {
        "Pressure_Rate_Set_Flag": plc.getMem("M3.0"),
        "AC_state": plc.getMem("M11.4"),
        "Intercom_State": plc.getMem("M14.3"),
        "Depressurisation_Confirm": plc.getMem("M15.1"),
        "Ceiling_Lights_State": plc.getMem("M13.5"),
        "Shutdown_button": plc.getMem("M1.6"),

        "Manual_Mode": plc.getMem("M14.0"),
        "Oxygen_Supply1_Manual": plc.getMem("M14.1"),
        "Oxygen_Supply2_Manual": plc.getMem("M14.2"),
        "Solenoid_Pump1_Manual": plc.getMem("M13.4"),
        "Pump1_Manual": plc.getMem("M13.6"),
        "Pump2_Manual": plc.getMem("M13.7")
    }
