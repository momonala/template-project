# Configuration Guide

This project separates **non-secret** config (version-controlled) from **secrets** (git-ignored) so you can safely share the repo while keeping API keys private.

## Non-secret configuration
1. Declare shared settings inside `[tool.config]` in `pyproject.toml` (flask ports, database paths, public feature flags, etc.).
2. If you add new keys there, update `src/config.py` to expose them via the CLI and add assertions to `tests/test_config.py` so the new flag is covered by CI.
3. Run `uv run config --help` to confirm the option is available, or `uv run config --all` to dump every non-secret value.

## Secrets (git-ignored)
- Sensitive values (API tokens, service credentials, private keys) belong in `src/values.py`. That file is ignored by git, so every developer or deployment must create their own copy.
- `src/values.py.example` contains stub values that CI, tests, or other teams can safely use. Keep the example in sync with the keys your code actually imports.

### Local setup
```bash
# Copy the example file to the git-ignored location
cp template-project/src/values.py.example src/values.py
# Edit src/values.py with the real secrets for your environment
```

### Example stub
```python
# Secrets used in CI/testing. Replace with production values locally.
FLASK_SECRET_KEY = "ci-secret"
TELEGRAM_API_TOKEN = "ci-telegram-token"
DATABASE_PASSWORD = "ci-db-password"
```

## CI & automation
Whenever CI, linting, or deployment pipelines need to run without real secrets, copy the `.example` stub into `src/values.py` before executing any commands. For GitHub Actions, the copy step looks like this:

```bash
if [ -f "src/values.py.example" ]; then
  cp src/values.py.example src/values.py
fi
```

Repeat the same block in every job that touches `src/values.py` so the file exists even though its contents are temporary.

## Template helpers
The helper script `copy-files-to-projects.sh` only mirrors shared bits such as hooks, `.gitignore`, or dotfiles. Configuration lives inside your project repository; update `pyproject.toml`, `src/config.py`, and `src/values.py.example` directly when you add new settings. This avoids needing to edit the helper script for every tweak.
