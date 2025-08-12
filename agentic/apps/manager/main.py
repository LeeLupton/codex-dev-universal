from packages.common.bus import subscribe
from packages.schema.models import WorkResult

# Simplified manager main loop

def main() -> None:
    for message in subscribe("results.*"):
        WorkResult.model_validate_json(message)  # would handle and schedule next steps

if __name__ == "__main__":
    main()
