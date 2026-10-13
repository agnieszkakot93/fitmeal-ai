"""Word-level helpers for ingredient names: inflection-tolerant stems and descriptors.

Polish declines nouns and adjectives ("mąka pszenna" -> "mąki pszennej"), so two
words are compared by their stems: the word plus the forms with a common case
ending removed. Stems keep diacritics, so "mąki" (flour) does not meet "mak"
(poppy seed); a diacritics-free stem only counts when it is long enough to be
unambiguous ("maslo" typed without "ł" still finds "masło").
"""

from __future__ import annotations

import re
from functools import cache

from app.core.text import fold

# Longest first. Polish case/number endings plus English plurals.
_ENDINGS = (
    "iego", "iemu", "ach", "ami", "ego", "emu", "ych", "ich", "ymi", "imi", "owi", "ies",
    "iej", "ów", "om", "ej", "ym", "im", "es", "ie", "ą", "ę", "a", "e", "i", "o", "u", "y", "s",
)  # fmt: skip
_MIN_STEM = 3
# a folded stem shorter than this is too ambiguous without its diacritics
_MIN_FOLDED_STEM = 4
# the fleeting "e" of Polish nouns: "cukier" -> "cukru", "czosnek" -> "czosnku"
_FLEETING_E = re.compile(r"^(.{2,}?)i?e([^aeiouyąęó]+)$")

# words in a name that never pick the food: joins and prepositions
FILLERS = frozenset({"z", "ze", "w", "we", "do", "na", "o", "of", "with", "the", "a", "an", "in"})

# preparation, state and size words: they describe the food, they don't name a
# different one ("ciepłe mleko" is milk, "frozen banana" is a banana)
_DESCRIPTOR_WORDS = """
    ciepły zimny gorący letni świeży mrożony młody dojrzały duży mały średni
    drobny gruby posiekany pokrojony starty roztopiony miękki twardo miękko
    ugotowany gotowany pieczony smażenie smażony gazowany niegazowany
    naturalny obrany umyty mielony rozgnieciony przeciśnięty opcjonalny
    fresh frozen warm cold hot lukewarm young ripe large small medium big
    chopped shredded diced sliced minced crushed grated melted softened peeled
    boiled cooked roasted finely roughly thinly sparkling still plain
    hard soft trimmed rinsed drained packed heaping heaped level
    vanilla unflavoured unflavored waniliowy
"""


def tokens(text: str) -> list[str]:
    """Lower-cased words of a name, punctuation trimmed, fillers dropped."""
    words = (w.strip(".,;:!?()\"'") for w in text.lower().split())
    return [w for w in words if w and fold(w) not in FILLERS]


@cache
def stems(word: str) -> frozenset[str]:
    """The word and its forms with one case ending (or a fleeting "e") removed."""
    word = word.lower()
    out = {word}
    for ending in _ENDINGS:
        if word.endswith(ending) and len(word) - len(ending) >= _MIN_STEM:
            out.add(word[: -len(ending)])
    for stem in list(out):
        m = _FLEETING_E.match(stem)
        if m:
            out.add(m.group(1) + m.group(2))
        if "ó" in stem:  # "sól" -> "soli", "wóz" -> "wozu"
            out.add(stem[::-1].replace("ó", "o", 1)[::-1])
    return frozenset(out)


@cache
def _folded_stems(word: str) -> frozenset[str]:
    return frozenset(fold(s) for s in stems(word) if len(fold(s)) >= _MIN_FOLDED_STEM)


def same_word(a: str, b: str) -> bool:
    """True when two words are inflections of each other ("oliwy" / "oliwa")."""
    if stems(a) & stems(b):
        return True
    return bool(_folded_stems(a) & _folded_stems(b))


_DESCRIPTORS = tuple(_DESCRIPTOR_WORDS.split())


@cache
def is_descriptor(word: str) -> bool:
    if any(c.isdigit() for c in word):
        return False
    w = word.lower()
    # adjectives decline in every gender and case, so compare by stem
    return any(same_word(w, d) or _adjective_stem(w) == _adjective_stem(d) for d in _DESCRIPTORS)


_ADJ_ENDINGS = ("ych", "ymi", "ego", "emu", "ej", "ym", "ie", "ia", "y", "a", "e", "ą", "i")


def _adjective_stem(word: str) -> str:
    w = fold(word)
    for ending in _ADJ_ENDINGS:
        e = fold(ending)
        if w.endswith(e) and len(w) - len(e) >= 4:
            return w[: -len(e)]
    return w
