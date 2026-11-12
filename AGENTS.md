# Leaderboard API

Small FastAPI app: a community-event leaderboard. In-memory store, no database.

## Commands
- Test: the TEST_CMD in factory.conf (must pass before any PR)
- Lint: the LINT_CMD in factory.conf

## Conventions
- Python 3.10+, FastAPI, type hints everywhere.
- Every endpoint gets a pytest test in `tests/`, written BEFORE the implementation.
- Keep functions under 30 lines. No new dependencies: requirements.txt is protected.
- State lives in `app/store.py` only. Endpoints never hold state.

## Factory rules
- Phase state lives in `.factory/` as markdown files. Never put plan or review text in code comments.
- Only the paths in SCOPE (factory.conf) may change. Do not touch factory.sh, lib/, gates/, .claude/ or this file.
- Security: no eval/exec, no shell calls from endpoints, validate all inputs with pydantic.

## Team rules (David's factory)
- Read the narrowest reasonable version of the ticket. If it needs a new dependency, plan only what the installed packages allow and list the rest under Out of scope.
- One test per behaviour. No duplicate or "surplus" tests that check the same thing twice.
- Never write raw input, secrets or personal data to files or logs.
- Update README.md usage only if the CLI output or flags change.
