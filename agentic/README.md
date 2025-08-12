# Agentic Monorepo

This repository contains a minimal agentic platform with a FastAPI backend, MCP server, workers, and a React web UI.

## Quickstart

```bash
uv sync
npm i --prefix web
docker compose -f infra/compose/docker-compose.yml up -d
uv run apps/gateway/main.py
npm run dev --prefix web
```

Open [http://localhost:5173](http://localhost:5173) in your browser.
