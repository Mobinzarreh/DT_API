"""Simulation Engine (MS) — runs predictive modeling based on scenario data."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from random import choice
from datetime import datetime, timedelta

from DT_API.data_store import job_data, scenario_data  # <-- Use shared instances

router = APIRouter(tags=["Modeling & Simulation"])

# In-memory simulation result store (can also be swapped for a Data object!)
simulation_results: Dict[str, "SimulationResult"] = {}

class SimulationRequest(BaseModel):
    """Request model for running the simulator."""
    scenario_id: str

class SimulationResult(BaseModel):
    """Response model for simulation results."""
    scenario_id: str
    delay_risk: str
    adjusted_schedule: List[Dict[str, str]]

def get_scenario_by_id(scenario_id: str):
    for scenario in scenario_data.read():
        if scenario.id == scenario_id:
            return scenario
    return None

@router.post("/run_simulator", response_model=SimulationResult)
def run_simulation(req: SimulationRequest) -> SimulationResult:
    """Run simulation based on scenario_id and real job shop data."""
    delay_risk = choice(["Low", "Medium", "High"])
    adjusted_schedule = []

    start_date = datetime.today()
    jobs = job_data.read()
    if not jobs:
        raise HTTPException(status_code=400, detail="No job data loaded. Please upload job data first.")

    scenario = get_scenario_by_id(req.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found.")

    # You could apply job_overrides from scenario here if desired

    for i, task in enumerate(jobs):
        scheduled_day = start_date + timedelta(days=i)
        adjusted_schedule.append({
            "task": f"{task.job_id}-{task.task_id}",
            "new_date": scheduled_day.strftime("%Y-%m-%d")
        })

    result = SimulationResult(
        scenario_id=req.scenario_id,
        delay_risk=delay_risk,
        adjusted_schedule=adjusted_schedule
    )

    simulation_results[req.scenario_id] = result
    return result

@router.get("/sim_result/{scenario_id}", response_model=SimulationResult)
def get_sim_result(scenario_id: str) -> SimulationResult:
    """Retrieve previously simulated results for a given scenario."""
    if scenario_id not in simulation_results:
        raise HTTPException(status_code=404, detail="Simulation result not found")
    return simulation_results[scenario_id]
