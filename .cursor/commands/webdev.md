---
description: "Web development coding standards and best practices for JavaScript, HTML, and CSS"
globs: ["*.js", "*.ts", "*.jsx", "*.tsx", "*.html", "*.css"]
alwaysApply: false
---

When this command is invoked, treat the following standards as mandatory for all code generation, edits, and reviews in this conversation. Apply them to the current task and any files the user references.

## Mindsets (Web / Clean Code)

- **Explicit over implicit** — No magic; make intent obvious. Avoid mental mapping.
- **Names reveal intent** — `userCount` not `n`; `MILLISECONDS_PER_DAY` not `86400000`.
- **Fail loudly** — Don't swallow errors; catch specific types; let real errors surface.
- **Local state by default** — Reach for Context/Redux only when props drilling is deep or state is truly global.
- **Composition over configuration** — Prefer `<Button><Icon />Label</Button>` over `<Button icon="x" label="Label" />` when it fits.
- **Accessibility is required** — Semantic HTML, focus management, keyboard nav. Not optional.
- **Clean up side effects** — Remove listeners, clear timers, cancel AbortControllers.

## TypeScript

- Use built-in types; avoid `any`; prefer `unknown` when type is uncertain.
- Discriminated unions for state machines and variant types.
- Branded types for domain primitives (e.g., `UserId`, `Email`).
- Leverage `satisfies` for inference with explicit constraints.
- Prefer interfaces for object shapes; type aliases for unions/intersections.

## Cleanup Types (Web Refactoring)

| Smell | Refactoring |
|-------|-------------|
| Inline functions in JSX `onClick={() => fn()}` | **Extract handler**; use `useCallback` if passed to memoized children |
| Magic strings/numbers (`'admin'`, `86400000`) | **Named constants** or enums |
| God component with 10+ props | **Split or compose**; use slots/children |
| Business logic in components | **Extract custom hook** or separate module |
| Broad `catch` blocks | **Catch specific errors**; re-raise or handle explicitly |
| Nested ternaries | **Extract function** or use `switch`/if-else |
| `div` soup | **Semantic HTML** — `nav`, `main`, `article`, `section` |
| Inline styles, hard-coded colors | **CSS custom properties** or design tokens |
| Attaching N listeners to N items | **Event delegation** on parent |
| Uncancelable fetch | **AbortController** for cleanup |

## Code Smells (Web-Specific)

- **Inline handlers in lists** → New function each render; breaks memoization. Extract.
- **Overused global state** → Modal, tab index in Context when only one subtree needs it. Keep local.
- **Magic strings** → `'admin'`, `'active'` scattered. Use constants or enums.
- **Clever one-liners** → Dense `reduce`/ternary chains. Split, name, simplify.
- **`any` type** → Use `unknown` and narrow, or proper types.
- **Missing cleanup** → `useEffect` with subscriptions/timers without return cleanup.
- **`!important` in CSS** → Refactor specificity; avoid as fix.
- **`eval()` or inline scripts** → XSS risk; use CSP; sanitize input.
- **`target="_blank"` without `rel="noopener noreferrer"`** → Security risk.

## Control Flow & Errors

- Fail loudly; don't swallow errors.
- Catch specific error types; avoid bare `catch`.
- Custom error classes for domain logic.
- Error boundaries for user-facing failures.

## Side Effects & State

- Don't mutate inputs unless documented.
- Minimize shared state; prefer explicit ownership.
- Event delegation for dynamic lists.
- Clean up: remove listeners, clear timers, cancel AbortControllers.

## Async & Performance

- `async/await`; avoid mixing sync/async in same layer.
- `AbortController` for cancellable fetch.
- `Promise.allSettled()` when partial failures are ok.
- Code splitting and lazy loading for large deps.
- `IntersectionObserver` or `requestIdleCallback` for non-critical work.

## HTML & Accessibility

