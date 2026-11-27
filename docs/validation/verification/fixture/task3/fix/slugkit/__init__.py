import re
import unicodedata


def slugify(text):
    """Lower-case ASCII slug: accents are transliterated, runs of anything else become one hyphen."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
