.PHONY: dev api ui db up down

dev: up api ui

api:
uv run apps/gateway/main.py

ui:
cd web && npm run dev

up:
docker compose -f infra/compose/docker-compose.yml up -d

down:
docker compose -f infra/compose/docker-compose.yml down
