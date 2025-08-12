from packages.schema.models import Plan
from . import dispatcher


def compile_workflow(plan: Plan) -> None:
    dispatcher.dispatch_plan(plan)
