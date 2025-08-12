import sys
from packages.schema.models import WorkItem, WorkResult


def handle(input: dict) -> dict:
    return {"committed": True}


def main() -> None:
    raw = sys.stdin.read()
    item = WorkItem.model_validate_json(raw)
    try:
        out = handle(item.input)
        res = WorkResult(run_id=item.run_id, step_id=item.step_id, ok=True, output=out)
    except Exception as e:
        res = WorkResult(run_id=item.run_id, step_id=item.step_id, ok=False, output={}, logs=str(e))
    print(res.model_dump_json())


if __name__ == "__main__":
    main()
