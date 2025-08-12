from fastapi import APIRouter
from .models import Plan
from . import scheduler

router = APIRouter()

runs = {}

@router.post("/runs")
def start_run(plan: Plan) -> dict:
    runs[plan.run_id] = {"state": "running"}
    scheduler.schedule(plan)
    return {"run_id": plan.run_id}

@router.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    return runs.get(run_id, {})

@router.post("/workflows/validate")
def validate(plan: Plan) -> dict:
    return {"ok": True, "steps": len(plan.steps)}
