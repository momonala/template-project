---
description: "Architecture, planning, and feedback practices for technical decision-making"
alwaysApply: true
---

When this command is invoked, apply these architecture and planning practices to the current task. Before implementation, follow the Requirements Clarification and Before Implementation sections. Use the examples for format.

## Mindsets (Architecture Principles)

- **Clarify before building** — Wrong work is worse than no work. Ask until unknowns are resolved.
- **Smallest change that delivers value** — Incremental over big-bang; defer detail until needed.
- **YAGNI** — You Aren't Gonna Need It. Build for current requirements, not hypothetical futures.
- **KISS** — Keep It Simple. Avoid over-engineering; simplest approach that works.
- **Design for change** — Identify what varies; encapsulate it. Prefer composition over inheritance.
- **Explicit trade-offs** — Every choice has costs. Document why, what was rejected, and why.
- **Plan for failure** — Error handling, retries, degradation. Systems fail; design for it.
- **Seek feedback early** — On approach and architecture, not just implementation.

## Requirements Clarification

- Ask the minimum questions needed to avoid wrong work.
- Treat as underspecified if unclear: objective, definition of done, scope, constraints, environment, safety/reversibility.
- Ask **1–5** questions that eliminate entire branches of work, not cosmetic details.
- Optimize for fast answers: numbered questions, multiple-choice with defaults, compact replies (e.g., `1b 2a`).
- Never assume unstated requirements silently.
- If answering wouldn't change code structure, dependencies, or behavior, don't ask.

## Before Implementation

- Do not run commands, edit files, or create designs that depend on unknowns.
- Low-risk discovery (read configs, docs) is ok when clearly labeled.
- If asked to proceed without answers: state assumptions as a short numbered list; proceed only after confirmation.
- Once answers are received: restate requirements in **1–3 sentences** (constraints + success criteria) before beginning.

## Decision Patterns (ADR-Style)

For significant decisions, document:

| Section | Content |
|---------|---------|
| **Context** | Problem, constraints, forces at play |
| **Decision** | Clear statement of what was chosen |
| **Rationale** | Why this over alternatives |
| **Alternatives considered** | What was rejected and why |
| **Consequences** | Positive, negative, risks, mitigations |
| **Trade-offs** | What we gave up (e.g., simplicity for scalability) |

Store in version control (e.g., `docs/adr/` or `decision-log.md`). Link superseded decisions to new ones.

## Planning Anti-Patterns (Avoid)

- **Big Design Up Front (BDUF)** — Comprehensive design before implementation; rigid, wastes effort when requirements shift. Prefer iterative, just-enough design.
- **Over-engineering** — Complex architecture when simpler suffices. Build for current needs.
- **Assuming without asking** — Proceeding on unstated requirements. Always clarify.
- **Skipping migration/rollback** — Major changes without path forward or back. Plan both.
- **Defending before understanding** — Responding to feedback without clarifying intent.
- **Patching symptoms** — When feedback reveals fundamental issues, iterate on approach, don't band-aid.
- **Premature abstraction** — Abstracting before you have 2–3 concrete cases. Wait for duplication.

## Architecture Decisions

- Prefer composition over inheritance; interfaces/protocols over concrete implementations.
- Design for change: identify what varies and encapsulate it.
- Consider the cost of abstraction; don't abstract prematurely.
- Make dependencies explicit; invert when appropriate (dependency inversion).
- Design for testability: injectable dependencies, isolated side effects.
- Document why technologies/patterns were chosen; include rationale and trade-offs.
- List alternatives considered and explain why they weren't selected.
- Explicitly explain why common alternatives were avoided when the choice is non-obvious.

## Planning & Scope

- Start with the smallest change that delivers value.
- Identify migration paths and rollback strategies before major changes.
- Consider incremental delivery over big-bang releases.
- Plan for failure: error handling, retries, degradation strategies.
- Document decisions and trade-offs; include alternatives and why not chosen.

## Feedback & Iteration

- Seek feedback early on architecture and approach, not just implementation.
- Present alternatives with trade-offs when multiple reasonable approaches exist.
- When receiving feedback: clarify intent before defending decisions.
- Iterate on approach if feedback reveals fundamental issues; don't just patch symptoms.

## Good vs Bad Examples

### Bad: Vague request, immediate implementation
```
User: "Add caching"
→ Implementing Redis cache without asking: what to cache? TTL? invalidation? existing infra?
```

### Good: Clarifying requirements
```
Before I start, I need:
1. Scope: Minimal change (default) / Refactor / New feature
2. Performance: Any specific requirements? If none, I'll optimize for maintainability.
3. Backward compatibility: Required? (default: yes)

Reply: defaults (or 1a 2none 3yes)
```

### Bad: Proceeding on assumptions
```
→ Implementing with Python 3.8, breaking changes, new DB schema — user expected 3.12, no breaking changes, existing schema
```

### Good: Stating assumptions
```
Proceeding with these assumptions:
1. Python 3.12+ only (per pyproject.toml)
2. No breaking API changes
3. Using existing database schema

Proceed?
```

### Bad: Decision without rationale
```
We're using PostgreSQL.
```

### Good: Architecture decision with rationale
```
Chose event-driven approach over polling because:
- Lower latency for real-time updates
- Better scalability (decoupled components)
- Trade-off: More complex error handling
```

### Bad: No alternatives documented
```
Using PostgreSQL for the database.
```

### Good: Alternatives considered (ADR-style)
```
Why PostgreSQL?
- Need ACID guarantees for financial transactions
- Supports JSON columns for flexible metadata
- Team has deep PostgreSQL expertise

Alternatives considered:
- MongoDB: Better for unstructured data, lacks strong ACID
- MySQL: Simpler, weaker JSON support
- DynamoDB: Great scale, vendor lock-in, team unfamiliar

Why not Redis as primary?
- Persistence guarantees insufficient for critical data
- Better as complementary cache (which we're using)
```

### Bad: Defending without clarifying
```
Reviewer: "Why not use polling?"
Author: "Event-driven is better." (no exploration of reviewer's concern)
```

### Good: Clarify then respond
```
Reviewer: "Why not use polling?"
Author: "What's driving that—simplicity, ops, or something else? For us, latency was the main constraint. If your concern is X, we could..."
```
