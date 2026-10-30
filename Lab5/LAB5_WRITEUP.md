# Lab 5: Static Code Analysis — Write-up

Repo: `L5_56_car-rental`, file analyzed: `car_rental.py`

## Summary of results

| Tool    | Before             | After          |
|---------|---------------------|----------------|
| Pylint  | 5.06/10, 38 findings | **10.00/10**, 0 findings |
| Bandit  | 11 findings (2 High, 4 Medium, 5 Low) | **0 findings** |
| Flake8  | 24 findings          | **0 findings** |

Reports: `pylint_report_before.txt` / `pylint_report_after.txt`,
`bandit_report_before.txt` / `bandit_report_after.txt`,
`flake8_report_before.txt` / `flake8_report_after.txt`.

## Identified Issues Table

| Issue | Type | Tool | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|
| SQL injection in `register_customer` | Security (High) | Bandit B608 | 23 | Customer data was interpolated into SQL with `%` string formatting, allowing SQL injection via name/licence/phone | Switched to a parameterized query (`?` placeholders) |
| SQL injection in `find_customer` | Security (Medium) | Bandit B608 | 26 | Search name was concatenated directly into the SQL string (`"x' OR '1'='1"` returned every row) | Switched to a parameterized query |
| Arbitrary code execution via `exec()` | Security (Medium) | Bandit B102 | 53 | `apply_promo` ran counter-staff-supplied text with `exec()`, letting any typed input run as Python code | Replaced the "rule string" with a plain numeric multiplier parameter (`apply_promo(amount, multiplier)`) — no code execution needed |
| Weak hash (SHA-1) | Security (High) | Bandit B324 | 48 | Licence numbers were hashed with SHA-1, a broken/weak algorithm | Switched to SHA-256 |
| Insecure temp file + permissive chmod | Security (High/Medium) | Bandit B306, B103 | 63, 67 | `tempfile.mktemp()` is a race-condition-prone, deprecated API, and the receipt file was then `chmod`'d to `0o777` (world read/write/execute) | Used `tempfile.mkstemp()` (atomic, secure creation) and tightened permissions to `0o600` |
| Hardcoded admin password | Security (Low) | Bandit B105/B107 | 70–71 | `"admin@rent"` was hardcoded as both the default argument and the comparison value | Removed the default; password is now read from an environment variable and compared with `hmac.compare_digest` |
| Bare `except: pass` | Security/Bug | Bandit B110, Flake8 E722 | 41 | Silently swallowed *any* exception (e.g. unknown plate), hiding real bugs | Replaced with an explicit `fleet.get(plate)` / `None` check — no exception needed at all |
| `assert` used for input validation | Security | Bandit B101 | 30 | Asserts are stripped when Python runs with `-O`, so the "customer must be registered" check could silently disappear in production | Replaced with an explicit `raise ValueError(...)` |
| Insecure `random` for booking codes | Security (Low) | Bandit B311 | 45 | Standard `random` is not suitable for anything security-sensitive (booking codes are semi-sensitive identifiers) | Switched to the `secrets` module |
| Mutable default argument | Bug | Pylint W0102 | 16 | `features=[]` is a single list shared across every call to `add_car`, so mutations would leak between unrelated cars | Changed default to `None` and initialize `features = []` inside the function body |
| `== True` / non-Pythonic boolean checks | Style/Bug | Pylint C0121, Flake8 E712 | 78 | `fleet[p]["available"] == True` instead of plain truthiness | Rewrote as a list comprehension using plain truthiness |
| Non-PEP8 function names | Style | Pylint C0103 | all functions | `addCar`, `registerCustomer`, etc. used camelCase instead of PEP 8 `snake_case` | Renamed every function (and all call sites) to `snake_case` |
| Missing docstrings | Style | Pylint C0114/C0116 | module + all functions | No module or function docstrings | Added a one-line docstring to the module and every function |
| Lines over 79/100 chars | Style | Pylint C0301, Flake8 E501 | multiple | Several lines (SQL, dict literals, print calls) exceeded the line-length limit | Wrapped long literals/calls across multiple lines |
| Missing blank lines between functions | Style | Flake8 E302/E305 | all functions | PEP 8 requires 2 blank lines before/after top-level defs | Added the required blank lines and a `if __name__ == "__main__":` guard |
| Unused import | Bug/Style | Pylint W0611, Flake8 F401 | 2 | `import json` was never used | Removed the import |
| `%`-style string formatting | Style | Pylint C0209 | 23, 65 | Older `%`/`.format()`-style formatting flagged in favor of f-strings | Converted to parameterized SQL (for queries) and f-strings (for the receipt text) |

*(17 issues documented and fixed — well above the lab's minimum of 4 — covering all Bandit findings, all issues needed to clear the 9.5 Pylint bar, and all Flake8 formatting findings.)*

## Reflection Questions

**1. What was the most severe issue you found, and why?**
The SQL injection vulnerabilities in `register_customer`/`find_customer` and the `exec()` call in `apply_promo` were the most severe. The injection flaws meant any user-supplied string (a customer name, for instance) could manipulate or exfiltrate data from the SQL database — demonstrated directly in `main()` where `find_customer("x' OR '1'='1")` returned every row before the fix. `exec()` was worse still: it ran arbitrary, unsanitized text as live Python code, meaning a malicious "promo rule" could do anything the host process could do (read files, spawn processes, etc.), not just manipulate pricing.

**2. How did the three tools complement each other?**
Bandit was the only tool that caught the *security*-specific issues (SQL injection, `exec`, weak hashing, insecure temp files, hardcoded credentials) — Pylint and Flake8 don't reason about security at all. Pylint caught *logic/design* problems that aren't security bugs but are still real bugs (mutable default argument, inconsistent returns, non-Pythonic comparisons) along with broader code-quality conventions (naming, docstrings). Flake8 was narrowly focused on PEP 8 *formatting* (blank lines, line length, bare except syntax) — it overlaps a little with Pylint (e.g. both flagged the bare `except`) but is much faster and style-only. Together they cover three largely distinct layers: security, design/correctness, and style.

**3. Were there any false positives or findings you chose not to act on, and why?**
No true false positives — every Bandit, Pylint, and Flake8 finding pointed at a real issue. One judgment call: Bandit's B311 flag on `random.randint` for booking codes is "Low" severity since booking codes aren't cryptographic secrets, but since the codes function as a quasi-unique lookup identifier I fixed it anyway by switching to `secrets` rather than suppressing the warning, since the cost of doing so was trivial.

**4. How does static analysis change how you'd approach writing code going forward?**
It pushes checks earlier and makes them automatic/repeatable rather than relying on a reviewer noticing, e.g., a hardcoded password or an f-string opportunity during code review. Running Bandit/Pylint/Flake8 (or wiring them into CI/pre-commit) catches entire categories of bugs — mutable defaults, SQL built with string formatting, bare excepts — before they ever reach a PR, which is far cheaper than finding them in production or during a security audit.
