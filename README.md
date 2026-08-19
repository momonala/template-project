NOTE: This is a template. Please update and add/remove sections accordingly. This document should serve as high level over and guide for any human or LLM working on this project, and they should gain enough context to get started on work immediately after reading. Therefore, they should be able to understand architecture, dataflow, API design/contract, and any wierd quirks after reading. This document should not contain style guides, marketing speak hyping up the app, AI slop. The intended audience is senior software engineers looking to build and maintain the project. Delete this note when filling out the README template.

# {{PROJECT_NAME}}

[![CI](https://github.com/momonala/{{PROJECT_NAME}}/actions/workflows/ci.yml/badge.svg)](https://github.com/momonala/{{PROJECT_NAME}}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/momonala/{{PROJECT_NAME}}/branch/main/graph/badge.svg)](https://codecov.io/gh/momonala/{{PROJECT_NAME}})

{{SHORT_DESCRIPTION}}

## Prerequisites

- {{LANGUAGE_VERSION}}+
- [uv](https://github.com/astral-sh/uv) for dependency management

## Configuration

This project uses a dual configuration system: non-secret settings are version-controlled, secrets are git-ignored.

### Non-Secret Configuration (Version Controlled)
Edit `pyproject.toml` under the `[tool.config]` section:
```toml
[tool.config]
flask_port = 5000
server_url = "192.168.x.x"
database_path = "data/app.db"
```

### Secret Configuration (Git-Ignored)
Copy `.env.example` to `.env` and populate it with sensitive values:
```python
from src.env import TELEGRAM_API_TOKEN, FLASK_SECRET_KEY
```

### View Configuration
```bash
# View all non-secret config
uv run config --all
```

## Installation

Install dependencies:
```bash
uv sync
```

Set up secrets:
```bash
# Copy the stub values for CI/testing and customize locally
cp .env.example .env
# Edit .env with your actual API keys/tokens
```

## Running

```bash
uv run app
```

Server runs at http://localhost:{{PORT}}

## Project Structure

```
{{REPO_NAME}}/
├── src/
│   ├── app.py                # {{FRAMEWORK}} application & routes
│   ├── config.py             # Non-secret config from pyproject.toml [tool.config]
│   ├── env.py                # Secrets loaded from .env (git-ignored)
│   ├── datamodels.py         # Data models / dataclasses
│   └── db.py                 # Database connection utilities
├── .env.example              # Stub secrets used in CI
├── pyproject.toml            # Dependencies & tool config
│
└── install/                  # Deployment scripts (optional)
    └── install.sh
```

## Architecture

```mermaid
flowchart LR
    subgraph External
        {{EXTERNAL_SERVICE}}[{{EXTERNAL_NAME}}]
    end
    subgraph Storage
        DB[({{DATABASE_FILE}})]
    end
    subgraph App
        Server[{{FRAMEWORK}} Server :{{PORT}}]
    end
    
    {{EXTERNAL_SERVICE}} -->|{{API_ACTION}}| Server
    Server --> DB
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Health check |
| `/{{MAIN_ENDPOINT}}` | {{HTTP_METHOD}} | {{ENDPOINT_DESCRIPTION}} |

### {{HTTP_METHOD}} /{{MAIN_ENDPOINT}}

```bash
curl -X {{HTTP_METHOD}} http://localhost:{{PORT}}/{{MAIN_ENDPOINT}} \
  -H "Content-Type: application/json" \
  -d '{{EXAMPLE_REQUEST_BODY}}'
```

Request body:
```json
{
  "{{FIELD_1}}": "{{FIELD_1_TYPE}} (required)",
  "{{FIELD_2}}": "{{FIELD_2_TYPE}} (optional)"
}
```

Response:
```json
{
  "status": "success",
  "data": {}
}
```
