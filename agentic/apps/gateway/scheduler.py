from packages.common.bus import publish
from packages.schema.models import Plan, WorkItem

# Simplified scheduler for MVP

def schedule(plan: Plan) -> None:
    ready = [s for s in plan.steps if not s.depends_on]
    for step in ready:
        item = WorkItem(run_id=plan.run_id, step_id=step.id, kind=step.kind,
                        input=step.input, reply_to=f"results.{plan.run_id}", tool=step.tool)
        publish(f"tasks.{step.kind}", item.model_dump_json())
