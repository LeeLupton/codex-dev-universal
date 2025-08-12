.PHONY: install lint test fix precommit

install:
\t[ -f requirements.txt ] && . .venv/bin/activate && pip install -r requirements.txt || true
\t[ -f package.json ] && npm ci || true

lint:
\t[ -d . ] && (. .venv/bin/activate && ruff check . && black --check . && mypy .) || true
\t[ -f package.json ] && npx eslint . || true

fix:
\t[ -d . ] && (. .venv/bin/activate && ruff check . --fix && black .) || true

test:
\t[ -f pytest.ini ] && (. .venv/bin/activate && pytest -q) || true
\t[ -f package.json ] && npm test -s || true

precommit:
\tpre-commit install
