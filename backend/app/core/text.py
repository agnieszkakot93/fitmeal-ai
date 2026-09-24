import unicodedata


def fold(text: str) -> str:
    """Lower-case and strip diacritics for matching ("Łyżka" → "lyzka", "pierś" → "piers").

    "ł" has no Unicode decomposition, so it is mapped explicitly.
    """
    text = " ".join(text.strip().lower().replace("ł", "l").split())
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))
