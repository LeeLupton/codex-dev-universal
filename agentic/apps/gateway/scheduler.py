from typing import List
from packages.schema.models import Plan, Step
from packages.common.bus import Bus
from .settings import settings

bus = Bus(settings.REDIS_URL)


def schedule(plan: Plan) -> None:
    """Publish steps with no dependencies."""
    ready: List[Step] = [s for s in plan.steps if not s.depends_on]
    for step in ready:
        channel = f"tasks.{step.kind}" if step.kind != "tool" else f"tasks.tool.{step.tool}"
        bus.publish(channel, {
            "run_id": plan.run_id,
            "step_id": step.id,
            "kind": step.kind,
            "input": step.input,
            "reply_to": f"results.{plan.run_id}",
            "tool": step.tool,
        })
