---
description: Documentation standards optimized for both human and LLM context quality and long-term maintainability
globs: ["**/*"]
alwaysApply: true
---

When this command is invoked, apply these documentation standards to the current task. Use them for any README creation, updates, or documentation changes the user requests.

## Mindsets (Documentation Principles)

- **Structured context, not prose** — Docs are project context for humans and LLMs. Optimize for scan and ingest.
- **Remove outdated immediately** — Misleading docs are worse than no docs. Delete or fix on sight.
- **Document why, not what** — Code shows what; docs explain rationale, trade-offs, constraints.
- **Executable over abstract** — Copy-paste commands beat "run the server." Examples must work.
- **One source of truth** — Single README in root. Avoid scattered, duplicated, or conflicting docs.
- **Sync with code** — Update docs in same commit as behavior changes. No drift.
- **Skip empty sections** — Remove or fill. Empty placeholders add noise.

## Documentation Types (Diátaxis-Inspired)

| Type | Purpose | Example |
|------|---------|---------|
| **What** | Problem, purpose, scope | "This is a webhook receiver that transforms events and stores them." |
| **How** | Step-by-step to accomplish a goal | Quick Start, configuration, deployment |
| **Why** | Rationale, trade-offs, decisions | "Key Decision: Why this architecture over alternatives" |
| **Reference** | Facts, structure, file map | Project structure, data models, config schema |

Match content to type. Don't mix "how to run" with "why we chose PostgreSQL."

## Documentation Anti-Patterns (Avoid)

- **Lava flow** — Undocumented or poorly explained code no one dares change. Document purpose and constraints.
- **Comment overuse** — Comments that restate code. Prefer self-documenting code; comment only *why*.
- **Documentation paradox** — Relying on docs to excuse unclear code. Fix the code first.
- **Template placeholders left in** — `{{VAR}}` or `TODO` in shipped docs. Remove or replace.
- **Wall of text** — Unformatted blocks. Use headings, lists, code blocks.
- **Dead links** — Broken references. Verify or remove.
- **Copy-paste failures** — Examples that don't run. Test commands and snippets.
- **Per-directory README sprawl** — Many small READMEs when one would do. Prefer root README unless required.
- **Obsolete diagrams** — Architecture that no longer matches code. Update or remove.

## When to Create or Update README

- **Create** when starting a project.
- **Update** in the same commit as major changes (features, APIs, architecture).
- **Do NOT update** for minor bug fixes, refactors without behavior change, comments, or patch-level dependency bumps.

## Writing Style

- Limit each section to 1–3 sentences.
- Be direct, factual, concrete; avoid marketing language.
- Prefer executable examples and commands over abstract descriptions.
- Use informative headings that describe the section's content.
- Remove all template placeholders.
- No need to document the API if one exists (e.g., OpenAPI).

## Required README Structure

Follow the structure in `README.md.template` (project root). Read that file for the full template when creating or updating README.

## Structural Rules

- Skip and remove empty sections entirely.
- Use consistent semantic patterns: what, how, tradeoffs, limitations.
- Reference concrete files, functions, entry points.
- Prefer explicit paths and names over vague descriptions.

## Decision & Context Docs

Create auxiliary docs when complexity warrants:

- `decision-log.md` or `docs/adr/`: Architectural/technical decisions with rationale.
- `changelog.md`: Human-readable summary of meaningful changes.

Keep concise and factual; separate *what* from *why*.

## README Update Rules

- Update "Last Updated" date (ISO format) on every meaningful change.
- Ensure examples are copy-paste plausible and reflect current behavior.
- Document tradeoffs and constraints for major design choices.

## Maintenance Rules

- Keep README in sync with codebase.
- Remove obsolete diagrams or explanations immediately.
- Update diagrams when data flow or system boundaries change.
- Single README.md in project root only.
- Avoid per-directory READMEs unless explicitly required.

## Good vs Bad Examples

### Bad: Vague, non-executable
```
To run the app, install dependencies and start the server.
```

### Good: Copy-paste ready
```bash
uv sync
uv run python app.py
# Server at http://localhost:8000
```

### Bad: Marketing prose
```
Our cutting-edge solution leverages state-of-the-art technology to deliver unparalleled performance and scalability for modern enterprises.
```

### Good: Direct, factual
```
Webhook receiver. Accepts events from Home Assistant, transforms them, stores in SQLite.
```

### Bad: Documenting what code does
```
# The get_user function fetches a user from the database by ID
def get_user(id: int): ...
```

### Good: Documenting why or constraints
```
# Uses connection pool; max 10 concurrent. See db.py for pool config.
```

### Bad: Empty section
```
## Architecture

## Contributing
```

### Good: Skip or fill
```
## Architecture

Mental model: event in → transform → store. See diagram below.
```

### Bad: Obsolete placeholder
```
## Configuration
See {{CONFIG_FILE}} for settings.
```

### Good: Concrete reference
```
## Configuration
See `docs/CONFIGURATION.md` for adding flags. Non-secret config in `pyproject.toml`; secrets in `src/values.py`.
```

### Bad: Wall of text
```
This project does many things. First you need to understand the architecture. The architecture is based on... (500 words)
```

### Good: Scannable structure
````
## What This Solves
Transforms webhook events and stores them for analysis.

## Quick Start
```bash
uv run python app.py
```

## Architecture
[Diagram] Data flow: External → Server → DB
````

## Development Workflow Integration

When generating or modifying code that affects project structure or behavior:

1. Check whether a README exists.
2. Determine if changes meet README update criteria.
3. Update documentation in the same response or commit.
4. Explicitly note when documentation was updated.
