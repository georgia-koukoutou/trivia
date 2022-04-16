import time


def is_string_blank(string: str) -> bool:

    return not is_string_not_blank(string)


def is_string_not_blank(string: str) -> bool:

    return string and not string.isspace()


def is_string_equals_ignore_case(a: str, b: str) -> bool:

    if is_string_blank(a) and is_string_blank(b):
        return True
    elif is_string_blank(a) or is_string_blank(b):
        return False
    else:
        return a.lower() == b.lower()


def current_timestamp() -> int:

    return int(round(time.time() * 1000))
