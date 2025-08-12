---

# CODEx PROMPT (generate a repository)

Create a monorepo named `agentic/` with the following structure, files, and contents. Use Python 3.11 for backend and MCP; use Node 20 for the web app. Prefer **uv** for Python workflow (but standard `pip` also works). Default runtime is **ProcessRuntime**; Docker is optional.

```
agentic/
  README.md
  .gitignore
  .env.example
  Makefile
  pyproject.toml
  uv.lock                 # create if using uv; otherwise omit
  apps/
    gateway/
      main.py
      api.py
      ws.py
      db.py
      models.py
      runtime_provider.py
      scheduler.py
      settings.py
      mcp_client.py
      requirements.txt    # minimal pin if not using pyproject extras
    manager/
      main.py
      orchestrator.py
      planner.py
      dispatcher.py
      persistence.py
      events.py
      repair.py
      settings.py
    runtime/
      base.py
      process_runtime.py
      docker_runtime.py
    mcp_server/
      main.py
      server.py
      schemas.py
      tools/
        __init__.py
        drive.py
        websearch.py
        python_run.py
        repo_git.py
        notify.py
  workers/
    plan/main.py
    research/main.py
    codegen/main.py
    eval/main.py
    repo/main.py
    notify/main.py
    transform/main.py
  packages/
    schema/
      __init__.py
      models.py
      tool_models.py
    common/
      __init__.py
      logger.py
      storage.py
      hashing.py
      security.py
      validation.py
      tracing.py
      bus.py
  workflows/
    build_service.yaml
  knowledge/.keep
  infra/
    compose/docker-compose.yml
    k8s/README.md
  web/
    package.json
    vite.config.ts
    index.html
    src/
      main.tsx
      App.tsx
      api.ts
      components/
        DagView.tsx
        RunConsole.tsx
        LogViewer.tsx
        ArtifactBrowser.tsx
        WorkflowEditor.tsx
```

## Top-level files

### `.gitignore`

```
__pycache__/
*.pyc
.env
.env.*
/data/
/runs/
/dist/
/node_modules/
/web/.vite
uv.lock
```

### `.env.example`

```
RUNTIME=process
DB_URL=postgresql+psycopg://agentic:agentic@localhost:5432/agentic
REDIS_URL=redis://localhost:6379/0
MCP_BIND=0.0.0.0:7000
WEB_PORT=5173
API_PORT=8080
GIT_TOKEN=
WEBSEARCH_PROVIDER=dummy
DRIVE_CLIENT_ID=
DRIVE_CLIENT_SECRET=
DRIVE_REDIRECT_URI=http://localhost:8080/api/drive/oauth/callback
```

### `Makefile`

```make
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
```

### `pyproject.toml`

```toml
[project]
name = "agentic"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.111",
  "uvicorn[standard]>=0.30",
  "pydantic>=2.8",
  "pydantic-settings>=2.3",
  "redis>=5.0",
  "psycopg[binary]>=3.2",
  "sqlalchemy>=2.0",
  "alembic>=1.13",
  "httpx>=0.27",
  "orjson>=3.10",
  "python-dotenv>=1.0",
  "typing-extensions>=4.12",
  "opentelemetry-sdk>=1.26",
  "opentelemetry-instrumentation-fastapi>=0.47b0",
  "cryptography>=42.0",
  "colorlog>=6.8",
]

[tool.uv]
dev-dependencies = ["pytest>=8.2","pytest-asyncio>=0.23","ruff>=0.5","mypy>=1.10"]
```

### `README.md`

Provide a concise overview and quickstart:

* `uv sync`
* `npm i --prefix web`
* `docker compose -f infra/compose/docker-compose.yml up -d`
* `uv run apps/gateway/main.py` and `npm run dev --prefix web`
* Open `http://localhost:5173`

---

## Backend: Gateway (FastAPI) — `apps/gateway/*`

### `settings.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RUNTIME: str = "process"
    DB_URL: str
    REDIS_URL: str
    API_PORT: int = 8080
    MCP_HOST: str = "127.0.0.1"
    MCP_PORT: int = 7000

    class Config:
        env_file = ".env"

