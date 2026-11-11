from hypothesis import given, strategies as st
from course_registration_parser import format_course_code, total_credits, parse_student_record

@given(st.text() | st.none())
def test_format_course_code_no_crash(s):
    try:
        result = format_course_code(s)
    except Exception as e:
        assert False, f"format_course_code crashed on {s!r} with: {type(e).__name__}: {e}"
    # Valid input gives the formatted code; anything else gives None.
    assert result is None or isinstance(result, str)

@given(st.text() | st.none())
def test_total_credits_no_crash(s):
    try:
        result = total_credits(s)
    except Exception as e:
        assert False, f"total_credits crashed on {s!r} with: {type(e).__name__}: {e}"
    # Valid input gives a non-negative whole number; anything else gives None.
    assert result is None or (isinstance(result, int) and result >= 0)

@given(st.text() | st.none())
def test_parse_student_record_no_crash(s):
    try:
        result = parse_student_record(s)
    except Exception as e:
        assert False, f"parse_student_record crashed on {s!r} with: {type(e).__name__}: {e}"
    # Valid input gives a dict with exactly the three fields; anything else gives None.
    assert result is None or set(result) == {"srn", "name", "status"}
