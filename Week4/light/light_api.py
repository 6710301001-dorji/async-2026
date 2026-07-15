import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Smart Lab Lighting API")


class LightControl(BaseModel):
    status: str


# Information about the four lights.
LIGHTS = {
    "light_1": {"name": "Door Light", "status": "OFF", "delay": 0.5},
    "light_2": {"name": "Operating Table Light A", "status": "OFF", "delay": 1.2},
    "light_3": {"name": "Operating Table Light B", "status": "OFF", "delay": 2.0},
    "light_4": {"name": "Front Board Light", "status": "OFF", "delay": 0.8},
}


@app.get("/api/{student_id}/lights")
async def get_lights(student_id: str):
    return LIGHTS


@app.post("/api/{student_id}/lights/{light_id}")
async def control_light(student_id: str, light_id: str, control: LightControl):
    if light_id not in LIGHTS:
        raise HTTPException(status_code=404, detail="Light not found")

    status = control.status.upper()
    if status not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Status must be ON or OFF")

    # Simulate the hardware delay.
    await asyncio.sleep(LIGHTS[light_id]["delay"])
    LIGHTS[light_id]["status"] = status

    return {
        "student_id": student_id,
        "light_id": light_id,
        "current_status": status,
    }


@app.delete("/api/{student_id}/lights/reset")
async def reset_lights(student_id: str):
    for light in LIGHTS.values():
        light["status"] = "OFF"

    return {"message": f"All lights for {student_id} were reset to OFF"}


# Run with: uvicorn light_api:app --reload --port 8000