settings = Settings()
```

### `db.py`

* SQLAlchemy engine/session for Postgres.
* Tables: `runs`, `steps`, `events`, `artifacts`, `tool_calls` (simple models for MVP).

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS runs(
          id TEXT PRIMARY KEY, goal TEXT, state TEXT, created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS steps(
          run_id TEXT, step_id TEXT, kind TEXT, state TEXT, deps TEXT, PRIMARY KEY(run_id, step_id)
        );
        CREATE TABLE IF NOT EXISTS events(
          run_id TEXT, seq BIGSERIAL PRIMARY KEY, ts TIMESTAMP DEFAULT NOW(), level TEXT, event TEXT, payload JSONB
        );
        CREATE TABLE IF NOT EXISTS artifacts(
          run_id TEXT, path TEXT, sha256 TEXT, size BIGINT, PRIMARY KEY(run_id, path)
        );
        """))
```

### `models.py`

Pydantic equivalents for API I/O (reuse `packages/schema/models.py` types).

### `mcp_client.py`

Thin TCP/HTTP client to call the local MCP server actions: `drive.search`, `drive.download`, `web.search`, `python.run`, `repo.git.*`, `notify.send`. For MVP, use HTTP over localhost with JSON payloads.

### `runtime_provider.py`

Select runtime based on env: `ProcessRuntime` or `DockerRuntime` (from `apps/runtime`).

### `scheduler.py`

* Topological executor for a `Plan` (see shared schema).
* Publishes `WorkItem` to Redis on `tasks.<kind>` (or `tasks.tool.<tool>`).
* Subscribes to `results.<run_id>` and updates DB; forwards events to WebSocket.

### `api.py`

FastAPI router:

* `POST /runs` start run from `workflow` + `inputs`
* `GET /runs/{id}` status
* `GET /runs/{id}/events` (SSE) optional
* `POST /workflows/validate` dry-run validation

### `ws.py`

WebSocket endpoint `/ws/runs/{id}` that streams live events.

### `main.py`

Boot FastAPI, include routers, init DB, connect Redis.

---

## Backend: Manager — `apps/manager/*`

### `settings.py`

Mirror gateway settings.

### `orchestrator.py`

* Compiles a workflow file + inputs → `Plan`.
* Validates DAG (acyclic), resource caps.
* Persists `runs` + `steps`.
* Calls `dispatcher` to enqueue ready steps.

### `planner.py`

* For `kind=plan` steps: call LLM (stub) to expand details; else just pass through.

### `dispatcher.py`

* Publishes `WorkItem` to Redis channels (`tasks.<kind>` or `tasks.tool.<tool>`).
* Enforces concurrency caps per kind.

### `persistence.py`, `events.py`, `repair.py`

* `persistence`: helpers for DB changes.
* `events`: append structured events (hash-chained).
* `repair`: on failure, feed logs to codegen/eval for fix attempts (stub).

### `main.py`

Background process: consumes `results.<run_id>` channels, updates state, schedules next steps.

---

## Runtime providers — `apps/runtime/*`

### `base.py`

```python
from typing import Protocol, Dict

class Runtime(Protocol):
    def submit(self, kind: str, env: Dict, workspace: str) -> None: ...
```

### `process_runtime.py`

* Spawns `python workers/<kind>/main.py` in a fresh **venv** (use `uv` if available) per worker type.
* Apply **ulimits**, **cgroups** (if available), and **egress deny** (simple iptables off by default, stub policy hooks included).

### `docker_runtime.py`

* `docker run --rm --network host -v {workspace}:/workspace agentic/worker-{kind}:latest`
* Only used if `RUNTIME=docker`.

---

## MCP server — `apps/mcp_server/*`

### `schemas.py`

JSON Schemas for each action input/output.

### `tools/*` (implementations)

#### `drive.py`

* Stubs that simulate Google Drive (real OAuth wires and API scaffolding present; if creds absent, return dummy data).
* Actions: `search`, `get`, `download`, `upload`.

#### `websearch.py`

* Provider adapter interface; MVP returns fixed mocked results but implements input/output shape, rate limit/backoff hooks.

#### `python_run.py`  (**core requirement**)

