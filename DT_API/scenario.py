from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from uuid import uuid4

from DT_API.data_store import Data  # Import the Data class or, if you set up scenario_data in data_store.py, import scenario_data directly

# If you set up scenario_data = Data() in data_store.py:
from DT_API.data_store import scenario_data

router = APIRouter(tags=["Scenario Engine"])

class JobOverride(BaseModel):
    job_id: str
    delay_days: Optional[int] = None
    new_due_date: Optional[str] = None
    new_processing_time: Optional[int] = None

class Scenario(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    job_overrides: Optional[List[JobOverride]] = None

class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    job_overrides: Optional[List[JobOverride]] = None

class ScenarioUpdate(BaseModel):
    description: Optional[str] = None
    job_overrides: Optional[List[JobOverride]] = None

@router.post("/scenario", summary="Create new scenario")
def create_scenario(scenario: ScenarioCreate) -> Scenario:
    scenario_id = str(uuid4())
    new_scenario = Scenario(
        id=scenario_id,
        name=scenario.name,
        description=scenario.description,
        job_overrides=scenario.job_overrides,
    )
    scenarios = scenario_data.read()
    scenarios.append(new_scenario)
    scenario_data.write(scenarios)
    return new_scenario

@router.get("/scenario", summary="Get all scenarios")
def get_all_scenarios() -> List[Scenario]:
    return scenario_data.read()

@router.get("/scenario/{scenario_id}", summary="Get scenario by ID")
def get_scenario(scenario_id: str) -> Scenario:
    scenarios = scenario_data.read()
    for scenario in scenarios:
        if scenario.id == scenario_id:
            return scenario
    raise HTTPException(status_code=404, detail="Scenario not found")

@router.patch("/scenario/{scenario_id}", summary="Update scenario")
def update_scenario(scenario_id: str, update: ScenarioUpdate) -> Scenario:
    scenarios = scenario_data.read()
    for i, scenario in enumerate(scenarios):
        if scenario.id == scenario_id:
            updated = scenario.model_copy(update=update.model_dump(exclude_unset=True))
            scenarios[i] = updated
            scenario_data.write(scenarios)
            return updated
    raise HTTPException(status_code=404, detail="Scenario not found")

@router.delete("/scenario/{scenario_id}", summary="Delete scenario")
def delete_scenario(scenario_id: str):
    scenarios = scenario_data.read()
    for scenario in scenarios:
        if scenario.id == scenario_id:
            scenarios.remove(scenario)
            scenario_data.write(scenarios)
            return {"deleted": scenario}
    raise HTTPException(status_code=404, detail="Scenario not found")
