import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("graduate", 10, 4, True)


def test_invalid_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_invalid_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)


def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4


# ---------- late_fee ----------
def test_not_late_no_fee():
    assert late_fee(0, 15, False) == 0


def test_waiver_no_fee():
    assert late_fee(5, 15, True) == 0


def test_late_within_first_week():
    assert late_fee(3, 15, False) == 500


def test_late_after_first_week():
    assert late_fee(10, 15, False) == 800


def test_heavy_load_surcharge():
    assert late_fee(3, 22, False) == 750


def test_fee_capped_at_2000():
    assert late_fee(30, 22, False) == 2000
