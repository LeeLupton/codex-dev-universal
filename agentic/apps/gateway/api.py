from fastapi import APIRouter
from packages.schema.models import Plan

from .scheduler import schedule

router = APIRouter()

@router.post("/runs")
async def start_run(plan: Plan):
    schedule(plan)
    return {"run_id": plan.run_id}

@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    return {"run_id": run_id, "status": "unknown"}

@router.post("/workflows/validate")
async def validate(plan: Plan):
    return {"ok": True}
