# Start Here

Entry point for a human or agent bootstrapping a new project from this template. Read this first; it explains what's already wired up, what you need to change, and how to write the README once the project takes shape.

## What this template gives you

- `pyproject.toml` — uv-managed deps, black/ruff/isort/mypy/pytest config. `[tool.config]` holds non-secret, version-controlled config.
- `src/env.py` — loads secrets from `.env` (git-ignored; `.env.example` is the checked-in stub with placeholder values used in CI).
- `src/config.py` — reads `[tool.config]` from `pyproject.toml`; exposed as `uv run config --all` / `--<key>`.
- `src/git_tool.py` — example job logic (`commit_db_if_changed`) for backing up a sqlite DB to git. Register it as a job with [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler) inside your app rather than running it as a separate process — see conventions below.
- `test-and-lint.sh` — pre-commit hook: pytest, black --check, ruff check, plus a guard that fails if the template's `install/projects_.service` hasn't been renamed/removed yet.
- `.github/workflows/ci.yml` — runs the same tests/lint on push to `main`, then a deploy job (currently a placeholder — wire it to your actual deploy target).
- `deploy.py` — rsyncs the project to a `pi-cloud` remote and manages sqlite data sync via systemd services in `install/`. Delete this and `install/` entirely if this project doesn't deploy to that infra.
- `README.md` — a fill-in-the-blank template for the project's real documentation (see below).

## Setting up a new project

1. Rename the project: update `name` in `pyproject.toml`, and rename `install/projects_.service` to match (or delete it if not deploying via systemd). One systemd service is enough — periodic jobs run in-process via Flask-APScheduler, not as a separate unit.
2. Decide if you need `deploy.py` / `install/` at all — delete them if this isn't a pi-cloud-deployed service.
3. Fill out `.env.example` with the actual secret keys the project needs (placeholder values only — real ones go in your local `.env`).
4. Add real `[tool.config]` entries to `pyproject.toml` for non-secret config.
5. Run `uv sync` and confirm `./test-and-lint.sh` passes before writing any project code.
6. Once the project's shape is real (endpoints, data flow, architecture decided), write `README.md`.

## Writing the README

`README.md` currently contains a template with a note at the top — delete that note once you fill it in. The README is the project's main source of documentation and entry point for any human or LLM picking up the work. After reading it, they should understand:

- Architecture and data flow (a diagram earns its place if the flow isn't obvious from prose)
- API design/contract — real endpoints, request/response shapes
- Any non-obvious quirks or constraints

Audience is a senior engineer maintaining the project — no style guides, no marketing language, no AI-slop enthusiasm. Say what's true, skip what's obvious from the code. See the `documentation` skill for more detail on this standard, and update the README whenever a diff changes architecture, data flow, or the API contract — don't let it drift.

## Other conventions for this project (and most of mine)

- Package management is always via `uv` — never invoke `python`/`pip` directly.
- For periodic/background tasks, use [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler) registered inside the Flask app — not the `schedule` package, a raw `while True: sleep()` loop, or a separate systemd unit.
- These are internal tools; don't build backwards-compatibility shims or defend against hypothetical future requirements. Change things directly when they need to change.
- Start small — don't handle every edge case on the first pass.
- Relevant skills to consider invoking depending on the task: `architecture`, `python`, `cleancode`, `documentation`, `sound-like-a-human`, `web-dev`, `avoid-vibe-coded-ui`.