- Semantic HTML; avoid div-heavy markup.
- Focus management for modals, dropdowns, dynamic content.
- ARIA when semantic HTML isn't enough; not as replacement.
- Keyboard navigation without mouse.
- Test with screen readers; don't rely on automated checkers alone.

## CSS Architecture

- Composition over deep nesting.
- CSS custom properties for theming.
- CSS containment for performance-critical components.
- `:where()` for lower specificity.
- Avoid `!important`; fix specificity instead.

## Security

- Sanitize input before rendering HTML (DOMPurify or similar).
- CSP headers; avoid `eval()` and inline scripts.
- Validate at boundaries (API responses, form inputs).
- `rel="noopener noreferrer"` for `target="_blank"` links.

## Good vs Bad Examples

### Bad: Inline handler in list (breaks memoization)
```tsx
{users.map(user => (
  <li key={user.id}>
    <button onClick={() => alert(user.name)}>Show</button>
  </li>
))}
```

### Good: Extracted handler
```tsx
const handleShow = (name: string) => () => alert(name);

{users.map(user => (
  <li key={user.id}>
    <button onClick={handleShow(user.name)}>Show</button>
  </li>
))}
```

### Bad: Magic strings
```typescript
if (user.role === 'admin') { ... }
if (status === 'active') { ... }
```

### Good: Constants or enum
```typescript
const Roles = { ADMIN: 'admin', USER: 'user' } as const;
if (user.role === Roles.ADMIN) { ... }
```

### Bad: Nested ternaries
```tsx
const label = status === 'active' ? '🟢' : status === 'pending' ? '🟡' : '🔴';
```

### Good: Extract function
```typescript
function getStatusLabel(status: Status): string {
  if (status === 'active') return '🟢 Active';
  if (status === 'pending') return '🟡 Pending';
  return '🔴 Inactive';
}
```

### Bad: Global state for local concern
```tsx
// Modal state in AppContext — whole app re-renders
const { isModalOpen, setModalOpen } = useContext(AppContext);
```

### Good: Local state
```tsx
function Page() {
  const [isModalOpen, setModalOpen] = useState(false);
  return (
    <>
      <button onClick={() => setModalOpen(true)}>Open</button>
      {isModalOpen && <Modal onClose={() => setModalOpen(false)} />}
    </>
  );
}
```

### Bad: God component
```tsx
<Button variant="primary" size="sm" isLoading icon="download" fullWidth align="left" />
```

### Good: Compose or split
```tsx
<Button>
  <Icon name="download" />
  Download
</Button>
```

### Bad: Broad catch
```typescript
try {
  await fetchData();
} catch (e) {
  console.log(e);  // swallows
}
```

### Good: Specific, re-raise
```typescript
try {
  await fetchData();
} catch (e) {
  if (e instanceof NetworkError) {
    showToast('Connection failed');
    return;
  }
  throw e;
}
```

### Good: Discriminated union for state
```typescript
type LoadingState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: Data }
  | { status: 'error'; error: Error };

function handleState(state: LoadingState) {
  switch (state.status) {
    case 'idle': return null;
    case 'loading': return <Spinner />;
    case 'success': return <DataView data={state.data} />;
    case 'error': return <ErrorView error={state.error} />;
  }
}
```

### Good: Event delegation
```javascript
listEl.addEventListener('click', (e) => {
  if (e.target.matches('.item')) handleItemClick(e.target.dataset.id);
});
```

### Good: AbortController for cleanup
```javascript
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal }).then(setData);
  return () => controller.abort();
}, [url]);
```

### Good: Focus management
```javascript
function openModal(modalEl) {
  const prev = document.activeElement;
  modalEl.showModal();
  modalEl.focus();
  modalEl.addEventListener('close', () => prev?.focus(), { once: true });
}
```

## Logging

- Log at boundaries and failure points, not in tight loops.
- Never log secrets or PII. Emojis ok for quick scan.
- Structured logging with context (request ID, user ID).
