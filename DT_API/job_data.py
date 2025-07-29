"""Job Data Acquisition — loads and stores job shop tasks from Excel."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

from DT_API.data_store import job_data  # <-- Import the shared data instance

router = APIRouter()

class JobTask(BaseModel):
    job_id: str
    task_id: str
    machine_id: str
    processing_time: int
    order: int
    start_time: Optional[str] = None
    due_date: str

@router.post("/acquire_job_data", summary="Ingest job shop data from Excel")
async def acquire_job_data(file: UploadFile = File(...)):
    """Reads Excel data and stores job tasks in shared memory."""
    try:
        df = pd.read_excel(file.file)
        df = df.fillna("")  # This makes all empty cells into empty strings!
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        jobs = [JobTask(**row) for row in df.to_dict(orient="records")]
        job_data.write(jobs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading job data: {str(e)}")
    
    return {"message": f"{len(job_data.read())} job tasks loaded successfully."}

@router.get("/job_data", response_model=List[JobTask], summary="Get stored job tasks")
def get_job_data():
    """Returns the list of stored job tasks."""
    return job_data.read()

__all__ = ["job_data", "JobTask"]