* **Shell-less, stateless** execution.
* Input: `{entrypoint, code?, args, timeout_sec, files[], allow_network, allowed_hosts[]}`
* Steps:

  1. Create fresh `call_dir = /runs/{run_id}/{step_id}/pyexec/{uuid}`.
  2. **Pre-startup validation** (see validation section).
  3. Materialize `files[]` under `call_dir/work/`; if `entrypoint=="inline"`, write `main.py`.
  4. Execute via embedded interpreter: `sys.argv = [entrypoint, *args]; runpy.run_path(...)` — **no shell**.
  5. Capture stdout/stderr, resource usage; block imports of native extensions (whitelist stdlib).
  6. **Post-run validation**: list new/changed files; compute sha256; forbid writes outside `/out` or `/tmp_subdir`.
  7. Append tamper-evident log entry (hash chaining).
  8. Return `{ return_code, stdout, stderr, produced_files[], metrics }`.

#### `repo_git.py`

* `init`, `add_all`, `commit`, `branch`, `push` (push only if `GIT_TOKEN` present). Pre-commit secret scan stub.

#### `notify.py`

* Sends in-process event to gateway (Redis pub) → UI toast.

### `server.py`

* FastAPI app exposing `/mcp/*` endpoints that route to tools.

### `main.py`

Run the MCP server on `MCP_BIND`.

---

## Shared types — `packages/schema/*`

### `models.py`

```python
from pydantic import BaseModel
from typing import Dict, List, Literal, Optional

Kind = Literal["plan","research","codegen","eval","repo","notify","tool"]

class Step(BaseModel):
    id: str
    kind: Kind
    input: Dict
    depends_on: List[str] = []
    tool: Optional[str] = None

class Plan(BaseModel):
    run_id: str
    goal: str
    steps: List[Step]

class WorkItem(BaseModel):
    run_id: str
    step_id: str
    kind: Kind
    input: Dict
    reply_to: str
    tool: Optional[str] = None

class WorkResult(BaseModel):
    run_id: str
    step_id: str
    ok: bool
    output: Dict = {}
    logs: Optional[str] = None
```

### `tool_models.py`

Action I/O models for MCP tools.

---

## Common utils — `packages/common/*`

* `logger.py`: structured logger with run\_id/step\_id.
* `hashing.py`: sha256 helpers and **log chain**: `prev_hash + record_json -> sha256`.
* `security.py`: basic FS and network policy stubs (deny symlinks crossing, no setuid, path allowlists).
* `validation.py`: **workspace manifest** (`path, sha256, size, mode`), pre/post checks.
* `storage.py`: artifact write/read; S3 later.
* `tracing.py`: OpenTelemetry setup.
* `bus.py`: Redis publish/subscribe wrappers.

---

## Workers — `workers/*/main.py`

All workers implement:

```python
def handle(input: dict) -> dict: ...
```

A thin runner:

```python
import json, sys
from packages.common.logger import get_logger
from packages.schema.models import WorkItem, WorkResult

def main():
    raw = sys.stdin.read()
    item = WorkItem.model_validate_json(raw)
    try:
        from . import main as impl
        out = impl.handle(item.input)
        res = WorkResult(run_id=item.run_id, step_id=item.step_id, ok=True, output=out)
    except Exception as e:
        res = WorkResult(run_id=item.run_id, step_id=item.step_id, ok=False, output={}, logs=str(e))
    print(res.model_dump_json())

if __name__ == "__main__":
    main()
```

### `plan/main.py`

* Uses LLM stub (no external calls) to expand constraints into per-file tasks; returns a refined `steps` payload for manager (MVP: echo).

### `research/main.py`

* Calls MCP `drive.search` and/or `web.search`, returns summaries with citations.

### `codegen/main.py`

* Generates per-file scaffolds (use string templates) into `/runs/{run_id}/repo`, returns diff summary.

### `eval/main.py`

* Runs `ruff`, `mypy`, `pytest -q` via MCP `python.run` with inline scripts (stateless), returns diagnostics.

### `repo/main.py`

* Calls MCP `repo.git.*` actions to init/add/commit (and branch/push if configured).

### `notify/main.py`

* Calls `notify.send` for UI toast & completion.

### `transform/main.py`

* Simple JSON mapping (jq-like) placeholder.

---

## Workflow example — `workflows/build_service.yaml`

