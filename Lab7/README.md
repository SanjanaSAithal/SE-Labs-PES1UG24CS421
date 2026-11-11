# Lab 7: Fuzzing for Input Validation Bugs

**Name:** Sanjana S Aithal
**SRN:** PES1UG24CS421

Fuzz testing of `course_registration_parser.py` (the Lab 6 course registration problem) with Hypothesis. The module reads course codes, credit lists and student records typed in by a user. The original version assumed every input was well formed.

## Files

| File | Description |
|------|-------------|
| `course_registration_parser.py` | Fixed module: all three functions handle any input without crashing |
| `test_course_registration_parser.py` | Completed Hypothesis fuzz tests, one per function |
| `PES1UG24CS421_SanjanaSAithal_LAB7.pdf` | Consolidated report: SS1 to SS4, bugs and fixes, both source files |
| `ss1_original_run.png`, `ss1_original_run_output.txt` | SS1: original module run |
| `ss2_fuzz_tests_failing.png`, `ss2_fuzz_tests_failing_output.txt` | SS2: fuzz tests failing on the original module |
| `ss3_fixed_run.png`, `ss3_fixed_run_output.txt` | SS3: fixed module run |
| `ss4_fuzz_tests_passing.png`, `ss4_fuzz_tests_passing_output.txt` | SS4: fuzz tests passing on the fixed module |

The PNGs are images generated from the recorded terminal output in the `.txt` files, not captures of a terminal window.

## How to run

```
pip install hypothesis pytest

python course_registration_parser.py
pytest test_course_registration_parser.py
```

## Bugs found by fuzzing

Each test feeds `st.text() | st.none()` to one function and fails if it raises. Hypothesis shrank the failures on the original module to these minimal inputs:

| Function | Failing input | Exception | Cause |
|----------|---------------|-----------|-------|
| `format_course_code` | `None` | `AttributeError` | Calls `.split()` without checking the type |
| `format_course_code` | `''` | `ValueError` | Unpacks `split()` into exactly two names |
| `total_credits` | `None` | `AttributeError` | Calls `.split()` without checking the type |
| `total_credits` | `''` | `ValueError` | `int('')` on an empty field (also `'4,,3'`, `'a'`) |
| `parse_student_record` | `None` | `AttributeError` | Calls `.split()` without checking the type |
| `parse_student_record` | `''` | `IndexError` | Reads `parts[1]` and `parts[2]` without checking the count |
| `parse_student_record` | `'\|'` | `IndexError` | Only two fields, so `parts[2]` is missing |

## Fixes

Every function now returns `None` for invalid input instead of raising, and `main()` prints an `Invalid ...` message in that case.

- **`format_course_code`**: rejects non-strings, requires exactly two words, a letters-only department and a digits-only number.
- **`total_credits`**: rejects non-strings and any field that is not 1 to 2 ASCII digits. Whitespace around a field is allowed (`'4, 3 ,4'` gives 11). ASCII-only matters because `str.isdigit()` accepts characters like `'²'` that `int()` rejects. The length cap stops `int()` from being called on a huge digit string, which Python refuses to convert (more than 4300 digits) and which is a denial-of-service risk.
- **`parse_student_record`**: rejects non-strings and requires exactly three non-empty fields, so `'a|b'`, `'a||c'` and `'a|b|c|d'` are all invalid.

The tests also check the return type (`str`, non-negative `int`, or a dict with exactly the keys `srn`, `name` and `status`, otherwise `None`). The fixed module passed 20,000 generated examples per test in addition to the default 100.
