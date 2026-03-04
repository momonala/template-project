---
name: code-simplifier
description: Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Grounded in Clean Code (Martin) and Refactoring (Fowler).
---

## Invocation

When the user invokes `/cleancode`, apply refinements to the specified scope. If the user provides a path or file after the command (e.g., `/cleancode src/utils/`), limit scope to that path. Otherwise, focus on recently modified code in the current session.

## Mindsets (Clean Code / Uncle Bob)

- **Boy Scout Rule**: Leave the codebase cleaner than you found it.
- **Single Responsibility Principle (SRP)**: Each function/class has one reason to change. Split when a unit does more than one thing.
- **Functions do one thing**: Small, focused. Zero args best; one or two ok; three+ is a smell.
- **Names reveal intent**: No mental mapping. Pronounceable, searchable. Replace magic numbers with named constants.
- **Don't comment bad code—rewrite it**: Comments explain why, not what. Delete commented-out code.
- **Law of Demeter**: Modules know only immediate collaborators. Avoid `a.getB().getC().doThing()`.
- **Prefer polymorphism over switch/if-else** when behavior varies by type.

## Cleanup Types (Refactoring Catalog)

Apply these when the corresponding smell appears:

| Smell | Refactoring |
|-------|-------------|
| Long function, duplicated logic | **Extract Function** (Extract Method) |
| Deep nesting, complex conditionals | **Replace Nested Conditional with Guard Clauses** |
| Magic numbers/strings | **Replace Magic Literal** with named constant |
| Too many parameters | **Introduce Parameter Object** or **Preserve Whole Object** |
| Boolean flag arguments | **Remove Flag Argument** — split into separate functions |
| Feature envy (class A manipulates B's data heavily) | **Move Function** or **Extract Class** |
| Dead code, unused functions | **Remove Dead Code** |
| Long parameter list | **Replace Parameter with Query** when value derivable |
| Obscured intent in condition | **Extract Variable** (Introduce Explaining Variable) |
| Duplication | **Extract Function**, **Parameterize Function**, or **Replace with Algorithm** |

## Code Smells (Clean Code Ch. 17)

- **Too many arguments** → Aim for 0–2; 3+ needs Extract Parameter Object or split
- **Output arguments** → Return values; avoid mutating inputs
- **Flag arguments** → Split into two functions
- **Dead function** → Delete
- **Duplication** → DRY via Extract Function, polymorphism
- **Wrong level of abstraction** → High-level and low-level mixed; separate
- **Feature envy** → Method uses another object's data more than its own; move logic
- **Obscured intent** → Extract Variable with meaningful name
- **Functions do multiple things** → Extract; one logical block per function
- **Negative conditionals** → Prefer positive: `if (isValid)` not `if (!isInvalid)`
- **Vertical separation** → Declare variables close to use

## Good vs Bad Examples

### Bad: Nested conditionals
```javascript
function getPayAmount() {
  let result;
  if (isDead) result = deadAmount();
  else {
    if (isSeparated) result = separatedAmount();
    else {
      if (isRetired) result = retiredAmount();
      else result = normalPayAmount();
    }
  }
  return result;
}
```

### Good: Guard clauses
```javascript
function getPayAmount() {
  if (isDead) return deadAmount();
  if (isSeparated) return separatedAmount();
  if (isRetired) return retiredAmount();
  return normalPayAmount();
}
```

### Bad: SRP violation (multiple responsibilities)
```python
def process_order(order):
    validate(order)
    total = calculate_total(order)
    save_to_db(order)
    send_email(order.customer, total)
    update_inventory(order.items)
```

### Good: Single responsibility
```python
def process_order(order):
    validated = order_validator.validate(order)
    return order_processor.execute(validated)  # orchestrator; delegates
```

### Bad: Magic numbers, unclear intent
```python
if user.age > 18 and len(user.purchases) >= 5:
    discount = 0.15
```

### Good: Named constants, explaining variables
```python
ADULT_AGE = 18
LOYALTY_THRESHOLD = 5
LOYALTY_DISCOUNT = 0.15

is_eligible = user.age >= ADULT_AGE and len(user.purchases) >= LOYALTY_THRESHOLD
if is_eligible:
    discount = LOYALTY_DISCOUNT
```

### Bad: Flag argument (function does two things)
```python
def format_date(dt, include_time=False):
    ...
```

### Good: Separate functions
```python
def format_date(dt): ...
def format_datetime(dt): ...
```

## Process

1. Identify target scope (user path or recently modified).
2. Scan for smells: long functions, duplication, magic literals, flag args, nesting.
3. Apply project standards from `.cursor/rules/` or `.cursor/commands/`.
4. Refactor using catalog; preserve behavior.
5. Verify: simpler, more maintainable, same functionality.

## Constraints

- **Never change behavior** — refactor only.
- **Avoid over-simplification** — no clever one-liners, nested ternaries, or removed helpful abstractions.
- **Prefer clarity over brevity** — explicit beats compact.
