import re
def lower_case(text):
    """Converts text to lowercase."""
    if not isinstance(text, str):
        return text
    return text.lower()
