from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RUNTIME: str = "process"
    DB_URL: str
    REDIS_URL: str
    MCP_HOST: str = "127.0.0.1"
    MCP_PORT: int = 7000

    class Config:
        env_file = ".env"


settings = Settings()
