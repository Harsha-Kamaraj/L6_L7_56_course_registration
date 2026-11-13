import re


def format_course_code(code):
    """
    Format a department and course number, e.g. 'cs 301' -> 'CS301'.

    Return None for non-strings or anything other than an ASCII alphabetic
    department and an ASCII digit-only number separated by whitespace.
    """
    if not isinstance(code, str):
        return None
    match = re.fullmatch(r"\s*([A-Za-z]+)\s+([0-9]+)\s*", code)
    if match is None:
        return None
    dept, number = match.groups()
    return dept.upper() + number


def total_credits(text):
    """
    Sum comma-separated integers, preserving the original signed-int behavior.

    Return None for non-strings, empty tokens, or invalid integers. Reject the
    entire list instead of silently dropping invalid credits or returning zero.
    """
    if not isinstance(text, str):
        return None
    try:
        return sum(int(credit) for credit in text.split(','))
    except ValueError:
        # Includes Python's conversion limit for excessively long integers.
        return None


def parse_student_record(line):
    """
    Parse exactly three non-empty 'SRN|name|status' fields, or return None.
    """
    if not isinstance(line, str):
        return None
    parts = [part.strip() for part in line.split('|')]
    if len(parts) != 3 or not all(parts):
        return None
    srn, name, status = parts
    return {"srn": srn.upper(), "name": name, "status": status.lower()}


def _display(result):
    return "Invalid input" if result is None else result


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", _display(format_course_code(value)))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", _display(total_credits(value)))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", _display(parse_student_record(value)))

if __name__ == "__main__":
    main()
