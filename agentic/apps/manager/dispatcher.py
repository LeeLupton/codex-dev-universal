from packages.schema.models import Plan
from packages.common.bus import Bus
from .settings import settings

bus = Bus(settings.REDIS_URL)


def dispatch_plan(plan: Plan) -> None:
    for step in plan.steps:
        if not step.depends_on:
            channel = f"tasks.{step.kind}" if step.kind != "tool" else f"tasks.tool.{step.tool}"
            bus.publish(channel, {
                "run_id": plan.run_id,
                "step_id": step.id,
                "kind": step.kind,
                "input": step.input,
                "reply_to": f"results.{plan.run_id}",
                "tool": step.tool,
            })
