from packages.common.bus import publish
from packages.schema.models import Plan, WorkItem


def dispatch(plan: Plan) -> None:
    for step in plan.steps:
        item = WorkItem(run_id=plan.run_id, step_id=step.id, kind=step.kind,
                        input=step.input, reply_to=f"results.{plan.run_id}", tool=step.tool)
        publish(f"tasks.{step.kind}", item.model_dump_json())
