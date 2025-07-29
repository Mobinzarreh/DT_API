from fastapi import FastAPI
from DT_API.job_data import router as job_data_router
from DT_API.scenario import router as scenario_router
from DT_API.simulator import router as simulator_router

app = FastAPI()

app.include_router(job_data_router)
app.include_router(scenario_router)
app.include_router(simulator_router)
