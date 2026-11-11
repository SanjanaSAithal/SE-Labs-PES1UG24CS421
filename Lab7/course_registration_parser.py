MAX_CREDIT_DIGITS = 2

def _is_ascii_digits(text):
    # str.isdigit() also accepts non-ASCII digits (superscripts, Arabic-Indic digits)
    # that int() rejects or that are not valid course numbers
    return text.isascii() and text.isdigit()

def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Returns None unless code has exactly two words: a letters-only
    department and a digits-only number.
    """
    if not isinstance(code, str):
        return None
    words = code.split()
    if len(words) != 2:
        return None
    dept, number = words
    if not (dept.isascii() and dept.isalpha() and _is_ascii_digits(number)):
        return None
    return dept.upper() + number

def total_credits(text):
    """
    Adds up comma-separated course credits.
    Returns None unless every value is a whole number of at most
    MAX_CREDIT_DIGITS digits.
    """
    if not isinstance(text, str):
        return None
    credits = [credit.strip() for credit in text.split(',')]
    for credit in credits:
        # The length cap also keeps int() away from huge digit strings, which
        # Python refuses to convert (ValueError) and which are slow to parse.
        if not _is_ascii_digits(credit) or len(credit) > MAX_CREDIT_DIGITS:
            return None
    return sum(int(credit) for credit in credits)

def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Returns None unless there are exactly three non-empty fields.
    """
    if not isinstance(line, str):
        return None
    parts = [part.strip() for part in line.split('|')]
    if len(parts) != 3 or not all(parts):
        return None
    return {"srn": parts[0].upper(),
            "name": parts[1],
            "status": parts[2].lower()}

def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    result = format_course_code(value)
    if result is None:
        print("Invalid course code:", repr(value))
    else:
        print("Formatted course code:", result)

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    result = total_credits(value)
    if result is None:
        print("Invalid credit list:", repr(value))
    else:
        print("Total credits:", result)

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    result = parse_student_record(value)
    if result is None:
        print("Invalid student record:", repr(value))
    else:
        print("Student record:", result)

if __name__ == "__main__":
    main()
