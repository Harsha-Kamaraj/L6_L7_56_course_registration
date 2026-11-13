# Lab 7 - Fuzzing for Input Validation Bugs

**Harsha K | PES1UG24CS666**

The parser handles invalid input without crashing. Each function returns `None`
for invalid data, and the interactive application prints `Invalid input`.

## Setup

Run from the repository root:

```bash
cd LAB7
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p screenshots
```

If the environment already exists, only `source .venv/bin/activate` is needed.

## Run the application and tests

```bash
python course_registration_parser.py
python -m pytest test_course_registration_parser.py
```

Validation: **31 passed**, including three Hypothesis properties and 28 regression
cases. The same three fuzz properties fail against the original buggy parser.
The recorded run used Python 3.14.6, pytest 9.2.0, Hypothesis 6.170.15, and seed 7.
The seed helps reproduce evidence; ordinary test runs also work without it.

| Function | Valid behavior | Invalid input |
|---|---|---|
| `format_course_code` | `cs 301` becomes `CS301`; whitespace is normalized | Reject non-strings, wrong field counts, non-alphabetic ASCII departments, or non-digit ASCII numbers |
| `total_credits` | `4,3,4` becomes `11`; signed integers retain the starter's behavior | Reject non-strings and any list containing an invalid/empty integer token; never silently return a partial sum |
| `parse_student_record` | Trim three fields; uppercase SRN and lowercase status | Reject non-strings, missing/extra fields, or blank fields |

## Screenshot commands (SS1-SS4)

Run these **one block at a time from `LAB7`** in your own Terminal. Each demo
prints the underlying Python command and inputs. Enlarge the Terminal window so
all output fits. On macOS, `screencapture -i` lets you select the output region;
press Space to select a whole window. Save genuine terminal captures using the
exact names below. You can also use Shift-Command-4 and move/rename the PNGs.

### SS1 - Buggy application crashes

```bash
clear
bash screenshot_demo.sh SS1
screencapture -i screenshots/SS1.png
```

Expected: entering `cs` triggers `ValueError` because the course number is missing.
The command intentionally exits with status 1.

### SS2 - Completed fuzz tests fail on buggy code

```bash
clear
bash screenshot_demo.sh SS2
screencapture -i screenshots/SS2.png
```

Expected: `3 failed, 28 deselected`. The three selected tests are the required
Hypothesis no-crash properties. Their complete tracebacks and minimized inputs
are saved in `evidence/SS2_buggy_tests.txt`. The screenshot demo shows a compact
summary; to inspect all failures, run:

```bash
cat evidence/SS2_buggy_tests.txt
```

The demo copies the original parser and current tests into a temporary directory,
runs them there, then removes that directory. The fixed parser stays in place.
The original file is preserved verbatim from commit `71e1df4`.

### SS3 - Fixed application handles invalid and valid input

```bash
clear
bash screenshot_demo.sh SS3
screencapture -i screenshots/SS3.png
```

Expected: all three malformed inputs print `Invalid input` without crashing.
A second run prints `CS301`, `11`, and the normalized student record.

### SS4 - Fixed tests pass

```bash
clear
bash screenshot_demo.sh SS4
screencapture -i screenshots/SS4.png
```

Expected: `31 passed`.

## Build the submission PDF

The committed `PES1UG24CS666_Harsha_K_LAB7_DRAFT.pdf` contains captured run
transcripts and reflection answers. **It is a draft, not the screenshot
deliverable.** Terminal screenshot automation was unavailable during preparation.

After saving all four screenshots:

```bash
python build_report.py
open PES1UG24CS666_Harsha_K_LAB7.pdf
```

The builder requires all four PNG files before creating the submission PDF.
Review the screenshots for legibility before submitting. To regenerate the
transcript draft while screenshots are missing, use `python build_report.py --draft`.

The starter README mentioned three reflection questions, but the supplied
handout contains none. The report therefore includes three clearly identified
reflections covering observed bugs, defensive fixes, and the benefits and limits
of fuzz testing. Replace them if your instructor supplies specific questions.

## Deliverables

Commit these in `LAB7`:

1. `course_registration_parser.py` - fixed application.
2. `test_course_registration_parser.py` - completed Hypothesis tests and regression cases.
3. `PES1UG24CS666_Harsha_K_LAB7.pdf` - SS1-SS4 and reflections (**pending your screenshots**).

After creating the final PDF, run from `LAB7`:

```bash
git add screenshots/SS1.png screenshots/SS2.png screenshots/SS3.png screenshots/SS4.png PES1UG24CS666_Harsha_K_LAB7.pdf
git commit -m "Lab 7: add screenshots and final report"
```

Supporting files include `screenshot_demo.sh`, `build_report.py`, `requirements.txt`,
and real before/after output under `evidence/`. Be ready to explain the minimized
failing inputs, the validation rules, and why no-crash tests also need checks for
correct valid results.
