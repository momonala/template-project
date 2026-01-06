# {{PROJECT_NAME}}

[![CI](https://github.com/momonala/{{PROJECT_NAME}}/actions/workflows/ci.yml/badge.svg)](https://github.com/momonala/{{PROJECT_NAME}}/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/momonala/{{PROJECT_NAME}}/branch/main/graph/badge.svg)](https://codecov.io/gh/momonala/{{PROJECT_NAME}})

{{SHORT_DESCRIPTION}}

## Tech Stack

- {{LANGUAGE_VERSION}} / {{FRAMEWORK}} backend
- {{DATABASE}} for data storage
- {{OTHER_TECH}}

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

## Prerequisites

- {{LANGUAGE_VERSION}}+
- [uv](https://github.com/astral-sh/uv) for dependency management

## Configuration

This project uses a dual configuration system:

### Non-Secret Configuration (Version Controlled)
Edit `pyproject.toml` under the `[tool.config]` section:
```toml
[tool.config]
flask_port = 5000
server_url = "192.168.x.x"
database_path = "data/app.db"
```

### Secret Configuration (Git-Ignored)
Create `src/values.py` for sensitive data:
```python
# src/values.py (git-ignored)
TELEGRAM_API_TOKEN = "your_token_here"
GOOGLE_MAPS_API_KEY = "your_key_here"
```

### View Configuration
```bash
# View all non-secret config
uv run config --all

# Get specific values
uv run config --flask-port
uv run config --server-url

# See all options
uv run config --help
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/{{GITHUB_USER}}/{{REPO_NAME}}.git
cd {{REPO_NAME}}
```

2. Install dependencies:
```bash
uv sync
```

3. Set up secrets:
```bash
# Copy template and fill in your secrets
cp template-project/src/values.py src/values.py
# Edit src/values.py with your actual API keys/tokens
```

## Running

```bash
uv run python app.py
```

Server runs at http://localhost:{{PORT}}

## Project Structure

```
{{REPO_NAME}}/
├── app.py                    # {{FRAMEWORK}} application & routes
├── datamodels.py             # Data models / dataclasses
├── db.py                     # Database connection utilities
├── pyproject.toml            # Dependencies & tool config
│
└── install/                  # Deployment scripts (optional)
    └── install.sh
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

## Key Concepts

| Concept | Description |
|---------|-------------|
| **{{CONCEPT_1}}** | {{CONCEPT_1_DESCRIPTION}} |
| **{{CONCEPT_2}}** | {{CONCEPT_2_DESCRIPTION}} |

## Data Models

```
{{MODEL_NAME}}
├── {{FIELD_1}}: {{FIELD_1_TYPE}}
├── {{FIELD_2}}: {{FIELD_2_TYPE}}
└── {{FIELD_3}}: {{FIELD_3_TYPE}}
```

## Storage

| File | Purpose |
|------|---------|
| `{{DATABASE_FILE}}` | {{DATABASE_DESCRIPTION}} |

## Deployment

{{DEPLOYMENT_INSTRUCTIONS}}

