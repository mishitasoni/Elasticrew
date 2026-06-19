import re


def anonymize_resume(text):

    # Email
    text = re.sub(
        r'[\w\.-]+@[\w\.-]+',
        '[EMAIL REMOVED]',
        text
    )

    # Phone
    text = re.sub(
        r'\+?\d[\d\s\-]{8,}',
        '[PHONE REMOVED]',
        text
    )

    # First line (usually candidate name)
    lines = text.splitlines()

    if lines:
        lines[0] = '[NAME REMOVED]'

    return "\n".join(lines)