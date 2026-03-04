---
description: "Test writing best practices for maintainability and effectiveness"
globs: ["**/test*.py", "**/*_test.py", "**/tests/**", "**/*.test.ts", "**/*.spec.ts"]
alwaysApply: false
---

When this command is invoked, treat the following standards as mandatory for all test writing, edits, and reviews in this conversation. Apply them to the current task and any files the user references.

## Mindsets (Test Principles)

- **Test behavior, not implementation** — Verify outcomes from the user/client perspective. Refactoring shouldn't break tests if behavior is unchanged.
- **FIRST** — Fast, Independent, Repeatable, Self-validating, Timely. Write tests with or before code.
- **Minimal tests, maximum coverage** — Fewest tests that cover edge cases. Avoid redundant assertions that exercise the same logic.
- **Atomic** — One test, one behavior. Failures point to a single cause.
- **Mock at boundaries only** — Mock I/O: network, database, filesystem, subprocess. Don't mock internal logic.
- **Flaky tests are worse than no tests** — They train developers to ignore failures. Fix or delete.

## Test Pyramid

- **Many unit tests** — Fast, isolated, test pure logic and single units.
- **Some integration tests** — Test boundaries (DB, API, external services) with real or in-memory implementations.
- **Few E2E tests** — Critical user journeys only; slow and brittle.

Avoid the ice-cream cone: many slow E2E tests, few unit tests.

## Cleanup Types (Test Refactoring)

| Smell | Refactoring |
|-------|-------------|
| Test depends on another test's state | **Isolate** — Each test sets up and tears down; no shared mutable state |
| Timing-dependent assertions (`sleep`, `setTimeout`) | **Abstract time** — Inject `TimeProvider` or use deterministic waits |
| Duplicated setup across tests | **Extract fixture** — Parametrize or shared setup with clear scope |
| Testing private methods directly | **Test via public API** — Behavior is exercised through the interface |
| One test asserts many unrelated things | **Split** — One assertion focus per test (or one logical behavior) |
| Brittle selectors (complex CSS, fragile IDs) | **Stable selectors** — `data-testid`, semantic queries, or user-facing text |
| Slow test suite | **Move slow tests** — Integration/E2E in separate suite; run unit tests first |
| Vague test name `test_works` | **Rename** — Describe scenario and expected outcome |

## Test Anti-Patterns (Avoid)

- **Flaky tests** — Non-deterministic pass/fail. Causes: timing, shared state, order dependence, external deps.
- **Order dependence** — Tests assume run order. Each test must pass in isolation.
- **Static mutable state** — Global or module-level vars shared across tests. Use fixtures or local setup.
- **Over-mocking** — Mocking internal classes. Mocks return mocks. Tests couple to implementation.
- **Testing implementation** — Asserting internal calls, private state. Breaks on refactor.
- **Brittle assertions** — Exact string match, full object equality when behavior is what matters.
- **Missing cleanup** — Leaked connections, temp files, event listeners. Use `teardown`/`finally`.
- **Slow unit tests** — Unit tests hitting real DB/network. Mock boundaries or move to integration.
- **Redundant tests** — Multiple tests asserting the same behavior with trivial variations.
- **Commenting out failing tests** — Fix or delete. Ignored tests hide real issues.

## Structure: Arrange-Act-Assert (AAA)

```
Arrange — Set up preconditions, inputs, mocks
Act     — Invoke the behavior under test
Assert  — Verify the outcome
```

Keep sections distinct. One Act per test when possible.

## Given-When-Then (BDD-Style)

For readability, structure as:

- **Given** — Preconditions and context
- **When** — The action or trigger
- **Then** — Expected outcome

Makes tests self-documenting.

## Mocking Boundaries

- **Mock** — External APIs, network, database, filesystem, subprocess, time (when it affects behavior).
- **Don't mock** — Internal business logic, pure functions, types you own. Use real implementations.

Uncle Bob: "Mock across architecturally significant boundaries, but not within those boundaries."

## Good vs Bad Examples

### Bad: Testing implementation
```python
def test_discount_calculator():
    calc = DiscountCalculator()
    # BAD: testing that internal method was called
    calc.calculate.assert_called_once_with(100)
```

### Good: Testing behavior
```python
def test_applies_10_percent_discount_for_loyalty_members():
    cart = Cart(items=[Item(price=100)])
    cart.apply_discount(user=LoyaltyMember())
    assert cart.total == 90
```

### Bad: Order-dependent, shared state
```python
counter = 0  # Global!

def test_first():
    global counter
    counter += 1
    assert counter == 1

def test_second():  # Fails if run first
    assert counter == 1
```

### Good: Isolated
```python
def test_increment():
    counter = 0
    counter += 1
    assert counter == 1

def test_independent():
    counter = 1  # Own setup
    assert counter == 1
```

### Bad: Timing-dependent
```python
def test_async_result():
    trigger_async()
    time.sleep(1)  # Flaky: may pass or fail
    assert result_ready()
```

### Good: Deterministic wait or mock
```python
def test_async_result():
    trigger_async()
    wait_for_condition(lambda: result_ready(), timeout=5)
    assert result_ready()
```

### Bad: Vague name
```python
def test_works(): ...
def test_user(): ...
```

### Good: Scenario and outcome
```python
def test_returns_404_when_user_not_found(): ...
def test_ignores_expired_sessions_on_login(): ...
```

### Bad: Over-mocking
```python
def test_order_total():
    mock_repo = Mock()
    mock_repo.get_items.return_value = [Mock(price=10)]
    mock_calc = Mock()
    mock_calc.compute.return_value = 10
    # Testing mocks, not behavior
```

### Good: Mock only boundaries
```python
def test_order_total():
    order = Order(items=[Item(price=10)])
    # Real calculation logic; mock only if DB/external
    assert order.total == 10
```

### Bad: One test, many behaviors
```python
def test_user_flow():
    register_user()
    login_user()
    create_post()
    like_post()
    assert ...
```

### Good: One logical behavior per test
```python
def test_registration_creates_user_with_hashed_password(): ...
def test_login_rejects_expired_token(): ...
```

### Bad: Brittle assertion
```python
assert str(result) == "Order(id=1, items=[...], total=99.99)"
```

### Good: Assert meaningful behavior
```python
assert result.total == 99.99
assert len(result.items) == 2
```

## Test Naming Conventions

- **Pattern**: `test_<scenario>_<expected_outcome>` or `test_<method>_<condition>_<result>`
- **Examples**: `test_apply_discount_when_loyalty_member_returns_reduced_price`, `test_login_with_expired_token_returns_401`

## When to Add or Update Tests

- Add tests for new behavior; update tests when behavior intentionally changes.
- Refactoring without behavior change: tests should not need updates. If they do, they may be testing implementation.
- Fix flaky tests immediately or delete. Do not skip or ignore.
