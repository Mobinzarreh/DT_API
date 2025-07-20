"""API for Mock Sensor Data Acquisition."""
from random import uniform, choice

from fastapi import FastAPI

app = FastAPI()

@app.get("/acquire")
def acquire_data():
    """Generate mock data for sensors."""
    return {
        "temperature": round(uniform(15.0, 30.0), 2),
        "humidity": round(uniform(30.0, 70.0), 2),
        "pressure": round(uniform(0.9, 1.1), 2),
        "sensor_status": choice(["active", "inactive", "error"])
    }
