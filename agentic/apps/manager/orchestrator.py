from packages.schema.models import Plan

from .dispatcher import dispatch

# Simplified orchestrator

def compile_and_run(plan: Plan) -> None:
    # In MVP, assume plan already validated
    dispatch(plan)
