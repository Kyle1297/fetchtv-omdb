import re
from django.core.exceptions import ValidationError

def year_range_validator(value):
    """
    A validator for either a single year or year range.

    Expects either YYYY, YYYY- or YYYY-YYYY.

    Note, the regex should be: r"^\d{4}[-]?$|^\d{4}[-]\d{4}$" - but for 
    some reason, Django can't handle the dash properly (it appears to be 
    a bug). Normal python can though. Feel free to test yourself.
    """
    regex = r"^\d{4}[-]?|^\d{4}[-]\d{4}$"
    if not re.match(regex, value):
        raise ValidationError(f"Value '{value}' is not a valid year or year range.")