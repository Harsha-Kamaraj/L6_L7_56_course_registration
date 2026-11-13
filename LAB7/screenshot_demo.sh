#!/usr/bin/env bash
# Run from any directory. SS1/SS2 deliberately exercise the preserved buggy code.
set -eu
cd "$(dirname "$0")"
lab_dir="$PWD"
python="$lab_dir/.venv/bin/python"
if [ ! -x "$python" ]; then
    echo "First create LAB7/.venv and install requirements.txt (see README.md)." >&2
    exit 1
fi

case "${1:-}" in
    SS1)
        echo 'SS1 - Original buggy application (from commit 71e1df4)'
        echo '$ python evidence/buggy/course_registration_parser.py'
        echo 'Input: cs (missing course number; crash expected)'
        printf 'cs\n' | "$python" evidence/buggy/course_registration_parser.py
        ;;
    SS2)
        echo 'SS2 - Completed Hypothesis tests against the original buggy module'
        # Isolate imports so these tests cannot accidentally use the fixed module.
        demo_dir=$(mktemp -d "${TMPDIR:-/tmp}/lab7-before.XXXXXX")
        trap 'rm -rf "$demo_dir"' EXIT
        cp evidence/buggy/course_registration_parser.py "$demo_dir/"
        cp test_course_registration_parser.py "$demo_dir/"
        cd "$demo_dir"
        echo '$ python -m pytest test_course_registration_parser.py -k no_crash --tb=short --hypothesis-seed=7'
        # Keep the full traceback as evidence; show a compact summary on screen.
        set +e
        "$python" -m pytest test_course_registration_parser.py -k no_crash \
            --tb=short --hypothesis-seed=7 > "$lab_dir/evidence/SS2_buggy_tests.txt" 2>&1
        result=$?
        set -e
        head -n 9 "$lab_dir/evidence/SS2_buggy_tests.txt"
        tail -n 5 "$lab_dir/evidence/SS2_buggy_tests.txt"
        echo 'Full tracebacks: evidence/SS2_buggy_tests.txt'
        exit "$result"
        ;;
    SS3)
        echo 'SS3 - Fixed application: malformed input is handled'
        echo '$ python course_registration_parser.py'
        echo 'Inputs: cs / 4,,3 / pes1ug24cs666|Harsha K'
        printf 'cs\n4,,3\npes1ug24cs666|Harsha K\n' | "$python" course_registration_parser.py
        echo
        echo 'Fixed application: valid input still works'
        echo 'Inputs: cs 301 / 4,3,4 / pes1ug24cs666|Harsha K|regular'
        printf 'cs 301\n4,3,4\npes1ug24cs666|Harsha K|regular\n' | "$python" course_registration_parser.py
        ;;
    SS4)
        echo 'SS4 - All tests against the fixed module'
        echo '$ python -m pytest test_course_registration_parser.py --hypothesis-seed=7'
        "$python" -m pytest test_course_registration_parser.py --hypothesis-seed=7
        ;;
    *)
        echo 'Usage: bash screenshot_demo.sh SS1|SS2|SS3|SS4' >&2
        exit 2
        ;;
esac
