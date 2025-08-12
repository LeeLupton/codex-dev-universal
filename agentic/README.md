# Agentic Monorepo

Quickstart:

1. `uv sync`
2. `npm i --prefix web`
3. `docker compose -f infra/compose/docker-compose.yml up -d`
4. `uv run apps/gateway/main.py` and `npm run dev --prefix web`
5. Open `http://localhost:5173`