```yaml
name: build_service
goal_template: "Build a CRUD service for {{resource}} with tests and a README."
inputs:
  resource: string
steps:
  - id: plan
    kind: plan
    input:
      constraints: ["90% test coverage", "mypy clean", "black/ruff"]
  - id: drive_search
    kind: tool
    tool: drive.search
    depends_on: [plan]
    input:
      query: "example ERD for {{resource}}"
      limit: 5
  - id: web_best_practices
    kind: tool
    tool: web.search
    depends_on: [plan]
    input:
      query: "service design best practices for {{resource}}"
  - id: codegen_api
    kind: codegen
    depends_on: [drive_search, web_best_practices]
    input:
      stack: "FastAPI + SQLAlchemy + Postgres"
      deliverables: ["api", "models", "migrations", "tests", "README.md"]
  - id: eval
    kind: eval
    depends_on: [codegen_api]
    input:
      commands: ["ruff .", "mypy .", "pytest -q"]
  - id: repo_commit
    kind: repo
    depends_on: [eval]
    input:
      message: "auto: scaffold {{resource}} service"
  - id: notify_done
    kind: notify
    depends_on: [repo_commit]
    input:
      message: "Run complete for {{resource}}"
```

---

## Infra — `infra/compose/docker-compose.yml`

Provide Redis + Postgres + optional MCP + gateway:

```yaml
version: "3.9"
services:
  redis:
    image: redis:7
    ports: ["6379:6379"]
  pg:
    image: postgres:16
    environment:
      POSTGRES_USER: agentic
      POSTGRES_PASSWORD: agentic
      POSTGRES_DB: agentic
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
  mcp:
    build:
      context: .
      dockerfile: Dockerfile.mcp   # (Codex: create a simple Python Dockerfile if desired)
    environment:
      - MCP_BIND=0.0.0.0:7000
    ports: ["7000:7000"]
    depends_on: [redis, pg]
  gateway:
    build:
      context: .
      dockerfile: Dockerfile.api   # (optional for containerized dev)
    environment:
      - DB_URL=postgresql+psycopg://agentic:agentic@pg:5432/agentic
      - REDIS_URL=redis://redis:6379/0
      - MCP_HOST=mcp
      - MCP_PORT=7000
    ports: ["8080:8080"]
    depends_on: [redis, pg, mcp]
volumes:
  pgdata:
```

---

## Web UI — `web/*`

### `package.json`

```json
{
  "name": "agentic-ui",
  "private": true,
  "version": "0.1.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.5.4",
    "vite": "^5.3.1",
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22"
  }
}
```

### `src/api.ts`

* Minimal client for Gateway API (`/runs`, `/ws/runs/{id}`).

### `components/*`

* `DagView.tsx` renders nodes/edges from step states.
* `RunConsole.tsx` shows status + buttons (retry failed step).
* `LogViewer.tsx` streams and filters logs.
* `ArtifactBrowser.tsx` lists artifacts for a run.
* `WorkflowEditor.tsx` textarea + validate button (POST `/workflows/validate`).

---

## Behavior & Guarantees to Implement

* **Manager loop:** topological scheduling, concurrency caps, retries, repair stub.
* **Bus:** Redis channels `tasks.<kind>` and `results.<run_id>`.
* **MCP server:** actions `drive.search|get|download|upload`, `web.search`, `python.run`, `repo.git.*`, `notify.send`.
* **python.run:** shell-less, stateless; pre/post workspace validation; immutable hash-chained logs.
* **Security:** per-worker env scoping; deny symlinks across workspace; no writes outside `/runs/<run_id>`; default **deny egress** with allowed hosts list.
* **Observability:** structured logs with `{ts, run_id, step_id, level, event}`; OpenTelemetry stubs.
* **UI:** start run, live DAG, per-step logs, artifacts, completion toast.

## Quickstart Commands

1. **Services**

```
docker compose -f infra/compose/docker-compose.yml up -d
```

2. **Backend**

```
uv sync
uv run apps/gateway/main.py
```

3. **UI**

```
cd web && npm i && npm run dev
```

4. **Open UI**: [http://localhost:5173](http://localhost:5173)
5. **Start Example Run** from the UI with workflow `build_service.yaml` and input `{ "resource": "Listing" }`.

---
