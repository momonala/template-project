# Apply Rule (Meta-Rule)

## Invocation

When the user invokes `/apply-rule` with text after it, parse the rule name from the user's message (the text after `/apply-rule`). If no rule name is provided, ask the user to specify one. Load the rule from `.cursor/commands/<rule-name>.md` and treat it as authoritative for the remainder of the task.

## Purpose

Force explicit application of a single, named project rule to guide **code generation, documentation changes** etc, even when automatic rule scoping would not normally apply. This meta-rule exists to reduce ambiguity, override default heuristics, and ensure consistent standards in cross-cutting or mixed-context tasks.

## Available Rules

Rules are defined in:

```
.cursor/commands/<rule-name>.md
```

Examples: `python`, `swift`, `webdev`, `architecture`, `docs`, `cleancode`, `tests`

**Usage:** Specify exactly one rule name per invocation. For multiple standards, invoke the command multiple times (e.g., `/apply-rule python` then `/apply-rule docs`).

## Execution Semantics

When this command is invoked:

1. **Resolve the rule**
  - Load `.cursor/commands/<rule-name>.md`
  - Treat it as authoritative for the remainder of the task
2. **Override defaults**
  - Ignore conflicting or less-specific rules
  - Ignore file-glob–based auto-application unless explicitly compatible
3. **Apply strictly**
  - All generated code, edits, reviews, and suggestions must conform
  - Existing code touched by the task must be brought into compliance
4. **Surface conflicts**
  - If existing code cannot be made compliant without semantic changes, explain the conflict explicitly
  - Do not silently violate the rule

## Enforcement Guarantees

- No partial application: the rule applies to the entire task
- No silent exceptions: deviations must be justified or rejected
- No dilution: avoid mixing guidance from multiple rules unless one explicitly allows it

## Output Expectations

- Generated output should visibly reflect the rule’s constraints
- Reviews should cite the rule when rejecting or requesting changes
- Documentation updates should align with the rule’s structure and tone

## Notes

- This command is declarative, not advisory
- Prefer explicit failure over implicit non-compliance
- If the rule is underspecified, follow its intent conservatively and note assumptions

