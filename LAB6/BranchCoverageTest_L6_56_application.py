import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register: every decision True and False ----------
# Decision 1: student_status not in MAX_CREDITS
@pytest.mark.parametrize("status", ["graduate", "", "REGULAR"])
def test_unknown_status_raises(status):
    with pytest.raises(ValueError, match="unknown status"):
        can_register(status, 10, 4, True)


@pytest.mark.parametrize("status", ["regular", "probation", "honors"])
def test_known_status_does_not_raise(status):
    assert can_register(status, 0, 3, True) == "registered"


# Decision 2: course_credits <= 0 (boundary: 0 is invalid, 1 is valid)
@pytest.mark.parametrize("credits", [0, -1])
def test_non_positive_course_credits_raises(credits):
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, credits, True)


def test_smallest_valid_course_credits():
    assert can_register("regular", 10, 1, True) == "registered"


# Decision 3: not prerequisites_met
def test_prerequisites_not_met():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_prerequisites_met():
    assert can_register("regular", 10, 4, True) == "registered"


# Decision 4: current + course > limit (boundary: exactly at limit is allowed)
@pytest.mark.parametrize(
    "status, current, course, expected",
    [
        ("regular", 20, 4, "registered"),               # exactly 24
        ("regular", 21, 4, "credit limit exceeded"),    # 25
        ("probation", 12, 4, "registered"),             # exactly 16
        ("probation", 13, 4, "credit limit exceeded"),  # 17
        ("honors", 24, 4, "registered"),                # exactly 28
        ("honors", 25, 4, "credit limit exceeded"),     # 29
    ],
)
def test_credit_limit_boundaries(status, current, course, expected):
    assert can_register(status, current, course, True) == expected


def test_prerequisites_checked_before_credit_limit():
    assert can_register("probation", 16, 4, False) == "prerequisites missing"


# ---------- waitlist_position ----------
# Decision 1: capacity <= 0
@pytest.mark.parametrize("capacity", [0, -5])
def test_non_positive_capacity_raises(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, capacity, 0)


# Decision 2: enrolled < capacity (boundary: enrolled == capacity is full)
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_last_seat_available():
    assert waitlist_position(39, 40, 5) == 0


def test_class_exactly_full_empty_waitlist():
    assert waitlist_position(40, 40, 0) == 1


def test_over_enrolled_treated_as_full():
    assert waitlist_position(45, 40, 0) == 1


# Decision 3: waitlist_length >= 10 (boundary: 9 still joins, 10 is closed)
def test_waitlist_one_below_limit():
    assert waitlist_position(40, 40, 9) == 10


@pytest.mark.parametrize("length", [10, 11, 50])
def test_waitlist_closed(length):
    assert waitlist_position(40, 40, length) == -1


# ---------- late_fee ----------
# Decision 1: days_late <= 0
@pytest.mark.parametrize("days", [0, -3])
def test_not_late_no_fee(days):
    assert late_fee(days, 15, False) == 0


# Decision 2: has_waiver
def test_waiver_no_fee():
    assert late_fee(5, 15, True) == 0


def test_no_waiver_pays_fee():
    assert late_fee(5, 15, False) == 500


# Decision 3: days_late <= 7 (boundary: 1, 7 flat; 8 starts the daily charge)
@pytest.mark.parametrize(
    "days, expected",
    [
        (1, 500),
        (7, 500),
        (8, 600),
        (10, 800),
    ],
)
def test_late_fee_week_boundary(days, expected):
    assert late_fee(days, 15, False) == expected


# Decision 4: credits > 20 (boundary: 20 no surcharge, 21 surcharge)
@pytest.mark.parametrize(
    "credits, expected",
    [
        (20, 500),
        (21, 750),
        (28, 750),
    ],
)
def test_heavy_load_surcharge_boundary(credits, expected):
    assert late_fee(3, credits, False) == expected


# Decision 5: fee > 2000 (boundary: exactly 2000 and 2000+ capped)
def test_fee_exactly_at_cap_not_changed():
    # 500 + (22 - 7) * 100 = 2000
    assert late_fee(22, 15, False) == 2000


def test_fee_one_step_over_cap_is_capped():
    # 500 + (23 - 7) * 100 = 2100 -> 2000
    assert late_fee(23, 15, False) == 2000


def test_surcharge_pushes_fee_over_cap():
    # 500 + (21 - 7) * 100 + 250 = 2150 -> 2000
    assert late_fee(21, 25, False) == 2000


def test_very_late_is_capped():
    assert late_fee(365, 25, False) == 2000


def test_below_cap_not_capped():
    # 500 + (20 - 7) * 100 = 1800
    assert late_fee(20, 15, False) == 1800
