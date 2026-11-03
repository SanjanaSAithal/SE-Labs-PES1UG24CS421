# Lab 6: Code and Branch Coverage

**Name:** Sanjana S Aithal
**SRN:** PES1UG24CS421

Coverage analysis of `course_registration.py`, a module that decides whether a student can register for a course, works out waitlist positions and charges late registration fees.

## Files

| File | Description |
|------|-------------|
| `course_registration.py` | The module under test (unchanged) |
| `test_course_registration.py` | Starter test file (unchanged) |
| `CodeCoverageTest_PES1UG24CS421_course_registration.py` | Test cases for code (line) coverage |
| `BranchCoverageTest_PES1UG24CS421_course_registration.py` | Test cases for branch coverage |
| `code_coverage_screenshot.png`, `code_coverage_output.txt` | Code coverage terminal output |
| `branch_coverage_screenshot.png`, `branch_coverage_output.txt` | Branch coverage terminal output |

The PNGs are images generated from the recorded terminal output in the `.txt` files, not captures of a terminal window.

## How to run

```
pip install coverage pytest

coverage run -m pytest CodeCoverageTest_PES1UG24CS421_course_registration.py
coverage report -m

coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS421_course_registration.py
coverage report -m
```

## Results for `course_registration.py`

| Test file | Tests | Measured | Coverage | Missing |
|-----------|-------|----------|----------|---------|
| Starter | 2 | Line and branch | 32% | Lines 6, 8, 10, 12, 18, 21-23, 27-39 |
| Code coverage | 13 | Line only | 100% | None |
| Code coverage | 13 | Line and branch | 98% | Branch `35->37` |
| Branch coverage | 30 | Line and branch | 100% (24 of 24 branches) | None |

## Analysis

The code coverage tests execute every line, yet the branch report still shows `35->37` as missing. Every late fee test that reaches line 35 uses more than 20 credits, so `if credits > 20` is never false. The surcharge line runs, but the path that skips it is never tested. This is why 100% line coverage does not mean every decision was tested.

The branch coverage tests close that gap with fees for 20 credits or fewer. They also check values on either side of each decision, which coverage does not require:

- `can_register`: the credit limit for each student status, and that prerequisites are checked before the limit
- `waitlist_position`: the last open seat, and waitlists of 9, 10 and 11
- `late_fee`: days 7 and 8, 20 and 21 credits, and fees at and above the 2000 cap
