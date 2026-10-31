# L6_L7_56 — Course Registration

Lab 6: Code and Branch Coverage

## About

A small Python module that decides whether a student can register for a course, works out waitlist positions and charges late registration fees.

## Files

| File | Description |
|------|-------------|
| `course_registration.py` | The module under test |
| `test_course_registration.py` | Starter test file |
| `CodeCoverageTest_L6_56_application.py` | Tests for code (line) coverage, 100% |
| `BranchCoverageTest_L6_56_application.py` | Tests for branch coverage, 100% |
| `screenshots/` | Terminal screenshots of the coverage reports |

## How to Run

Run all commands from the `LAB6` folder.

### 1. Setup

```bash
cd LAB6
python3 -m venv .venv
source .venv/bin/activate
pip install coverage pytest
```

### 2. Code coverage

```bash
coverage run -m pytest CodeCoverageTest_L6_56_application.py
coverage report -m
```

### 3. Branch coverage

```bash
coverage run --branch -m pytest BranchCoverageTest_L6_56_application.py
coverage report -m
```

`-m` lists the line numbers that were not covered. Without the venv activated, use `.venv/bin/coverage` instead of `coverage`.

### 4. Run the tests only

```bash
pytest CodeCoverageTest_L6_56_application.py BranchCoverageTest_L6_56_application.py
```

