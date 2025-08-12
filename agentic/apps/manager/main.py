from packages.common.bus import Bus
from .settings import settings

bus = Bus(settings.REDIS_URL)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
