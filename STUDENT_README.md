# My calculator submission

A terminal calculator built with static/class/instance methods, a Factory,
Command objects, and a Strategy lookup. Tests keep 100% line coverage.

## Setup, run, and test

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python -m calculator             # run the calculator
python -m pytest --cov=calculator --cov-report=term-missing --cov-fail-under=100
```

Requires Python 3.12 or newer.

## Example conversation

```
Calculator. Commands: add, subtract, multiply, divide, history, exit
calc> add 5 3
8
calc> multiply -2 1.5
-3
calc> divide 6 0
Error: Cannot divide by zero
calc> add 5
Error: 'add' needs exactly 2 numbers, got 1. Example: add 5 3
calc> power 2 3
Error: unknown command 'power'. Try add, subtract, multiply, divide, history, or exit
calc> history
add 5 3 = 8
multiply -2 1.5 = -3
calc> exit
Goodbye!
```

Failed calculations are never added to history. End-of-input (Ctrl+D / Ctrl+Z)
also ends the program cleanly.

## Static, class, and instance methods

- **Static:** `Operations.add/subtract/multiply/divide` use only `a` and `b`.
  They need no `self` or `cls`.
- **Class:** `Calculation.create()` receives `cls`, so
  `ArithmeticCalculation.create(...)` builds an `ArithmeticCalculation`.
- **Instance:** `ArithmeticCalculation.execute()` uses `self.a`, `self.b`, and
  `self.operation`, which belong to that one calculation.

## Factory, Command, and Strategy

Tracing `add 5 3` (also commented in `cli.py`):

1. `handle_line` reads the input and checks that `add` exists.
2. **Strategy:** `OPERATIONS["add"]` selects `Operations.add`.
3. **Factory:** `ArithmeticCalculation.create(5.0, 3.0, Operations.add)` builds the calculation.
4. **Command:** `CalculateCommand(calculation, history, "add").execute()` runs it,
   records `add 5 3 = 8` in history, and returns `8.0`.
5. The CLI prints `8`.

## OOP

- **Encapsulation:** a calculation holds its own numbers and operation.
  `HistoryCommand.execute()` returns a copy, so callers cannot change the stored list.
- **Abstraction:** `Calculation` promises `execute()` and cannot be created directly.
- **Inheritance:** `ArithmeticCalculation` inherits `create()` and `__init__` from `Calculation`.
- **Polymorphism:** `CalculateCommand` calls `calculation.execute()` on any
  `Calculation`; each subclass can do the work differently.
- **Composition:** a `CalculateCommand` holds a calculation and the history list;
  a calculation holds an operation function.

## SOLID

- **Single responsibility:** `Operations` does math, `Calculation` runs one
  calculation, commands manage history, `cli.py` handles input and output.
- **Open/closed:** to add `power`, write `Operations.power` and add
  `"power": Operations.power` to `OPERATIONS`. `ArithmeticCalculation.execute()`
  and the commands do not change, because they just call whatever operation they hold.
- **Liskov substitution:** any `Calculation` subclass can replace another in
  `CalculateCommand` if its `execute()` returns a number or raises an error
  (tested with a stub subclass).
- **Interface segregation:** the only thing a command needs from a calculation
  is `execute()`.
- **Dependency inversion:** `CalculateCommand` depends on the `Calculation`
  abstraction, and a calculation depends on an operation function passed in,
  so addition is not hard-coded in either.

## Tests and GitHub Actions

Tests are in `tests/` (operations, calculation/factory, commands/history, CLI
sessions, and the `python -m` entry point). They cover all of `calculator/`
at **100% line coverage**.

Successful Actions run: **PASTE YOUR RUN URL HERE**

## Coverage exclusions

Only one: `Calculation.execute()` is marked `# pragma: no cover`. It is an
abstract placeholder that declares the contract and has no behavior to test.
The `__main__.py` entry point is *not* excluded; `tests/test_main.py` runs it
with `runpy`.
