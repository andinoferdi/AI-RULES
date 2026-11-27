import re


def slugify(text):
    """Lower-case ASCII slug: runs of anything else become one hyphen."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
