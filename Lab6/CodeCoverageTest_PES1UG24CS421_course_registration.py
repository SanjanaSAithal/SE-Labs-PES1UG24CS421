# Name: Sanjana S Aithal
# SRN: PES1UG24CS421
# Lab 6: test cases for code (line) coverage

import pytest
from course_registration import can_register, waitlist_position, late_fee


# can_register
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_invalid_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


# waitlist_position
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_invalid_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1

def test_next_waitlist_position():
    assert waitlist_position(40, 40, 3) == 4


# late_fee
def test_not_late_has_no_fee():
    assert late_fee(0, 12, False) == 0

def test_waiver_has_no_fee():
    assert late_fee(5, 12, True) == 0

def test_within_a_week_with_heavy_load_surcharge():
    assert late_fee(3, 21, False) == 750

def test_long_delay_is_capped():
    assert late_fee(30, 21, False) == 2000
