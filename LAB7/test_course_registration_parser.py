import pytest
from hypothesis import given, strategies as st
from course_registration_parser import format_course_code, total_credits, parse_student_record

# Include ordinary non-string values as well as the handout's text/None inputs.
inputs = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers()), st.dictionaries(st.text(), st.integers()),
)


@given(inputs)
def test_format_course_code_no_crash(s):
    try:
        result = format_course_code(s)
    except Exception as error:
        pytest.fail(f"format_course_code crashed for {s!r}: {error}")
    assert result is None or isinstance(result, str)


@given(inputs)
def test_total_credits_no_crash(s):
    try:
        result = total_credits(s)
    except Exception as error:
        pytest.fail(f"total_credits crashed for {s!r}: {error}")
    assert result is None or isinstance(result, int)


@given(inputs)
def test_parse_student_record_no_crash(s):
    try:
        result = parse_student_record(s)
    except Exception as error:
        pytest.fail(f"parse_student_record crashed for {s!r}: {error}")
    assert result is None or (
        isinstance(result, dict) and set(result) == {"srn", "name", "status"}
        and all(isinstance(value, str) and value for value in result.values())
    )


@pytest.mark.parametrize("value, expected", [
    ("cs 301", "CS301"), ("  ece\t204  ", "ECE204"),
    ("cs 001", "CS001"), (None, None), (123, None), ("", None),
    ("cs", None), ("cs 301 extra", None), ("123 abc", None),
])
def test_course_code_results(value, expected):
    assert format_course_code(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("4,3,4", 11), (" 4, 0, 3 ", 7), ("0", 0), ("-1,3", 2),
    (None, None), ([], None), ("", None), ("4,,3", None),
    ("one,two", None), ("4,3.5", None), ("4,", None),
])
def test_credit_results(value, expected):
    assert total_credits(value) == expected


@pytest.mark.parametrize("value, expected", [
    (" pes1ug23cs001 | Asha | REGULAR ",
     {"srn": "PES1UG23CS001", "name": "Asha", "status": "regular"}),
    (None, None), ({}, None), ("", None), ("srn|name", None),
    ("srn|name|regular|extra", None), ("||", None),
    ("srn| |regular", None),
])
def test_student_record_results(value, expected):
    assert parse_student_record(value) == expected
