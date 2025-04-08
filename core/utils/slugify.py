import re
import unicodedata

from django.utils.text import slugify as _slugify
from transliterate import detect_language, translit


def slugify(text, language_code=None):
    """Slugify the given text.

    If no ``language_code`` is given, auto-detect the language code from
    text given.

    :param str text:
    :param str language_code:
    :return str:
    """
    try:
        if str(text).replace(".", "", 1).isdigit():
            if int(float(text)) == float(text):
                text = str(int(float(text)))
            return str(text).replace(".", "-", 1)
    except Exception:
        pass

    if not language_code:
        language_code = detect_language(text)
    if language_code:
        transliterated_text = translit(text, language_code, reversed=True)
        slug = unicodedata.normalize("NFKD", transliterated_text).encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"\.", "-", slug).strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug).strip().lower()
        return re.sub(r"[-\s]+", "-", slug)

    return _slugify(text)
