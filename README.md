# SRP Digital Twin API Prototype

A modular FastAPI-based digital twin for simulation, scenario management, and scheduling analytics.

## Features

- Upload job shop data from Excel
- Define and manage scenarios with job overrides
- Run and retrieve simulations
- Modular architecture: job_data, scenario, simulator

## Quick Start

1. `poetry install` (or `pip install -r requirements.txt`)
2. `uvicorn DT_API.main:app --reload`
3. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## File Structure

- `main.py` — App entrypoint
- `job_data.py` — Job shop data endpoints
- `scenario.py` — Scenario management
- `simulator.py` — Simulation engine
- `data_store.py` — Shared in-memory data class

## Example Usage

1. Upload job data via `/acquire_job_data`
2. Create a scenario (with job overrides)
3. Run simulation with `/run_simulator`
4. Retrieve results via `/sim_result/{scenario_id}`

## Requirements

- Python 3.9+
- FastAPI, pydantic, pandas, etc.

## For demo: Upload `sample_jobshop_data.xlsx` included.
