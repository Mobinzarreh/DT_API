# SRP Digital Twin API Prototype

A modular FastAPI-based digital twin for simulation, scenario management, and scheduling analytics.

## Features

- Upload job shop data from Excel
- Define and manage scenarios with job overrides
- Run and retrieve simulations
- Modular architecture: `job_data`, `scenario`, `simulator`

## Quick Start

1. `poetry install` (or `pip install -r requirements.txt`)
2. `uvicorn DT_API.main:app --reload`
3. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI

## File Structure

- `main.py` — App entrypoint
- `job_data.py` — Job shop data endpoints
- `scenario.py` — Scenario management
- `simulator.py` — Simulation engine
- `data_store.py` — Shared in-memory data class
- `data/sample_jobshop_data.xlsx` — Demo job shop data for upload

## Example Usage (with Swagger UI)

1. **Upload job data**  
   Use the `/acquire_job_data` endpoint and upload `data/sample_jobshop_data.xlsx`.

2. **Create a scenario with a job override**  
   Use the `/scenario` POST endpoint and try this example JSON:
   ```json
   {
     "name": "Delay J1 by 2 days",
     "description": "Test delay for Job J1",
     "job_overrides": [
       {"job_id": "J1", "delay_days": 2}
     ]
   }
