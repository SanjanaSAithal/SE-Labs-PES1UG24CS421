# Name: Sanjana S Aithal
# SRN: PES1UG24CS421
# Lab 6: test cases for branch coverage

import pytest
from course_registration import can_register, waitlist_position, late_fee


# can_register
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_zero_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_negative_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -1, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_prerequisites_checked_before_credit_limit():
    assert can_register("regular", 24, 4, False) == "prerequisites missing"

def test_regular_over_limit():
    assert can_register("regular", 21, 4, True) == "credit limit exceeded"

def test_probation_at_limit():
    assert can_register("probation", 12, 4, True) == "registered"

def test_probation_over_limit():
    assert can_register("probation", 13, 4, True) == "credit limit exceeded"

def test_honors_at_limit():
    assert can_register("honors", 24, 4, True) == "registered"

def test_honors_over_limit():
    assert can_register("honors", 25, 4, True) == "credit limit exceeded"


# waitlist_position
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_last_seat_available():
    assert waitlist_position(39, 40, 5) == 0

def test_zero_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)

def test_negative_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, -5, 0)

def test_first_on_waitlist():
    assert waitlist_position(40, 40, 0) == 1

def test_last_waitlist_slot():
    assert waitlist_position(40, 40, 9) == 10

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_over_full():
    assert waitlist_position(45, 40, 11) == -1


# late_fee
def test_not_late_has_no_fee():
    assert late_fee(0, 12, False) == 0

def test_negative_days_has_no_fee():
    assert late_fee(-1, 12, False) == 0

def test_waiver_has_no_fee():
    assert late_fee(5, 12, True) == 0

def test_first_day_late():
    assert late_fee(1, 12, False) == 500

def test_last_day_of_flat_fee():
    assert late_fee(7, 20, False) == 500

def test_first_day_of_daily_fee():
    assert late_fee(8, 20, False) == 600

def test_surcharge_starts_above_twenty_credits():
    assert late_fee(3, 21, False) == 750

def test_daily_fee_with_surcharge():
    assert late_fee(8, 21, False) == 850

def test_fee_exactly_at_cap():
    assert late_fee(22, 20, False) == 2000

def test_fee_just_over_cap():
    assert late_fee(23, 20, False) == 2000

def test_surcharge_pushes_fee_over_cap():
    assert late_fee(20, 21, False) == 2000
