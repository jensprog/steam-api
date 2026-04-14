import re

"""Regex validator for username input"""


def parse_username(username):
    pattern = "^[a-zA-Z0-9_.-]*$"
    if not re.match(pattern, username):
        raise ValueError("Username can only have letters, numbers, hyphen, dot and underscore")
    return username
