---
description: "Arduino/ESP style: readability, maintainability, cleanness, and simplicity for sketches and embedded C++"
globs: ["*.ino", "*.cpp", "*.c"]
alwaysApply: false
---

When this command is invoked, treat the following standards as mandatory for all code generation, edits, and reviews in this conversation. Apply them to the current task and any files the user references.

## Mindsets (Embedded / Clean Code)

- **Thin `setup()` and `loop()`** — Delegate to named functions; intent obvious at a glance.
- **Non-blocking over blocking** — `delay()` freezes everything; use `millis()` for timing.
- **Names reveal intent** — `ledPin`, `lastReadTime`, `BLINK_INTERVAL_MS` not `p`, `t`, `500`.
- **Single Responsibility** — One function, one job. Extract when logic grows.
- **Explicit state** — Few clear variables (`lastActionTime`, `intervalMs`); no hidden globals.
- **Simplest approach** — Avoid extra abstractions until needed. RAM and flash are limited.
- **Code is read more than written** — Write for the next person (or future you).

## Structure & Organization

- Constants and pin numbers at top (or `namespace Config`).
- Group related logic into small, focused functions.
- Split by concern: sensors, display, networking in separate files when it helps.
- Use `const` and `constexpr`; prefer over `#define` for type safety.

## Cleanup Types (Arduino Refactoring)

| Smell | Refactoring |
|-------|-------------|
| `delay()` in `loop()` | **Replace with millis()** — store `lastTime`, compare `millis() - lastTime >= interval` |
| Magic numbers (500, 13, 1023) | **Replace with named constants** — `BLINK_MS`, `LED_PIN`, `ADC_MAX` |
| Fat `loop()` with nested logic | **Extract Function**; keep loop as dispatcher |
| Repeated pin/read/write pattern | **Extract to helper** or small function |
| Scattered globals | **Group into struct** or `namespace`; pass to functions |
| Long ISR doing real work | **Minimal ISR** — set flag; handle in `loop()` |
| `#define` for typed values | **Replace with `const`** — `const uint8_t PIN = 13` |
| Duplicated timing logic | **Extract `bool isIntervalElapsed(last, interval)`** |
| Platform-specific code mixed in | **Isolate with `#ifdef ESP32`** or platform-specific functions |

## Code Smells (Arduino-Specific)

- **Blocking `delay()` in loop** → Use `millis()`; sketch can't respond during delay
- **Magic numbers** → `digitalWrite(13, HIGH)` → `digitalWrite(LED_PIN, HIGH)`
- **Raw pin numbers** → Use `uint8_t` and named constants
- **Heavy work in ISR** → Set flag only; do work in `loop()`
- **`String` on AVR** → Prefer fixed buffers or `F()` for literals; avoid heap fragmentation
- **`loop()` > 30 lines** → Extract; loop should read like a table of contents
- **Copy-paste duplication** → Extract function; one place to fix
- **Inconsistent naming** → Pick style (camelCase vs snake_case) and stick to it
- **Commented-out code** → Delete; use Git for history
- **Debug `Serial.println` scattered** → One helper/macro; `#ifdef DEBUG` to disable

## Good vs Bad Examples

### Bad: Blocking, magic numbers
```cpp
void loop() {
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}
```

### Good: Non-blocking, named constants
```cpp
const uint8_t LED_PIN = LED_BUILTIN;
const unsigned long BLINK_INTERVAL_MS = 500;

unsigned long lastToggleTime = 0;
bool ledOn = false;

void loop() {
  if (millis() - lastToggleTime >= BLINK_INTERVAL_MS) {
    lastToggleTime = millis();
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  }
}
```

### Bad: Fat loop, nested logic
```cpp
void loop() {
  if (digitalRead(2) == HIGH) {
    int val = analogRead(A0);
    if (val > 512) {
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(13, LOW);
    }
  }
  // ... more nested logic
}
```

### Good: Thin loop, named functions
```cpp
void loop() {
  if (buttonPressed()) {
    handleButtonAction();
  }
  updateLedFromSensor();
}
```

### Bad: Heavy ISR
```cpp
void IRAM_ATTR onButton() {
  digitalWrite(LED_PIN, HIGH);
  delay(100);  // BAD: blocking in ISR!
  sendNetworkRequest();
}
```

### Good: Minimal ISR, logic in loop
```cpp
volatile bool buttonPressed = false;

void IRAM_ATTR onButton() {
  buttonPressed = true;
}

void loop() {
  if (buttonPressed) {
    buttonPressed = false;
    handleButtonAction();
  }
}
```

### Bad: Magic numbers, no config
```cpp
int raw = analogRead(A0);
float temp = raw * 0.0049 * 100;
if (temp > 30) { ... }
```

### Good: Named constants, config block
```cpp
namespace Config {
  const uint8_t SENSOR_PIN = A0;
  const float ADC_MV_PER_STEP = 4.9f;
  const float TEMP_THRESHOLD_C = 30.0f;
}

float temp = analogRead(Config::SENSOR_PIN) * Config::ADC_MV_PER_STEP / 100.0f;
if (temp > Config::TEMP_THRESHOLD_C) { ... }
```

### Bad: Scattered globals
```cpp
int x, y, z;
unsigned long t1, t2, t3;
bool a, b, c;
```

### Good: Grouped state
```cpp
struct AppState {
  unsigned long lastBlinkTime = 0;
  unsigned long lastReadTime = 0;
  bool ledOn = false;
  int sensorValue = 0;
};
```

## Hardware & I/O

- Define pins once; use `uint8_t` for pin numbers.
- Group `pinMode()` in `setup()`; consistent order (inputs, outputs, peripherals).
- Document non-obvious hardware (pull-ups, active-low) in one place.
- ISR: set flag or single variable only; real work in `loop()`.

## Platform Awareness (AVR vs ESP)

- **AVR**: Limited RAM — avoid large buffers, `String`, heavy dynamic allocation.
- **ESP**: More RAM; async/WiFi ok; keep same structure (thin loop, named functions).
- Isolate platform code: `#ifdef ESP32` or separate platform files.

## Libraries & Debugging

- Include only what you need.
- Wrap tricky APIs in small named functions.
- One debug helper/macro; `#ifdef DEBUG` to compile out.
- Document fragile timing or hardware quirks in one place.
