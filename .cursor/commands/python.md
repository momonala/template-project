---
description: "Python coding standards and best practices for modern Python 3.12+ development"
globs: ["*.py"]
alwaysApply: true
---

When this command is invoked, treat the following standards as mandatory for all code generation, edits, and reviews in this conversation. Apply them to the current task and any files the user references.

## Mindsets (Zen of Python / Clean Code)

- **Explicit is better than implicit** — No magic; make intent obvious.
- **Simple is better than complex** — Flat over nested; direct over clever.
- **Readability counts** — Code is read far more than written.
- **Errors should never pass silently** — Fail loudly; catch specific exceptions.
- **There should be one obvious way** — Prefer standard library and common idioms.
- **Single Responsibility** — One reason to change per function/class.
- **Names reveal intent** — `user_count` not `n`; `MAX_RETRIES` not `3`.

## Type Hints

- Prefer built-in: `list[str]`, `dict[str, int]`, `str | None` over `Optional[str]`.
- Avoid `typing` unless needed for `Protocol`, `TypeVar`, `Generic`.
- Use `@dataclass` or `TypedDict` for structured data.

## Docstrings

- One-line for simple: `"""Return the user's name."""`
- Google-style for non-trivial: Args, Returns, Raises.
- Document *why* and constraints, not *what* the code does.

## Error Handling

- Fail loudly. Catch specific exceptions; avoid bare `except:`.
- Prefer `raise` over returning `None` or error codes for exceptional cases.
- Use context managers for cleanup (`with`).

## Side Effects & State

- Don't mutate inputs unless documented.
- Avoid global state; use dependency injection.
- Context managers for resources (files, connections, locks).

## Data Structures

- `dataclasses` for structured data with minimal behavior.
- `@dataclass(frozen=True)` for immutable.
- Prefer composition over inheritance.

## Cleanup Types (Python Refactoring)

| Smell | Refactoring |
|-------|-------------|
| Long function, nested logic | **Extract Function**; use guard clauses |
| Magic numbers/strings | Named constants at module/class level |
| `if isinstance(x, A): ... elif isinstance(x, B): ...` | **Replace with polymorphism** or `match`/`case` |
| Mutable default args `def f(x=[])` | Use `None` and assign in body |
| Try/except too broad | Catch specific exceptions; let others propagate |
| Manual resource cleanup | **Extract to context manager** |
| Repeated dict/list building | **Extract to helper** or comprehension |
| Flag arguments `def f(verbose=False)` | Split into separate functions |
| Long parameter list | **Introduce Parameter Object** (dataclass) |

## Code Smells (Python-Specific)

- **Mutable default argument** → `def f(items=None): items = items or []`
- **Bare except** → `except SpecificError:` or `except Exception:` with re-raise
- **`is` for value comparison** → Use `==` for values; `is` only for `None`, singletons
- **`type(x) == SomeClass`** → Prefer `isinstance(x, SomeClass)`
- **`len(sequence) > 0`** → Use `if sequence:` (truthy check)
- **`for i in range(len(lst))`** → `for i, item in enumerate(lst):`
- **`dict.get` with default then check** → `if key in d:` or handle `KeyError`
- **String concatenation in loop** → `"".join(parts)` or list comprehension
- **`from module import *`** → Explicit imports

## Good vs Bad Examples

### Bad: Mutable default, magic number
```python
def fetch_users(limit=100):
    users = []
    for i in range(limit):
        ...
```

### Good: Explicit default, named constant
```python
DEFAULT_PAGE_SIZE = 100

def fetch_users(limit: int = DEFAULT_PAGE_SIZE) -> list[User]:
    return [_fetch_one(i) for i in range(limit)]
```

### Bad: Bare except, swallowing errors
```python
try:
    result = risky_operation()
except:
    pass
```

### Good: Specific exception, re-raise
```python
try:
    result = risky_operation()
except ConnectionError as exc:
    logger.error("Connection failed: %s", exc)
    raise
```

### Bad: Nested conditionals
```python
def get_discount(user):
    if user:
        if user.is_premium:
            return 0.2
        elif user.orders > 10:
            return 0.1
    return 0
```

### Good: Guard clauses
```python
def get_discount(user: User | None) -> float:
    if not user:
        return 0.0
    if user.is_premium:
        return 0.2
    if user.orders > 10:
        return 0.1
    return 0.0
```

### Bad: Anti-patterns
```python
if type(x) == str: ...
if len(items) > 0: ...
for i in range(len(items)):
    do(items[i])
```

### Good: Pythonic
```python
if isinstance(x, str): ...
if items: ...
for item in items:
    do(item)
```

### Bad: Manual resource cleanup
```python
f = open(path)
data = f.read()
f.close()
```

### Good: Context manager
```python
with open(path) as f:
    data = f.read()
```

### Bad: SRP violation
```python
def process_order(order):
    validate(order)
    total = sum(item.price for item in order.items)
    save_to_db(order)
    send_email(order.customer, total)
```

### Good: Delegate
```python
def process_order(order: Order) -> None:
    order_validator.validate(order)
    order_processor.execute(order)
```

## Configuration & Databases

- Avoid magic numbers/strings; prefer explicit config.
- Module-level constants ok when scoped to one file.
- Use transactions for DB work; context managers for connections/sessions/cursors.

## Logging

- Log at boundaries and failure points, not in tight loops.
- Never log secrets or PII. Emojis ok for quick visual traceability.
- Use `logger.error("msg: %s", var)` not f-strings for lazy interpolation.

## Testing

- Use pytest; parametrize; avoid test classes.
- Test behavior, not implementation. Mock only I/O boundaries.
- Atomic tests; minimal set to cover edge cases.
- Add/update tests alongside code changes.

## Modern Python 3.12+

- Pattern matching (`match`/`case`) for type-based dispatch.
- Type parameter syntax: `def func[T](x: T) -> T:`.
- Prefer `pathlib.Path` over `os.path`.

## Documentation

- When making structural changes, update README or related docs.
